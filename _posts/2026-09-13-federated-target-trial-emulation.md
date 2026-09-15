---
layout: post
title: "Federated Target Trial Emulation: Protocols, Weighting, and Distributed Survival Analysis"
description: "A detailed methodology reading of FL-TTE: cohort alignment, federated propensity scores, weighted Cox risk sets, optimization, inference, privacy, and the limits of comparison with pooled data."
permalink: /rwe/federated-target-trial-emulation/
date: 2026-09-13 12:00:00 -0400
research_area: real-world-evidence
paper_year: 2025
paper_venue: npj Digital Medicine
reading_focus: "How shared trial protocols, federated propensity scores, and weighted Cox models work across hospitals, with close attention to local risk sets and pooled-data equivalence."
rwe_topics: [Federated analysis, Propensity scores, Survival analysis]
foundation_notes: [cox-proportional-hazards, inverse-probability-weighting, weighted-survival-analysis]
math: true
tags: [Method, Pharmacoepidemiology, Target Trial Emulation, Federated Learning, IPTW, Survival Analysis]
---

**Paper:** Haoyang Li, Chengxi Zang, Zhenxing Xu, Weishen Pan, Suraj Rajendran, Yong Chen, and Fei Wang. *Federated target trial emulation using distributed observational data for treatment effect estimation*. **npj Digital Medicine 8, 387 (2025)**, published July 1, 2025. [Journal article](https://doi.org/10.1038/s41746-025-01803-y).

These notes explain the supplied 15-page article, with particular attention to its nine numbered equations, algorithm, clinical protocols, and theoretical claims. The publisher's supplementary methods and the public reference code were also inspected. **Reported methods, independently derived teaching equations, and unresolved implementation details are identified separately.** Page numbers without a qualifier refer to the main PDF.

**The central idea:** multiple hospitals use a common trial protocol, learn a shared treatment-assignment model, calculate patient weights locally, and collaborate on a survival model while keeping patient records at their institutions. This can make the analysis resemble an analysis of a larger combined cohort. Its causal credibility still depends on the trial design and identification assumptions. In addition, **the paper's local Cox risk sets do not become an unstratified pooled risk set merely because model parameters are averaged.**

<nav class="table-of-contents" aria-label="Contents" markdown="1">

**Contents**

1. [What FL-TTE contributes and what it estimates](#contribution)
2. [Notation and the complete data flow](#notation)
3. [Federated protocol design and harmonization](#protocol)
4. [The Alzheimer's disease trials](#ad-protocol)
5. [The sepsis trial and time-zero problems](#sepsis-protocol)
6. [Propensity scores: the model, likelihood, gradient, and Hessian](#propensity)
7. [Federated optimization and proximal regularization](#optimization)
8. [IPTW, stabilization, balance, and positivity](#weighting)
9. [Cox regression from hazards to partial likelihood](#cox)
10. [Weighted Cox regression and tied events](#weighted-cox)
11. [Local versus pooled risk sets and sufficient summaries](#risksets)
12. [Standard errors, confidence intervals, and model comparison](#inference)
13. [Federation, local analysis, and meta-analysis](#meta-analysis)
14. [The causal assumptions that federation cannot supply](#assumptions)
15. [The theoretical guarantees and their boundaries](#theory)
16. [Empirical evaluation and reported results](#results)
17. [Privacy and sensitivity analyses](#privacy)
18. [What the public code clarifies and leaves unresolved](#code)
19. [A reproducible analysis, from protocol to final estimate](#reproduce)
20. [Source map and connections to other notes](#sources)

</nav>

## 1. What FL-TTE contributes and what it estimates
{: #contribution }

### 1.1 Two problems are solved at different levels

A target trial emulation starts with a causal question: what would happen if eligible people initiated treatment A rather than treatment B? Observational records do not contain randomized assignments, so the analyst defines eligibility, treatment strategies, baseline, outcomes, follow-up, causal contrast, and adjustment procedures before interpreting the treatment comparison.

A federated analysis starts with a computational restriction: the eligible records are distributed across institutions that cannot exchange patient-level data. An algorithm must operate using local computation and agreed messages. **Federation changes where an analysis is computed. It does not, by itself, create randomization.**

FL-TTE combines these two tasks. Its practical contribution is an integrated workflow for distributed time-to-event studies: a common trial design, federated logistic regression for propensity scores, inverse probability of treatment weighting, and federated Cox regression. The main empirical question is whether its estimates and covariate balance resemble those obtained when the same underlying records can be pooled. The evaluations use real EHR cohorts rather than a simulation with a known causal data-generating effect. [Main article, pp. 1–2 and 10–12.](https://www.nature.com/articles/s41746-025-01803-y)

### 1.2 Three meanings of “better” must remain separate

| Question | Appropriate evidence | What the paper supplies |
| --- | --- | --- |
| Does distributed computation approximate a chosen centralized analysis? | Agreement under matched cohorts, losses, weights, risk sets, and inference procedures | Comparisons with pooled estimates and balance statistics |
| Does the estimator recover a causal treatment effect? | A valid emulation plus identification assumptions and suitable estimation | Observational analyses; the relevant assumptions remain necessary |
| Does the estimate generalize to another population? | Explicit target population, transport assumptions, and appropriate weighting or validation | Multiple heterogeneous institutions, which broaden coverage but do not establish transportability to every setting |

The paper often calls deviation from the pooled estimate “bias.” In these notes, **discrepancy from the pooled estimate** is the more precise description of the directly observed quantity. A pooled observational estimate can itself have confounding, time-alignment, measurement, model, or selection bias.

### 1.3 The effect is an initiation contrast summarized by a hazard ratio

The authors describe their analyses as intention-to-treat, more precisely an **observational analog of an ITT initiation effect**. Groups are defined by the baseline treatment strategy, rather than by sustained adherence throughout follow-up. There is no randomized assignment variable in these EHRs. The effect of initiating a treatment can differ from the effect of taking it continuously for five years.

For illustration, let $$T^a$$ be the counterfactual event time under baseline initiation strategy $$a\in\{0,1\}$$. A clear causal quantity could be a five-year risk difference,

$$
P(T^1\leq5)-P(T^0\leq5),
$$

or a contrast between survival curves. These are teaching definitions, not the paper's reported primary effect scale. FL-TTE reports an adjusted hazard ratio, usually written $$\exp(\widehat\beta_A)$$. The corresponding causal interpretation requires an explicit marginal or conditional hazard model. A hazard ratio of 0.86 does not mean that 14% fewer patients will develop the outcome by five years.

## 2. Notation and the complete data flow
{: #notation }

Use different symbols for treatment, follow-up time, training rounds, and trial populations. The paper uses some symbols in more than one role; the following notation makes the computational dependencies explicit.

| Symbol | Meaning |
| --- | --- |
| $$k=1,\ldots,K$$ | Institution or site |
| $$i=1,\ldots,N_k$$ | Eligible individual within site $$k$$ |
| $$N=\sum_kN_k$$ | Total number of eligible analysis records for a particular emulated trial |
| $$p_k=N_k/N$$ | Site's share of those records; a model-aggregation weight |
| $$A_{ki}$$ | Baseline treatment indicator: trial strategy 1 or comparator strategy 0 |
| $$Z_{ki}$$ | Pretreatment covariates used to model treatment assignment |
| $$\pi$$ | Logistic-regression coefficients for the propensity score |
| $$e_\pi(Z_{ki})$$ | Estimated probability of strategy 1 given the covariates |
| $$w_{ki}$$ | Individual's treatment weight |
| $$U_{ki},\Delta_{ki}$$ | Observed follow-up duration and event indicator; $$\Delta=0$$ denotes censoring for the event being modeled |
| $$X_{ki}$$ | Outcome-model predictors, explicitly including treatment when its coefficient is estimated |
| $$\beta$$ | Cox-regression coefficients; $$\beta_A$$ is the treatment coefficient |
| $$r$$ | Federated optimization round; it is not clinical follow-up time |
| $$t$$ | Time since the chosen clinical baseline |
| $$R_k(t),D_k(t)$$ | Local risk set immediately before $$t$$ and local events at $$t$$ |

A site retains a table conceptually containing $$\{A,Z,U,\Delta\}$$. The server coordinates parameters and other approved summaries. A propensity score is a function of local covariates and shared parameters; it need not be sent to the server to calculate the local individual's weight.

<pre class="mermaid">flowchart TD
    P["Agree on eligibility, treatments, baseline, outcome, follow-up"] --> D["Each site creates the same analysis schema"]
    D --> L["Federated logistic regression: share model updates"]
    L --> W["Each site calculates treatment weights"]
    W --> B["Check overlap, weights, and covariate balance"]
    B --> C["Federated weighted survival analysis"]
    C --> I["Estimate treatment coefficient and valid uncertainty"]
    I --> R["Compare results and assess design limitations"]
</pre>

This diagram is a teaching reconstruction of the dependencies. The paper's Box 1 instead places propensity-score and Cox updates together inside an outer federation loop. Thus one should not infer from the conceptual sequence that the published implementation necessarily freezes a fully converged propensity model before any Cox update.

<figure>
  <a href="{{ '/assets/rwe/federated-tte/figure-1-overview-page.png' | relative_url }}"><img src="{{ '/assets/rwe/federated-tte/figure-1-overview-page.png' | relative_url }}" alt="Original page 3 of Li et al., containing Figure 1: cohort construction and the federated propensity-score and Cox-model workflow." width="1241" height="1648" loading="lazy"></a>
  <figcaption>Original Figure 1 and its page from Li et al. (2025), reproduced without content edits. The model messages connect institutions; the patient tables stay local. Click for full size. Source: the supplied article, p. 3; <a href="https://doi.org/10.1038/s41746-025-01803-y">article</a>, <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>.</figcaption>
</figure>

## 3. Federated protocol design and harmonization
{: #protocol }

### 3.1 A common model requires a common meaning for each row and column

Sharing coefficient vectors is useful only when their positions have the same interpretation. If column 12 means prior diabetes at one site and current insulin use at another, averaging its coefficients has no coherent meaning. If one site measures age in years and another standardizes it locally, even identical column names do not guarantee comparable coefficients.

Before training, institutions therefore need an agreed definition of the analysis unit, treatment labels, observation windows, diagnosis and medication mappings, laboratory units, missingness rules, outcome ascertainment, and censoring. A protocol should also specify how to handle records spanning more than one institution. The main article describes common clinical rules but does not present a complete distributed terminology-mapping or cross-site deduplication algorithm.

“Federated protocol design” here should be understood as coordinated trial specification and local implementation. It is not a learned algorithm that automatically reconciles incompatible local protocols.

### 3.2 What is shared, and at which stage?

| Stage | Local work | Information needed for coordination |
| --- | --- | --- |
| Feasibility and eligibility | Apply inclusion/exclusion rules to EHRs | Definitions, site counts, available covariates, ascertainment limitations |
| Feature construction | Create covariates from the agreed baseline window | Common dictionary, coding rules, units, and transformation parameters |
| Treatment modeling | Evaluate loss and update logistic parameters | Shared model and returned updates; counts for aggregation |
| Weight diagnostics | Calculate scores, weights, overlap, and balance | Approved summaries sufficient to identify global and site-level failures |
| Outcome modeling | Create risk sets and optimize weighted survival loss | Parameters/updates in the published method; additional risk-set summaries would be necessary for an exact unstratified pooled Cox reconstruction |
| Inference | Calculate uncertainty contributions | An explicit method for covariance, weighting uncertainty, and dependence |

The last two rows are particularly consequential. A parameter vector is a small message, but it does not encode all information in an event-time risk set. Similarly, averaging final coefficients does not automatically provide a valid variance estimate for the combined estimator.

### 3.3 The target population is a choice, not an automatic consequence of federation

The default site weights $$N_k/N$$ give larger institutions more influence. This corresponds to the mixture of eligible records in the participating network, subject to the actual loss normalization. It does not give every hospital equal importance. A policy question targeting a national population or a specified health-system mix would require an additional argument for those population weights.

More institutions can improve coverage and estimation stability. They do not repair structural nonpositivity: if a clinically defined subgroup never receives the comparator anywhere, no amount of averaging can directly reveal its comparator outcome from these data.

## 4. The Alzheimer's disease trials
{: #ad-protocol }

### 4.1 Source population and trial-specific cohorts

INSIGHT contains records from five New York City health systems. The article describes a source network of 5,532,428 patients and a pool of **35,435 patients with recorded mild cognitive impairment (MCI)**, distributed as 5,803, 4,764, 6,670, 10,926, and 7,272 across the five sites. These are not the exposed and comparator sample sizes for every drug trial. Each drug-specific eligibility and initiation comparison creates a further cohort.

The nine trial drugs are aspirin, amlodipine, atorvastatin, lidocaine, acetaminophen, famotidine, pantoprazole, fluticasone, and albuterol. They are evaluated as possible drug-repurposing signals for delayed AD onset, rather than as a claim that all nine are established AD treatments. [Main article, pp. 2 and 12.](https://www.nature.com/articles/s41746-025-01803-y)

### 4.2 Protocol components

| Component | Main article's description | Methodological interpretation |
| --- | --- | --- |
| Population | Recorded MCI; age at least 50 at MCI diagnosis | The target group is people with MCI, not all older adults |
| Prior observation | At least one year before treatment initiation, without an upper limit on baseline history | Observability and lookback duration can vary between people |
| Dementia exclusion | No recorded AD or related dementia during the five years before index | Absence of a code is the operational rule; it is not proof of lifelong absence of disease |
| Strategies | Initiate the trial drug or initiate a similar alternative within the same ATC level-2 class | Active-comparator new-user design, intended to improve clinical comparability |
| Baseline | First prescription initiating the relevant strategy, after eligibility is satisfied | Eligibility, strategy classification, and outcome follow-up should align here |
| Primary outcome | Newly recorded AD diagnosis | An EHR diagnosis endpoint, potentially affected by care utilization and diagnostic practice |
| Follow-up | Until AD, loss to follow-up, five years, or database end, whichever occurs first | A censored time-to-first-event analysis |
| Contrast | Observational analog of an ITT initiation effect | Subsequent adherence is not explicitly maintained as a sustained intervention |
| Estimation | Baseline IPTW followed by Cox regression | Requires sufficient confounder control, overlap, and a suitable survival model |

An ATC level-2 class is fairly broad. “Same class” is a design rule, not proof that the trial and comparator drugs have identical indications or are equally suitable for every patient. Exact comparator membership and inclusion rules should be recoverable for each trial.

### 4.3 The 267 covariates

The main article reports **267 adjusted covariates**: age, sex/gender as operationally recorded, elapsed time from MCI diagnosis to drug initiation, 64 comorbidity/risk-factor variables, and medication history for the 200 most frequently prescribed drugs. Age and MCI-to-initiation time are continuous; the described comorbidity and medication indicators are binary. The 64 conditions draw on the Chronic Conditions Data Warehouse and expert-selected AD risk factors; ICD-9/10 codes operationalize diagnoses.

The two clocks are distinct: age or disease duration may predict both prescribing and prognosis, whereas follow-up time begins at initiation. Including the MCI-to-initiation interval attempts to account for differences in how far people have progressed through their observable disease course before entering the comparison.

The article does not establish that every predictor is measured perfectly or that insurance, education, disease severity, utilization, and other relevant confounding information are fully observed. In fact, it acknowledges missing information such as health insurance as a source of residual confounding.

### 4.4 Event and censoring records

For someone with AD during follow-up, observed time is the interval from initiation to the first AD diagnosis and $$\Delta=1$$. For someone without AD who remains observable through the horizon, time reaches the relevant follow-up endpoint and $$\Delta=0$$. If follow-up ends earlier because records stop, the last prescription or diagnosis date, whichever is later, defines the censoring time.

The article's “negative event” category means no AD recorded through complete follow-up. In a Cox input table it is still a **censored observation at the administrative horizon**, not an occurrence of an opposite biological event. Someone with two years of observation and no AD must not be coded as a five-year AD-free outcome.

Death requires separate attention. It prevents subsequent AD diagnosis and is a competing event, not simply an ordinary missing visit. The main AD protocol does not provide a detailed competing-death analysis. Consequently, the AD hazard result should not be silently relabeled a five-year cumulative-incidence effect accounting for death.

### 4.5 Confirmation of initiation can use future information

The main article requires two prescriptions **within a 30-day window**. Supplementary Table 1 instead specifies a **minimum one-month interval**. This discrepancy remains unresolved. Both descriptions also require information after the first prescription. [Supplementary Table 1, pp. 6–7.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41746-025-01803-y/MediaObjects/41746_2025_1803_MOESM1_ESM.pdf)

The causal issue is not merely the wording of a date interval. If eligibility at the first prescription requires a later second prescription, patients must remain observable and eligible long enough to satisfy that requirement. This can select on post-baseline events or survival. A reproducible emulation must explain whether it uses a landmark, a grace-period strategy, cloning and censoring, or another method that aligns this confirmation rule with follow-up. Baseline weighting alone cannot remove time-related selection created by an incorrectly defined entry rule.

## 5. The sepsis trial and time-zero problems
{: #sepsis-protocol }

### 5.1 Data, enrollment, and treatment

The sepsis evaluation combines eICU data from 191 sites during 2014–2015 and MIMIC-IV from one site during 2008–2019. The source populations contain 200,859 and 73,181 records, respectively. The reported analysis cohort contains **1,834 treated and 19,624 comparator patients**, totaling **21,458**: eICU contributes 1,233 treated and 13,410 controls; MIMIC contributes 601 and 6,214. Fifty-two of the 192 sites have fewer than ten eligible patients, an important motivation for sharing information across institutions.

The main article identifies suspected infection by antibiotic administration together with collection of a body-fluid culture. It uses a simplified infectious-critical-illness definition based on **SOFA at least 2**, explicitly distinguishing this from a **two-point increase over baseline** in the Sepsis-3 definition. These definitions must not be substituted for one another when reproducing the cohort.

Eligibility includes adulthood and sepsis during the first 24 hours after ICU admission. The article excludes prior infection or corticosteroid use. Figure 1 additionally shows first-stay selection and exclusion of cardiothoracic surgical service records. The reported treatment comparison is no corticosteroid initiation versus hydrocortisone initiation at **at least 160 mg/day** in a window spanning **10 hours before to 24 hours after ICU admission**. These are the study's historical exposure rules, not treatment recommendations. [Main article, pp. 3, 10, and 12.](https://www.nature.com/articles/s41746-025-01803-y)

### 5.2 Baseline measurements

The adjustment variables include vital signs, laboratory measurements, demographic factors, BMI categories, and the Elixhauser comorbidity index. The main text specifically mentions heart rate, mean arterial pressure, respiratory rate, oxygen saturation, systolic arterial blood pressure, temperature, age, sex, and BMI, as well as biochemical, hematological, and physiological measurements.

The preprocessing description removes values beyond the 99th percentile and imputes missing values with medians. When multiple values exist in the 24-hour enrollment window, it selects the worst value. The exact direction of “worst” depends on the variable: clinically adverse high and low values cannot be handled by an unexplained universal maximum operator. The article does not fully specify whether trimming thresholds and imputation medians are site-specific or global, nor all rules for variables with different units or measurement frequencies.

### 5.3 Why temporal overlap matters

Some patients can begin corticosteroids before ICU admission or during the first 24 hours, while covariates are summarized across those same 24 hours. A measured blood pressure or laboratory value may therefore occur **after treatment begins**. Treating it as a baseline confounder could adjust for an effect of treatment or for a variable influenced by treatment and prognosis.

A concrete example: patient A starts the study drug at hour 2, and the worst recorded blood pressure occurs at hour 10. That blood pressure is not necessarily a pretreatment covariate for an hour-2 initiation question. A model can balance its distribution beautifully while targeting the wrong causal adjustment set.

Likewise, treatment classification using information through hour 24 cannot be treated as known at admission without specifying how the intervention's grace period is handled. Someone must survive long enough to initiate later in that window. Choosing treatment initiation as time zero only for treated patients and admission for controls makes their risk clocks systematically different.

Supplementary Table 2 explicitly uses those arm-specific baselines, whereas the main Data section describes follow-up from admission. The table also allows corticosteroid-equivalent doses, and its threshold wording alternates between “at least” and “more than” 160 mg/day. These operational differences require resolution. [Supplementary Table 2, pp. 7–8.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41746-025-01803-y/MediaObjects/41746_2025_1803_MOESM1_ESM.pdf)

### 5.4 Outcomes and competing events

The primary outcome is 28-day mortality. Secondary outcomes are time to ICU discharge and time to cessation of mechanical ventilation, where cessation requires 24 hours without ventilatory support. The article states that death is treated as a competing risk for secondary outcomes. It does not identify enough model details in the main methods to equate the reported secondary HRs unambiguously with either cause-specific or Fine–Gray subdistribution HRs.

For discharge, a higher event hazard refers to a faster rate of discharge among the relevant risk set; for mortality, a higher hazard refers to a faster rate of death. A higher HR therefore does not have the same desirable or undesirable direction across these endpoints. An intervention can also change mortality, which changes who remains available for discharge or extubation.

Follow-up is described as ending at death, discharge, or loss to follow-up. A 28-day mortality estimand needs a clear statement about post-discharge mortality ascertainment or how discharge censoring is handled. The nominal horizon alone does not ensure complete ascertainment after patients leave the ICU or hospital.

### 5.5 Clone–censor–weight sensitivity analysis

The main article reports an additional analysis with a common ICU-admission time zero. Each eligible person is cloned into both strategies; a clone is censored when observed treatment becomes incompatible with its assigned strategy. Inverse probability of censoring weights, based on baseline covariates, address the selection created by artificial censoring. Results are described as largely similar to the primary estimates.

The logic is that an untreated patient early in a grace period can still be compatible with both “initiate within the window” and “do not initiate” strategies. Cloning preserves this compatibility instead of deciding a baseline group using future treatment. Censoring then removes a clone when its strategy becomes impossible or is violated.

This addresses an important timing problem, but validity still requires a precise grace period, correctly measured adherence/compatibility, positivity for remaining compatible, and an adequate censoring model. Baseline-only censoring predictors may be insufficient when evolving severity affects both treatment initiation and prognosis. The sensitivity analysis should not be read as a proof that all immortal-time, post-treatment-adjustment, and informative-censoring problems have disappeared.

## 6. Propensity scores: the model, likelihood, gradient, and Hessian
{: #propensity }

### 6.1 What the logistic model predicts

Equation (1) defines a propensity score. With an intercept included in $$Z$$,

$$
e_\pi(Z)=P(A=1\mid Z)=\frac{\exp(\pi^\top Z)}{1+\exp(\pi^\top Z)}.
$$

The linear predictor $$\pi^\top Z$$ adds covariates multiplied by their coefficients; the logistic transformation maps this real number into a probability between zero and one. The outcome being predicted is **treatment initiation**, not death, AD, or treatment benefit.

For example, an intercept-only prediction of 0.2 means that the model expects 20% of comparable records to be treated. A rich model lets age, comorbidities, prior drugs, and other baseline factors change that prediction. The goal in this application is to support adjustment for treatment selection. High treatment-prediction accuracy is not by itself a successful causal design; near-perfect predictions can indicate poor overlap.

### 6.2 The local likelihood: Equation (3)

The likelihood of one observed binary label is $$e^A(1-e)^{1-A}$$. If $$A=1$$, this becomes $$e$$; if $$A=0$$, it becomes $$1-e$$. Holding the observed data fixed and choosing coefficients gives site $$k$$'s log likelihood,

$$
\ell_k(\pi)=\sum_{i=1}^{N_k}\left[A_{ki}\log e_\pi(Z_{ki})+(1-A_{ki})\log\{1-e_\pi(Z_{ki})\}\right].
$$

This is Equation (3), with treatment renamed $$A$$. The article calls it a partial log likelihood; mathematically it is an ordinary Bernoulli logistic log-likelihood contribution from one site. Its form differs from the Cox partial likelihood discussed later.

Suppose two local patients have fitted probabilities 0.8 and 0.3; the first is treated and the second is a comparator. Their contribution is $$\log(0.8)+\log(0.7)\approx-0.5798$$. A model giving probabilities 0.6 and 0.4 scores $$\log(0.6)+\log(0.6)\approx-1.0217$$. The first candidate fits these two labels better. This comparison is only one piece of the full-data optimization.

### 6.3 Deriving the score and curvature

The following derivatives are teaching derivations of Equation (3). Because the derivative of the logistic function is $$e(1-e)$$, differentiation gives

$$
g_k(\pi)=\frac{\partial\ell_k}{\partial\pi}
=\sum_i Z_{ki}(A_{ki}-e_{ki}),
$$

$$
H_k(\pi)=\frac{\partial^2\ell_k}{\partial\pi\partial\pi^\top}
=-\sum_i e_{ki}(1-e_{ki})Z_{ki}Z_{ki}^\top.
$$

Here $$e_{ki}=e_\pi(Z_{ki})$$. The gradient combines treatment-prediction residuals with feature values. A treated person with $$e=0.8$$ contributes 0.2 to the intercept gradient; a comparator with $$e=0.3$$ contributes −0.3. All records jointly determine the update direction.

The matrix $$Z Z^\top$$ contains pairwise feature products. The negative Hessian measures curvature, or information about coefficient directions. It is positive semidefinite, not automatically positive definite: collinear predictors, separation, or insufficient variation can make logistic fitting unstable.

### 6.4 What can be aggregated exactly for logistic regression?

For an ordinary equal-patient pooled logistic likelihood,

$$
\ell_{\mathrm{pool}}(\pi)=\sum_k\ell_k(\pi),\qquad
g_{\mathrm{pool}}(\pi)=\sum_kg_k(\pi),\qquad
H_{\mathrm{pool}}(\pi)=\sum_kH_k(\pi).
$$

If every site evaluates these quantities at the **same current coefficients**, a server can perform a pooled Newton update using aggregated score and curvature without receiving records:

$$
\pi_{r+1}=\pi_r-H_{\mathrm{pool}}(\pi_r)^{-1}g_{\mathrm{pool}}(\pi_r).
$$

The minus sign is the Newton root-finding convention for the score; the Hessian of the log likelihood is negative. Equivalently, add information-inverse times the score. In practice a linear system is solved rather than explicitly forming an inverse.

This demonstrates why federated logistic estimation is possible. It is **not a claim that FL-TTE uses Newton aggregation**: Box 1 describes local optimization followed by parameter averaging. Those are different algorithms, even when intended to target related objectives.

## 7. Federated optimization and proximal regularization
{: #optimization }

### 7.1 The two levels of averaging

A conventional equal-patient federated objective uses each site's **mean** negative log likelihood,

$$
F_k(\pi)=-\frac{1}{N_k}\ell_k(\pi),\qquad
F(\pi)=\sum_kp_kF_k(\pi)=-\frac{1}{N}\sum_k\ell_k(\pi).
$$

Averaging locally, then weighting sites by $$N_k/N$$, gives each patient weight $$1/N$$. Equation (4), read literally, instead multiplies a **summed** local log likelihood by $$p_k$$. That scales total site influence approximately as $$N_k^2/N$$ when average contributions are similar.

If sites have two and six people, equal-patient contributions have a 1:3 ratio. Multiplying their already-summed losses by 2/8 and 6/8 gives a 1:9 ratio. This is why “sum or mean?” is a substantive question. The supplementary proof defines mean local losses, but that convention is not displayed in main Equation (4). A reader should not silently replace the printed objective and declare exact pooling.

### 7.2 Parameter averaging is not probability averaging

In a simple FedAvg round, the server distributes shared parameters $$\pi_r$$. Each site initializes from them, performs local optimization, and returns $$\pi_{k,r+1}$$. The server forms

$$
\pi_{r+1}=\sum_kp_k\pi_{k,r+1}.
$$

If sites weighted 0.25 and 0.75 return a particular coefficient as 0.4 and 0.8, the aggregated coefficient is 0.7. This does not mean averaging patient propensity scores, since the logistic transformation is nonlinear. It also does not imply that one round reaches the centralized maximum-likelihood estimate.

At a shared starting point, averaging one appropriately normalized full-gradient step reproduces the corresponding global gradient step. After multiple local steps, sites follow different parameter paths. Their average need not equal the path of centralized training. Learning rates, local step counts, participation, regularization, and stopping criteria therefore matter.

### 7.3 FedProx and the meaning of its coefficient

A mathematically consistent teaching form of a local proximal objective is

$$
\min_u\left\{F_k(u)+\frac{\mu}{2}\lVert u-\pi_r\rVert_2^2\right\}.
$$

During that local fit, $$\pi_r$$ is fixed and $$u$$ changes. The penalty discourages moving far from the current shared model; it is not the same as ridge shrinkage toward zero. Its gradient is $$\mu(u-\pi_r)$$. If the shared vector is (0.4, 0.8) and a candidate is (0.6, 0.7), squared distance is 0.05. With $$\mu=2$$, the penalty is 0.05.

The main article reports $$\mu=2$$. Larger values constrain local departure more strongly, but can also slow useful adaptation. They do not make site populations identical or remove site-specific unmeasured confounding.

### 7.4 Sign conventions and algorithm names

The consistent choices are **maximize log likelihood minus a nonnegative penalty**, or **minimize negative log likelihood plus that penalty**. Equations (4) and (9) add $$L_{\mathrm{reg}}$$ while describing a log likelihood, and the text instantiates it with positive squared distances. Maximizing that expression literally would reward divergence. The intended minimization convention needs to be restored explicitly when implementing it.

The paper compares FedAvg, FedAvgM, and FedProx. Its description identifies an adjacent-round squared-parameter difference with FedAvgM. Standard FedAvgM is defined by server momentum, so the named algorithm should not be reconstructed solely from that penalty. The reported sensitivity comparison does not supply every momentum or optimization setting. [Original FedAvg](https://proceedings.mlr.press/v54/mcmahan17a.html), [FedProx](https://arxiv.org/abs/1812.06127), and [FedAvgM](https://arxiv.org/abs/1909.06335) provide the algorithm definitions.

### 7.5 The combined loop in Box 1

Box 1 sends both $$\pi$$ and $$\beta$$ to sites, obtains updated propensity and outcome parameters, and averages them by patient count. In dependency order, a local Cox update uses weights derived from the propensity model available at that point. If weights change across rounds, the Cox objective changes too.

The box's aggregation lines use a previous-round superscript where the immediately preceding steps describe updated local parameters. This appears to be an indexing inconsistency; the useful interpretation is to aggregate the parameters actually returned in that round. The publication does not provide a complete round count, local-epoch schedule, numerical convergence tolerance, or trial-specific optimization log in the main text.

## 8. IPTW, stabilization, balance, and positivity
{: #weighting }

### 8.1 The paper's weights

Equation (2) gives ordinary, **unstabilized** ATE-style treatment weights,

$$
w_{ki}=\frac{A_{ki}}{e_{ki}}+\frac{1-A_{ki}}{1-e_{ki}}.
$$

A treated person with $$e=0.8$$ receives weight 1.25. A comparator with the same score receives weight 5, because that observed choice is rarer among otherwise similar people. An individual receives the weight for the action actually observed, not both weights simultaneously.

These are not hospital aggregation weights. $$p_k$$ determines how sites contribute to model fitting; $$w_{ki}$$ determines how a patient's observed treatment-outcome record contributes to the adjusted comparison.

### 8.2 Why inverse probabilities recover a common covariate distribution

For any function $$f(Z)$$, the following identity explains the weighting idea:

$$
E\left[\frac{A f(Z)}{e(Z)}\right]
=E\left[\frac{E(A\mid Z)f(Z)}{e(Z)}\right]
=E[f(Z)].
$$

The analogous comparator identity uses $$(1-A)/(1-e)$$. Thus, with the true propensity score and positivity, both weighted arms recover features of the same covariate distribution. Replacing $$f(Z)$$ by an outcome requires the additional causal identification assumptions; balance alone is not a proof of exchangeability.

In a finite sample with estimated scores, equality is approximate. A correctly specified propensity model is one route to consistent weighting. A misspecified common logistic model can remain biased even with many sites and many patients.

### 8.3 Stabilization and clipping are separate decisions

For a specified population treatment prevalence $$q=P(A=1)$$, a common stabilized alternative is

$$
w^{\mathrm{stab}}=\frac{Aq}{e(Z)}+\frac{(1-A)(1-q)}{1-e(Z)}.
$$

Stabilization changes scale by arm. Clipping replaces extreme weights with a bound. Normalizing weights to have mean one is yet another operation. None is identical to changing the propensity score model.

**The main Equation (2) reports neither stabilized numerators nor a clipping threshold.** The current public code uses stabilized weights and clipping; those observations are documented separately in §18. They should not be retroactively asserted as the exact settings used to create the published figures without a matched analysis configuration.

A local treatment prevalence is not necessarily a global prevalence. If each hospital stabilizes using its own treated fraction, the resulting weighted combination can preserve a different site mix than global stabilization. Under effect heterogeneity or a misspecified hazard model, choices of weights can also change the summary being estimated. A numerical cap reduces the influence of extreme observations but introduces a bias–variance tradeoff and changes the exact inverse-probability estimating equation.

### 8.4 Balance diagnostics

For covariate $$j$$ and arm $$a$$, a weighted mean is

$$
\bar Z_{a,j}^{\,w}=\frac{\sum_{ki:A_{ki}=a}w_{ki}Z_{ki,j}}{\sum_{ki:A_{ki}=a}w_{ki}}.
$$

A standardized mean difference divides the difference in arm means by a specified reference standard deviation. A common form is

$$
\mathrm{SMD}_j=
\frac{\bar Z_{1,j}^{\,w}-\bar Z_{0,j}^{\,w}}
{\sqrt{(s_{1,j}^2+s_{0,j}^2)/2}}.
$$

Whether the denominator uses weighted or preweighting variance must be stated; conventions differ. “Successful balancing ratio” is the fraction of selected covariates passing a specified absolute-SMD threshold. It is not the fraction of patients successfully treated, nor a statistical test of no unmeasured confounding.

Global balance can be calculated without exporting records by summing arm-specific weighted counts, first moments, and second moments. It should be accompanied by **within-site** checks: imbalances of opposite signs can cancel in a network-wide mean. Balancing only the reported means also does not ensure balance of nonlinear relationships, interactions, or the entire joint distribution.

### 8.5 Effective sample size and overlap

The teaching diagnostic

$$
\mathrm{ESS}_a=\frac{(\sum_{A=a}w)^2}{\sum_{A=a}w^2}
$$

summarizes how concentrated weights are within an arm. A cohort with thousands of people can have a small effective sample size if a few people carry most of the weight. The main paper reports balancing ratios but does not give a complete trial-by-site set of score distributions, extreme-weight summaries, or effective sample sizes. These are useful additional checks, not reported results to invent.

## 9. Cox regression from hazards to partial likelihood
{: #cox }

### 9.1 Hazard is an instantaneous event rate among those still at risk

For event time $$T$$,

$$
h(t\mid X)=\lim_{\Delta t\to0}
\frac{P(t\leq T<t+\Delta t\mid T\geq t,X)}{\Delta t}.
$$

Equation (5) specifies

$$
h(t\mid X)=h_0(t)\exp(\beta^\top X).
$$

The unspecified $$h_0(t)$$ describes the time pattern of baseline hazard. The exponential multiplier describes relative hazards. If $$X=(A,Z^\top)^\top$$ and there is no treatment interaction, comparing otherwise equal predictor vectors with $$A=1$$ versus $$A=0$$ yields $$\exp(\beta_A)$$.

The paper reuses $$z$$ for covariates in both PS and Cox expressions, without explicitly writing treatment into Equation (5). To estimate a treatment coefficient, its outcome-model design matrix must contain treatment. A treatment-only weighted Cox model and an IPTW Cox model additionally adjusted for baseline predictors are different specifications; their HRs need not have the same marginal/conditional interpretation.

### 9.2 Where the risk-set denominator comes from

Suppose exactly one person has an event at time $$t$$. Conditional on one event occurring among those at risk, that person's modeled share of the total hazard is

$$
\frac{h_0(t)\exp(\beta^\top X_i)}{\sum_{j\in R(t)}h_0(t)\exp(\beta^\top X_j)}
=\frac{\exp(\beta^\top X_i)}{\sum_{j\in R(t)}\exp(\beta^\top X_j)}.
$$

The common baseline hazard cancels. Multiplying these conditional contributions over observed events gives the ordinary Cox partial likelihood, corresponding to Equation (6). “Partial” reflects elimination of the unspecified baseline-hazard component, rather than using only a randomly selected subset of people.

People without an event still matter: they contribute to the denominator while they remain observed and at risk. Someone censored at month 3 contributes to a month-2 risk set but not to a month-4 risk set. The event indicator alone therefore cannot replace the complete time-and-event data.

### 9.3 Proportional hazards and the effect scale

The basic Cox model assumes the relative multiplier does not vary with time. It does not assume a constant baseline event rate. If treatment's effect changes over follow-up, a single fitted HR is a model-dependent summary that can depend on follow-up, censoring, and weighting.

Hazard ratios are also noncollapsible: conditional and marginal HRs can differ even without confounding. Combining different populations or different covariate-adjusted models can change an HR without revealing a causal bias. For absolute risks, additional baseline-hazard/survival estimation and a clearly defined standardization population are required.

## 10. Weighted Cox regression and tied events
{: #weighted-cox }

### 10.1 Rewrite Equation (7) in a readable form

Let $$D_k(t)$$ contain the individuals at site $$k$$ whose event occurs at $$t$$, and $$R_k(t)$$ those still at risk. With fixed weights during a Cox update, Equation (7) is

$$
L_k(\beta)=\prod_t\prod_{i\in D_k(t)}
\left\{
\frac{\exp(\beta^\top X_{ki})}
{\sum_{j\in R_k(t)}w_{kj}\exp(\beta^\top X_{kj})}
\right\}^{w_{ki}}.
$$

Its log form is easier to differentiate:

$$
\ell_k(\beta)=\sum_t\sum_{i\in D_k(t)}w_{ki}
\left[\beta^\top X_{ki}-\log\left\{\sum_{j\in R_k(t)}w_{kj}\exp(\beta^\top X_{kj})\right\}\right].
$$

There are two appearances of the patient weights. A person in the risk set contributes weighted relative hazard to the denominator. If that person has the event, their own event contribution is multiplied by their weight, represented by the exponent in the product form.

### 10.2 Why the numerator has no visible weight

A pseudo-population interpretation might suggest a numerator $$w_i\exp(\beta^\top X_i)$$. Including it would add $$\sum_{\mathrm{events}}w_i\log w_i$$ to the log likelihood. With weights held fixed, that term does not depend on $$\beta$$ and therefore does not change the optimizing Cox coefficients. Its omission is not the same issue as omitting weights from risk sets or from event contributions.

### 10.3 Ties and the Breslow-style structure

When several people fail at the same recorded time, all their numerator terms use the same risk-set denominator in Equation (7). This is a **Breslow-style treatment of ties**. It does not show the sequential denominator adjustments of Efron's method or an exact combinatorial tied-event likelihood.

Discrete EHR timestamps can create many ties, making the convention consequential. A reproducible comparison needs the same tie handling in local, federated, and pooled analyses. The article's statement that lifelines 0.29 was used is not enough to infer every argument passed to a fitter or override the explicitly printed likelihood.

### 10.4 A weighted event is not several newly observed patients

If a patient has weight five, the likelihood contribution is amplified, but the study has not observed five independent copies of that person's outcome. Treating weighted sample size as actual independent sample size can make confidence intervals artificially narrow. This is one reason variance estimation deserves a separate derivation rather than being inferred from the weighting formula.

## 11. Local versus pooled risk sets and sufficient summaries
{: #risksets }

### 11.1 Equation (8) retains each site's denominator

Equation (8) multiplies the local likelihoods across sites. Its denominator still uses $$R_k(t)$$. The log of that product is $$\sum_k\ell_k(\beta)$$. For a common coefficient vector, this resembles a **Cox model stratified by site**, with an unspecified baseline hazard for each site and comparisons made within sites.

An unstratified pooled Cox likelihood instead puts all eligible people still at risk at time $$t$$ into one denominator:

$$
R_{\mathrm{pool}}(t)=\bigcup_kR_k(t),\qquad
\sum_k\sum_{j\in R_k(t)}w_{kj}\exp(\beta^\top X_{kj}).
$$

These are different models and different estimating equations. Summing local losses after their local denominators have been formed cannot reconstruct a ratio whose denominator should first have combined the sites. Federated optimization can approximate a chosen distributed objective, but it cannot make the mathematical distinction disappear.

### 11.2 A small numerical example

At one common event time, consider four people. Both event and risk-set weights are shown; assume treatment is the only Cox predictor.

| Site | Person | Treatment $$A$$ | Weight | Event at this time? |
| --- | --- | ---: | ---: | --- |
| 1 | A | 1 | 2 | Yes |
| 1 | B | 0 | 1 | No |
| 2 | C | 0 | 1 | Yes |
| 2 | D | 1 | 3 | No |

At $$\beta=0$$, all unweighted relative hazards equal one. Site 1 has total weighted risk 3 and weighted treatment total 2. Its score contribution is $$2-2(2/3)=2/3$$. Site 2 has total risk 4 and treatment total 3; its score is $$0-1(3/4)=-3/4$$. Summed local score is therefore $$-1/12$$.

Pooling first gives total risk 7, treatment total 5, event weight 3, and event treatment total 2. The pooled score is $$2-3(5/7)=-1/7$$. Both methods use the same people, weights, and candidate coefficient, yet their slopes differ. They are optimizing different comparisons. This is a teaching example, not a dataset from the article.

### 11.3 Deriving the score and Hessian using risk-set summaries

The following derivation makes the precise communication requirement visible. Define, at site $$k$$ and event time $$t$$,

$$
S_k^{(0)}(t,\beta)=\sum_{j\in R_k(t)}w_{kj}e^{\beta^\top X_{kj}},
$$

$$
S_k^{(1)}(t,\beta)=\sum_{j\in R_k(t)}w_{kj}e^{\beta^\top X_{kj}}X_{kj},
$$

$$
S_k^{(2)}(t,\beta)=\sum_{j\in R_k(t)}w_{kj}e^{\beta^\top X_{kj}}X_{kj}X_{kj}^\top.
$$

These are a scalar, a vector, and a matrix. Also define event summaries

$$
d_k^w(t)=\sum_{i\in D_k(t)}w_{ki},\qquad
E_k^w(t)=\sum_{i\in D_k(t)}w_{ki}X_{ki}.
$$

Differentiating the weighted log likelihood gives the local score

$$
U_k(\beta)=\sum_t\left[E_k^w(t)-d_k^w(t)\frac{S_k^{(1)}(t,\beta)}{S_k^{(0)}(t,\beta)}\right],
$$

and local observed information, the negative Hessian,

$$
I_k(\beta)=\sum_t d_k^w(t)
\left[
\frac{S_k^{(2)}}{S_k^{(0)}}-
\left(\frac{S_k^{(1)}}{S_k^{(0)}}\right)
\left(\frac{S_k^{(1)}}{S_k^{(0)}}\right)^\top
\right].
$$

Every ratio in the last expression is evaluated at the same $$t,\beta$$. The bracket is a weighted covariance matrix of predictors in that risk set. The score compares the predictors carried by observed events with the model's expected predictors among those at risk.

### 11.4 What an exact pooled calculation would require

For an unstratified pooled model, compute $$S^{(q)}=\sum_kS_k^{(q)}$$ for $$q=0,1,2$$ and aggregate event summaries **before forming the ratios**. Sites would need a consistent global event-time grid, risk-set definitions, current coefficient vector, weights, covariate transformations, and tie convention. At each iteration the summaries depend on the current coefficients, so they are generally not a one-time fixed sufficient statistic for all possible $$\beta$$.

For a site-stratified model, form each site's ratios first, then add the resulting score and information. Both can be distributed without sharing a patient table, but they have different messages and assumptions. Fine-grained summaries can also leak information at small sites, so mathematical sufficiency does not equal a privacy guarantee.

The paper's Box 1 describes parameter exchanges. It does not specify a global event-time summary protocol of the form just derived. These equations are therefore **an explanatory reconstruction of what exact pooled or stratified computations would require**, not an undocumented feature attributed to FL-TTE.

### 11.5 Equation (9) introduces another weighting layer

Equation (9) inserts $$p_k$$ outside local log-likelihood contributions, plus regularization. This is not simply taking the logarithm of Equation (8); the latter would yield an unweighted sum of local log likelihoods. If local contributions already sum events, multiplying again by site patient proportion changes site influence.

A site-stratified, patient-weighted objective, a patient-proportion-weighted average of local objectives, and an unstratified pooled objective must be distinguished explicitly. Similar empirical HRs do not prove these objectives are algebraically identical.

<figure>
  <a href="{{ '/assets/rwe/federated-tte/equations-and-algorithm-page.png' | relative_url }}"><img src="{{ '/assets/rwe/federated-tte/equations-and-algorithm-page.png' | relative_url }}" alt="Original page 11 of Li et al., showing Box 1 algorithm, Box 2 theoretical statements, and weighted Cox Equations 7 through 9 with site-local risk sets." width="993" height="1319" loading="lazy"></a>
  <figcaption>Original p. 11, reproduced without content edits. Read the superscript k on each risk set and the additional site weight in Equation (9). The surrounding explanations distinguish the printed equations from teaching reconstructions. <a href="https://doi.org/10.1038/s41746-025-01803-y">Li et al. (2025)</a>; <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>.</figcaption>
</figure>

## 12. Standard errors, confidence intervals, and model comparison
{: #inference }

### 12.1 From the coefficient to the reported interval

For a treatment coefficient and a suitable standard error,

$$
\widehat{HR}=e^{\widehat\beta_A},\qquad
CI_{95\%}=\left[e^{\widehat\beta_A-1.96\,SE},\ e^{\widehat\beta_A+1.96\,SE}\right].
$$

Exponentiation makes the interval asymmetric on the HR scale even when it is symmetric on the log-HR scale. A null-effect Wald test uses $$\widehat\beta_A/SE$$ because $$HR=1$$ corresponds to $$\beta_A=0$$.

The main article reports HRs, intervals, and Z-tests but does not fully derive the covariance estimator underlying its federated results. In particular, Equations (5)–(9) are not enough to establish adjustment for estimated propensity scores, clustering, regularization, or model selection.

### 12.2 Model-based information versus robust covariance

In a conventional correctly specified, unweighted likelihood analysis, inverse observed information provides a model-based covariance approximation. An IPTW pseudo-likelihood changes this calculation. A generic estimating-equation sandwich has the form

$$
\widehat V=A^{-1}BA^{-\top},
$$

where $$A$$ measures the sensitivity of the estimating equation to parameters and $$B$$ measures variability of the corresponding independent-unit influence contributions. For Cox models, those contributions must account for participation in risk sets; they are not obtained by treating the displayed event terms as unrelated independent records.

To account jointly for propensity and outcome estimation, one can conceptually stack treatment-model and outcome-model estimating equations for $$\theta=(\pi,\beta)$$, derive a joint sandwich, and extract its treatment-coefficient block. A suitable bootstrap is another option. These are possible inferential strategies, not methods fully specified in the main paper.

If an entire site's records are treated as a dependence cluster, inference also depends on the number of sites and small-cluster behavior. Five health systems do not provide the same basis for cluster-robust asymptotics as 192 sites. Patient-level and site-level clustering answer different dependence questions.

### 12.3 Normalization must agree between the Hessian and covariance

For a loss already summed over $$n$$ observations, its Hessian contains the sample-size factor. Dividing its inverse by $$n$$ again generally adds an unjustified extra reduction in variance. For an average loss, an additional sample-size adjustment may instead be needed, depending on how the other variance terms are defined. It is the complete convention that matters.

This warning is particularly relevant when comparing code that uses mean cross-entropy for PS fitting with summed Cox loss for outcome fitting. One cannot transfer a covariance formula between them without tracking the normalization.

### 12.4 A federated–pooled difference is a correlated comparison

The federated and pooled estimates in this study use overlapping, often identical underlying records. For their difference,

$$
\mathrm{Var}(\widehat\beta_{FL}-\widehat\beta_{pool})
=V_{FL}+V_{pool}-2\,\mathrm{Cov}(\widehat\beta_{FL},\widehat\beta_{pool}).
$$

An independent-estimates Z-test would omit the covariance term. The publication does not explain its treatment in sufficient detail to verify the comparison tests. A large p-value also does not demonstrate statistical equivalence; an equivalence analysis would require a prespecified acceptable difference and appropriate inference. For computational benchmarking, paired discrepancies, parameter tolerances, and sensitivity to matched settings are often more directly informative.

## 13. Federation, local analysis, and meta-analysis
{: #meta-analysis }

### 13.1 Five different pipelines

| Pipeline | Treatment modeling | Outcome estimation | Main consequence |
| --- | --- | --- | --- |
| Local analysis | Each site estimates its own PS | Each site produces its own HR | Small cohorts, differing models, and limited overlap can destabilize results |
| Fixed-effect meta-analysis | Usually completed locally first | Combine local log-HRs using inverse-variance weights | Targets a common-effect synthesis under its assumptions; does not reconstruct patient-level risk sets |
| Random-effects meta-analysis | Usually completed locally first | Combine estimates allowing between-site variation | Reflects heterogeneity and often widens uncertainty; target differs from a simple patient-count mixture |
| FL-TTE | Shared PS learned through repeated local updates | Shared Cox parameters learned through federation | Uses information across institutions during estimation, not only after each local fit is complete |
| Pooled analysis | Fit from merged records | Fit a specified centralized survival model | A computational reference only if the cohort and modeling choices are defined consistently |

### 13.2 Why meta-analysis can disagree

For local log-HR estimates $$\widehat b_k$$ and variances $$v_k$$, familiar teaching formulas are

$$
\widehat b_{FE}=\frac{\sum_kv_k^{-1}\widehat b_k}{\sum_kv_k^{-1}},\qquad
\widehat b_{RE}=\frac{\sum_k(v_k+\tau^2)^{-1}\widehat b_k}{\sum_k(v_k+\tau^2)^{-1}}.
$$

Here $$\tau^2$$ is between-site effect variance. The paper compares fixed- and random-effects methods but does not provide enough main-text detail to identify every heterogeneity estimator and small-sample correction. These formulas explain the usual weighting distinction, rather than asserting a particular software setting.

Meta-analysis may combine locally misspecified models, poorly balanced comparisons, nonconverged fits, or different conditional HRs. It cannot recover patient-level overlap missing from local design solely by weighting final HRs. Conversely, a well-designed stratified or meta-analytic analysis can be appropriate when the scientific question concerns site-specific effects. Disagreement with an unstratified pooled coefficient is not automatically evidence that meta-analysis is causally wrong.

The authors assume heterogeneity in baseline covariates rather than in the treatment effect when motivating the pooled benchmark. Different underlying baseline hazards, conditional versus marginal effects, and site-specific treatment mechanisms also matter. The observed heterogeneity of local estimates need not be entirely true effect heterogeneity; it can also reflect sampling, design, ascertainment, or estimation differences.

### 13.3 Meta-analysis itself does not rebalance individuals

A final inverse-variance combination of HRs does not assign new IPTW weights to the original patients. Therefore, a “balancing ratio for meta-analysis” requires an additional definition: for example, a summary of the locally weighted covariate distributions used before synthesis. The paper reports such ratios but does not fully describe their construction in its main methods. They should not be interpreted as a standard intrinsic output of fixed- or random-effects meta-analysis.

## 14. The causal assumptions that federation cannot supply
{: #assumptions }

### 14.1 Consistency and well-defined strategies

Observed outcomes for someone following strategy $$a$$ must correspond to that person's counterfactual outcome under the defined strategy. This requires a treatment definition precise enough for the question: initiation, active ingredient, dose, route, exposure window, and relevant co-interventions. “Any drug in a broad class” may describe several intervention versions with different effects.

### 14.2 Conditional exchangeability

A baseline initiation analysis requires a condition such as

$$
(T^0,T^1)\perp A\mid Z,
$$

or a site-aware version conditioning on $$Z$$ and institution $$S$$. It says that after the stated adjustment, treatment selection carries no additional information about counterfactual outcome times. This is an assumption about the data-generating process, not a property ensured by fitting logistic regression.

If institution affects treatment choice and outcome through factors not captured in $$Z$$, a shared model that omits it may not remove confounding. On the other hand, merely adding site indicators may expose within-site lack of overlap. The publication does not establish that all relevant institutional factors or treatment interactions were included.

### 14.3 Positivity

For every covariate profile included in the target population, both strategies need positive probability. If exchangeability is assumed conditional on site, overlap must be adequate within the relevant site–covariate strata. Pooling someone treated at one site with someone untreated at another cannot substitute for a justified cross-site comparability assumption.

Tiny institutions may have no treated patients, no comparator patients, or no events. Shared parameters can improve numerical stability, but the data still contain little or no local information about the treatment contrast. A model can extrapolate; the analyst must recognize that extrapolation.

### 14.4 Censoring and competing events

Baseline treatment weights adjust treatment selection, not automatically loss-to-follow-up selection. If censoring depends on prognostic factors beyond what the outcome analysis handles, additional censoring modeling or a different estimator is needed. Artificial censoring in clone–censor–weight analyses requires its own weights and assumptions.

Death before AD, discharge before a monitored hospital endpoint, and death before extubation are not interchangeable with administrative database end. They change which counterfactual outcome is being estimated. A cause-specific hazard comparison and a cumulative-incidence contrast answer different questions.

### 14.5 Correct measurement, alignment, and model specification

The treatment, covariates, baseline, and outcome must be measured in comparable ways across sites. Pretreatment covariates must precede the treatment decision they adjust. The PS model must adequately capture treatment selection, while the chosen Cox model must support the intended HR interpretation. A model with many covariates is not automatically more valid if some are post-treatment variables, colliders, or poorly measured proxies.

Finally, none of these conditions is a theorem about convergence. A federated algorithm can converge perfectly to a biased observational analysis. This is the most important boundary between the statistical-design problem and the distributed-computing problem.

## 15. The theoretical guarantees and their boundaries
{: #theory }

### 15.1 What Box 2 reports

Theorem 1 assumes a Lipschitz and smooth loss with strong convexity. Using the article's constants, the two reported **right-hand-side bound expressions** are

$$
B_{FL}=\sqrt{\frac{4C^2}{\mu\sigma_{\min}N}},\qquad
B_{meta}=\sqrt{\frac{4C^2p_k}{\lambda\sigma_{\min}N_k}}.
$$

Here $$C$$ controls sensitivity of the loss to parameter changes, $$\lambda$$ describes strong convexity, $$\mu$$ is the proximal coefficient, and $$\sigma_{\min}$$ is a minimum Hessian eigenvalue. **The left-hand sides are inconsistent:** the main results paragraph uses log-HR distances for both methods, whereas Box 2 bounds $$\lVert\log HR_{FL}-\log HR_{pool}\rVert$$ for federation but $$\lVert\log HR_{meta}-\log HR_{pool}\rVert^2$$ for meta-analysis. A norm and a squared norm cannot be compared as though they were the same quantity. The symbols $$B_{FL}$$ and $$B_{meta}$$ above name the printed right-hand sides, without silently repairing that discrepancy.

Theorem 2 states an $$O(1/R)$$ convergence rate toward an approximation of a global optimum, where $$R$$ is the number of iterations. [Box 2, p. 11.](https://www.nature.com/articles/s41746-025-01803-y)

The supporting argument proceeds from stability under changing one observation to a generalization bound, and then uses loss curvature to relate error to coefficient distance. The supplement explicitly uses mean local losses. [Supplementary Notes 1–2, pp. 2–5.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41746-025-01803-y/MediaObjects/41746_2025_1803_MOESM1_ESM.pdf)

### 15.2 Why stability, curvature, and sample size appear

For intuition, changing one record changes an average local gradient on an order of $$1/N_k$$ under bounded contributions. Strong curvature limits how far the optimum can move in response to that perturbation. Averaging the resulting local change with $$p_k$$ scales its effect on the shared parameter.

Curvature also provides a teaching inequality: for a strongly convex objective with minimum curvature $$m>0$$ and minimizer $$\beta^\star$$,

$$
F(\beta)-F(\beta^\star)\geq\frac m2\lVert\beta-\beta^\star\rVert^2.
$$

If an excess-objective bound is actually available, this inequality converts it into a coefficient-distance bound. This explains the square root and inverse-curvature terms. It does not by itself prove that an observed HR is close to the true causal effect.

### 15.3 The sample-size factor cancels in both displayed bounds

Using the paper's definition $$p_k=N_k/N$$ gives

$$
\frac{p_k}{N_k}=\frac1N,
\qquad B_{meta}=\sqrt{\frac{4C^2}{\lambda\sigma_{\min}N}}.
$$

Thus both **right-hand-side expressions** scale as $$N^{-1/2}$$ after substitution. This is not yet a comparable distance-rate statement: if Box 2's squared meta-analysis norm is read literally, taking another square root gives a bound on meta-analysis distance scaling as $$N^{-1/4}$$. If both left-hand sides were intended as ordinary norms, they would instead share the displayed $$N^{-1/2}$$ distance scaling. That source inconsistency must be resolved before asserting one coherent comparison.

For the displayed right-hand sides, the remaining comparison is driven by $$\mu$$ versus $$\lambda$$, not an uncancelled distinction between total sample size and local sample size. Moreover, conventional meta-analysis uses inverse-variance weights, whereas these expressions use patient proportions. The connection between the theorem's meta-analytic object and the empirical fixed/random-effects analyses therefore needs care.

### 15.4 A smaller upper bound does not order realized errors

If method A's error is at most 0.1 and method B's is at most 0.2, it does not follow that A's actual error is smaller: the realized values could be 0.09 and 0.01. The bounds support statements about worst-case control under their assumptions. They do not establish that FL-TTE must be closer to pooled estimates in every dataset, much less closer to causal truth.

Increasing a proximal coefficient changes the optimization problem or the local-update dynamics. It cannot be treated as a cost-free way to prove arbitrary accuracy. The reference point, approximation error, number of local steps, and model bias must also be controlled.

### 15.5 Generalization error is not automatically excess risk

A stability result commonly bounds the difference between population risk and empirical risk for a fitted algorithm. A coefficient-distance argument instead needs an excess-risk or excess-objective bound relative to the relevant minimizer. These are related but distinct quantities. A useful decomposition is

$$
\begin{aligned}
R(\widehat\beta)-R(\beta^\star)
={}&[R-\widehat R](\widehat\beta)
+[\widehat R(\widehat\beta)-\widehat R(\beta^\star)]\\
&+[\widehat R-R](\beta^\star).
\end{aligned}
$$

The middle term contains empirical optimization error. Controlling one generalization gap does not automatically control all three terms or the difference between optima of **different risk-set objectives**. These notes therefore treat the theoretical claims as conditional bounds, not a complete proof of finite-sample equivalence to an unstratified pooled Cox analysis.

### 15.6 Applicability to weighted survival models

Strong convexity is not guaranteed for every Cox design: limited event information, collinearity, and separation can produce near-zero Hessian eigenvalues. Very large IPTW weights can undermine uniform bounded-gradient constants. A Cox event contribution depends on many individuals through its risk set, so replacing one patient can alter more than one event term. An independent-record stability argument needs to handle this dependence explicitly.

The printed theorem also varies between norms and squared norms in different places, and moving a log-HR bound through exponentiation requires an appropriate parameter-range or local Lipschitz argument. These are reasons to avoid repeating the broad phrase “theoretically unbiased.” The main accomplishment of the theoretical discussion is a proposed stability-and-optimization justification under idealized conditions; it is not a proof of the observational identification assumptions in §14.

## 16. Empirical evaluation and reported results
{: #results }

### 16.1 What was evaluated

The two settings deliberately differ. INSIGHT represents relatively sparse, irregular longitudinal outpatient and hospital records for a chronic condition. eICU/MIMIC provides dense short-term critical-care observations. The authors compare pooled, federated, individual-site, fixed-effect meta-analytic, and random-effects meta-analytic estimates, along with covariate balancing ratios.

The main paper does **not** describe a simulation with known treatment effects, repeated Monte Carlo datasets, empirical coverage probabilities, or mean squared error against a known causal truth. “Validated across 192 hospitals” refers to an empirical distributed analysis of these records, not 192 randomized trials.

### 16.2 All nine AD comparisons in Figure 5

Values below are transcribed from Figure 5. Entries are HR (95% CI); they compare the trial drug with its defined active comparator.

| Trial drug | Pooled | FL-TTE | Fixed-effect meta-analysis | Random-effects meta-analysis |
| --- | --- | --- | --- | --- |
| Aspirin | 0.93 (0.91–0.95) | 0.93 (0.90–0.96) | 0.86 (0.84–0.88) | 0.95 (0.87–1.04) |
| Amlodipine | 0.84 (0.81–0.86) | 0.84 (0.81–0.88) | 0.90 (0.88–0.92) | 0.88 (0.81–0.95) |
| Atorvastatin | 0.85 (0.84–0.86) | 0.86 (0.83–0.89) | 0.88 (0.85–0.91) | 0.88 (0.81–0.95) |
| Lidocaine | 0.90 (0.87–0.92) | 0.91 (0.89–0.92) | 0.85 (0.83–0.87) | 0.88 (0.82–0.95) |
| Acetaminophen | 0.89 (0.88–0.91) | 0.91 (0.88–0.94) | 0.94 (0.93–0.96) | 0.96 (0.86–1.08) |
| Famotidine | 0.89 (0.86–0.92) | 0.91 (0.88–0.94) | 0.93 (0.91–0.95) | 0.93 (0.86–1.01) |
| Pantoprazole | 0.88 (0.85–0.91) | 0.91 (0.88–0.94) | 1.09 (1.05–1.13) | 0.95 (0.82–1.10) |
| Fluticasone | 1.01 (0.97–1.04) | 1.04 (0.99–1.09) | 1.11 (1.05–1.18) | 1.12 (1.01–1.25) |
| Albuterol | 0.90 (0.86–0.93) | 0.86 (0.82–0.91) | 0.85 (0.82–0.88) | 0.85 (0.79–0.92) |

Pantoprazole is a clear example of how synthesis methods can change conclusions: fixed-effect meta-analysis is above one, while pooled, FL-TTE, and random-effects point estimates are below one. This is a result requiring explanation of site data, design, estimands, and precision; it is not direct clinical evidence that one mathematical combination uncovers the true drug effect.

The local AD estimates are highly heterogeneous, with the article reporting average $$I^2=0.942\pm0.008$$ across the trials and opposite directions across sites in seven of nine comparisons. These observations motivate the use of shared information, while also motivating a careful examination of site-specific ascertainment and treatment mechanisms.

<figure>
  <a href="{{ '/assets/rwe/federated-tte/figure-5-ad-results-page.png' | relative_url }}"><img src="{{ '/assets/rwe/federated-tte/figure-5-ad-results-page.png' | relative_url }}" alt="Original article page containing Figure 5, comparing pooled, federated, fixed-effect, and random-effects estimates for nine AD drug trials." width="1282" height="1703" loading="lazy"></a>
  <figcaption>Original Figure 5 and its page, reproduced without content edits. The table above improves accessibility of the main estimates; the original also shows null-effect and pooled-comparison tests. <a href="https://doi.org/10.1038/s41746-025-01803-y">Li et al. (2025), p. 7</a>; <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>.</figcaption>
</figure>

### 16.3 Sepsis outcomes in Figure 6

| Outcome | Pooled | FL-TTE | Fixed-effect meta-analysis | Random-effects meta-analysis |
| --- | --- | --- | --- | --- |
| 28-day mortality | 1.10 (1.05–1.15) | 1.08 (1.02–1.14) | 1.16 (1.09–1.23) | 1.01 (0.94–1.07) |
| Time to ICU discharge | 1.03 (0.99–1.08) | 1.04 (0.99–1.09) | 1.09 (1.04–1.14) | 1.14 (1.09–1.20) |
| Time to ventilation cessation | 1.03 (0.98–1.08) | 1.02 (0.97–1.07) | 1.00 (0.95–1.05) | 1.00 (0.95–1.06) |

The FL-TTE mortality estimate is close to the pooled reference, with a reported difference-test statistic of 0.39 and p=0.693. This is agreement with the reported reference under the study's analysis, not evidence that the estimated adverse association is a randomized treatment effect. The temporal concerns in §5 remain relevant regardless of the numerical agreement.

The article illustrates the five largest ICU sites for local estimates, while the federated analysis includes 192 sites. The reported heterogeneity of those displayed local estimates averages $$I^2=0.892\pm0.007$$ across the three endpoints. The plotted subset should not be confused with the complete network.

### 16.4 Covariate balancing results

| Setting and summary | Pooled | FL-TTE | Fixed-effect meta-analysis | Random-effects meta-analysis |
| --- | --- | --- | --- | --- |
| INSIGHT mean balancing ratio | 0.965 ± 0.067 | 0.926 ± 0.066 | 0.767 ± 0.055 | 0.772 ± 0.062 |
| ICU mean balancing ratio | 1.000 ± 0.000 | 0.985 ± 0.014 | 0.667 ± 0.000 | 0.722 ± 0.000 |

These results support improved measured balance in the authors' implemented federated workflow relative to their local/synthesis alternatives. They do not mean every covariate is balanced in every trial or site, nor that a proportion of 0.985 represents a 98.5% probability of an unbiased estimate. The exact threshold, denominator conventions, and construction of meta-analysis balance summaries matter for reproduction.

## 17. Privacy and sensitivity analyses
{: #privacy }

### 17.1 Keeping records local is a data-flow property

The model avoids sending raw patient tables to the coordinating server. It still sends information derived from those records. Parameters, gradients, counts, or small risk-set summaries can reveal information, particularly with repeated queries or small institutions. The paper itself acknowledges model inversion and reconstruction risks.

The main privacy extension perturbs shared gradients with Gaussian noise and reports an $$(\epsilon,\delta)$$ setting of $$\epsilon=1.0$$ and $$\delta=1/N$$, where $$N$$ is trial sample size. Its purpose is to reduce how much the released computation can depend on one protected contribution. It is not encryption and does not prevent interception of network packets by itself.

For a complete differential-privacy claim, the implementation must define neighboring datasets, the protected unit, clipping or sensitivity control, the noise multiplier, sampling, the accountant, and composition across rounds and multiple trials. The main article does not provide all those quantities. A stated privacy budget should therefore be distinguished from an independently verified end-to-end privacy guarantee.

### 17.2 The reported checks

The authors report retained accuracy under the privacy extension, compare different federated aggregation/regularization choices, compare with a federated IPW-MLE alternative, and repeat the ICU analysis using clone–censor–weight alignment. The overall reported pattern is that the federated estimates remain comparatively close to the pooled analysis.

These checks probe different vulnerabilities. Noise sensitivity concerns the computational privacy–accuracy tradeoff; changing the aggregation algorithm concerns optimization; clone–censor–weight concerns trial-time alignment. A favorable result in one category does not validate the others.

The statement about nine ICU privacy trials appears in the main text although its principal ICU evaluation has three outcomes. The additional stratification/analysis grouping needs to be specified before that number is treated as nine distinct primary clinical questions.

## 18. What the public code clarifies and leaves unresolved
{: #code }

The [public reference file, fltte.py, at commit 4cc50f5](https://github.com/lihy96/FederatedTrialEmulations/blob/4cc50f541148dc7bb9f974d739b80dcb00434b4c/fltte.py), was inspected on September 13, 2026. The downloaded file was verified against that immutable commit. This is a source-code reading, not a successful reproduction of the published experiments; the repository does not identify a complete configuration matching each published analysis.

### 18.1 Weight construction and model specification

The inspected file's `cal_weights` uses stabilized weights, adds $$10^{-5}$$ to score denominators, and clamps weights to $$[10^{-6},100]$$; fitting subsequently normalizes them to mean one. This differs from unstabilized Equation (2). Its logistic model uses two linear logits, equivalent to binary logistic regression through their difference. The outcome vector includes treatment and baseline predictors. The file also contains feature-selection gates and additional optional penalties not developed in the main equations.

These observations clarify why the publication's mathematical description cannot be treated as a complete executable specification. In particular, selecting or shrinking covariates through outcome-informed gates changes the fitting problem and can affect both confounding adjustment and uncertainty. It should not be silently combined with a theorem assuming a fixed, strongly convex model.

### 18.2 Optimization and covariance require validation

The inspected loss builds local risk sets and a weighted Breslow-style objective. Its PS cross-entropy is averaged, while its Cox loss is summed. Its standard-error calculation inverts a Hessian and then divides diagonal variances by the event count. The script leaves `df`, `site_list`, and `args` unset and supplies no populated `fit_options`, so it is a template requiring additional inputs rather than a runnable reproduction.

The normalization difference matters for the reasoning in §12.3. A full audit would need to trace scaling, feature selection, penalties, and the final federated variance calculation before accepting intervals. Likewise, site-specific feature standardization must be reconciled with parameter averaging: coefficients expressed in different local units should not be averaged as if they used a common coordinate system.

### 18.3 Settings that must not be invented

The main paper reports Python 3.10, lifelines 0.29, and a proximal coefficient of 2, plus the privacy budget above. It does not supply complete trial-specific learning rates, local epoch counts, global round counts, momentum settings, convergence tolerances, feature-selection settings, or a fully populated configuration. The available file requests several such values but does not establish their published numerical choices.

The main Methods do not provide a definitive stabilized-versus-unstabilized, clipping, robust-variance, or global-versus-local preprocessing configuration matched to every figure. The appropriate conclusion is **incomplete reproducibility detail**, not an invented list of hyperparameters and not a claim that current code observations prove the published results were generated incorrectly.

## 19. A reproducible analysis, from protocol to final estimate
{: #reproduce }

The following is a teaching reconstruction of the decisions needed to implement an analysis inspired by FL-TTE. It deliberately includes decisions that the article leaves unresolved.

1. **Specify the causal question.** Name the patient population, initiation strategies, outcome, horizon, and effect measure. Decide whether the intended summary is marginal, conditional, site-stratified, or a transported network effect.
2. **Align the timeline.** Make eligibility assessment, treatment assignment, and start of follow-up coherent. Resolve prescription-confirmation rules, treatment grace periods, and pre-/post-treatment measurement windows before fitting models.
3. **Harmonize the local analysis tables.** Use common code lists, units, treatment labels, outcome definitions, and transformations. Record per-site exclusions, counts, overlap, missingness, and event ascertainment.
4. **State the treatment-model objective.** Distinguish summed from mean local loss, include relevant site structure if justified, and specify all feature transformations and optimizer settings.
5. **Train and diagnose the shared PS.** Monitor convergence and compare an equivalent centralized fit where permitted. Do not choose models only by treatment-prediction AUC.
6. **Compute prespecified weights.** Record whether numerators are stabilized, which population supplies their prevalence, whether weights are truncated, and whether they are normalized. Examine score overlap, weights, effective sample size, and measured balance globally and within sites.
7. **Fix the survival estimand and risk-set model.** Decide between local/site-stratified and pooled risk sets; specify treatment and other predictors, tie handling, competing events, censoring, and proportional-hazards assessment.
8. **Implement the corresponding distributed computation.** Match the communication scheme to that model. Parameter averaging and global risk-set aggregation must not be described as interchangeable.
9. **Estimate uncertainty for the actual estimator.** Track sum/mean normalization, estimated weights, clustering, penalties, and any model selection. Use a validated sandwich or resampling strategy appropriate to the full procedure.
10. **Benchmark like with like.** A pooled comparator should use the same cohort, transformations, weights, outcome model, risk sets, tie convention, and variance method before discrepancies are attributed to federation.
11. **Audit privacy separately.** Document the messages and protected unit, and verify any claimed differential-privacy mechanism and composition budget.
12. **Report limits alongside results.** Distinguish numerical agreement, measured covariate balance, causal identification, and population generalization. Provide the final executable configuration and protocol deviations.

A useful implementation sketch is:

```text
Agree on protocol and a common feature coordinate system.
At each site: construct eligible records with treatment, baseline covariates,
              duration, and event indicators.

Repeat shared treatment-model rounds:
    distribute current parameters;
    optimize a prespecified local objective;
    aggregate compatible parameter updates;
    assess convergence.

At each site: calculate prespecified IPTW weights.
Aggregate approved balance and overlap diagnostics.

Choose the survival target explicitly:
    site-stratified: retain each site's risk-set denominator;
    unstratified pooled: aggregate risk-set summaries before ratios.

Optimize the chosen weighted survival model.
Calculate valid covariance for the full procedure.
Exponentiate the treatment coefficient; report uncertainty and diagnostics.
```

This sketch keeps the methodological choices visible. The paper's contribution is the proposal and empirical demonstration of a federated TTE workflow; faithful application requires resolving those choices rather than treating the federation loop as a substitute for trial design.

## 20. Source map and connections to other notes
{: #sources }

| Topic | Main-paper location |
| --- | --- |
| Motivation, cohorts, and pooled benchmark assumption | pp. 1–2 |
| Cohort flow and federated architecture | Figure 1, p. 3 |
| Site heterogeneity | Figure 2, p. 4 |
| Local-site comparisons | Figures 3–4, pp. 5–6 |
| AD and ICU meta-analysis comparisons | Figures 5–6, pp. 7–8 |
| Balance results | Figures 7–10, pp. 8–9 |
| Sensitivity analyses and interpretation limits | pp. 6 and 9–10 |
| PS model and objectives | Equations (1)–(4), p. 10 |
| Cox model and weighted local risk sets | Equations (5)–(9), pp. 10–11 |
| Federation algorithm and theoretical claims | Boxes 1–2, p. 11 |
| Detailed AD/ICU data construction and software statement | p. 12 |

**Primary sources:** [Journal article and PDF](https://www.nature.com/articles/s41746-025-01803-y), [publisher's supplementary material](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41746-025-01803-y/MediaObjects/41746_2025_1803_MOESM1_ESM.pdf), and [reference-code repository](https://github.com/lihy96/FederatedTrialEmulations). The displayed source pages preserve their original content and attribution. Teaching examples, rewritten notation, score/Hessian derivations, and methodological critiques in these notes are explanatory additions.

For the related screening workflow, read [High-Throughput Target Trial Emulation for Alzheimer's Disease Drug Repurposing]({{ '/rwe/high-throughput-ad-target-trial-emulation/' | relative_url }}). For the separate problem of assisting protocol construction, see [EmulatRx: Agentic Trial Design]({{ '/rwe/emulatrx-agentic-trial-design/' | relative_url }}). Neither workflow removes the temporal, identification, or survival-model requirements described here.

Background explanations are available in [Inverse Probability Weighting]({{ '/causal-inference/inverse-probability-weighting/' | relative_url }}), [The Cox Proportional Hazards Model]({{ '/causal-inference/cox-proportional-hazards/' | relative_url }}), [Weighted Survival Analysis]({{ '/causal-inference/weighted-survival-analysis/' | relative_url }}), and [Clone–Censor–Weight]({{ '/causal-inference/clone-censor-weight/' | relative_url }}).
