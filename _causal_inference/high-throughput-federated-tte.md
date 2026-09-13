---
layout: "causal-note"
title: "High-Throughput Drug Screening and Federated Target Trial Emulation"
description: "A complete study companion to high-throughput drug screening and federated TTE: IPTW, model selection, Bonferroni correction, federated LR and weighted Cox, and competing events."
group: "Extensions"
order: 23
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-13"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. What does each paper extend?", "anchor": "section-1"}, {"title": "2. Topics and methodological questions", "anchor": "section-2"}, {"title": "3. Discussion: what is the IPTW framework?", "anchor": "section-3"}, {"title": "4. Reading the original text: High-throughput cohorts, ML-PS, and every data level in Boxes 1–2", "anchor": "section-13"}, {"title": "5. Discussion: Does classical IPTW require train/test splitting? How does LR obtain each propensity score?", "anchor": "section-28"}, {"title": "5.1 “Participating in fitting” differs from “fitting using only oneself”", "anchor": "section-29"}, {"title": "5.2 Fitting an actual LR to the existing 1,000-person example", "anchor": "section-30"}, {"title": "5.3 Treated people and controls within the same disease stratum have the same e(L)", "anchor": "section-31"}, {"title": "5.4 Is fitting and weighting the same people data leakage?", "anchor": "section-32"}, {"title": "5.5 Differences from this paper and cross-fitting", "anchor": "section-33"}, {"title": "5.6 Connecting to a research example: Multiple baseline variables, comparing drug A with B", "anchor": "section-34"}, {"title": "5.7 Does TTE require equal group sizes?", "anchor": "section-35"}, {"title": "5.8 How do the g-formula and IPTW differ?", "anchor": "section-36"}, {"title": "5.9 Why does ATT weight treated people by 1 and controls by odds?", "anchor": "section-37"}, {"title": "5.10 Stabilized IPTW and SW_i: Define first, then read the formula", "anchor": "section-38"}, {"title": "5.11 How does baseline IPTW extend to sustained A/B strategies?", "anchor": "section-44"}, {"title": "5.12 How is survival analysis weighted in TTE?", "anchor": "section-45"}, {"title": "5.13 Why does high-throughput TTE need a Bonferroni correction?", "anchor": "section-46"}, {"title": "5.14 Reading the federated TTE paper: Why is treatment the dependent variable and baseline covariates the independent variables?", "anchor": "section-56"}, {"title": "5.15 How are IPTW and propensity-score matching related, and how do they differ?", "anchor": "section-62"}, {"title": "5.16 Unpacking federated LR: From one patient's probability to training across hospitals", "anchor": "section-63"}, {"title": "5.17 Unpacking federated weighted Cox: Equations (5)–(9)", "anchor": "section-77"}, {"title": "5.18 How do competing events affect AD risk, Cox models, and IPTW?", "anchor": "section-100"}, {"title": "6. References and source articles", "anchor": "section-39"}]
previous_note: "/causal-inference/g-estimation/"
next_note: "/causal-inference/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). Foundational framework: [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}).

<aside class="study-callout study-callout--note" markdown="1">

**Purpose of this note**

This note examines the methods used in the two papers below, including IPTW, high-throughput cohort construction, propensity-score model selection, multiple testing, federated regression, and competing events. Coverage is selective and focuses on methodological explanation.

</aside>


## 1. What does each paper extend?
{: #section-1 }

| Paper | Extension | Connections to existing notes |
| --- | --- | --- |
| Zang et al., 2023, *High-throughput target trial emulation for Alzheimer’s disease drug repurposing with real-world data*, Nature Communications 14:8180 | Scales TTE into a large drug-repurposing screening workflow; compares machine-learning propensity-score models within IPTW, emphasizing baseline covariate balance after model selection | [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}); [Clinical Records, NLP, Imaging, and Machine Learning]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }}) |
| Li et al., 2025, *Federated target trial emulation using distributed observational data for treatment effect estimation*, npj Digital Medicine 8:387 | Extends TTE to multiple institutions without sharing patient-level data; connects federated protocol design, federated IPTW, and federated Cox modeling | [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}); [Cox Proportional Hazards]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}) |

The first primarily asks how to conduct many drug comparisons at scale; the second asks how to collaborate on estimation when data remain distributed across institutions. In both, examine the target population, strategies, time zero, outcome, target effect, and identification assumptions individually.

## 2. Topics and methodological questions
{: #section-2 }

- **High-throughput TTE:** defining protocols and comparator drugs; distinguishing propensity-score prediction performance from covariate balance; interpreting screening and cross-database validation.
- **Federated TTE:** which computations remain local and which information is exchanged; differences from aggregate-data analysis and meta-analysis; handling site heterogeneity and the target population.
- **Connections and limits:** which implementation steps are extended, which causal identification assumptions remain, and whether high-throughput screening can be connected to federated analysis.

These questions guide the methodological discussion below. The analysis distinguishes the authors’ claims, interpretation, and issues that require further verification.

## 3. Discussion: what is the IPTW framework?
{: #section-3 }

**Inverse probability of treatment weighting (IPTW) changes each record’s contribution so that treated and control groups represent the same target-population composition before outcomes are compared.** IPW is the general term; IPTW addresses treatment selection, while IPCW addresses censoring selection.

Here “framework” means a workflow: **define the target → assemble baseline variables → estimate treatment probabilities → calculate weights → inspect balance and extreme weights → conduct weighted outcome and uncertainty analyses**. Calculating weights alone does not complete effect estimation.

### Locating IPTW within TTE
{: #section-4 }

**TTE is the overall design-and-analysis framework; IPTW is one estimation method for addressing confounding of treatment selection within it.** Its use is prespecified in the protocol. Weights are calculated after observational records have been organized to emulate the target trial, then used in outcome analysis.

The following is a teaching sequence; actual research may iterate between the protocol and data feasibility:

<pre class="mermaid">flowchart TD
    A[&quot;Specify target trial: population, strategies, assignment, outcome, follow-up, estimand, analysis&quot;] --&gt; B[&quot;Emulate with records: eligibility, strategy grouping, time zero&quot;]
    B --&gt; C[&quot;Assemble pretreatment confounding information; assess exchangeability and positivity&quot;]
    C --&gt; D[&quot;Estimate propensity scores and calculate IPTW&quot;]
    D --&gt; E[&quot;Check weighted balance, overlap, and extreme weights&quot;]
    E --&gt; F[&quot;Estimate effects and uncertainty with weighted risk or survival analysis&quot;]
    F --&gt; G[&quot;Interpret using identification assumptions and sensitivity analyses&quot;]</pre>

| Stage | Concrete question | IPTW’s role or limit |
| --- | --- | --- |
| 1. Design the target trial | Who participates, which strategies are compared, and what are baseline, outcome, horizon, and target effect? | Prespecify confounding adjustment, covariates, and diagnostics. The target population affects weight choice; do not apply a formula before deciding the question |
| 2. Map observational records to the trial | Who is eligible then, which strategies are compatible with their actions, and when are outcomes counted? | IPTW does not establish correct enrollment, grouping, or time zero; these require explicit design |
| 3. Address nonrandom treatment selection | Why do health status and medication history make some people more likely to receive a treatment? | Estimate probabilities of observed treatment choices conditional on baseline information and construct IPTW so both groups can represent the same baseline target composition |
| 4. Diagnose adjustment | Are measured variables balanced, is there adequate overlap, and do a few large weights drive results? | Inspect diagnostics after weighting. Revise models if necessary, or explicitly revise the target population/strategies when warranted; do not select models for favorable outcomes |
| 5. Analyze outcomes | How do risks, survival curves, or HRs differ under the strategies? | Use weights in the relevant estimators; weights themselves are not treatment effects |
| 6. Interpret results | Is a causal interpretation warranted, and for which population? | Balance does not establish absence of unmeasured confounding. Design, measurement, censoring, and model conditions still require assessment |

#### It addresses the random-assignment component without actually randomizing
{: #section-5 }

In an actual randomized trial, strategy assignment at time zero is independent of baseline prognostic factors under the randomization mechanism. Chance imbalance can still occur in a finite sample.

An observational emulation groups people using actual care records. Health status may affect both medication and outcome, so the trial’s protection against confounding cannot simply be assumed. IPTW addresses this difference: under adequate confounding information, positivity, consistency, reliable probability estimation, and other relevant conditions, weighting supports the target causal comparison.

**It changes analytical contributions, not actual treatment assignment or group membership.** Randomization makes both measured and unmeasured baseline factors independent of assignment under its mechanism; observational IPTW provides no such guarantee for unmeasured confounding.

Within the seven target-trial components, IPTW therefore relates both to observational emulation of treatment assignment and to the analysis plan. It cannot by itself determine whether a study estimates ITT, initiation, or sustained-strategy PP. That depends jointly on strategy definitions, observed assignment information, follow-up, and analysis.

#### “When to use it” means both research workflow and patient time
{: #section-6 }

- **Research workflow:** specify adjustment in the protocol, build the analytical cohort, estimate propensity scores, calculate and diagnose weights, and finally analyze outcomes using them. The probability model predicts treatment; follow-up outcomes should not select weights that produce a significant drug effect.
- **Patient time:** confounding information for baseline IPTW precedes the treatment decision and adjusts selection at time zero. Researchers may compute weights years later from historical records; that does not turn later health measurements into baseline variables.
- **Sustained-treatment questions:** subsequent treatment decisions may require time-updated treatment weights. Artificial censoring for protocol deviations requires corresponding censoring weights. A single baseline IPTW does not automatically address all later selection, and the same adherence process should not be adjusted twice.

#### Connecting to the 1,000-person example
{: #section-7 }

TTE first specifies the question: how would treatment versus no treatment at baseline affect one-year mortality in these 1,000 people? It defines eligibility, baseline, and follow-up. Observed records then show that the treated and control groups contain 80% and 20% high-risk patients. **IPTW enters here, addressing their different pretreatment compositions.** After weighting makes each group represent a population split equally between low and high risk, weighted risks can be calculated. §§3.1–3.3 show the arithmetic.

For the foundational design see [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}); for the complete protocol components see [The Hormone-Therapy Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}).

### 3.1 Why is a direct comparison unfair?
{: #section-8 }

Use the teaching data from [the same 1,000-person table]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-1): compare one-year mortality after initiating versus not initiating treatment at baseline, temporarily assuming everyone’s one-year outcome is known.

| Pretreatment health | Treated people | Treated deaths | Untreated people | Untreated deaths |
| --- | ---: | ---: | ---: | ---: |
| Low risk | 100 | 5 | 400 | 40 |
| High risk | 400 | 80 | 100 | 40 |

Crude risks are 85/500 = 17% in the treated group and 80/500 = 16% in controls. Yet 80% of treated people are high-risk, compared with only 20% of controls. The comparison mixes treatment with differences in health composition.

The target question concerns the original 1,000 people, half low-risk and half high-risk: what would their risks be if all were treated versus all untreated? Both groups should therefore represent this equal mixture.

For the multivariable A/B research workflow, see [the complete multivariable LR–IPTW example]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15). The single-variable table here is retained for introductory calculation; the two datasets should not be mixed.

### 3.2 Propensity scores predict treatment choice
{: #section-9 }

Let $$A=1$$ mean treatment, $$A=0$$ no treatment, and $$L$$ pretreatment health. The propensity score is:

$$
e(L)=P(A=1\mid L).
$$

$$e$$ names the function, $$P$$ denotes probability, and the vertical bar means given. Read this as the probability of receiving treatment among people with these pretreatment characteristics. It is not mortality probability or the probability the drug works. This probability is estimated from observational data, not an actual investigator-controlled randomization probability.

Treatment probability is 100/500 = 0.2 among low-risk people and 400/500 = 0.8 among high-risk people. With multiple baseline characteristics, logistic regression or other machine-learning models can estimate individual probabilities.

### 3.3 Why invert probabilities, and why do the two groups use different formulas?
{: #section-10 }

There are only 100 low-risk treated people, but they need to represent the 500 low-risk people in the target population. Each record must therefore contribute 500/100 = 5 times its original amount—the inverse of the treatment probability, 0.2.

Common unstabilized baseline weights for the average effect in the full target population are:

$$
w_i=\begin{cases}
1/e(L_i),&A_i=1,\\
1/[1-e(L_i)],&A_i=0.
\end{cases}
$$

$$i$$ indexes individuals; $$w_i$$ is a unitless weight; $$L_i$$ and $$A_i$$ are that person’s health and observed action. In practice use estimated propensity scores. Treated people receive the inverse treatment probability; controls receive the inverse no-treatment probability. **Invert the probability of the action actually observed. Do not apply 1/e to everyone.**

| Health and action | Probability of the action | Weight | Weighted people | Weighted deaths |
| --- | ---: | ---: | ---: | ---: |
| Low risk, treated | 0.2 | 5 | 100 × 5 = 500 | 5 × 5 = 25 |
| High risk, treated | 0.8 | 1.25 | 400 × 1.25 = 500 | 80 × 1.25 = 100 |
| Low risk, untreated | 0.8 | 1.25 | 400 × 1.25 = 500 | 40 × 1.25 = 50 |
| High risk, untreated | 0.2 | 5 | 100 × 5 = 500 | 40 × 5 = 200 |

Weights apply to the whole record, so both people and deaths must be weighted. Increasing only the denominator would artificially lower risk.

Weighted treated risk is (25 + 100)/1,000 = 12.5%; weighted control risk is (50 + 200)/1,000 = 25%. The risk difference is −12.5 percentage points and the risk ratio is 0.5. These are teaching numbers, not paper findings.

Weighting preserves the risks within each health stratum and changes the strata’s contributions to the overall mean. The “pseudo-population” is this weighted distribution; no patients are added and no individual’s other counterfactual is observed. Standard errors cannot treat the inflated weighted count as independent observations.

### 3.4 Connecting this to the 2023 paper
{: #section-11 }

Source locations: PDF p. 10, Table 1; p. 11, “ML-PS and IPTW,” equation (1); p. 12, “Statistical analysis.”

- **Study groups:** initiation of a target drug versus alternative drugs. The paper’s control group does not mean no medication at all. Its $$Z$$ corresponds to $$A$$ here, and its baseline covariates $$X$$ correspond to $$L$$.
- **ML-PS:** machine learning estimates the probability of receiving the target drug. The authors compare model classes and use weighted balance and other metrics for selection. A higher treatment-prediction AUC does not guarantee better confounding control.
- **Stabilized IPTW:** treated weights are $$P(A=1)/e(L)$$, and control weights are $$P(A=0)/[1-e(L)]$$. Numerators are the corresponding action proportions in the overall analytical population; denominators are probabilities conditional on baseline characteristics. Both numerators are 0.5 in this example, changing weights 5 and 1.25 to 2.5 and 0.625. The normalized group risks remain 12.5% and 25%. Stabilization neither guarantees elimination of extreme weights nor adds independent information; this scaling property of group means should not be generalized to every weighted model.
- **Balance diagnostics:** standardized mean differences (SMDs) and other measures compare weighted measured characteristics. An SMD expresses a between-group difference relative to variability; it is neither a treatment effect nor a p-value.
- **Outcome analysis:** the paper uses weighted Cox and adjusted Kaplan–Meier estimates and reports adjusted HRs and survival differences. IPTW specifies records’ contributions, while survival methods address event timing. An HR is not a five-year risk ratio. With censoring, the simple complete-outcome proportions used here cannot be applied directly.

The methods also assume noninformative censoring for time-to-event analyses. Using IPTW therefore does not establish that loss-to-follow-up bias was automatically addressed. §4 discusses model-selection rules and limits of what the reported extreme-weight procedures establish.

### 3.5 When is a causal interpretation warranted?
{: #section-12 }

1. **Adequate confounding information:** within measured health strata, groups can represent comparable patients’ outcomes under their respective treatments. Unrecorded severity, health behaviors, or similar factors may violate this.
2. **Available comparison data—positivity:** both actions can occur in relevant covariate combinations of the target population. Infinite weights cannot create evidence where no controls exist; near-zero probabilities can let a few records dominate.
3. **Defined interventions and reliable timing:** treatment, baseline, and outcomes are correctly defined, consistency and related conditions hold, and post-treatment variables are not indiscriminately treated as baseline confounders.
4. **Appropriate estimation:** treatment probabilities are reliable, missingness and censoring are handled appropriately, and outcome and uncertainty estimators suit the problem.

Measured balance is diagnostic evidence, not proof against unmeasured confounding. IPTW cannot automatically repair an incorrect time zero or immortal time bias. For sustained medication use, baseline IPTW alone does not address later discontinuation selection; longitudinal treatment or censoring weights should follow the target strategy.

**Self-check:** a person has treatment probability 0.8 but is actually untreated. What is the weight? It is 1/(1 − 0.8) = 5, using the probability of the action actually observed: no treatment.

For the full foundational derivation see [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}); for survival-outcome interpretation see [Cox Proportional Hazards]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}).

## 4. Reading the original text: High-throughput cohorts, ML-PS, and every data level in Boxes 1–2
{: #section-13 }

Basis: Results, Fig. 1, and Boxes 1–2 on pages 2–4 of the 2023 paper's PDF, plus Methods, Table 1, and Equations (1)–(5) on pages 10–12. This section explains the reported algorithm step by step; it does not claim an audit of the open-source code. Illustrative sample sizes, scores, and SMD examples are not study results.

### Source excerpt
{: #section-40 }

> Taking the OneFlorida database (see Data Section) as our discovery set, we included 73,927 patients with MCI diagnosis from 2012 to 2020 (Fig. 1a). We found 1,825 unique drug ingredients and, for each drug ingredients we emulated 100 trials by building different comparison groups (exposed to random alternative drugs, or exposed to similar drugs under the same ATC-L2 category), leading to 182,500 trials in total. We focused on 66 drugs with 6,600 emulated trials of which each treatment group has ≥ 500 patients.
>
> For each emulated trial, we randomly partitioned the data into mutually exclusive training and testing subsets with a ratio of 80:20. Different machine learning-based propensity score (ML-PS) models, including regularized logistic regression (LR), gradient-boosted machines (GBM), multi-layer perceptrons (MLP), and long short-term memory networks (LSTM), were trained on the same training set following a tenfold cross-validation (CV) procedure (“Method” Section and Fig. 1b), and the best model hyperparameters were selected by following three strategies: (a) the area under the receiver operating characteristic curve (AUC) score on the validation fold during the CV procedure, (b) the cross-entropy loss (negative log-transformed likelihood) on the validation fold during the CV procedure, and (c) our proposed strategy, which leverages balance performance on the training and validation combined folds, and AUC on the validation fold during the CV procedure (Method Section and Box 1).
>
> We evaluated the performance of selected models in terms of balancing baseline covariates before and after IPTW on the training, testing, and combined datasets. We considered 267-dimensional baseline covariates including age, gender, comorbidities, and medication use history (Method section). We considered one covariate as balanced if its standardized mean difference (SMD) of its prevalence ≤ 0.1<sup>24</sup>, and one emulated trial before/after IPTW is balanced if the ratio of unbalanced features among all covariates before/after IPTW ≤ 2%<sup>7</sup>. We summarized our cross-validation algorithm for the ML-PS model selection and training in Box 1 (Method section), the evaluation algorithm in Box 2 (Method section), and an illustration in Fig. 1b.

### Summary of the source passage
{: #section-41 }

The study used OneFlorida as its discovery dataset and included 73,927 patients diagnosed with mild cognitive impairment (MCI) during 2012–2020 (Fig. 1a). It identified 1,825 distinct drug ingredients. For every ingredient, 100 trials were emulated by constructing different comparison groups: people receiving randomly selected alternative drugs, or people receiving similar drugs in the same ATC-L2 category. This produced 182,500 emulations overall. The focused analysis included 66 drugs and their 6,600 emulations, with at least 500 patients in each target-treatment group.

Within every emulation, the data were randomly divided into nonoverlapping training and test subsets in an 80:20 ratio. On the same training subset, tenfold cross-validation trained machine-learning propensity-score models: regularized logistic regression (LR), gradient-boosted machines (GBM), multilayer perceptrons (MLP), and long short-term memory networks (LSTM). Three separate strategies selected hyperparameters: (a) validation-fold area under the receiver operating characteristic curve (AUC); (b) validation-fold cross-entropy, the negative log likelihood; or (c) the authors' strategy, combining covariate balance across the training and validation folds with AUC on the validation fold (Methods and Box 1).

The selected models were evaluated for baseline-covariate balance before and after IPTW in training, test, and combined datasets. The 267-dimensional baseline covariates included age, gender, comorbidities, and medication history. An individual covariate was considered balanced when its standardized mean difference (SMD) was no greater than 0.1<sup>24</sup>. An emulation was considered balanced before or after IPTW when, in the corresponding state, no more than 2% of all covariates remained unbalanced<sup>7</sup>. Box 1 summarizes cross-validation for model selection and training, Box 2 evaluation, and Fig. 1b illustrates the procedure. The superscripts 24 and 7 are references in the original passage; the subsequent sections clarify the continuous-variable and treatment-group terminology.

### Fig. 1: Overall workflow
{: #section-42 }

![Fig. 1: High-throughput target trial emulation, ML-PS selection, and drug-repurposing screening](/assets/causal-inference/tte-extension/zang-2023-fig-1.png)

### Boxes 1–2: Model training, selection, and evaluation algorithms
{: #section-43 }

![Boxes 1 and 2: Cross-validation for ML-PS selection and evaluation on training and test datasets](/assets/causal-inference/tte-extension/zang-2023-box-1-2.png)

*Fig. 1 and Boxes 1–2 from Zang et al. (2023) accompany the analysis below.*

### 4.1 First identify the role of this passage within TTE
{: #section-14 }

Fig. 1a constructs a target trial emulation cohort for each drug; Fig. 1b selects propensity-score models for IPTW and checks covariate balance; only Fig. 1c proceeds to weighted survival analysis and candidate-drug screening.

The focus is **how to select a treatment-probability model better suited to baseline confounding adjustment**. Its label is receipt of the target or comparator medication, not future AD occurrence.

### 4.2 What do 73,927, 1,825, 100, 182,500, 66, and 6,600 mean?
{: #section-15 }

- **OneFlorida discovery set:** the electronic health record database first used for method evaluation and candidate-signal discovery. MarketScan is an insurance claims database used for replication in another database. Database-level discovery/replication differs from train/test splitting within each emulation.
- **73,927:** the OneFlorida pool of patients diagnosed with MCI (mild cognitive impairment) during 2012–2020. This is neither each drug cohort's size nor all OneFlorida patients, and does not mean everyone later develops AD (Alzheimer's disease). Formal drug comparisons additionally apply age, prior AD, observation, treatment, and other eligibility criteria.
- **1,825 unique drug ingredients:** distinct drug ingredients identified in this population. Prescriptions are grouped by ingredient; brands, individual prescriptions, and individual doses are not separate candidate drugs.
- **100 emulations per drug:** repeat emulations of the same target drug with different constructed control groups. Methods specifies 50 random-control and 50 same-ATC-L2 emulations. These are neither 100 actual randomized trials, 100-fold CV, nor 100 model fits.
- **182,500:** the paper's reported overall emulation count, 1,825 × 100. Its scope differs from the focused 6,600-emulation analysis.
- **66 drugs and 6,600 emulations:** this section focuses on 66 drugs meeting “at least 500 eligible patients in the treatment group,” with 66 × 100 = 6,600. Treatment group means each comparison's target-drug group; it does not establish at least 500 in each group or at least 500 AD events.

A patient may appear in emulations for different drugs or control constructions. Trial sample sizes cannot be added as independent patients, and repeated emulation results need not be independent.

### 4.3 Why two control types? What exactly is random?
{: #section-16 }

**Random alternative drugs:** construct controls from eligible recipients of other medications. Randomness enters investigators' selection of comparison data, not patients' actual medication allocation. Comparator indications may differ from the target drug, so indication and disease differences still need attention.

**Same ATC-L2:** construct comparisons from other drugs in the target drug's second-level ATC class. ATC classifies drugs by anatomical, therapeutic, pharmacological, and chemical characteristics; the second level is a pharmacological or therapeutic subgroup, broader than an individual ingredient. It helps identify closer comparators, but shared classification does not ensure comparable prescribing indications, severity, or patients. [WHO ATC structure](https://www.who.int/tools/atc-ddd-toolkit/atc-classification)

An emulation can be summarized as “target-drug initiators versus alternative-drug initiators selected in this round.” This passage and Boxes 1–2 alone do not establish that every control group contains exactly one ingredient or that sampling across all 100 rounds is independent. Exact sampling units, ratios, and random seeds need implementation checks.

Changing controls can change the clinical contrast and analytical population, so 100 emulations are not simply 100 independent measurements of one fixed parameter. Their purpose is to examine dependence on comparator construction, not turn observational research into a randomized trial.

### 4.4 Each level of Fig. 1a
{: #section-17 }

The top level is database population coverage; the next is the MCI pool, people with AD records, and ingredient count; only the next level applies eligibility for a specific drug. Thus, OneFlorida's 10,530 AD patients in the figure cannot directly become an individual drug trial's event count, nor can all be assumed to occur after that trial's time zero.

The two paths represent target-drug and alternative-drug initiators. Eligibility includes MCI diagnosis before medication initiation, sufficient baseline records, no prior AD/related dementia, and other criteria. Controls additionally exclude relevant target-drug users. Methods/Table 1 specifies age ≥50 and baseline observation ≥1 year; the figure abbreviates these as >50 and >1 year. Exact reproduction needs a code check for these boundary differences.

At the bottom, $$n_t,n_c$$ are treatment and control counts; $$n_{t,1},n_{c,1}$$ count recorded AD; $$n_{t,0},n_{c,0}$$ count people without AD who meet the complete-follow-up definition; $$n_{t,c},n_{c,c}$$ denote incomplete follow-up. The first t/c subscript indicates group; a second c indicates censoring. Incomplete follow-up does not confirm five years without AD. The figure does not replace explicit censoring coding and risk-set analysis.

### 4.5 Two layers of splitting within one emulation
{: #section-18 }

Consider an emulation with 1,000 people:

```text
One drug and one control-construction round: 1,000 people
├─ Outer training set: 800 people, used by Box 1
│  ├─ Inner fitting: 9 folds each time, approximately 720 people
│  └─ Inner validation: 1 fold each time, approximately 80 people, rotating 10 times
└─ Outer test set: 200 people, reserved for Box 2 evaluation
```

**Mutually exclusive** means that this emulation's training and test subsets do not overlap, not that patients cannot appear in another emulation. The text says random splitting, but does not alone establish treatment-stratified sampling, time-based splitting, or site-based splitting.

80:20 is not the treatment-to-control ratio; both training and test sets should contain data supporting comparison of the groups. Randomly splitting data does not randomize treatment.

**10-fold CV:** divide the 800 people into 10 parts; train on 9 and validate on the remaining 1, rotating until every part has served as validation. These are ten parts of 800, not ten parts of all 1,000. Fold sizes can differ slightly when counts are not divisible.

The outer test set is an internal holdout, not an external database. “Unseen” means records unused in a particular fit, not guaranteed generalization to other hospitals or periods.

### 4.6 Unpacking 267-dimensional baseline covariates
{: #section-19 }

Methods gives **age 1 + sex 1 + time from MCI diagnosis to drug initiation 1 + comorbidities 64 + prior drug ingredients 200 = 267**.

- Age and the time interval are continuous variables.
- Sex is binary-coded according to the paper's protocol; the 64 comorbidity and 200 prior-medication indicators are also 0/1. These indicate presence or absence of database records, whose reliability depends on recording and phenotype definitions.
- “267 dimensions” means 267 information columns per person, not 267 patients, outcomes, or trials.
- LSTM also uses temporal pretreatment comorbidity and medication histories; not every model has only one static 267-element input vector. Balance checks still concern the specified baseline covariates.

Historical medication is pretreatment confounding information; the target-drug label defines the current strategy group. Do not conflate them or use subsequent AD occurrence as a PS input.

### 4.7 Four model families, parameters, and hyperparameters
{: #section-20 }

Every ML-PS model estimates “the probability of membership in the target-drug group given baseline information.” An output of 0.7 means an estimated 70% treatment probability, not a 70% probability that the drug works.

| Model | Beginner's interpretation | Relevant settings in this paper |
| --- | --- | --- |
| LR: regularized logistic regression | Combine weighted features and map them to a 0–1 probability; regularization limits excessive coefficients or complexity | L1, L2, no regularization; inverse regularization strength |
| GBM: gradient-boosted machines | Successively improve treatment-probability predictions with tree models, representing nonlinearity and interactions | Tree depth, leaf count, minimum samples per leaf |
| MLP: multi-layer perceptron | A multilayer neural network processes feature combinations | Hidden width/depth, learning rate, weight decay |
| LSTM: long short-term memory | A sequence network uses the ordering and evolution of pretreatment history | A two-layer bidirectional LSTM with attention; hidden dimension and other settings searched |

A bidirectional LSTM processes the already delimited historical sequence; it does not authorize using post-time-zero information. The GBM description mentions random forests as base learners while identifying LightGBM as the implementation. Verify the exact architecture in code; this wording does not make GBM and random forests the same algorithm.

**Parameters** are learned from training data, such as LR coefficients and neural-network connection weights. **Hyperparameters** specify how learning occurs and how much complexity is allowed, such as regularization strength, tree depth, or hidden width. In Box 1, $$\phi$$ denotes learnable parameters, $$\theta$$ a hyperparameter configuration, and $$f_{\theta,\phi}$$ the model determined by both; uppercase $$\Theta,\Phi$$ are candidate sets. A prime marks the final selection, a hat a fitted value, and superscript $$k$$ a fold, not exponentiation.

“Same training set” means models are compared using the same outer training sample. It does not alone guarantee identical inner splits, seeds, or feature representations for every model. In Box 1's written sequence, K-fold partitioning occurs within each hyperparameter configuration.

Methods search settings for reproduction: LR inverse strength from $$10^{-3}$$ to $$10^3$$ in exponent steps of 0.5; GBM depths 3/4/5, leaf counts 5/25/45/65/85/105, and minimum leaf samples 200/250/300; MLP hidden dimensions 32/64/128 or two layers [32,32]/[64,64]; LSTM hidden dimensions 64/128/256; both neural-network families use learning rates 0.001/0.0001, weight decay 0.001/0.0001/0.00001/0.000001, 15 epochs, and batch size 128. An epoch is one pass through training data; a batch is the set used for one parameter update. These are the paper's choices, not universal optimal settings.

### 4.8 What do AUC, cross-entropy, and balance assess?
{: #section-21 }

**AUC:** area under the ROC curve. Across probability thresholds, ROC compares the true-positive rate (the proportion of treated people predicted treated) with the false-positive rate (the proportion of controls predicted treated). AUC measures ranking: for a randomly selected treated person and control, how often does the model assign the treated person a higher treatment probability? Ties usually count one-half. 0.5 is near random ranking and 1 perfect ranking; AUC is not classification accuracy. Higher AUC means better treatment discrimination in those data, not better causal identification.

**Binary cross-entropy** measures the probability assigned to the actual action. For an actual treated person, loss is $$-\log p$$; for an untreated person, $$-\log(1-p)$$. $$p$$ is the model's treatment probability, and $$\log$$ is the natural logarithm here; the negative sign makes smaller assigned probabilities yield greater loss. For an actual treated person, predicting 0.9 gives loss approximately 0.105, while 0.1 gives approximately 2.303.

For $$m$$ people, a common average loss is:

$$
L=-\frac{1}{m}\sum_{i=1}^{m}\{T_i\log p_i+(1-T_i)\log(1-p_i)\}.
$$

In Box 1, $$T_i$$ is the treatment label, 1 for the target drug and 0 for control; $$p_i$$ is person i's predicted treatment probability. $$\sum$$ sums over people, and division by m averages. This is treatment-prediction loss, not a treatment effect. For label 1 only the first term remains; for 0 only the second. Independent Bernoulli-label likelihood multiplies actual-action probabilities; logarithms turn multiplication into addition, and a negative sign gives this negative log-likelihood. Sum and mean differ only by a fixed scale. Regularized models may add a penalty to the fitting objective.

**Balance** asks whether converting those probabilities to IPTW brings the groups' baseline characteristics closer. Predictive ranking, probability fit, and weighted balance are different metrics.

AUC is insensitive to probability changes that preserve ordering, but IPTW depends on numerical probabilities. Moving a treated person's probability from 0.6 to 0.99 changes their weight; assigning an actual control a treatment probability of 0.99 gives an unstabilized weight of 1/(1−0.99)=100. Easy treatment prediction may itself reflect poor overlap.

### 4.9 Three selection strategies: Fitting objectives differ from selection criteria
{: #section-22 }

| Strategy | Hyperparameter selection in inner CV |
| --- | --- |
| (a) AUC | Prefer higher validation-fold AUC |
| (b) Cross-entropy | Prefer lower validation-fold cross-entropy |
| (c) Authors' strategy | First minimize the mean count of unbalanced variables across folds; break ties with higher mean validation AUC |

**These do not separately train an “AUC model,” a “cross-entropy model,” and an “SMD model.”** Box 1 first learns parameters using a fitting objective such as cross-entropy, then compares hyperparameter candidates with the selected criterion. It does not directly perform gradient descent on SMD or simply add AUC and SMD into one score.

For example, candidate A has mean imbalance count 4 and AUC 0.70; B has 7 and 0.85; C has 4 and 0.74. The authors' strategy eliminates B first, then selects C for its higher AUC. AUC-only selection chooses B. These values are illustrative.

### 4.10 SMD and two levels of passing criteria
{: #section-23 }

For a beginner's step-by-step calculation, see [Step Six: Check Weighted Balance in the Four Baseline Variables]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-22). It moves from the purpose of diagnostics, weighted means, and variances to hand calculations of simulated SMDs, separate overlap/weight/ESS checks, and the limits of those checks.

**Typography correction: The text says SMD ≤0.1; the following 24 is a citation number. The 7 after 2% is also a citation number.** It is not 0.124 or 2% raised to the seventh power.

For one covariate, the paper uses:

$$
\mathrm{SMD}=\frac{|\mu_1-\mu_0|}{\sqrt{(s_1^2+s_0^2)/2}}.
$$

$$\mu_1,\mu_0$$ are its group means and $$s_1^2,s_0^2$$ sample variances. The absolute value measures magnitude only; the denominator takes the square root of the average variance to supply a scale. Units cancel, so SMD is unitless and is not a p-value.

Example: mean ages 72 and 68 years with standard deviations 10 in both groups give SMD=4/10=0.4. Weighted means 70.5 and 70.0 with standard deviations near 10 give SMD≈0.05. The former fails the 0.1 threshold, the latter passes. For a binary diabetes indicator, its mean is the recorded proportion, explaining “prevalence” in the article. Age and time intervals have continuous-variable means and should not all be called prevalence.

After weighting, replace means and variances in that expression with the following, computed within each group:

$$
\mu_w=\frac{\sum_i w_i x_i}{\sum_i w_i},\qquad
s_w^2=\frac{\sum_i w_i}{(\sum_i w_i)^2-\sum_i w_i^2}\sum_i w_i(x_i-\mu_w)^2.
$$

$$x_i$$ is person i's feature and $$w_i$$ their IPTW; summation is within that group only. The first is a weighted mean; the second sums weighted squared deviations and multiplies by a finite-sample correction. When every weight is 1, variance returns to the sum of squared deviations divided by “number of people minus 1.” The original Eq. (3) prints $$s_{weight}$$ on the left, but its right side and text describe variance; $$s_w^2$$ here avoids squaring variance again. This explains the authors' reported diagnostic, not a claim that every SMD implementation uses the same denominator.

The two thresholds are:

1. Individual variable: SMD≤0.1 counts as balanced.
2. Entire emulation: the count with SMD>0.1 divided by all variables must be ≤2% to count the emulation as balanced.

For D=267, 2%×267=5.34. Since counts are integers, **at most 5 unbalanced variables pass; 6 do not**. 5/267≈1.87%, and 6/267≈2.25%.

Equation (4)'s indicator adds 1 for each variable exceeding 0.1 and 0 otherwise; summing yields the imbalance count. Before/after means before/after weighting, not before/after treatment: both assess baseline characteristics.

This operational diagnostic permits a few measured variables to remain unbalanced. It does not weight by confounding importance or prove identical joint distributions or absence of unmeasured confounding. A severely imbalanced important confounder warrants caution even if the total count passes.

### 4.11 Box 1 step by step: Pay attention to the scope of “whole”
{: #section-24 }

Input $$X\in\mathbb R^{n\times d}$$ is the matrix of n training patients and d covariate columns; $$T\in\{0,1\}^n$$ is their treatment-label vector. Here n is the outer training count; $$\cup$$ combines folds into the full training set, and K=10. **Box 1 uses T for treatment, whereas Methods survival notation uses Z for treatment and T for event time.** This reuses a symbol; Box 1's T is not survival time.

Continue the example of 1,000 overall, 800 training, and 200 test participants:

| Box 1 step | Operation |
| --- | --- |
| 1 | Initialize the current best configuration with an imbalance count of positive infinity and AUC of 0, allowing the first eligible candidate to replace it; no infinitely many variables were actually counted |
| 2–3 | Take one hyperparameter configuration and divide 800 people into 10 folds |
| 4–5 | Hold out approximately 80 people; fit parameters on the other 720, with hyperparameters fixed for this round |
| 6 | Use that fitted model to predict all 800, then calculate stabilized IPTW, SMDs, and the imbalance count |
| 7 | Calculate AUC only in the held-out 80 |
| 8 | Rotate the validation fold, completing 10 fits and evaluations |
| 9 | Average the 10 imbalance counts and separately the 10 validation AUCs |
| 10 | Compare mean imbalance counts first; break ties with mean AUC, without first testing significance |
| 11 | Repeat for every candidate configuration |
| 12 | Fix selected hyperparameters and retrain one final model on all 800 |
| 13 | Use the retrained model to recalculate weights, SMDs, and imbalance count for the 800 |
| 14 | Return the final model, retrained training-set imbalance count, and selected configuration's CV validation AUC |

**Step 6's whole (X,T) is 720+80=800, not 1,000.** Each inner model assesses balance in its combined seen fitting folds and unseen validation fold, but AUC only in the validation fold.

A candidate's mean imbalance count over 10 folds may be 4.3: an average of counts, not 0.3 of a variable. It also differs from the final retrained model's integer count. Step 14's AUC is the selected configuration's CV AUC, not the final model's outer-test AUC.

This neither ensembles the 10 models nor performs standard cross-fitting that retains only each person's out-of-fold prediction. Every fold model predicts all 800; what is averaged is imbalance counts and validation AUCs. One model is retrained afterward. Box 1 does not use outer-test data for hyperparameter selection, while balance over the inner whole deliberately includes seen records and is not purely held-out balance evaluation.

### 4.12 Box 2: Evaluate one fixed final model on three datasets
{: #section-25 }

| Data | Illustrative size | Operation | Interpretation |
| --- | ---: | --- | --- |
| Train | 800 | Predict PS; compute weights, SMDs, and imbalance count | Performance among people used for fitting |
| Test | 200 | Apply the same model and independently compute balance diagnostics | Performance among held-out people |
| Combined | 1,000 | Recombine both sets and recalculate weights and overall SMD/count | Performance in the full analytical cohort |

Box 2 does not require retraining on the test set or changing the final model to one retrained on all 1,000. It applies the same selected model; combined diagnostics include training records and are not independent external validation.

**Distinguish the two “combined” sets:** in Box 1, inner fitting plus validation equals the outer training set; in Box 2, outer training plus test equals the full emulation.

Combined SMD must be recalculated from pooled weighted means and variances, not 0.8×training SMD+0.2×test SMD. Imbalance counts also cannot simply be added: a variable's direction and magnitude of imbalance can differ across subsets. Box 2 returns three imbalance counts, not treatment effects, AD prediction accuracies, or three new models.

### 4.13 How do Figs. 1b and 1c reconnect to the overall study?
{: #section-26 }

In Fig. 1b's upper-left panel, X is baseline features, Z treatment, and Y outcome. A DAG (directed acyclic graph) expresses causal relationships: confounders can affect treatment and outcome; mediators lie on treatment-to-outcome paths; colliders have two causes and conditioning on them can open a blocked path. The article also performs sensitivity analyses using knowledge and causal-discovery algorithms for variable selection. Algorithmically inferred graphs are not automatically the true causal graph, and all correlated variables cannot be treated as confounders.

Green Train and red Test show the outer split; rotating Fold 1…10 below denotes CV within Train only. Model icons indicate candidate families. Balance-diagnostic points show feature SMDs before and after weighting; the balance scale symbolizes baseline comparability, not proven drug efficacy.

Fig. 1c takes diagnostically assessed emulated trials into IPTW-weighted survival analysis, producing adjusted HRs, survival differences, and other outputs, then applies multiple-comparison correction, cross-database validation, literature checks, and sensitivity analyses to identify candidates for further research. The survival curves illustrate the workflow, not a confirmed drug effect.

For example, if 60 of a drug's 100 emulations meet the balance criterion, its balance-success proportion is 60/100=60%, matching the idea of Eq. 5. This means neither 60% of patients benefit nor a 60% probability of efficacy. Comparisons of models and selection strategies primarily concern such balance performance. The later formal screening description in Methods selects PS configurations from the LR model space using the authors' strategy; it does not mean all four families independently establish the same drug effect.

### 4.14 Reading boundaries and self-check
{: #section-27 }

- **Four kinds of repetition:** 100 control constructions per drug; one 80:20 split per emulation; 10-fold CV per candidate; and a search over multiple hyperparameter configurations. They occur at different levels and are not interchangeable.
- **Three kinds of “good”:** accurate treatment prediction, balanced weighted baseline characteristics, and reliable causal identification. The first two provide diagnostics but cannot independently establish the third.
- **Design still requires separate review:** Methods uses the first prescription as baseline while requiring at least two later prescriptions spanning at least 30 days to confirm effective initiation. This uses future information to confirm enrollment/exposure and may create selection or immortal-time-related problems requiring implementation review. Good balance in Boxes 1–2 does not automatically eliminate them; this observation alone does not determine bias direction or size.
- **Implementation boundary:** Methods mentions trimming the lowest/highest 1% of extreme weights, but that wording alone does not establish whether records are removed or values truncated; reproduction requires checking code. This section explains the reported algorithm, not a completed code audit.

Self-check: in one 1,000-person emulation, who fits a particular inner model, where is balance evaluated, and where is AUC evaluated? Approximately 720, 800, and 80 people, respectively; the outer 200 are not yet used for fitting or selection. After selection and retraining, Box 2 separately diagnoses the 800, 200, and 1,000.


## 5. Discussion: Does classical IPTW require train/test splitting? How does LR obtain each propensity score?
{: #section-28 }

**Classical baseline IPTW generally does not require a train/test split. A common approach fits one propensity-score model using all analytical patients' pretreatment features and actual treatment labels, then computes scores and weights for those same people.** The paper's 80:20 split, CV, and model-selection strategies add methodological comparisons and evaluation; they are neither the definition nor a required step of IPTW.

### 5.1 “Participating in fitting” differs from “fitting using only oneself”
{: #section-29 }

With 1,000 people, the model receives 1,000 rows of baseline features L and treatment labels A. LR estimates one shared coefficient set, not a separate model per person. Each person can contribute to estimating those coefficients and then use them to obtain their own predicted probability.

For patient i, actual label A_i is the fitting target and helps estimate shared coefficients. To predict their propensity score, insert L_i into the fitted function. A_i is neither an input feature to that function nor a command to set probability to 0 or 1. Only later, when constructing weights, does actual A_i determine whether to use the treatment or nontreatment probability.

PS fitting does not use follow-up outcome Y to predict treatment or choose weights by which model produces significant drug effects.

### 5.2 Fitting an actual LR to the existing 1,000-person example
{: #section-30 }

Code low risk as L=0 and high risk as L=1. Among 500 low-risk people, 100 are treated; among 500 high-risk people, 400 are treated.

Specify:

$$
p_i=\frac{1}{1+\exp[-(\beta_0+\beta_1 L_i)]}.
$$

p_i is the model's current treatment probability for patient i; L_i is pretreatment disease coding; β_0 is the intercept and β_1 the disease coefficient, both estimated from the entire cohort. exp is the exponential function; the negative sign applies to the whole parenthesized expression. The outer mapping converts any real number to a 0–1 probability.

Fitting searches for coefficients that make observed treatment labels more likely under the model, equivalently minimizing binary cross-entropy. Software tries coefficients, calculates individual probabilities and overall error, and updates until convergence conditions hold; regularized versions add coefficient penalties.

Both disease strata here contain treated people and controls, and the model has only an intercept and one binary disease variable. Unregularized maximum likelihood exactly reproduces the two observed treatment proportions:

$$
\widehat\beta_0=-\log4\approx-1.3863,\qquad
\widehat\beta_1=2\log4\approx2.7726.
$$

Hats indicate estimated coefficients, and log is the natural logarithm. These coefficients give:

- Low risk L=0: linear combination −log4, predicted probability 1/(1+4)=0.2.
- High risk L=1: linear combination log4, predicted probability 1/(1+1/4)=0.8.

The coefficients are not arbitrarily stipulated; they are the LR maximum-likelihood solution for this simple stratified dataset. With multiple continuous features, additional model restrictions, or regularization, exact reproduction of every subgroup's observed proportion is not guaranteed.

### 5.3 Treated people and controls within the same disease stratum have the same e(L)
{: #section-31 }

| Patient | Disease L | Actual A | Predicted treatment probability | Unstabilized weight |
| --- | ---: | ---: | ---: | ---: |
| A | 0 | 1 | 0.2 | 1/0.2=5 |
| B | 0 | 0 | 0.2 | 1/(1−0.2)=1.25 |
| C | 1 | 1 | 0.8 | 1/0.8=1.25 |
| D | 1 | 0 | 0.8 | 1/(1−0.8)=5 |

The probability answers “how likely are people with these features to receive treatment?”, not a restatement of an action already taken. Knowing Patient A was treated is consistent with estimating e(L)=0.2; the unknown is the conditional probability, not A's treatment fact.

With more features, the linear combination adds age, history, and other terms. Different L values produce different probabilities. People with identical values for every model input receive the same prediction from the same model.

### 5.4 Is fitting and weighting the same people data leakage?
{: #section-32 }

In conventional low-dimensional parametric propensity-score analysis, this is a common, theoretically supported same-sample estimation arrangement; reuse does not automatically make it wrong. The aim is the cohort's target causal effect, not a claim of independently validated predictive performance in new patients. [Austin and Stuart (2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4626409/)

“Permitted estimation” does not mean “no overfitting.” Small samples, many variables, excessive flexibility, complete separation, or near-deterministic treatment choices can cause extreme probabilities and unstable weights. Parametric models also require checks of form, overlap, balance, weight distributions, and appropriate uncertainty estimation. Training performance is not independent test performance.

Similarly, one can estimate a mean from the full sample and use it to calculate those people's deviations; multiple estimation steps using one sample are not logically contradictory. IPTW still has its own statistical assumptions, however; that analogy cannot establish validity of every workflow.

### 5.5 Differences from this paper and cross-fitting
{: #section-33 }

| Approach | Fitting and prediction arrangement | Meaning |
| --- | --- | --- |
| Common baseline LR-IPTW | Fit one model on everyone, then predict and weight everyone | No train/test split required |
| This paper's main workflow | Select hyperparameters and retrain within the outer 80%; apply the same model to training, test, and combined data | Compare selection strategies and balance in seen and unseen data |
| Cross-fitting | Train on other folds and predict only the current held-out fold; rotate so everyone receives a prediction fitted without themselves | Reduce each record's direct fitting influence on its own probability estimate; can accompany some flexible-model estimators |

CV tuning followed by retraining on all data still produces same-sample fitted values; it is not cross-fitting. Cross-fitting is also not mandatory for every IPTW analysis and cannot independently repair unmeasured confounding or positivity. Its inference guarantees depend on the estimator, model convergence, and other conditions.

Start with the first row: **everyone's (L,A) → fit shared coefficients → insert each L to obtain ê(L) → use actual A to compute weights → assess balance and analyze Y.**


### 5.6 Connecting to a research example: Multiple baseline variables, comparing drug A with B
{: #section-34 }

The full calculation is consolidated in [Complete multivariable LR-IPTW example comparing drug A with drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15), where group 0 is no longer untreated. It uses 3,000 simulated patients: 1,119 initiate A and 1,881 B. LR jointly includes age, diabetes, severity, and prior background treatment C.

The fitted model is η=−0.686970+0.480725×age10+0.781641×D+0.617510×S−0.498737×H, with ê(L)=1/[1+exp(−η)]. age10=(age−70)/10; D is diabetes 0/1, S a continuous severity score, and H prior use of background treatment C, coded 0/1. η is log-odds; coefficients describe A/B treatment choice, not efficacy.

For example, patient 2 (age 80.299, D=1, S=0.402844, H=0) has ê≈0.698157, actually initiates A, and receives unstabilized weight≈1.432343. Patient 4 (age 68.214, D=1, S=1.066546, H=1) has ê≈0.542066, actually initiates B, and receives weight=1/(1−ê)≈2.183719.

Everyone jointly fits the same LR, then everyone receives predictions, without train/test splitting; individuals do not have separate coefficients. After weighting, all four SMDs are below 0.1. Crude one-year hospitalization risks are A=14.03% and B=12.33%; IPTW risks are A=10.88% and B=15.03%. These are simulated teaching results with no clinical-significance or actual-efficacy meaning. The main example also supplies stabilized weights, connections to ATT and longitudinal/censoring weights, and runnable scripts.

When returning to Boxes 1–2, expand the four baseline columns to the paper's feature set and replace “fit directly on everyone” with the authors' selection and evaluation arrangement. Treatment prediction, weighting, and outcome analysis remain separate steps.

### 5.7 Does TTE require equal group sizes?
{: #section-35 }

No. Equal raw counts do not imply baseline balance, and unequal counts do not prevent appropriate IPTW. The multivariable A/B example has 1,119 versus 1,881 patients, without deleting people to force 1:1. Each group's risk divides its weighted event count by its own weight sum; sums need not match. Equal weighted counts in the single-variable example are a result of that teaching dataset, not a framework requirement.

See [Must the Two Groups Have the Same Number of People?]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-21). Assess the common target population, confounding adjustment, overlap, and precision, rather than equality of total counts.

### 5.8 How do the g-formula and IPTW differ?
{: #section-36 }

Both can estimate the same A-versus-B initiation effect. G-computation fits an outcome model, predicts hospitalization risk after setting everyone to A and then B, and averages. IPTW fits a treatment-choice model and computes outcomes after weighting actual A/B records. See [4.1. Multivariable Drug A versus B: The G-Formula and IPTW Answer the Same Question]({{ "/causal-inference/g-formula/" | relative_url }}#section-9) for models, results on the same data, and applicable conditions. Neither automatically removes unmeasured confounding or repairs incorrect time zero. Their difference is how observed records estimate mean outcomes under interventions, not “one causal and one predictive.”

### 5.9 Why does ATT weight treated people by 1 and controls by odds?
{: #section-37 }

ATT restricts the target population to actual recipients of the target treatment. The treated group already has the target composition, so its weight is 1; controls receive ê/(1−ê) to estimate outcomes if that same population received the control strategy. For row-by-row counts, events, and the 17%/34% calculation in the 500-person example, plus the multivariable A/B connection, see [ATT: Define Whose Question You Are Answering Before Computing Control Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-7). This changes the target population; it neither sets treatment probabilities to 1 nor analyzes treated people without using control data.

### 5.10 Stabilized IPTW and SW_i: Define first, then read the formula
{: #section-38 }

SW_i is person i's stabilized weight; SW is the abbreviation and i the patient index. In the baseline A/B example, obtain ê(L) from multivariable LR, then use 0.373/ê(L) for A and 0.627/[1−ê(L)] for B. The numerator is the drug's proportion in the full analytical cohort, and the denominator the probability conditional on that patient's history. A weight is not a probability and can exceed 1.

Ordinary weights replace those numerators with 1; stabilization multiplies everyone within a drug group by the same constant. It changes overall scale without altering relative within-group contributions, so normalized group risks, their difference, and within-group effective sample sizes remain unchanged here. The name does not guarantee improved precision or eliminate near-zero denominators. Stabilization is neither weight truncation nor a change from ATE to ATT.

For each component and calculation, see [Step Five: Use A's Probability for Drug A and B's for Drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-20). Symbol definitions now appear before that section's patient table. A separate 100-person table begins with raw A/B counts of 40/60: ordinary weighting makes each group represent 100 people, whereas stabilized weight sums are 40/60. Within both groups, low- and high-risk people remain equally represented. The theoretical explanation of ‘in expectation’ is in an optional details section.

### 5.11 How does baseline IPTW extend to sustained A/B strategies?
{: #section-44 }

See [Longitudinal IPTW: Sustained Drug A versus Drug B and Why Weights Multiply Across Periods]({{ "/causal-inference/longitudinal-iptw/" | relative_url }}) for a separate beginner's explanation. It motivates multiplication through successive selections of people, allows treatment to change subsequent health, and uses two multivariable LR models to calculate actual-action probabilities for AA/BB/AB/BA. The paper's baseline model-selection workflow does not automatically constitute an analysis of sustained longitudinal strategies. Each decision requires the appropriate history, temporal ordering, and correspondence to the strategy.

### 5.12 How is survival analysis weighted in TTE?
{: #section-45 }

The companion [Weighted Survival Analysis in TTE: From Risk Sets to Survival Curves and Cox Models]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}) first explains events, censoring, and risk sets. An eight-person A/B table then weights events and at-risk records at each time and multiplies the KM survival contributions. It connects these calculations to weighted Cox models, multivariable LR, time-varying weights, and inference. This fills in the survival-analysis component of Fig. 1c without conflating PS fitting with outcome-risk prediction.

### 5.13 Why does high-throughput TTE need a Bonferroni correction?
{: #section-46 }

**High-throughput drug screening looks for effects across many drugs. Even if every analysis uses an appropriate method, random variation can produce apparently effective candidates. Bonferroni moves from controlling false positives in each individual test to controlling them across a whole family of tests. It informs significance judgments after effect estimation; it does not calculate propensity scores or patient weights.**

#### Step one: What are we testing when we compare only drug A with drug B?
{: #section-47 }

Suppose the question is whether eligible people who initiate A, versus B, have different one-year mortality risks. We use risk at a fixed time here, without needing a Cox model yet.

The true risk difference in the population is what we want to know; its estimate varies across finite samples. Even if the true mortality risks under A and B are equal, one sample may have fewer deaths in group A. Under its assumptions, IPTW can adjust for confounding, but it cannot remove finite-sample random variation.

Call the statement “A and B have equal one-year mortality risks in the target population” the **null hypothesis**, written $$H_0$$. A hypothesis test asks how unusual the observed result would be if $$H_0$$ and the statistical model and sampling assumptions held.

A **p value** is the probability, under the null and relevant assumptions, of a test statistic at least as extreme as the observed one. A two-sided test counts extreme results in both directions, A being better and A being worse. A one-sided test addresses a direction specified beforehand; its direction cannot be selected after seeing the result.

Thus, p = 0.03 **does not mean “a 3% probability that A is ineffective,”** or “a 97% probability that A is effective.”

The **significance level $$\alpha$$** is a prespecified bound on the tolerated false-positive rate, often 0.05. For a well-calibrated test under a true null, repeatedly sampling from the same population and performing the same test would wrongly reject the null in no more than 5% of repetitions. This is a **type I error**, or false positive. The 5% describes the procedure's long-run error rate, not the probability that a particular positive conclusion already obtained is false.

#### Step two: Why do more screened drugs make it easier to find something “significant” by chance?
{: #section-48 }

Consider a teaching scenario with 20 prespecified comparisons: A₁ versus B, A₂ versus B, …, A₂₀ versus B. Suppose all true effects are zero and every test separately uses a 0.05 threshold.

For easy calculation, initially assume independent tests and an actual false-positive probability of exactly 0.05 for each test:

- One test avoids a false positive with probability 0.95.
- Two tests both avoid one with probability 0.95 × 0.95.
- All 20 avoid one with probability $$0.95^{20}$$, approximately 35.85%.
- At least one false positive occurs with probability $$1-0.95^{20}$$, approximately **64.15%**.

Actual screening comparisons share patients or comparator drugs, so their tests are usually correlated. Independence here only illustrates the accumulation of opportunities; the numerical result is not the paper's actual false-positive rate.

| Number of simultaneous tests | Probability of at least one false positive when each uses 0.05: teaching scenario with all nulls true, independence, and exactly 5% error per test |
| --- | --- |
| 1 | 5.00% |
| 10 | 40.13% |
| 20 | 64.15% |
| 66 | 96.61% |
| 312 | Approximately 99.99999% |

A different question is the average number of false positives. If all nulls are true and each test has exactly a 0.05 error rate, 312 tests produce an expected 312 × 0.05 = 15.6 false positives. This expectation does not require independence. It does not guarantee 15 or 16 every time, nor say that 5% of the positive results are false.

#### Step three: What does Bonferroni control?
{: #section-49 }

First define a **family**: the set of hypotheses whose results will be interpreted together and whose false-positive risk we want to control together. The 20 prespecified candidate-drug comparisons are one example.

The **family-wise error rate (FWER)** is the probability of wrongly rejecting at least one true null hypothesis in this family. Even if some drugs really are effective, FWER still concerns erroneous rejection of any remaining true nulls.

A target of FWER ≤ 0.05 means that repeating the entire research procedure would yield at least one false positive with probability no greater than 5%. It does not give each selected drug a 95% probability of effectiveness, nor imply that at most 5% of selected drugs are ineffective.

#### Step four: Allocate the family's 0.05 across its tests
{: #section-50 }

Define:

- $$m$$: the total number of hypothesis tests in the family requiring correction.
- $$\alpha$$: the desired upper bound on the family's error rate, such as 0.05.
- $$\alpha/m$$: the significance threshold allocated to each test.

The Bonferroni rule is:

$$
\text{Per-test threshold}=\frac{\alpha}{m}.
$$

For $$m=20$$, this is 0.05 / 20 = 0.0025. A p value of 0.03 formerly passed the 0.05 threshold; it now has to fall below 0.0025. Death records, IPTW weights, and the estimated risk difference do not change. Only the threshold for sufficiently strong statistical evidence changes.

**Why does dividing by m work?**

The probability of at least one error cannot exceed the sum of the individual error probabilities. If each of 20 tests has an error probability no greater than 0.0025, the family's probability of at least one error is no greater than 20 × 0.0025 = 0.05. Some errors can occur together; summing their probabilities double-counts these overlaps, giving an upper bound.

This probability relationship is the union bound. **It does not require independent tests.** It requires valid p values under each true null and proper inclusion of the family to be controlled. Nor must all drugs be ineffective: the number of true nulls is at most m, so their summed error probabilities still cannot exceed 0.05.

#### Step five: Alternatively, report adjusted p values without changing the threshold
{: #section-51 }

Let $$p_j$$ be the raw p value for test j. Its Bonferroni-adjusted value is:

$$
p_{j,\mathrm{adj}}=\min(1,m\,p_j).
$$

Here j is simply a test index. The function min chooses the smaller of two numbers, so the reported adjusted p value never exceeds 1. For example, 20 × 0.08 = 1.6 is reported as 1.

These approaches make the same decision:

1. Compare the raw p value with 0.05 / m.
2. Compare the adjusted p value with 0.05.

**Choose one. Do not multiply p by m and then compare it with 0.05 / m: that corrects twice.**

These are teaching results for three of a study's 20 prespecified comparisons:

| Comparison | Estimated one-year mortality risk difference: candidate minus B | Raw p value | Adjusted p value: 20 × p | Significant after correction? |
| --- | --- | --- | --- | --- |
| A₁ versus B | −3 percentage points | 0.030 | 0.600 | No |
| A₂ versus B | −4 percentage points | 0.002 | 0.040 | Yes |
| A₃ versus B | −5 percentage points | 0.0001 | 0.002 | Yes |

The risk differences remain −3, −4, and −5 percentage points. A₁ fails the corrected threshold: “insufficient evidence under this multiple-testing standard” is appropriate. This does not prove that A₁ and B are identical.

#### Step six: Where does the paper's 0.00016 come from?
{: #section-52 }

In “Screening and prioritization,” the paper explicitly gives **0.05 / 312 ≈ 1.6 × 10⁻⁴**. The 312 is the sum of 66 drug-level evaluations in OneFlorida and 246 in MarketScan. A drug may be evaluated in both databases, so 312 is not a count of distinct drugs after deduplication. The paper first summarizes successfully balanced emulations for each drug and reports drug-level bootstrap p values. It does not simply use the total number of emulated trials as this denominator. [Methods and screening criteria](https://www.nature.com/articles/s41467-023-43929-1#Sec10)

For a drug-level raw p = 0.001, the result is below 0.05 but above 0.05 / 312 and therefore fails the threshold. Equivalently, the adjusted p is 312 × 0.001 = 0.312. A raw p = 0.0001 gives an adjusted p = 0.0312 and passes. Use the full precision of 0.05 / 312 in calculations, rounding only for display.

**m counts tests requiring joint error control. It is not the number of patients, covariates, CV folds, or necessarily computer model runs.**

If a study defines one prespecified summary test per drug, consider that drug-level family. If instead it tests 100 comparator constructions and promotes only the smallest p, it adds selection opportunities; “only one drug, therefore one test” is inadequate. Likewise, choosing the most significant outcome, time point, subgroup, or model after seeing results is not fixed by correcting only the few final results displayed.

#### Step seven: Where does Bonferroni enter TTE?
{: #section-53 }

| Stage | Main work | Main question addressed |
| --- | --- | --- |
| Target-trial design | Define the population, A/B strategies, time zero, outcome, and follow-up | Whose causal question are we answering, and what is it? |
| Cohort construction and confounding adjustment | Baseline multivariable LR → PS → IPTW → balance and weight diagnostics | Appropriately handle measured confounding of treatment choice |
| Outcome analysis and inference | Weighted survival analysis or risk estimation; effects, standard errors, and p values | How large and how uncertain is the estimated effect? |
| Multiple-testing decisions | Define the family and apply Bonferroni or another method | How often might the whole screening process produce a chance positive? |
| Further evaluation | Effect magnitude, clinical relevance, external replication, and sensitivity analyses | Does the candidate warrant further research? |

Plan the family and correction rule before inspecting results. The numerical comparison with the threshold follows calculation of p values. Bonferroni does not alter patient weights, train ML-PS models, or divide the SMD threshold of 0.1 by the number of drugs.

#### Step eight: What can and cannot be concluded after passing the correction?
{: #section-54 }

Passing means meeting the prespecified multiple-testing standard for statistical evidence. It does not establish a causal drug effect by itself. Unmeasured confounding, incorrect time zero, informative censoring, or inappropriate standard errors can all produce excessively small p values. Bonferroni cannot repair these problems; its guarantee assumes that the input tests are valid.

An ordinary 95% confidence interval excluding the null also does not automatically pass Bonferroni. For corresponding two-sided tests and intervals from the same model, an equivalent interval-based correction raises each interval's confidence level to $$1-\alpha/m$$. For m = 20 this is 99.75%; for m = 312 it is approximately 99.98397%. Intervals become wider while point estimates remain unchanged. This correspondence cannot be mechanically applied to one-sided tests, different bootstrap definitions, or intervals from different models.

#### Step nine: Why not always use Bonferroni?
{: #section-55 }

It is simple, intuitive, and allows dependence among tests. With many tests, however, the threshold becomes very low and may miss true effects: power decreases. It can be especially conservative when tests are highly correlated or contain redundant information. High-throughput research must address multiplicity, but need not always choose Bonferroni.

Holm also controls FWER, using stepwise thresholds and generally offering more power than simple Bonferroni. Benjamini–Hochberg controls a different quantity, the **false discovery rate (FDR)**: the expected proportion of erroneous rejections among all rejections across repetitions, defining that proportion as zero when there are no rejections. Its guarantees also depend on the tests' dependence structure. FWER ≤ 5% and FDR ≤ 5% are not interchangeable. [Official R documentation on p-value adjustment](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html)

**Self-check:** Ten candidate drugs are prespecified, family-level α = 0.05, and one drug has raw p = 0.01. The per-test threshold is 0.005 and its adjusted p is 0.10, so it fails. Correction does not shrink its effect estimate or establish that the drug has no effect.

### 5.14 Reading the federated TTE paper: Why is treatment the dependent variable and baseline covariates the independent variables?
{: #section-56 }

**Source excerpt:**

> Specifically, treatment assignment served as the dependent variable, while baseline covariates acted as independent variables.

**Interpretation:** The model treats observed treatment group as the dependent variable and baseline covariates as its independent variables.

**In plain language, this LR is a propensity-score model. It inputs pretreatment characteristics, learns their relationship with actual treatment choice, and outputs the probability of receiving the target treatment. This step does not predict death or disease.**

#### First identify every column using drugs A and B
{: #section-57 }

For teaching, we rewrite the passage's exposed/nonexposed comparison as A versus B to connect with earlier sections. This does not imply that the paper's nonexposed group necessarily receives one particular drug B.

Let Z record actual initiation: Z = 1 for A, Z = 0 for B. Let L contain pretreatment age, diabetes, severity, and use of background treatment C.

| Patient | Age | Diabetes: yes 1, no 0 | Pretreatment severity | Background treatment C: used 1, not used 0 | Actual group Z |
| --- | --- | --- | --- | --- | --- |
| Patient 1 | 75 | 1 | 2 | 0 | 1: drug A |
| Patient 2 | 60 | 0 | 0 | 1 | 0: drug B |
| Patient 3 | 75 | 1 | 2 | 0 | 0: drug B |

**Independent variables** are explanatory or predictive input columns: the first four baseline characteristics here. The **dependent variable** is the label the model fits: the last column, observed treatment group Z.

The statistical name “dependent variable” does not necessarily refer to the study's final clinical outcome. One study can fit multiple models, each with its own label. Treatment is the PS model's label; the subsequent survival model uses event times and censoring information to analyze clinical outcomes.

Nor does “independent variables” imply mutual statistical independence. Age and diabetes can be correlated. The terminology itself does not establish causal relationships.

#### What does multivariable LR calculate?
{: #section-58 }

Write the conditional probability of A as e(L), where e is a probability function and L the patient's baseline characteristics. A hat marks an estimated probability, $$\widehat e(L)$$.

LR multiplies features by coefficients and adds them into a score η, then converts that score into a probability between zero and one:

$$
\eta=\beta_0+\beta_1\frac{\text{age}-70}{10}+\beta_2\text{diabetes}+\beta_3\text{severity}+\beta_4\text{background treatment C},
$$

$$
\widehat e(L)=\frac{1}{1+\exp(-\eta)}.
$$

β₀ is the intercept; the remaining β coefficients are learned from training data. Subtracting 70 from age and dividing by 10 expresses age in decades relative to 70. The function exp is exponential; software can perform the probability conversion.

For hand calculation, **suppose** the fitted coefficients are −0.5, 0.4, 0.8, 0.6, and −0.3. These are hypothetical teaching coefficients, not paper estimates or the coefficients actually fitted in the preceding 3,000-person simulation.

Patient 1's score is:

$$
\eta_1=-0.5+0.4\times0.5+0.8\times1+0.6\times2-0.3\times0=1.7.
$$

Thus $$\widehat e(L_1)\approx0.846$$: the model estimates that patients with these features have approximately an 84.6% probability of A and a 15.4% probability of B. **This is neither Patient 1's one-year death probability nor the probability that A works.**

#### Why predict group membership when the actual group is known?
{: #section-59 }

Actual group membership and its probability are different information.

Patient 1 actually used A, a fact coded 1. Their score can still be 0.846 rather than 1. Patient 3 actually used B, coded 0. If their inputs exactly match Patient 1's, the same model also gives Patient 3 an A probability of 0.846, not zero.

During training, software uses everyone's L and actual Z to estimate shared coefficients under which the observed choices are plausible. During prediction, it substitutes each L into the fitted formula. It learns treatment-choice patterns from many people rather than copying each person's observed 0/1 label.

#### How is that probability subsequently used in IPTW?
{: #section-60 }

For ordinary baseline ATE IPTW, A recipients receive $$1/\widehat e(L)$$ and B recipients $$1/[1-\widehat e(L)]$$. Patient 1 therefore has weight approximately 1/0.846 = 1.18; Patient 3 has approximately 1/0.154 = 6.47. Calculations use unrounded probabilities.

These characteristics more often correspond to A, so actual B recipients with these features are relatively uncommon. Giving those B records greater weight helps the weighted B group represent this type of patient. This adjusts baseline-composition differences due to treatment selection; it does not directly weight people according to their likelihood of dying.

Stabilized IPTW additionally multiplies the numerator by the corresponding marginal group proportion. Targets such as ATT require other weights. The formula here illustrates ordinary ATE weighting and does not establish which numerator the paper uses.

#### What changes when training is “federated”?
{: #section-61 }

In the source passage, the authors use federated learning to train global LR. Institutions jointly train a model whose relationship remains “baseline characteristics → probability of treatment group.” Federation describes cross-institution training arrangements, without changing this LR's dependent variable to death or disease. The methods specify what is exchanged and how iteration proceeds.

The whole sequence is **baseline characteristics → federated LR propensity scores → individual IPTW → federated Cox survival analysis → adjusted HR and confidence interval**. PS LR and Cox have different jobs within the same study.

### 5.15 How are IPTW and propensity-score matching related, and how do they differ?
{: #section-62 }

See [IPTW versus PSM]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-48) for a detailed comparison starting from the same multivariable LR. It explains matching versus weighting, ATE/ATT, common support, balance diagnostics, and subsequent outcome analysis.

### 5.16 Unpacking federated LR: From one patient's probability to training across hospitals
{: #section-63 }

#### Source excerpts
{: #section-64 }

![Local and global objectives for federated LR](/assets/causal-inference/tte-extension/li-2025-federated-lr-objective.png)

![Hospital weights, regularization, and federated algorithms](/assets/causal-inference/tte-extension/li-2025-federated-lr-regularizers.png)

The excerpts above are from Li et al. (2025). All patients, coefficients, and numbers below are teaching examples. Equations (3)–(4) have been checked against the journal webpage. This discussion explains the formulas and identifies notation issues; it does not establish what the authors' code actually implements.

#### 1. Locate the task: These formulas are still training a propensity-score model
{: #section-65 }

Several hospitals jointly fit LR using pretreatment features to predict actual use of A versus B. Only after obtaining the final model do they calculate individual propensity scores, then IPTW, and then analyze outcomes. These formulas have not yet estimated a drug's effect on mortality.

The paper uses different notation from earlier sections: **T is the observed treatment label, and z the baseline feature vector.** Do not mistake z for the earlier treatment indicator Z. T here is not survival time either.

#### 2. Symbol dictionary
{: #section-66 }

| Symbol | Meaning | Example |
| --- | --- | --- |
| K | Total participating hospitals | Two hospitals |
| k | Hospital index | k = 1 is the first hospital |
| Nₖ | Number of patients in hospital k | N₁ = 2 |
| n | Patient index within that hospital | n = 1, 2 |
| $$T_n^{(k)}$$ | Actual treatment label for patient n in hospital k | 1 for A, 0 for B |
| $$z_n^{(k)}$$ | That patient's baseline features | Age, diabetes, severity, background treatment C |
| π | The full LR coefficient set, including intercept | Corresponds to the earlier LR β vector; not the circle constant |
| $$e(z_n^{(k)})$$ | This person's predicted probability of A under the current coefficients | 0.8 |
| $$L_{PS}^{(k)}(\pi)$$ | Likelihood contribution of hospital k's treatment labels for these LR coefficients | Changes with π |
| log | Natural logarithm | log(0.8) ≈ −0.2231 |
| pₖ | Hospital aggregation proportion Nₖ/N | N is the sum of patient counts across hospitals |

Superscript (k) labels a hospital; it is not exponentiation. PS abbreviates propensity score, rather than an operation. Changing π changes the predicted probabilities. The notation e(z) suppresses that dependence; $$e_\pi(z)$$ makes it explicit.

#### 3. How does multivariable LR produce a probability?
{: #section-67 }

For example, let z = (1, (age−70)/10, diabetes, severity, background treatment C), where the initial 1 supplies the intercept. Take current coefficients π = (−0.5, 0.4, 0.8, 0.6, −0.3). These are candidate coefficients for a teaching calculation, not coefficients trained from the few-person table here.

Multiply corresponding entries and add them to obtain $$\eta=\pi^Tz$$. The superscript T means transpose and is unrelated to the treatment label T.

For someone aged 75, with diabetes, severity 2, and no use of C, η = −0.5 + 0.4×0.5 + 0.8×1 + 0.6×2 − 0.3×0 = 1.7.

$$
e_\pi(z)=\frac{1}{1+\exp(-\eta)}\approx0.8455.
$$

This is the model's probability of A for that person. Training adjusts the shared coefficients π so that the actual treatment labels of all patients receive more plausible probabilities.

#### 4. Why does one patient's contribution contain two parts?
{: #section-68 }

Temporarily remove hospital and patient indices:

$$
T\log e+(1-T)\log(1-e).
$$

Because T is either zero or one, it acts like a switch:

- Actual A, T = 1: the expression becomes log(e); the second term is multiplied by zero.
- Actual B, T = 0: it becomes log(1−e); the first term is multiplied by zero.

It simply takes **the logarithm of the probability the model assigns to the treatment actually received**.

| Actual drug | Predicted probability e of A | Probability assigned to the actual drug | Patient's log-likelihood contribution |
| --- | --- | --- | --- |
| A | 0.8 | 0.8 | log(0.8) ≈ −0.2231 |
| A | 0.2 | 0.2 | log(0.2) ≈ −1.6094 |
| B | 0.8 | 0.2 | log(0.2) ≈ −1.6094 |
| B | 0.2 | 0.8 | log(0.8) ≈ −0.2231 |

Since −0.2231 exceeds −1.6094, a better-fitting model obtains a larger log likelihood. Actual B recipients should not contribute log(e), because e always means the probability of A.

#### 5. Why do likelihoods multiply and log likelihoods add?
{: #section-69 }

An individual's 0/1 treatment label is a Bernoulli variable. The probability of the observed label can be written $$e^T(1-e)^{1-T}$$: T = 1 leaves e; T = 0 leaves 1−e.

Under the usual conditionally independent Bernoulli model, given patient features, the joint probability of all observed labels multiplies their corresponding probabilities. Holding the data fixed and treating the coefficients as quantities to choose makes this expression a likelihood. It is not the probability that the coefficients are true.

For example, in one hospital Patient 1 actually receives A with model e = 0.8, and Patient 2 actually receives B with model e = 0.3:

$$
L=0.8\times(1-0.3)=0.56.
$$

Taking logarithms gives:

$$
\log L=\log0.8+\log0.7\approx-0.5798.
$$

Logs turn multiplication into addition, simplify calculation and differentiation, and avoid numerical problems from multiplying many small probabilities. Since log is increasing, maximizing L and maximizing log L give the same optimizing coefficients.

**The Σ in equation (3) counts n from 1 through Nₖ, adding every patient's contribution within that hospital.**

The paper calls this a partial log likelihood. The expression is actually the ordinary Bernoulli LR log-likelihood contribution from one hospital, rather than the risk-set-based Cox partial likelihood.

#### 6. What does software actually do during training?
{: #section-70 }

Keep patient features and observed T fixed, change π, and recompute probabilities and log likelihood. Optimization finds a more suitable shared coefficient set. It does not independently set each A patient's probability to 1 and each B patient's to 0.

Compare another candidate model for the same two patients. Suppose its coefficients give Patient 1 probability 0.6 and Patient 2 probability 0.4. Its log likelihood is log0.6 + log0.6 ≈ −1.0217, below the earlier −0.5798. Looking only at these two patients' likelihood, the earlier candidate is better.

Software often **minimizes negative log likelihood**, adding a minus sign to equation (3). In this example the loss improves from 1.0217 to 0.5798. This is the summed binary cross-entropy; dividing by the number of people gives average cross-entropy.

To understand update directions, one patient's log-likelihood gradient with respect to the coefficients is (T−e)z. A gradient is a collection of numbers indicating which small coefficient changes increase the score. For the intercept, the corresponding feature entry is 1: an A recipient with e = 0.8 contributes 0.2; a B recipient with e = 0.3 contributes −0.3. Contributions from all patients jointly determine coefficient updates. Gradient ascent maximizes log likelihood, whereas gradient descent minimizes its negative. One patient's contribution cannot determine the direction of the entire coefficient update.

#### 7. What do the two summation levels in the global formula do?
{: #section-71 }

Abbreviate hospital k's local log likelihood as $$\ell_k(\pi)$$. Equation (4) has the structure:

$$
\sum_{k=1}^{K}p_k\left[\ell_k(\pi)+L_{reg}(\pi)\right].
$$

The inner level aggregates patients within a hospital, and the outer level aggregates hospitals. The proportion pₖ = Nₖ/N weights each hospital; these proportions sum to 1.

If hospital 1 has two people and hospital 2 has six, total N = 8, p₁ = 0.25, and p₂ = 0.75. A hospital's aggregation weight is not an individual's IPTW: the former organizes model training; the latter adjusts treatment comparisons after model fitting.

**The paper's normalization convention needs checking.** Equation (3) already sums patient contributions. If equation (4) then multiplies that sum by Nₖ/N, each person's data contribution is additionally multiplied by their hospital's proportion. Here, each patient in hospital 2 receives coefficient 0.75, versus 0.25 in hospital 1—a threefold difference.

If individual losses have similar magnitude, a hospital's total contribution then scales like $$N_k^2/N$$. The two-person and six-person hospitals contribute in a 1:9 ratio, versus 1:3 under equal weighting of patients.

A common federated objective that gives patients equal weight is:

$$
F_k(\pi)=-\frac{1}{N_k}\sum_{n=1}^{N_k}\left[T_n^{(k)}\log e_\pi(z_n^{(k)})+(1-T_n^{(k)})\log(1-e_\pi(z_n^{(k)}))\right],
$$

$$
F(\pi)=\sum_k\frac{N_k}{N}F_k(\pi)=-\frac1N\sum_k\ell_k(\pi).
$$

Average within each hospital first, then aggregate by patient-count proportions: every patient's weight becomes 1/N. Alternatively, directly sum hospital log-likelihood sums without another factor Nₖ/N. Read literally, the printed formula is not this standard equal-patient objective. It may omit a convention that local losses are averaged, but code verification is needed. The distinction matters especially when hospital sample sizes differ. [Original FedAvg paper](https://proceedings.mlr.press/v54/mcmahan17a.html)

#### 8. Federated training does more than add likelihood scores
{: #section-72 }

An objective says how to score a model; a training algorithm says how to change its coefficients. A general teaching description of FedAvg is:

1. The server sends current shared coefficients to each hospital.
2. Each hospital starts from that common point and performs several local updates.
3. Each returns its updated parameters or updates.
4. The server aggregates them using sample proportions and sends out the next round's shared coefficients.

Suppose the two hospitals return 0.4 and 0.8 for one coefficient. The server's result is 0.25×0.4 + 0.75×0.8 = 0.7. Other coefficient positions are aggregated similarly. Averaging coefficients does not directly average patients' propensity scores; the logistic transformation is nonlinear.

One aggregation round is not an exact solution to the optimum from centralized training on all patients. Local step counts, learning rates, heterogeneity, and convergence affect the process. The local objective supplies a scalar score; updating requires gradients or parameter information. Calculating the global objective does not require sending patient records to the server.

#### 9. Why introduce regularization?
{: #section-73 }

Hospitals may differ in patient age, disease severity, prescribing habits, and other features, causing local updates to move in different directions. Regularization or proximal constraints limit particular parameter changes to help stabilize optimization. They do not make the true patient distributions identical or prove that unmeasured confounding has disappeared.

For FedProx, let $$\pi_t$$ be the fixed coefficients sent by the server in the current round, and u the local candidate coefficients optimized at hospital k. A standard local objective is:

$$
\min_u\left\{F_k(u)+\frac{\mu}{2}\|u-\pi_t\|^2\right\}.
$$

$$F_k$$ is the local mean negative log likelihood. The following nonnegative penalty discourages local coefficients from moving too far from this round's shared starting point. During local optimization, $$\pi_t$$ is fixed and u varies. The paper's abbreviated π and $$\pi^{(k)}$$ do not clearly display these roles and round dependence.

The expression $$\|u-\pi_t\|^2$$ sums the squared coefficient differences. For two displayed coefficients, global (0.4, 0.8) and local (0.6, 0.7) give squared distance (0.6−0.4)² + (0.7−0.8)² = 0.05. With μ = 2, the penalty is 2/2 × 0.05 = 0.05.

μ controls constraint strength: larger values discourage departing from the global starting point more strongly; μ = 0 removes the penalty. Dividing by 2 simplifies differentiation, giving derivative $$\mu(u-\pi_t)$$; it does not represent two hospitals. A proximal penalty shrinks toward the global starting point, unlike ordinary ridge's shrinkage directly toward zero. [Original FedProx paper](https://arxiv.org/abs/1812.06127)

#### 10. The printed plus sign cannot be interpreted without the optimization direction
{: #section-74 }

The screenshot adds a positive squared distance to log L. If maximized literally, that term rewards distance, contrary to the intended constraint. The consistent penalty conventions are:

- **Maximize log likelihood minus a nonnegative penalty.**
- **Minimize negative log likelihood plus a nonnegative penalty.**

Suppose two models both have log likelihood −10 and penalties 1 and 5. Incorrectly adding and maximizing gives −9 and −5, favoring the model farther away. Subtraction gives −11 and −15, correctly favoring the smaller distance.

Treat the screenshot as a formulation needing clarification of its sign convention. Do not implement “log L plus positive squared penalty” as a maximization objective literally. This observation does not establish the same error in the authors' code.

#### 11. How should the three algorithm descriptions be read?
{: #section-75 }

**FedAvg:** The paper sets $$L_{reg}=0$$. Intuitively, there is no such explicit penalty: hospitals update locally, and the server computes a weighted average. This does not mean stopping training or having no hyperparameters.

**The screenshot's squared difference between adjacent rounds:** $$\pi_t^{(k)}-\pi_{t-1}^{(k)}$$ subtracts a hospital's previous-round coefficients from its current-round coefficients. Its squared norm measures the size of the change. Used consistently as a penalty, it can discourage large jumps between rounds. Here t indexes training rounds, not patient follow-up time or treatment occasions in longitudinal IPTW.

**This is not the standard definition of FedAvgM.** FedAvgM's central feature is server momentum: the server retains some information from previous aggregated updates, combines it with the present update, and updates the shared model. It is not simply an adjacent-parameter squared penalty added to local loss. Read the paper's direct identification of the two cautiously. [Original FedAvgM paper](https://arxiv.org/abs/1909.06335)

**FedProx:** Local optimization penalizes departure from the current global starting point, as in the squared-distance example above. It encourages, rather than guarantees, equality of local and global coefficients.

#### 12. Connecting back to IPTW
{: #section-76 }

After multiple training rounds, obtain global coefficients $$\widehat\pi$$. Each hospital inserts local patients' baseline z to calculate $$e_{\widehat\pi}(z)$$. For a final e = 0.8, ordinary IPTW is 1.25 for an A recipient and 5 for a B recipient. Next assess balance and weights, then undertake appropriate outcome analysis.

| Easily confused quantity | What it controls or represents |
| --- | --- |
| π | LR coefficients mapping features to probabilities |
| pₖ = Nₖ/N | Hospital aggregation proportion |
| e(z) | One patient's probability of A |
| Individual IPTW | A patient's contribution to treatment-effect analysis |
| μ | Strength of the proximal penalty |
| t | Federated training round |

Source check: [Li et al. (2025), methods equations (3)–(4) and Box 1](https://www.nature.com/articles/s41746-025-01803-y). The normalization and sign issues above are mathematical checks of the printed formulas. Their implementation requires a separate code review.

### 5.17 Unpacking the federated weighted Cox formulas: Equations (5)–(9)
{: #section-77 }

**Continuous beginner route:** [Ordinary Cox → weighted Cox in TTE → federated Cox]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}#section-12). Use one example to understand ordinary Cox, add IPTW, and then move to local risk sets and parameter aggregation across hospitals.

#### Original figures
{: #section-101 }

![Cox hazard function and unweighted partial likelihood](/assets/causal-inference/tte-extension/li-2025-cox-5-6.png)

![Weighted Cox and the federated objective](/assets/causal-inference/tte-extension/li-2025-cox-7-9.png)

![Site weights and regularization](/assets/causal-inference/tte-extension/li-2025-cox-aggregation.png)

We unpack these expressions using a teaching example of time from initiation of drug A or B to all-cause death. First read [Survival analysis from zero]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}#section-1). These numbers are not the paper’s results. The formula structure was checked against the journal webpage; the implementation code has not been audited.

#### 1. The prediction target changes: from treatment choice to the rate of events
{: #section-78 }

The preceding LR model maps baseline characteristics to the probability of receiving drug A, from which IPTW is calculated. Cox instead maps treatment and selected covariates to the instantaneous death rate at time t among people who have not yet died. LR coefficients π and Cox coefficients β are different parameter sets, with different training labels and objectives.

Here t denotes patient follow-up time. In the preceding federated parameter subscripts, t denoted a training round. These meanings must be kept separate.

#### 2. Equation (5): h(t|z) = h₀(t) exp(βᵀz)
{: #section-79 }

The hazard h(t|z) is the instantaneous event rate at time t, conditional on remaining event-free until then. For example, if h = 0.02 per month, over a very short interval of 0.1 month with an approximately constant rate, event probability is approximately 0.02 × 0.1 = 0.002. This is not the probability of dying by t, nor does it mean a fixed 2% dies every month. A rate need not be below 1.

The baseline hazard h₀(t) is the model’s rate when all input variables equal zero, and may change over time. “Baseline” here does not mean the instant treatment begins, or a constant rate. Covariates can be centered, so an all-zero input is a model reference rather than necessarily a real “zero-year-old patient.”

The expression βᵀz multiplies each coefficient by its corresponding input and sums the products; superscript T denotes transposition. The positive quantity exp(βᵀz) is a multiplier of the baseline hazard, **not the LR probability e(z)**. Here exp is the exponential function, while e(z) names the propensity-score function.

The paper uses z for Cox inputs in general. This notation alone does not establish that they are exactly the same inputs used in baseline LR. To estimate an A/B treatment HR, the Cox design matrix must include a treatment indicator or an equivalent treatment parameterization.

For the simplest comparison after IPTW, we use a working model containing only treatment indicator A: A=1 for drug A and A=0 for drug B. Write $$h(t\mid A)=h_0(t)\exp(\beta_A A)$$. Thus $$h_B(t)=h_0(t)$$ and $$h_A(t)=h_0(t)\exp(\beta_A)$$, giving $$HR=\exp(\beta_A)$$. If $$\beta_A=\log(0.5)$$, HR=0.5: the model’s hazard among surviving A recipients is half the corresponding hazard among surviving B recipients. Cumulative mortality probability need not be halved.

If Cox also includes age, diabetes, and other covariates, βᵀz can expand to β_A A + β_age × age + β_D × diabetes + …. The treatment coefficient generally describes an HR conditional on these inputs. Distinguish a weighted, treatment-only marginal working model from a covariate-adjusted conditional model. A causal interpretation of an HR also requires care, particularly because the groups’ survivor populations can differ during follow-up.

#### 3. Recognizing risk sets in one patient table
{: #section-80 }

Assume baseline multivariable LR has already produced propensity scores; we do not fit another LR here. This four-person table is a teaching device, not a randomized trial or an adequate sample for a substantive study.

| Patient | Actual drug | Follow-up record, months | LR probability of drug A | Unstabilized IPTW |
| --- | --- | --- | --- | --- |
| Person 1 | A | Dies at month 2 | 0.5 | 2 |
| Person 2 | A | Alive at the end of month 6 | 0.5 | 2 |
| Person 3 | B | Dies at month 4 | 0.8 | 5 |
| Person 4 | B | Last confirmed alive at month 3, then lost to follow-up | 0.5 | 2 |

Immediately before the month-2 death, all four patients remain observed and alive: the risk set is {Person 1, Person 2, Person 3, Person 4}. Person 1 belongs to the risk set immediately before their own death.

Person 4 is lost at month 3 and leaves subsequent risk sets, but their earlier information remains. Immediately before the month-4 death, the risk set is {Person 2, Person 3}: Person 1 has died and Person 4 has been lost.

In $$R_i^{(k)}$$, i indexes an event time and k indexes a hospital. E is the number of distinct event times: here E=2, with t₁=2 and t₂=4. It is neither the six-month horizon nor the four patients. Event-time and patient indices differ; Equation (6)’s use of i as shorthand for the event patient can obscure this distinction.

#### 4. Equation (6): given an event now, who is the event patient?
{: #section-81 }

Without tied event times, one event contributes:

$$
\frac{\exp(\beta^Tz_{\mathrm{event}})}{\sum_{j\in R_i}\exp(\beta^Tz_j)}.
$$

The numerator is the actual event patient’s relative hazard. The denominator sums relative hazards over all patients j in risk set R_i. Under the Cox model, this is the event-identity contribution conditional on an event occurring at that time—not the patient’s probability of dying by that time.

Why does h₀(t) disappear? Within a risk set, the model gives everyone a common baseline hazard, which cancels between numerator and denominator. We can therefore estimate β without first specifying h₀(t)’s shape: this is central to partial likelihood. Predicting an entire survival curve still requires baseline cumulative hazard information; h₀(t) has not ceased to exist.

Let $$r=\exp(\beta_A)$$ denote a candidate HR. Try r=0.5: each A patient has relative hazard 0.5 and each B patient has relative hazard 1.

At month 2, the denominator is 0.5+0.5+1+1=3. Person 1’s numerator is 0.5, giving a contribution of 1/6.

At month 4, only Person 2 and Person 3 remain. The denominator is 0.5+1=1.5, and Person 3’s numerator is 1, giving 2/3.

Π means multiply all the contributions, so the unweighted partial likelihood is (1/6) × (2/3) = 1/9. These are conditional event-identity contributions, **not the survival probabilities multiplied in Kaplan–Meier estimation**.

For arbitrary r, this table gives $$[r/(2r+2)]\times[1/(r+1)]$$. Software varies β_A, and therefore r, to find a larger partial likelihood. Evaluating it once does not estimate the HR.

#### 5. Equation (7): why does IPTW appear twice?
{: #section-82 }

Temporarily suppress hospital and tied-event indices and examine one event:

$$
\left[\frac{\exp(\beta^Tz_{\mathrm{event}})}{\sum_{j\in R_i}w_j\exp(\beta^Tz_j)}\right]^{w_{\mathrm{event}}}.
$$

**First, w_j appears in the denominator.** Every person still in the risk set contributes their relative hazard multiplied by their own weight, forming a weighted risk set.

**Second, the event weight appears as the exponent outside the brackets.** The event patient belongs to the denominator, but their observed event also requires a weighted contribution. Since $$\log(a^w)=w\log(a)$$, taking logs multiplies this event’s log contribution by w. The exponent is not a dose, w actual deaths, or an instruction to interpret a death probability raised to a power.

Weighting only the denominator omits the event contribution’s weight; weighting only the event omits risk-set weighting. Weights describe statistical contributions rather than new real patients.

The absence of w from the paper’s numerator is not necessarily an error. Including the event weight there adds $$w_{\mathrm{event}}\log w_{\mathrm{event}}$$ after taking logs. When propensity-score weights are fixed during Cox optimization, that term does not depend on β and does not change its optimum. The printed formula can therefore be viewed as a weighted partial-likelihood objective with such constants omitted. Each weighted fraction should not automatically be read as a normalized event-identity probability.

#### 6. Weighting the four-person example step by step
{: #section-83 }

Continue evaluating the candidate HR r=0.5.

At month 2, Person 1 contributes 2×0.5=1 to the weighted risk set, Person 2 contributes 1, Person 3 contributes 5×1=5, and Person 4 contributes 2×1=2: total 9. Event patient Person 1 has weight 2, so:

$$
\text{Month-2 contribution}=\left(\frac{0.5}{9}\right)^2.
$$

At month 4, the risk set contains only Person 2 and Person 3. Its denominator is 2×0.5+5×1=6. Event patient Person 3 has weight 5:

$$
\text{Month-4 contribution}=\left(\frac{1}{6}\right)^5.
$$

Multiply the contributions to obtain the weighted partial likelihood at this candidate HR. Its log form is easier to read:

$$
\ell_w=2[\log0.5-\log9]+5[\log1-\log6].
$$

For a general candidate r:

$$
\ell_w(r)=2[\log r-\log(4r+7)]-5\log(2r+5).
$$

Maximizing this curve produces the fitted value. The unweighted optimum in this example is r=1; the weighted optimum is approximately r=0.8982. This miniature example checks the formula; four records cannot establish a credible treatment effect. Weighting does not guarantee that an HR will move in a particular direction.

#### 7. D, q, and nested products: multiple events at the same time
{: #section-84 }

$$\mathcal D_i^{(k)}$$ is hospital k’s set of event patients at time t_i; $$|\mathcal D_i^{(k)}|$$ is its size. q enumerates people within that set. For example, if two people die at month 4, q takes values 1 and 2.

Equation (7)’s inner product multiplies contributions from event patients at the same time; the outer product multiplies across distinct event times. An empty event set contributes a product of 1. People who remain at risk still enter denominators for that hospital’s other events.

The screenshot repeatedly uses the same complete risk-set denominator for tied events. Its structure is a **Breslow-type treatment of ties**, rather than an exact formula universally used by every Cox implementation. Efron, Breslow, and exact methods are different choices. See the [official R survival documentation](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html).

#### 8. Equation (8): multiply hospital contributions without pooling risk sets
{: #section-85 }

Ignoring regularization and additional hospital weights, Equation (8) has the structure $$L(\beta)=\prod_k L^{(k)}(\beta)$$. Every hospital uses the same coefficient vector β, constructs its own local event contributions, and these are multiplied. Taking logs yields $$\sum_k\ell_k(\beta)$$.

**The denominator remains R_i^(k), the risk set within one hospital.** When hospital 1 has an event, hospital 2’s at-risk patients do not enter hospital 1’s denominator under this expression.

This structure corresponds to within-hospital comparisons with shared coefficients, as in a hospital-stratified Cox model. It is not the same as putting all patients into a single unstratified Cox model. A stratified model can have hospital-specific baseline hazards h₀ₖ(t) and common β; a pooled unstratified model instead uses a common risk set across hospitals at each event time. The product of local contributions can correspond to a centralized, hospital-stratified objective, although additional weighting, regularization, or finite-round optimization can further change results.

Shared β means jointly estimating model coefficients, not averaging independently estimated hospital HRs or assuming identical baseline mortality rates everywhere. See the [official explanation of stratified Cox models](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html).

#### 9. Equation (9): unpack the federated objective from one patient outward
{: #section-86 }

![Equation (9): the federated weighted Cox partial log-likelihood objective](/assets/causal-inference/tte-extension/li-2025-cox-eq9-closeup.png)

The paper introduces it as follows:

> Finally, the partial log-likelihood of our federated CoxPH model is shown in Eq. (9).

In plain language, the equation presents the federated Cox proportional hazards model’s partial log-likelihood.

**Start with the operation: select candidate Cox coefficients, calculate weighted event contributions within each hospital, combine them locally, then aggregate using hospital proportions and add the chosen regularization term. Software repeatedly changes the coefficients to find better values.**

The expression is long because it simultaneously represents patients, event times, hospitals, and optimization. Read from the inside rather than memorizing the whole expression. The source’s normalization and penalty-sign conventions require clarification; we first expand the printed formula faithfully, then discuss those issues separately. This is not a code audit.

##### 9.1 Lay out the complete printed expression
{: #section-87 }

$$
\log L(\boldsymbol\beta)
=
\sum_{k=1}^{K}p_k
\left\{
\log\left[
\prod_{i=1}^{E}
\prod_{q=1}^{|\mathcal D_i^{(k)}|}
\left(
\frac{\exp(\boldsymbol\beta^T\boldsymbol z_{i,q}^{(k)})}
{\displaystyle\sum_{j\in R_i^{(k)}}w_j^{(k)}\exp(\boldsymbol\beta^T\boldsymbol z_j^{(k)})}
\right)^{w_{i,q}^{(k)}}
\right]
+L_{\mathrm{reg}}(\boldsymbol\beta)
\right\}.
$$

Inside the braces, log acts on the whole product. L_reg is outside that log but remains inside the braces multiplied by hospital weight p_k. **This is neither log(product + L_reg) nor an expression with the hospital proportion inside the log.**

| Symbol | Reading | What does it index or represent? |
| --- | --- | --- |
| K, k | Total hospitals, hospital k | Hospitals |
| E, i | Number of distinct event times, event-time index i | Event times during follow-up |
| $$R_i^{(k)}$$ | Hospital k’s risk set immediately before t_i | People still observed and event-free |
| $$j\in R_i^{(k)}$$ | Iterate over patient j in the risk set | All at-risk patients, not only event patients |
| $$\mathcal D_i^{(k)}$$ | Hospital k’s event set at t_i | People who actually die then |
| $$\lvert\mathcal D_i^{(k)}\rvert$$ | Number of people in the set | Two if two people die simultaneously |
| q | The q-th event patient in that set | Distinguishes patients with the same event time |
| $$z_{i,q}^{(k)},z_j^{(k)}$$ | Event-patient and risk-set-patient model inputs | For example, the A/B indicator and selected covariates |
| β | Cox coefficient vector | Parameters to estimate, not LR coefficients π |
| w | One patient’s IPTW | Magnitude of a patient’s contribution |
| $$p_k=N_k/N$$ | Hospital sample proportion | Hospital-level contribution, not IPTW |
| L_reg | Regularization term | Additional parameter constraint; see the sign convention below |

The source uses E for event times generally. One interpretation uses the combined grid of event times across hospitals: if a hospital has no event at a time, its D set is empty and the inner product equals 1. Enumerating each hospital’s own event times is also possible, provided that the appropriate local risk sets are used.

##### 9.2 Innermost term: what number is exp(βᵀz)?
{: #section-88 }

βᵀz multiplies corresponding coefficients and variables and sums them. With treatment A and age, for example, βᵀz = β_A A + β_age × age. Superscript T is transposition, not a treatment label; exp is the exponential function.

For hand calculation, retain the weighted treatment-only Cox working model: A=1 for drug A and A=0 for drug B. Let $$r=\exp(\beta_A)$$, the candidate model’s HR:

- Drug A patient: $$\exp(\beta_A\times1)=r$$.
- Drug B patient: $$\exp(\beta_A\times0)=1$$.

Try r=0.5, corresponding to candidate $$\beta_A=\log(0.5)\approx-0.6931$$. This is **a trial parameter used to evaluate the model, not a fitted result**. Relative hazards are 0.5 for A and 1 for B; that 0.5 is neither a propensity score nor a death probability.

##### 9.3 The denominator: the current weighted risk set, not everyone enrolled
{: #section-89 }

Temporarily name the denominator $$B_i^{(k)}(\beta)$$:

$$
B_i^{(k)}(\beta)
=\sum_{j\in R_i^{(k)}}w_j^{(k)}\exp(\beta^Tz_j^{(k)}).
$$

B is simply a convenient name for the denominator, not an indicator for drug B. Read the calculation in order: select someone in the risk set → calculate their relative hazard → multiply by IPTW → sum over all people in that risk set.

Reuse the four-person table, now assigned to hospital 1. Baseline multivariable LR has already provided PS values; these teaching scores were not fitted from the four records alone.

| Patient | Drug | Follow-up record | LR probability of drug A | IPTW w |
| --- | --- | --- | --- | --- |
| Person 1 | A | Dies at month 2 | 0.5 | 2 |
| Person 2 | A | Alive at the end of month 6 | 0.5 | 2 |
| Person 3 | B | Dies at month 4 | 0.8 | 5 |
| Person 4 | B | Last confirmed alive at month 3, then lost to follow-up | 0.5 | 2 |

At month 2, all four are in the risk set immediately before the death. At candidate r=0.5:

$$
B_1^{(1)}=2\times0.5+2\times0.5+5\times1+2\times1=9.
$$

At month 4 only Person 2 and Person 3 remain:

$$
B_2^{(1)}=2\times0.5+5\times1=6.
$$

Person 1 has died and Person 4 has been lost, so neither enters the month-4 denominator. Event patients still belong to the risk set immediately before their events: Person 1 at month 2 and Person 3 at month 4 each enter their own denominator.

##### 9.4 The numerator: the actual event patient’s relative hazard
{: #section-90 }

Person 1 dies at month 2 and, as a drug A patient, has relative hazard 0.5: the fraction is 0.5/9.

Person 3 dies at month 4 and, as a drug B patient, has relative hazard 1: the fraction is 1/6.

The numerator gives the actual event patient’s relative hazard; the denominator gives the weighted total relative hazard of everyone at risk in that hospital at that time. This is not deaths divided by enrollment, nor a treatment probability.

The event contribution itself has not yet been weighted. That next layer must not be omitted.

##### 9.5 The exponent w: the event itself also contributes according to its weight
{: #section-91 }

Person 1 has weight 2, giving the month-2 contribution:

$$
\left(\frac{0.5}{9}\right)^2.
$$

Person 3 has weight 5, giving the month-4 contribution:

$$
\left(\frac16\right)^5.
$$

A square or fifth power does not mean that one patient died repeatedly. Its meaning is clearest after taking logs:

$$
\log(a^w)=w\log a.
$$

The exponent w multiplies the event’s log contribution by w. A patient therefore contributes in two ways: while at risk, their weight enters the denominator; when an event occurs, their weight also controls the event contribution. Weighting just one location generally does not reproduce this weighted Cox objective.

Be careful with “larger means more important.” When 0<a<1, raising a to a larger power makes the number smaller. This does not mean the patient matters less. Between two candidate coefficient sets, a larger w amplifies the record’s **difference in log scores**. For candidate fractions 0.1 and 0.2, that difference is log 2 with weight 1 and 5 log 2 with weight 5.

Adding the event weight to the numerator would add only w log w to the log expression. For Cox optimization with fixed weights, this additional term does not depend on β and does not change the best β. The printed equation omits such constants; its fractions should not simply be interpreted as individual event probabilities that sum to 1.

##### 9.6 Two products: event patients within a time, then distinct times
{: #section-92 }

Π means multiply these terms, not add them.

- The inner product over q separately calculates and multiplies the contributions if two people have events at the same time.
- The outer product over i multiplies the contributions from the first event time, second event time, and so on.

This example has one event patient per time, so each inner product contains one term. Hospital 1’s product at the candidate coefficient is:

$$
L^{(1)}_w(\beta)=\left(\frac{0.5}{9}\right)^2\left(\frac16\right)^5.
$$

In a different teaching scenario, suppose two patients a and b have events together, with weights w_a and w_b, relative hazards r_a and r_b, and common denominator B. That time contributes $$(r_a/B)^{w_a}(r_b/B)^{w_b}$$. Its log is $$w_a\log r_a+w_b\log r_b-(w_a+w_b)\log B$$. The screenshot reuses the common denominator, corresponding to Breslow-type tie handling; do not equate this mechanically with other ties algorithms.

##### 9.7 The outer log: turn a product into additive contributions
{: #section-93 }

Use three identities: log(ab)=log a+log b; log(a^w)=w log a; and log(a/b)=log a−log b. Hospital 1’s score is therefore:

$$
\ell_1(\beta)=2[\log0.5-\log9]+5[\log1-\log6]\approx-14.739541.
$$

Here ℓ₁ is shorthand for hospital 1’s log contribution. **It is a score for comparing candidate coefficients, not an HR, p value, or survival probability.**

The complete local log expansion is:

$$
\ell_k(\beta)=\sum_{i=1}^{E}\sum_{q=1}^{|\mathcal D_i^{(k)}|}
 w_{i,q}^{(k)}
\left[
\beta^Tz_{i,q}^{(k)}
-\log\left(\sum_{j\in R_i^{(k)}}w_j^{(k)}\exp(\beta^Tz_j^{(k)})\right)
\right].
$$

Since log(exp(x))=x, the exponential in the numerator becomes βᵀz. Understand this expanded expression, then return to the product in the screenshot: they are two ways of writing the same local data contribution.

##### 9.8 Add a second hospital and calculate the outermost layer
{: #section-94 }

Suppose hospital 2 has two patients: Person 5 takes B and dies at month 1; Person 6 takes A and remains alive through month 6. Both have baseline PS 0.5 and IPTW 2. Use the same candidate HR r=0.5.

Hospital 2’s month-1 local risk set contains only Person 5 and Person 6. The denominator is 2×1+2×0.5=3; event patient Person 5 has numerator 1 and weight 2:

$$
\ell_2(\beta)=2[\log1-\log3]\approx-2.197225.
$$

Total sample size N=4+2=6, so p₁=4/6=2/3 and p₂=2/6=1/3. **Set regularization to zero and follow the printed expression literally**:

$$
J_{\mathrm{printed}}(\beta)
=\frac23\ell_1(\beta)+\frac13\ell_2(\beta)
\approx -10.558769.
$$

This global number is the score for candidate r=0.5 under this objective, not a final estimate. J names the complete printed optimization objective, distinguishing it from a likelihood without additional hospital proportions.

Change the coefficient to one corresponding to r=1 and repeat. Hospital 1 scores −14.525341, hospital 2 scores −2.772589, and the printed global objective is −10.607757. Because the score at r=0.5 is higher, the printed objective prefers r=0.5 **among these two candidates**. This does not establish an optimum of exactly 0.5; optimization must continue.

A crucial detail remains: when hospital 2 has its month-1 death, hospital 1’s four patients do not enter its denominator. A risk set pooled across both hospitals would have denominator 9+3=12 at that time, rather than 3. **Aggregating hospital scores does not automatically pool risk sets.**

##### 9.9 L_reg: where is it added, and what does it constrain?
{: #section-95 }

Temporarily hide the detailed data term. The printed expression has the outer form:

$$
J_{\mathrm{printed}}(\beta)=\sum_kp_k[\ell_k(\beta)+L_{reg}(\beta)].
$$

L_reg is an additional parameter constraint, not an event, patient weight, or baseline hazard. If every hospital truly has the same L_reg independent of k, the weights summing to 1 leave one copy after aggregation. A local FedProx penalty, however, normally depends on the local candidate parameters and the current round’s global reference, and should be expressed with the relevant hospital and round dependence.

For one local treatment coefficient, suppose the server sends reference β_ref=−0.3, the local candidate is u=−0.7, and μ=2. The nonnegative penalty is:

$$
P_k(u)=\frac\mu2(u-\beta_{ref})^2=\frac22(-0.7+0.3)^2=0.16.
$$

At u=−0.4, the penalty is only 0.01. Local fitting must trade off fit to the data against departing from the common starting point. During this local update β_ref is fixed, while u is optimized.

**The sign matters.** If ℓ is a log-likelihood to maximize, maximize ℓ−P. If minimizing negative log-likelihood, use −ℓ+P. The screenshot’s “+L_reg” acts as a penalty only under a consistent sign convention. Together with the preceding description of L_reg as a positive squared distance, one cannot literally maximize “ℓ + positive distance”: that would reward divergence. This flags the printed convention; it does not establish that the code contains the same problem.

##### 9.10 Why hospital proportions p_k and patient weights w are different
{: #section-96 }

| Comparison | Patient IPTW w | Hospital proportion p_k |
| --- | --- | --- |
| Origin | Patient’s PS and actual treatment | Hospital enrollment divided by total enrollment |
| Location | Risk-set denominator and event exponent | Outside the complete hospital objective |
| Immediate role | Adjust patient contributions to the treatment comparison | Determine relative influence of hospital objectives |
| Directly interchangeable? | No | No |

Report these weights’ origins separately. For a fixed within-hospital constant, some ways of incorporating p_k into patient weights can yield the same data-term optimization up to parameter-independent constants. Regularization and variance still require corresponding treatment; that algebra does not make the weights conceptually identical.

Equation (8) multiplies hospital likelihoods, whose log is simply $$\sum_k\ell_k$$. Adding p_k in Equation (9) gives a different weighted objective, not merely an algebraic rewrite. If each local ℓ_k already sums events, multiplying by hospital sample proportion changes hospital influence again. Whether a local term is first averaged, and its averaging denominator, require checking the implementation. Do not silently insert a denominator and present it as the authors’ actual procedure.

##### 9.11 An objective function is neither a training algorithm nor a reported effect
{: #section-97 }

We just calculated a score for a given β. Training instead involves a sequence: the server sends parameters → hospitals update locally from the shared starting point → parameters or updates return → the server aggregates → another round begins. Averaging a few likelihood scores alone does not produce an HR; optimization needs parameter and gradient information or equivalent update machinery.

After obtaining treatment coefficient $$\widehat\beta_A$$, compute $$HR=\exp(\widehat\beta_A)$$. A 95% CI also requires an appropriate standard error. Patient records, PS weights, and timing are treated as given during the current Cox coefficient update; that does not eliminate weight-estimation uncertainty from inference for the complete study.

**Restate Equation (9) in order:** relative hazard → local weighted risk-set denominator → event contribution and its weight → all events at that time → all local event times → logarithm → regularization convention → hospital-proportion aggregation. Keep three interpretation boundaries explicit: local risk sets, local normalization, and the penalty sign.

##### 9.12 Self-check: five questions about the nested structure
{: #section-98 }

1. Why is Person 4 absent from the month-4 denominator? Person 4 was lost at month 3 and is no longer in the observed risk set.
2. Where is Person 1’s weight at month 2? In both the weighted denominator and the exponent of Person 1’s own event contribution.
3. What does q do when two patients die simultaneously? It enumerates their separate event contributions.
4. Is p_k a treatment probability? No: it is a hospital sample proportion.
5. Does calculating a negative global score produce an HR? No: optimize β, then exponentiate the treatment coefficient.

#### 10. Iteration, HRs, and confidence intervals
{: #section-99 }

The server sends current β, hospitals update using local risk sets and patient weights, and the server aggregates parameters for the next round. Defining an objective does not prove that finitely many rounds of parameter averaging attain its exact optimum. If the model includes treatment coefficient β_A, the final HR is $$\exp(\widehat\beta_A)$$.

A 95% CI requires uncertainty estimation. A common Wald form is $$\exp[\widehat\beta_A\pm1.96\,SE(\widehat\beta_A)]$$, but the standard-error calculation must suit IPTW, clustering, and the federated design. Weighted contributions are not newly observed independent patients. Equations (5)–(9) alone do not establish how PS-estimation uncertainty or hospital dependence was handled; those require examining the inference implementation.

Baseline IPTW does not automatically address informative censoring. Assess the Cox proportional-hazards assumption, measured balance, overlap, and weight stability separately. An HR is not a risk ratio and cannot by itself provide an absolute risk at a chosen year.

Source comparison: [Li et al. (2025), Federate Cox Proportional Hazards Model, Equations (5)–(9)](https://www.nature.com/articles/s41746-025-01803-y). The discussion of Equations (8)–(9) and local risk sets is a mathematical reading of the printed formulas, not a code-audit result.



### 5.18 How do competing events affect AD risk, Cox models, and IPTW?
{: #section-100 }

See [Competing Events and Adaptations of Classical Methods]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}#section-47). The detailed explanation starts with death versus loss to follow-up, calculates 1−KM and AJ/CIF by hand, and then addresses cause-specific Cox, Fine–Gray, weighted AJ, PSM, and the g-formula. It also distinguishes the TTE total-effect question from a hypothetical question in which death is eliminated.

## 6. References and source articles
{: #section-39 }

1. Zang et al. (2023). [Journal article](https://doi.org/10.1038/s41467-023-43929-1). Locations: PDF pages 1–4 and 10–12.
2. Li et al. (2025). [Journal article](https://doi.org/10.1038/s41746-025-01803-y). Initial locations: PDF pages 1–2.
