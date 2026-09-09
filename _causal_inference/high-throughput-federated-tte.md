---
layout: "causal-note"
title: "High-Throughput Drug Screening and Federated Target Trial Emulation"
description: "Explore high-throughput drug screening, IPTW model selection, data splits, balance diagnostics, and federated TTE questions."
group: "Extensions"
order: 23
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. What does each paper extend?", "anchor": "section-1"}, {"title": "2. Where subsequent discussions belong", "anchor": "section-2"}, {"title": "3. Discussion: what is the IPTW framework?", "anchor": "section-3"}, {"title": "4. Reading the original text: High-throughput cohorts, ML-PS, and every data level in Boxes 1–2", "anchor": "section-13"}, {"title": "5. Discussion: Does classical IPTW require train/test splitting? How does LR obtain each propensity score?", "anchor": "section-28"}, {"title": "6. References and local originals", "anchor": "section-39"}]
previous_note: "/causal-inference/g-estimation/"
next_note: "/causal-inference/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). Foundational framework: [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}).

<aside class="study-callout study-callout--note" markdown="1">

**Purpose of this note**

This extension to the main TTE route collects discussions of the two papers below. It currently includes a beginner’s explanation of the IPTW framework and a detailed companion to the 2023 paper’s high-throughput cohorts, Fig. 1, Boxes 1–2, and model selection. Other topics remain open for discussion; this is not a completed critical review of both papers in full.

</aside>


## 1. What does each paper extend?
{: #section-1 }

| Paper | Extension | Connections to existing notes |
| --- | --- | --- |
| Zang et al., 2023, *High-throughput target trial emulation for Alzheimer’s disease drug repurposing with real-world data*, Nature Communications 14:8180 | Scales TTE into a large drug-repurposing screening workflow; compares machine-learning propensity-score models within IPTW, emphasizing baseline covariate balance after model selection | [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}); [Clinical Records, NLP, Imaging, and Machine Learning]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }}) |
| Li et al., 2025, *Federated target trial emulation using distributed observational data for treatment effect estimation*, npj Digital Medicine 8:387 | Extends TTE to multiple institutions without sharing patient-level data; connects federated protocol design, federated IPTW, and federated Cox modeling | [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}); [Cox Proportional Hazards]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}) |

The first primarily asks how to conduct many drug comparisons at scale; the second asks how to collaborate on estimation when data remain distributed across institutions. In both, examine the target population, strategies, time zero, outcome, target effect, and identification assumptions individually.

## 2. Where subsequent discussions belong
{: #section-2 }

- **High-throughput TTE:** defining protocols and comparator drugs; distinguishing propensity-score prediction performance from covariate balance; interpreting screening and cross-database validation.
- **Federated TTE:** which computations remain local and which information is exchanged; differences from aggregate-data analysis and meta-analysis; handling site heterogeneity and the target population.
- **Connections and limits:** which implementation steps are extended, which causal identification assumptions remain, and whether high-throughput screening can be connected to federated analysis.

These are questions for further discussion, not established conclusions. Later additions will organize questions, explanations, and examples by topic, identify source pages or figures, and distinguish authors’ claims, interpretation, and issues still requiring verification.

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

For each component and calculation, see [Step Five: Use A's Probability for Drug A and B's for Drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-20). Symbol definitions now appear before that section's patient table.

## 6. References and local originals
{: #section-39 }

1. Zang et al. (2023). [Journal article](https://doi.org/10.1038/s41467-023-43929-1). Locations: PDF pages 1–4 and 10–12.
2. Li et al. (2025). [Journal article](https://doi.org/10.1038/s41746-025-01803-y). Initial locations: PDF pages 1–2.
