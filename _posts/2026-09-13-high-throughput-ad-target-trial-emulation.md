---
layout: post
title: "High-Throughput Target Trial Emulation for Alzheimer's Drug Repurposing"
description: "A detailed methodology guide to Zang et al.: trial protocols, comparator sampling, time zero, machine-learning propensity scores, balance-based cross-validation, stabilized IPTW, weighted survival analysis, screening, replication, and causal limitations."
permalink: /rwe/high-throughput-ad-target-trial-emulation/
date: 2026-09-13 11:00:00 -0400
research_area: real-world-evidence
paper_year: 2023
paper_venue: Nature Communications
reading_focus: "How repeated drug-initiation comparisons use balance-selected propensity scores, stabilized weights, and survival models to screen drug-repurposing hypotheses."
rwe_topics: [Drug repurposing, Propensity scores, Survival analysis]
foundation_notes: [target-trial-emulation, inverse-probability-weighting, weighted-survival-analysis]
math: true
tags: [Method, Pharmacoepidemiology, Target Trial Emulation, Drug Repurposing, Propensity Scores, Causal Inference]
---

**Paper:** Chengxi Zang et al., *High-throughput target trial emulation for Alzheimer's disease drug repurposing with real-world data*, **Nature Communications 14, 8180**, published December 11, 2023. [Journal article](https://www.nature.com/articles/s41467-023-43929-1) · [DOI](https://doi.org/10.1038/s41467-023-43929-1) · [Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-43929-1/MediaObjects/41467_2023_43929_MOESM1_ESM.pdf) · [Authors' code](https://github.com/calvin-zcx/RWD4Drug).

This study asks whether existing medications are associated with a lower rate of subsequently recorded Alzheimer's disease (AD) among people with previously recorded mild cognitive impairment (MCI). Its methodological contribution is a **screening workflow that repeatedly emulates drug-initiation comparisons and selects propensity-score models primarily for covariate balance**. The reported drug candidates are hypotheses from observational data, not established treatments for preventing AD.

These notes explain the supplied 16-page article and its 72-page supplement. Main-paper page numbers and supplement page numbers are distinguished throughout. Equations labeled as explanatory unpack the estimators rather than add analyses the authors performed. A small, explicitly labeled implementation audit uses the public code revision `a783e8d86f60a3d9c7f7715419e90afb1cdb28c8`, dated November 3, 2023; it does not establish which script generated every published result.

<nav class="table-of-contents" aria-label="Contents" markdown="1">

**Contents**

1. [What is being estimated, and what is being screened?](#question)
2. [Data sources and the different meanings of sample size](#data)
3. [The target-trial protocol, component by component](#protocol)
4. [Eligibility, phenotype codes, and observed new use](#eligibility)
5. [Comparator construction and repeated emulations](#comparators)
6. [Time zero, refill confirmation, and follow-up](#time-zero)
7. [Baseline covariates and their representations](#covariates)
8. [What the propensity-score models learn](#ps-models)
9. [All reported model architectures and hyperparameters](#hyperparameters)
10. [Stabilized IPTW, clipping, and overlap](#weights)
11. [Balance diagnostics: SMDs and the trial-level threshold](#balance)
12. [The exact model-selection algorithm in Boxes 1–2](#selection)
13. [Weighted Cox and Kaplan–Meier outcome analyses](#survival)
14. [Aggregation, bootstrap inference, screening, and multiplicity](#screening)
15. [The five candidates and what cross-database replication means](#results)
16. [Sensitivity analyses and causal-discovery adjustment](#sensitivity)
17. [Simulation design, estimands, and limitations](#simulations)
18. [Causal assumptions and the remaining threats](#limitations)
19. [Reproducibility details and source discrepancies](#reproducibility)
20. [A complete worked workflow and related reading](#workflow)

</nav>

## 1. What is being estimated, and what is being screened?
{: #question }

There are two linked research questions. The **methodological question** is which propensity-score modeling and selection procedure most reliably balances measured baseline characteristics in many observational drug comparisons. The **substantive question** is which medications show a sufficiently consistent association with delayed AD diagnosis to justify further investigation.

For a particular target drug, one emulation compares eligible people initiating that drug with eligible people initiating alternative medications. The authors then rebuild the comparison group repeatedly. They estimate an adjusted hazard ratio within each adequately balanced emulation, summarize results across those emulations, and require evidence in both an EHR database and an insurance-claims database.

The process therefore has several distinct units:

- A **patient record** supplies baseline history, treatment initiation, and observed follow-up.
- A **drug-specific emulation** contains treated and comparison records and its own fitted propensity model.
- A **drug-specific screening result** summarizes the balanced subset of repeated emulations.
- A **replicated candidate** satisfies the screening criteria in both data sources.

The study does not train one universal model whose output is the causal effect of every medication. It repeatedly fits treatment-assignment models and survival analyses to different assembled comparisons. Nor does an emulation become a randomized trial because weighted covariates satisfy a balance threshold. “Target trial emulation” names the design framework; IPTW is the adjustment method within that framework. [Main paper, pp. 2–4 and 10–12.](https://www.nature.com/articles/s41467-023-43929-1)

<figure>
  <a href="{{ '/assets/rwe/high-throughput-ad/figure-1-pipeline.png' | relative_url }}"><img src="{{ '/assets/rwe/high-throughput-ad/figure-1-pipeline.png' | relative_url }}" alt="Original study pipeline showing cohort selection, propensity-model selection, balance assessment, and drug screening" loading="lazy"></a>
  <figcaption>Figure 1 from Zang et al. (2023), cropped from the supplied PDF to retain the original figure. The left branch constructs drug-specific comparisons; the lower panels separate propensity-model selection from survival analysis and screening. Reproduced under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; no scientific content was changed. The Methods use inclusive eligibility thresholds where the schematic uses shorthand inequality labels.</figcaption>
</figure>

## 2. Data sources and the different meanings of sample size
{: #data }

The two sources differ in geography, clinical capture, and how medication records arise:

| Level | OneFlorida | MarketScan |
| --- | --- | --- |
| Data type | Patient-level EHR data | Administrative insurance claims |
| Observation period | January 2012–April 2020 | January 2009–June 2020 |
| Source-database population | 14,883,388 patients | 164,148,434 enrollees |
| Geography described | Primarily Florida, with selected locations in Georgia and Alabama | Across the United States |
| MCI-coded source population | 73,927 | 424,961 |
| AD-coded patients within the MCI source population, Figure 1/Supplement Table S1 | 10,530 | 67,973 |
| Drug ingredients identified | 1,825 | 2,489 |
| Drugs retained with at least 500 eligible treated patients | 66 | 246 |
| Emulations for these retained drugs | 6,600 | 24,600 |

The combined warehouse size is approximately 179 million records of patients/enrollees across databases. It is not the number of people in a single analysis, and adding source counts does not establish a deduplicated national population. Likewise, the initial MCI counts precede the complete drug-specific eligibility process: Supplementary Table S1 includes age distributions extending below 50, whereas each trial requires age at MCI diagnosis of at least 50.

The headline of more than 4,300 drugs and roughly 430,000 emulations describes the broad enumeration stage. The reported ingredient counts sum to 4,314 **database-specific ingredient entries**; some drugs occur in both sources. The primary sufficiently large screening sets contain 66 + 246 = **312 database-specific drug analyses**, each with 100 comparator emulations. These distinctions matter for computational scale, multiplicity, and the strength of independent evidence. [Main paper, pp. 2, 4–6, 9; Supplementary Table S1, p. 3.](https://www.nature.com/articles/s41467-023-43929-1)

The manuscript describes MarketScan as nationally representative. Nationwide coverage alone does not establish representativeness of uninsured people, every insurance category, or the broader MCI population. The appropriate reading is that it provides a geographically broader and differently measured replication source.

## 3. The target-trial protocol, component by component
{: #protocol }

Table 1 of the paper places a hypothetical randomized trial beside its observational emulation. The core components are:

| Component | Hypothetical trial | Operational emulation |
| --- | --- | --- |
| Eligibility | MCI; age at least 50; no previous AD/dementia; no previous target-drug use | Selected diagnosis codes; MCI before drug initiation; at least one year of observable history; no recorded AD/related dementia in the preceding five years; first observed drug prescription |
| Treatment strategies | Initiate the target drug versus initiate an alternative | Classify according to observed initiation; require a second prescription separated by at least approximately one month to confirm initiation |
| Assignment | Random assignment at baseline | Observed treatment choice; assume conditional exchangeability given measured baseline covariates and use IPTW |
| Time zero | Eligibility, assignment, and follow-up start coincide | First prescription of the assigned drug, with the refill-confirmation qualification discussed below |
| Outcome | AD onset | First recorded AD diagnosis in follow-up |
| Follow-up | Until AD, loss to follow-up, or five years | Also ends at the database cutoff; two-year horizon in sensitivity analysis |
| Contrast | Intention-to-treat effect of assignment | Observational analog of an initiation contrast, with baseline exposure classification |
| Analysis | Time-to-event comparison | Stabilized-IPTW weighted Cox and Kaplan–Meier analyses; screen and summarize balanced emulations |

An intervention must be understood at the level actually recorded. The medication grouping is by major active ingredient, not a fully specified regimen including dose, route, formulation, duration, and adherence. Two people assigned the same ingredient can receive different versions of treatment. This is relevant to consistency and to how a later confirmatory trial should define its intervention.

The paper calls the contrast an observational analog of intention to treat. This means initial exposure group is retained during follow-up. It does **not** mean there was randomized assignment, documented intent independent of receipt, or an analysis of continuous adherence. A per-protocol effect of sustained use would require additional strategy definitions and adjustment for time-varying adherence and confounding. The authors identify that as future work. [Table 1, p. 10; “Causal associations of interest,” p. 11; Discussion, p. 9.](https://www.nature.com/articles/s41467-023-43929-1)

## 4. Eligibility, phenotype codes, and observed new use
{: #eligibility }

### 4.1 The eligibility checks are relative to each person's index date

For each drug-specific cohort, the paper requires:

1. At least one recorded MCI diagnosis in the source period.
2. Age **at least 50 at MCI diagnosis**, without an upper age limit.
3. The first MCI diagnosis occurs **before** the first prescription of the drug defining that person's group.
4. At least **one year** between the first available database record and the index date, with no stated upper limit on baseline history.
5. No recorded AD or AD-related dementia diagnosis in the **five years before** index.

These rules do not require five fully observed years before baseline. Someone with only one year of records may satisfy the no-recorded-dementia rule despite having four earlier unobserved years. Similarly, first prescription **in the database** is not necessarily first prescription in a person's life. An adequate observation window reduces prevalent-user misclassification but cannot establish lifetime nonuse.

The source text uses “baseline period” for all available history before index after requiring a minimum of one year. It does not specify a common fixed one-year covariate window for everyone. Therefore people with longer recorded histories may have more opportunities to accumulate diagnosis and medication indicators. A reproduction should inspect and document the exact lookback implementation rather than replace it with a one-year window by assumption.

### 4.2 Exact phenotype definitions from Supplementary Table S3

The supplement supplies the diagnosis-code definitions:

| Phenotype | ICD-9 codes | ICD-10 codes | Role |
| --- | --- | --- | --- |
| MCI | `331.83`, `294.9` | `G31.84`, `F09` | Identify the source population |
| AD | `331.0` | `G30`, `G30.0`, `G30.1`, `G30.8`, `G30.9` | Exclude prevalent AD; identify incident follow-up AD |
| AD-related dementias | `294.10`, `294.11`, `294.20`, `294.21`, `290.*` | `F01.*`, `F02.*`, `F03.*` | Baseline exclusion |

The rule accepts any listed code. In particular, `294.9` and `F09` denote unspecified mental disorders due to physiological or other classified conditions; they are broader than a specific MCI code. Consequently the operational cohort should be described as **patients meeting the study's MCI code algorithm**, not necessarily people with a uniformly adjudicated neuropsychological MCI diagnosis. Likewise, first AD coding is the observed endpoint; it is not the biological beginning of AD pathology. [Supplementary Table S3, p. 7.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-43929-1/MediaObjects/41467_2023_43929_MOESM1_ESM.pdf#page=7)

### 4.3 What “new user” can and cannot establish

A new-user design aligns covariate collection before initiation and avoids comparing long-term survivors of one treatment with new users of another. Here initiation is determined from the first observed prescription plus a later confirmation. The design has the useful new-user intention, but incomplete prior capture and the confirmation requirement require separate scrutiny. Neither covariate balance nor a large database repairs a time-zero definition that uses future information.

## 5. Comparator construction and repeated emulations
{: #comparators }

For each retained target drug, the authors construct **100 comparisons**:

- **50 random-drug controls:** eligible initiators of other medications.
- **50 same-class controls:** eligible initiators of medications in the same second-level Anatomical Therapeutic Chemical classification, ATC-L2, as described in the manuscript.

The comparison index date is initiation of the **alternative drug**, so its baseline history and follow-up are anchored to that person's own initiation. Patients in the target-drug group, or with target-drug use before the comparison baseline, are excluded from controls. The wording in Table 1 is somewhat broader, saying patients prescribed the trial drug are excluded; a reproduction should verify the temporal scope of that exclusion, especially whether it ever uses future exposure.

Supplementary Table S2 specifies a target control-group size of **three times the treated-group size**. That is a sampling design choice, not a causal requirement. Actual displayed counts can be smaller when the available control pool is limited. There is no requirement that treatment and control groups be equal-sized for IPTW or Cox analysis.

The random-drug control is still **another-drug initiation strategy**. Calling it placebo-like does not make it an actual placebo comparison, a no-treatment comparison, or a well-defined common alternative. Its results depend on the mix of diseases, treatment indications, care patterns, and medications entering that pool. Same-class comparison can improve clinical comparability, but ATC-L2 is broad and does not guarantee identical indications, disease severity, routes, or prescribing circumstances.

The repeated analyses explore sensitivity to comparison-group construction. They are not 100 independently recruited randomized trials. The target-drug patients commonly recur, and comparison patients can overlap across repetitions. A drug-versus-one-mixture comparison and a drug-versus-another-mixture comparison may also target somewhat different contrasts. Averaging their hazard ratios does not automatically produce the effect of a single clearly defined alternative strategy.

**Implementation observation.** In the pinned `main_revise_testset.py`, alternative drug cohorts are shuffled and accumulated, target-exposed records are excluded, and controls are sampled toward the 3:1 target. Thus “random drug” need not mean exactly one fixed named alternative per emulation. This script also has an ATC fallback to random candidates if no eligible same-class alternatives exist; for GPI-coded data it groups by the first two GPI digits. These are details of the inspected script, not proof that every published class-based comparison used that exact path. [Pinned comparator implementation](https://github.com/calvin-zcx/RWD4Drug/blob/a783e8d86f60a3d9c7f7715419e90afb1cdb28c8/iptw/main_revise_testset.py#L188).

## 6. Time zero, refill confirmation, and follow-up
{: #time-zero }

### 6.1 The intended chronology

The design intends the following sequence for each person:

```text
First observed record ───── first MCI diagnosis ───── first drug prescription
        baseline history, minimum one year                     time zero
                                                               │
                                                AD event, censoring, or horizon
```

The actual positions of the first observed record and first MCI diagnosis can vary, but MCI must precede index and all baseline variables must be collected before treatment initiation.

### 6.2 A later prescription is used to confirm the earlier initiation

The Methods require at least two consecutive prescriptions over 30 days, while Table 1 describes at least two prescriptions separated by at least one month. Time zero nevertheless remains the **first prescription**. This is a methodological tension: membership in the analytic cohort depends on information occurring after nominal baseline.

Consider a teaching example. Patient A fills a first prescription on day 0 and a confirming prescription on day 40. Patient B starts on day 0 but dies, leaves the data source, stops treatment because of an adverse effect, or never refills before day 40. Requiring later confirmation can retain A and exclude B based on their subsequent course. The resulting comparison is partly among people who remain observable and meet a future-use condition.

This creates a **potential post-baseline selection and immortal-time problem**. “Immortal” must be used carefully: the requirement necessarily entails surviving or remaining observable long enough to obtain confirmation under many real-world circumstances, but the paper does not establish that an AD diagnosis itself always prevents a second prescription. The exact bias depends on event ordering, exclusion logic, and how time between prescriptions is counted. It would be too strong to assert that every included patient was guaranteed AD-free throughout that interval.

Methods capable of addressing such a condition include redefining a landmark target population at confirmation or specifying a grace-period strategy with appropriate cloning/censoring/weighting. These are **possible redesigns**, not methods used in this study, and they change the target question. Merely moving the follow-up start without reconsidering eligibility and the estimand is insufficient.

### 6.3 Follow-up and event classification

The primary follow-up horizon is five years, shortened to two years in sensitivity analysis. Follow-up ends at the earliest of:

1. First AD diagnosis after baseline.
2. Loss to follow-up according to available prescription/diagnosis records.
3. The chosen horizon.
4. The source-database end date.

The paper distinguishes three record situations. A **positive event** is an AD diagnosis within follow-up; its time is days from baseline to first AD diagnosis. A **negative event** means no AD diagnosis and evidence of observation through the horizon; its recorded time is the follow-up horizon. A **censored observation** means no AD diagnosis and the last prescription and diagnosis dates both precede the horizon; its time is the later of those two last dates minus baseline.

For survival analysis, the latter two situations both have an event indicator of zero but contribute different amounts of observed time. A person observed without AD for 18 months cannot simply be counted as AD-free at five years. Administrative truncation at the database cutoff must also be applied consistently. [“Follow-up” and “Outcomes,” main p. 11.](https://www.nature.com/articles/s41467-023-43929-1)

### 6.4 What censoring adjustment is actually used?

The paper assumes **noninformative censoring**. It does not add an inverse-probability-of-censoring model to the baseline treatment weights. Using a Cox model or Kaplan–Meier curve accommodates incomplete observation under the relevant censoring assumptions; it does not make informative loss to follow-up harmless.

Death is not separately specified as a competing event in the reported protocol. Because death prevents a later recorded AD diagnosis, a full causal interpretation of AD incidence should distinguish death from ordinary loss to follow-up. A cause-specific hazard, a cumulative incidence function with competing death, and a hypothetical AD risk if death were prevented answer different questions. The reported analyses do not settle those distinctions.

## 7. Baseline covariates and their representations
{: #covariates }

### 7.1 The 267-variable representation

The primary adjustment set contains:

| Block | Dimensions | Encoding |
| --- | ---: | --- |
| Age | 1 | Continuous |
| Self-reported sex/gender | 1 | Binary representation in the study |
| Time from first MCI diagnosis to drug initiation | 1 | Continuous |
| Selected comorbidities | 64 | Binary indicators from ICD-9/10 definitions |
| Prior medication ingredients | 200 | Binary medication-history indicators |
| **Total** | **267** | |

The 64 comorbidities draw on the Chronic Conditions Data Warehouse and expert-selected AD risk factors. The complete ICD definitions are supplied in Supplementary Table S4, placed at the end of the supplement because of its size. Medication-history variables use the 200 most prevalent prescribed ingredients. OneFlorida drug codes are mapped from NDC/RxNorm to major active ingredients using RxNorm/UMLS; MarketScan drugs are grouped using the first eight digits of Medi-Span GPI.

The MCI-to-initiation interval is important because two people can have the same coded diagnoses but be at different observed points in the cognitive-disease trajectory. It is still only a proxy for underlying duration or severity; it does not recover cognition scores, biomarker status, or unrecorded progression.

Binary history variables summarize **whether a condition or medication was recorded**, not necessarily its severity, dose, persistence, or absence in reality. The paper does not provide a general imputation model for unmeasured clinical factors. A zero in a code-derived indicator should not be interpreted as a validated negative clinical finding.

### 7.2 Temporal inputs for the LSTM

The LSTM model additionally receives sequences of diagnoses and medication histories across baseline time. It can distinguish histories that have the same “ever observed” indicators but different order or concentration of records. All those sequences should remain pretreatment. Bidirectionality refers to reading a **baseline sequence** in both directions; it need not imply access to post-initiation outcomes.

The manuscript does not fully specify temporal binning, padding, maximum sequence length, or all embedding dimensions. The code gives additional architectural detail below, but a faithful reproduction also requires the preprocessing files and the specific execution configuration.

### 7.3 Why more covariates are not automatically better controls

Adjustment is motivated by common causes of treatment choice and AD diagnosis. An outcome predictor may improve precision, but an instrument-like predictor of prescribing can worsen overlap without controlling additional confounding; conditioning on a collider can create an association. The paper therefore also evaluates a smaller, knowledge-guided and causal-discovery-guided set. That is a sensitivity analysis of the adjustment assumptions, not proof that the selected graph is the true causal graph.

## 8. What the propensity-score models learn
{: #ps-models }

Let $$Z_i=1$$ indicate target-drug initiation and $$Z_i=0$$ indicate the sampled alternative initiation. Let $$X_i$$ be baseline information, $$T_i$$ observed follow-up time, and $$\Delta_i$$ the AD-event indicator. We use $$\Delta$$ here to avoid confusing the outcome indicator with a potential-outcome risk.

The propensity score is:

$$
e(X_i)=P(Z_i=1\mid X_i).
$$

This is a probability of **receiving the target treatment among the assembled comparison population**. It is not the probability of AD, a probability that treatment succeeds, or a randomized assignment probability known by design.

Every propensity model is trained to predict $$Z$$ from $$X$$ by binary cross-entropy:

$$
\mathcal L(\theta)=-\frac{1}{n}\sum_i
\left[Z_i\log\widehat e_\theta(X_i)
 +(1-Z_i)\log\{1-\widehat e_\theta(X_i)\}\right],
$$

with the specified regularization for the model. AD outcomes do not enter this training loss. The innovation is in **selecting among trained propensity models**, not replacing their prediction loss with a direct AD-effect objective.

The same patient can have different propensity scores in different emulations because the sampled alternatives, comparison population, fitted model, and marginal treatment prevalence change. A propensity score is therefore a property of a treatment-comparison problem, not an intrinsic permanent score attached to a person.

A high treatment AUC only means the model ranks actual treatment choice well. If treatment groups are nearly separable, it may correspond to poor overlap and extreme weights. Conversely, a model with slightly lower AUC can produce more useful weighted balance. The study tests that difference empirically rather than assuming the best classifier is the best confounding-adjustment model.

## 9. All reported model architectures and hyperparameters
{: #hyperparameters }

### 9.1 Regularized logistic regression: LR-PS

The model is:

$$
\widehat e(X)=\operatorname{expit}(\beta_0+X^\top\beta),
\qquad \operatorname{expit}(u)=\frac{1}{1+e^{-u}}.
$$

The search includes **L1 regularization, L2 regularization, and no regularizer**. For regularized models, the inverse regularization parameter is:

$$
C\in\{10^{-3},10^{-2.5},10^{-2},10^{-1.5},10^{-1},10^{-0.5},
10^0,10^{0.5},10^1,10^{1.5},10^2,10^{2.5},10^3\}.
$$

Smaller $$C$$ means stronger regularization in this convention. L1 can shrink coefficients to zero; L2 continuously shrinks them. No regularization is a distinct setting, not a meaningful additional value of $$C$$. Conceptually this gives 26 regularized combinations plus the unpenalized case, although exact software grids can include other fixed settings or duplicates.

LR is linear in the chosen predictors on the log-odds scale. It is nonlinear as a probability function but does not automatically learn arbitrary interactions among raw covariates. Model selection can improve the chosen fit within the search space; it cannot ensure that this space contains the true treatment-assignment mechanism.

### 9.2 Gradient-boosted model: GBM-PS

The paper uses LightGBM and searches:

| Hyperparameter | Candidate values |
| --- | --- |
| Maximum tree depth | 3, 4, 5 |
| Maximum leaves per tree | 5, 25, 45, 65, 85, 105 |
| Minimum samples per leaf | 200, 250, 300 |

These form 54 nominal grid combinations. Trees can express threshold effects and interactions without explicitly specifying products of covariates. The main Methods describe the GBM as having “random forest as base learners”; that wording should not be treated as a precise mathematical definition of gradient boosting. The implementation is based on LightGBM, and exact boosting mode, number of trees, learning rate, and other fixed options require the execution configuration.

### 9.3 Multilayer perceptron: MLP-PS

The searched hidden structures are **[32], [64], [128], [32, 32], [64, 64]**. A one-entry list denotes one hidden layer; a two-entry list denotes two. Learning rate is **$$10^{-3}$$ or $$10^{-4}$$**, and weight decay is **$$10^{-3},10^{-4},10^{-5},10^{-6}$$**. This gives 40 nominal combinations.

The paper reports **15 epochs** and **batch size 128**, using Adam for deep models. In the pinned `mlp.py`, hidden layers apply affine transformations, ReLU activations, and a configurable dropout module; the final layer outputs a logit. The presence of a dropout module does not establish a nonzero dropout rate in every experiment. [Pinned MLP implementation](https://github.com/calvin-zcx/RWD4Drug/blob/a783e8d86f60a3d9c7f7715419e90afb1cdb28c8/iptw/PSModels/mlp.py).

### 9.4 LSTM with temporal attention: LSTM-PS

The manuscript describes a **two-layered bidirectional LSTM**, searches hidden dimensions **64, 128, 256**, and uses the same two learning rates, four weight-decay values, 15 epochs, and batch size 128. The nominal grid contains 24 combinations. It follows the earlier implementation of Liu et al., cited by the paper.

The inspected code provides a more concrete view: diagnosis and medication sequences have separate linear embeddings and separate bidirectional LSTM encoders. Each produces a temporal sequence of hidden states. A linear layer followed by `tanh` gives an attention score at each position, masked normalization gives temporal weights, and the weighted hidden-state sum is concatenated with sex, age, and MCI-to-index time. A ReLU hidden layer and a final linear layer produce the treatment logit.

For one stream, an explanatory representation is:

$$
h_t=\operatorname{BiLSTM}(E x_{1:L})_t,\qquad
a_t=\tanh(v^\top h_t+b),\qquad
\alpha_t=\frac{m_t e^{a_t}}{\sum_s m_s e^{a_s}+\epsilon},
$$

$$
r=\sum_t\alpha_t h_t.
$$

Here $$m_t$$ masks empty/padded positions. Diagnosis and medication representations are concatenated before the final treatment-prediction head. Attention summarizes the pretreatment record; it is not an estimate of a covariate's causal effect.

**Source discrepancy:** the pinned code constructs two separate `nn.LSTM` modules without setting `num_layers`, so each uses the one-layer default. That differs from a literal reading of “two-layered” as two stacked recurrent layers per stream. The note preserves both observations and does not claim that the manuscript's architecture description and this code path are identical. [Main p. 11; pinned LSTM implementation](https://github.com/calvin-zcx/RWD4Drug/blob/a783e8d86f60a3d9c7f7715419e90afb1cdb28c8/iptw/PSModels/lstm.py).

### 9.5 The LSTM balance representation also deserves attention

Supplementary Table S2 states that the LSTM-based approach summarizes diagnosis and medication sequences by **normalized temporal attention learned from training data** when computing balance. The code returns both the hidden representation and attention-weighted original code vectors.

This matters because comparing SMDs of fixed binary history indicators with SMDs of learned attention-weighted histories is not exactly the same diagnostic target. A model may balance its selected representation without balancing every raw occurrence pattern or clinically important feature. The paper itself criticizes the earlier LSTM approach's SMD estimation. A strong follow-up comparison should assess all candidate propensity models on a common, prespecified set of raw clinical covariates as well as any model-specific summaries.

The reported result is therefore appropriately phrased as **regularized LR performed best under the studied representations, tuning grids, data sources, and balance criteria**. It is not a universal theorem that linear propensity models dominate deep learning.

## 10. Stabilized IPTW, clipping, and overlap
{: #weights }

### 10.1 Deriving the treatment weights

With $$\widehat\pi=P_n(Z=1)$$, the empirical treated fraction of an assembled dataset, the stabilized treatment weight is:

$$
w_i=Z_i\frac{\widehat\pi}{\widehat e(X_i)}
 +(1-Z_i)\frac{1-\widehat\pi}{1-\widehat e(X_i)}.
$$

For treated people, use the probability of treatment; for controls, use the probability of the alternative. The numerator is the **marginal** group probability, while the denominator is conditional on baseline information. If the sampled ratio is exactly 1:3, $$\widehat\pi=0.25$$; it is not automatically 0.5.

A teaching example makes the arithmetic concrete. With $$\widehat\pi=0.25$$, a treated patient with $$\widehat e=0.10$$ receives $$0.25/0.10=2.5$$. A control patient with $$\widehat e=0.10$$ receives $$0.75/0.90\approx0.833$$. The first person's observed action is relatively unusual given the model, so the record represents more similar people taking that action.

Under correct propensity modeling, exchangeability, and positivity, weighting can make measured baseline distributions comparable. It does not change actual prescriptions, create observations of both potential outcomes, or add independent people. The effective precision depends on the distribution of weights, not simply their sum.

### 10.2 Stabilization does not fix positivity violations

If $$\widehat e$$ approaches zero for a treated person or one for a control, the weight can still be large. Multiplying by a marginal probability does not create missing comparison patients. Strong predictors of drug choice, uncommon indications, and restrictive eligibility may leave regions with little common support.

Useful diagnostics include propensity-score overlap, weight percentiles and maxima, and effective sample size:

$$
\operatorname{ESS}=\frac{(\sum_i w_i)^2}{\sum_i w_i^2}.
$$

This ESS formula is a teaching diagnostic, not an additional reported result. It should be calculated separately by arm as well as overall when auditing a comparison. Good mean balance can coexist with a small effective sample size.

### 10.3 What does “trim the extreme 1%” mean here?

The paper says it trims the smallest and largest 1% of weights, but does not fully distinguish deleting records from clipping their weights. Those operations have different consequences. Deleting patients changes the analyzed population; clipping retains records but replaces their influence, potentially trading reduced variance for residual bias.

The pinned `evaluation.py` implements **pooled percentile clipping**. It calculates the first and 99th percentiles across both arms, then applies:

$$
\widetilde w_i=\min\{q_{0.99},\max(q_{0.01},w_i)\}.
$$

It also includes fallback rules: if the upper quantile exceeds 50, it uses the 80th percentile instead; if the lower quantile is at most $$10^{-6}$$, it uses the 20th percentile. Infinite weights are set to zero before these operations. A different file, `evaluation_revise.py`, uses fixed clipping bounds. These details make exact script selection consequential. The simple percentile expression above describes the normal branch of the inspected function, not every execution path. [Pinned weight function](https://github.com/calvin-zcx/RWD4Drug/blob/a783e8d86f60a3d9c7f7715419e90afb1cdb28c8/iptw/evaluation.py#L937).

Clipping is not a proof of adequate overlap. After any clipping, balance must be reassessed using the **actual weights used in the outcome analysis**. A reproduction should report how often fallback rules are triggered and compare conclusions across reasonable clipping choices; those frequencies are not given in the manuscript.

## 11. Balance diagnostics: SMDs and the trial-level threshold
{: #balance }

### 11.1 Standardized mean difference

For baseline covariate $$j$$, the paper uses:

$$
\operatorname{SMD}_j=
\frac{\lvert\mu_{1j}-\mu_{0j}\rvert}
{\sqrt{(s_{1j}^2+s_{0j}^2)/2}}.
$$

It measures the absolute between-arm mean difference relative to variability. For a binary code indicator, the mean is a prevalence. SMD is not an outcome effect, a hypothesis-test p-value, or evidence that unmeasured covariates are balanced.

After weighting, means and variances are computed within each arm using the weights. Writing the paper's variance expression explicitly as a variance avoids its ambiguous $$s_{\mathrm{weight}}$$ symbol:

$$
\mu_w=\frac{\sum_i w_i x_i}{\sum_i w_i},\qquad
s_w^2=\frac{\sum_i w_i}{(\sum_i w_i)^2-\sum_i w_i^2}
\sum_i w_i(x_i-\mu_w)^2.
$$

These expressions apply separately to every covariate in each group, and the weighted means/variances enter the SMD formula. Degenerate covariates with zero variance need a documented software rule; the printed formula alone does not specify all such edge cases. [Main Eqs. 2–4, p. 12.](https://www.nature.com/articles/s41467-023-43929-1)

### 11.2 From one covariate to one “balanced trial”

A covariate passes if $$\operatorname{SMD}_j\le0.1$$. The number failing after weighting is:

$$
U=\sum_{j=1}^{D}\mathbf 1[\operatorname{SMD}_{w,j}>0.1].
$$

An emulation passes the overall balance gate when:

$$
U\le0.02D.
$$

With $$D=267$$, this permits at most **five** failing covariates, since $$0.02\times267=5.34$$ and $$U$$ is an integer. Thus “balanced” does not mean all 267 covariates meet the threshold. It also does not distinguish whether the remaining imbalance concerns weak outcome predictors or a very important prognostic factor. A sensitivity analysis uses a stricter criterion with no unbalanced covariates.

For one drug with $$R=100$$ emulations, the balancing success rate is:

$$
\widehat P_{\mathrm{balance}}=
\frac1R\sum_{r=1}^{R}\mathbf1[U_r\le0.02D].
$$

This is a fraction of comparator emulations satisfying a diagnostic rule. It is not the probability that the drug is effective or that an effect estimate is unbiased.

### 11.3 Why SMD success is necessary but not sufficient

Mean balance does not guarantee balance of interactions, tails, longitudinal trajectories, or unobserved severity. A few remaining unbalanced outcome predictors can matter more than many balanced weak predictors. Moreover, a restrictive comparator pool can produce limited overlap that clipping masks in a simple mean comparison. The paper explicitly acknowledges that good SMD performance is insufficient to establish low bias.

## 12. The exact model-selection algorithm in Boxes 1–2
{: #selection }

This is the central methodological contribution. There are **two nested meanings of training versus validation**, and confusing them changes the method.

### 12.1 Outer 80:20 split

Within each emulation, patients/records are randomly partitioned into an 80% training portion and a held-out 20% test portion. The 80% portion is used to select hyperparameters and fit the selected propensity model. The 20% portion evaluates how that model behaves on unseen records.

This test set is not MarketScan. MarketScan is a **separate database-level replication source**, within which the same within-emulation splitting can occur. Likewise, a validation fold inside cross-validation is not the outer test set.

### 12.2 Tenfold cross-validation inside the 80%

For each candidate hyperparameter setting $$\theta$$:

1. Divide the 80% training portion into ten folds.
2. Fit the candidate on nine folds using treatment cross-entropy.
3. Use this fold-specific model to predict propensity scores on the **entire 80% portion**, including both the nine fitting folds and the held-out validation fold.
4. Calculate stabilized weights and weighted SMDs on that combined 80%, then count failing covariates.
5. Calculate treatment-prediction AUC on **only the held-out validation fold**.
6. Repeat over all ten folds and average the balance count and validation AUC.

With $$U_{\theta k}$$ the failing-covariate count on the combined inner data and $$A_{\theta k}$$ validation AUC:

$$
\overline U_\theta=\frac1{10}\sum_{k=1}^{10}U_{\theta k},
\qquad
\overline A_\theta=\frac1{10}\sum_{k=1}^{10}A_{\theta k}.
$$

Choose the configuration with the **smallest** $$\overline U_\theta$$. Only if balance counts tie, prefer the **largest** $$\overline A_\theta$$. This is lexicographic selection, not a weighted sum of balance and AUC.

```text
best_balance = infinity
best_auc = -infinity
for each hyperparameter configuration:
    for each of 10 validation folds:
        fit propensity model on the other 9 folds
        assess weighted balance on all 10 folds together
        assess treatment AUC on the held-out fold only
    average the two diagnostics across folds
    keep the smallest average imbalance count
    use average held-out AUC only to break a tie
refit the winning configuration on the entire 80% training portion
```

This pseudocode explains Box 1. Outcomes are not used to choose a favorable drug effect at this stage. The design intentionally evaluates balance partly on records used to fit each candidate because the final weighted analysis includes such records. [Boxes 1–2, main p. 4; Methods, p. 12.](https://www.nature.com/articles/s41467-023-43929-1)

### 12.3 Refit and evaluate the three populations

After choosing hyperparameters, refit the model on all of the 80% training portion. Box 2 then assesses balance using that fitted model on:

| Evaluation population | What it checks |
| --- | --- |
| The 80% training portion | Balance among records used to fit the final propensity model |
| The held-out 20% | Balance on unseen records |
| The combined 100% | Balance of the full assembled emulation used for overall assessment |

The point is not that test-set balance is unimportant. The authors find that selecting only for validation AUC or cross-entropy can improve some test metrics while leaving poorer balance in the larger training portion, yielding poorer balance in the combined analysis. Their proposed criterion aims to improve that combined balance.

### 12.4 This is not cross-fitting

Cross-fitting would give each person's nuisance prediction from a model fitted without that person, usually combining out-of-fold predictions across all records. Here Box 1 refits on the whole 80%, and Box 2 applies that model to both training and test data. Predictions for the 80% are therefore in-sample.

Classical propensity-score adjustment does not inherently require a train/test split, and using the same baseline treatment data to fit a PS model and construct weights is not automatically forbidden leakage. The relevant concerns are overfitting, calibration, positivity, bias, and valid inference. What is inappropriate is calling this algorithm out-of-fold cross-fitting or assuming predictive held-out performance alone proves causal validity.

### 12.5 Benchmarks and the nested-CV sensitivity analysis

The alternatives select models by validation AUC or validation cross-entropy alone. Comparisons are conducted within LR, GBM, MLP, and LSTM classes. Figure 2 shows LR balance performance, while supplement figures cover the other classes and MarketScan. The figure displays drugs with at least 10% balanced repetitions, uses 1,000 bootstrap repetitions for plotted intervals, and uses two-sided Welch tests to compare means of binary balance-success indicators.

A separate sensitivity analysis uses **10 outer folds and 5 inner folds**. This distinguishes evaluating the whole selection procedure from evaluating a configuration chosen within one split. Similar balance conclusions were reported. It does not eliminate uncertainty due to repeated patient reuse across comparator emulations or make the downstream causal assumptions unnecessary.

## 13. Weighted Cox and Kaplan–Meier outcome analyses
{: #survival }

### 13.1 The propensity model supplies weights, not outcome predictions

For every adequately balanced emulation, the selected LR-PS model supplies stabilized weights for survival analysis. The main reported effect measure is the **adjusted hazard ratio**, estimated using a weighted Cox proportional-hazards model, with a Wald chi-square test within an emulation.

An explanatory marginal structural Cox form is:

$$
\lambda^z(t)=\lambda_0(t)\exp(\beta z),\qquad
\mathrm{HR}=e^\beta.
$$

An illustrative weighted partial log-likelihood, ignoring tie-handling details, is:

$$
\ell_w(\beta)=\sum_{i:\Delta_i=1}w_i
\left[\beta Z_i-\log\left\{\sum_{j\in\mathcal R(T_i)}w_j e^{\beta Z_j}\right\}\right].
$$

The risk set $$\mathcal R(T_i)$$ contains people still observed and AD-event-free just before that event time. Weights affect both event contributions and the composition of the risk set. The equation is explanatory; the actual estimator and tie handling follow the survival software. The inspected implementation fits treatment-only weighted Cox with `robust=True`, which requests robust variance estimation. That still does not by itself account for uncertainty from all propensity-model selection and repeated-emulation stages.

### 13.2 HR is not a five-year risk ratio

An HR of 0.80 summarizes a relative instantaneous AD-diagnosis rate under the model among those remaining event-free. It does not say that five-year cumulative AD risk is reduced by exactly 20%, nor that every individual's risk changes by that amount. Hazards compare evolving survivor groups, and a constant HR additionally relies on the proportional-hazards working assumption.

The paper uses the phrase “five-year risk” when reporting HRs. The precise interpretation is **a hazard-ratio estimate from follow-up administratively limited to five years**. A risk difference or risk ratio requires an estimated cumulative event probability at a specified horizon.

### 13.3 Weighted Kaplan–Meier survival differences

The paper also uses an adjusted Kaplan–Meier estimator. For group $$z$$, an explanatory weighted curve is:

$$
\widehat S_z(t)=\prod_{u\le t}
\left[1-\frac{\sum_{i:Z_i=z}w_i\mathbf1(T_i=u,\Delta_i=1)}
{\sum_{i:Z_i=z}w_i\mathbf1(T_i\ge u)}\right].
$$

At a horizon $$\tau$$, the **AD-free survival difference** is:

$$
\mathrm{SD}(\tau)=\widehat S_1(\tau)-\widehat S_0(\tau).
$$

Positive SD means higher estimated AD-free survival under target initiation. If the outcome framework supports defining risk as $$1-S_z(\tau)$$, the corresponding AD risk difference is:

$$
\mathrm{RD}(\tau)=\{1-\widehat S_1(\tau)\}-\{1-\widehat S_0(\tau)\}
=-\mathrm{SD}(\tau).
$$

The signs are opposite. With competing death, $$1-\mathrm{KM}$$ does not automatically equal the real-world cumulative incidence of AD, so that interpretation needs additional care. Detailed survival-difference results appear in Supplementary Tables S5–S6; several headings in the five-year table retain two-year wording, making the table title and footnote necessary context.

### 13.4 The paper's criticism of a naive ATE should be read narrowly

The authors contrast their survival analysis with earlier use of $$E[Y^1-Y^0]$$ and warn about censoring. The problem is **not the risk-difference estimand itself**. At a fixed horizon, an average treatment effect on the binary event indicator is a valid risk difference when identified and estimated appropriately.

The problem is treating incomplete follow-up as a known negative outcome, or analyzing only complete cases without addressing the selection mechanism. Survival-based standardization or suitable censoring-adjusted methods can estimate fixed-horizon causal risks and their difference. The present study chooses HRs and survival differences rather than a naive complete-outcome mean difference. [Main “Statistical analysis” and “Comparison with existing works,” p. 12.](https://www.nature.com/articles/s41467-023-43929-1)

## 14. Aggregation, bootstrap inference, screening, and multiplicity
{: #screening }

### 14.1 Only balanced emulations enter the reported drug summaries

For drug $$m$$ in source $$s$$, let $$\mathcal B_{ms}$$ index emulations satisfying the balance rule. The paper reports sample means of outcome estimates over that set. For HRs, the corresponding explanatory notation is:

$$
\overline{\mathrm{HR}}_{ms}=
\frac1{\lvert\mathcal B_{ms}\rvert}\sum_{r\in\mathcal B_{ms}}\widehat{\mathrm{HR}}_{msr}.
$$

This is a mean of fitted HRs, not a pooled patient-level Cox model, a random-effects meta-analysis, or necessarily the exponentiated mean log-HR. The paper does not present it as a formally identified common marginal causal parameter across all comparator mixtures.

The Methods specify **1,000 bootstrap repetitions** for 95% intervals around these drug-level summary means and bootstrap hypothesis testing of whether mean adjusted HR is below one. Within-emulation Cox Wald p-values and across-emulation bootstrap p-values are different quantities.

Because treatment patients and some comparison records recur, bootstrap resampling of emulation estimates describes variation across the chosen emulations under that procedure. It should not automatically be interpreted as full patient-sampling uncertainty from independent studies. A comprehensive uncertainty analysis would need to consider patient reuse, comparator sampling, PS fitting and selection, and the balance filter. The article does not establish that all these sources are propagated by its reported bootstrap.

### 14.2 Screening criteria

The screening paragraph specifies:

1. At least **10%** of a drug's 100 emulations must be successfully balanced.
2. Adjusted HRs must indicate a decrease relative to one.
3. The drug-level bootstrap p-value must be below the corrected threshold.
4. The significant decreased association must be observed in **both databases**.
5. Candidates are ranked by estimated adjusted HR.

The exact wording says “the adjusted hazard ratios from all the balanced trials smaller than 1,” while the statistical-analysis paragraph defines a mean-HR bootstrap test. It is ambiguous whether this is intended as a literal requirement that every retained repetition have HR below one, or a statement about the aggregated estimates. The inclusion of fluticasone despite a same-class OneFlorida summary above one makes a strict every-repetition interpretation difficult to reconcile with the displayed results. These notes therefore distinguish the **unambiguous mean-HR significance and cross-source replication rules** from that unresolved wording.

### 14.3 What is the Bonferroni denominator?

The reported threshold is:

$$
\alpha_{\mathrm{screen}}=\frac{0.05}{312}
\approx1.6\times10^{-4},\qquad312=66+246.
$$

The denominator is the number of retained **database-specific drug analyses**, not the number of patients, folds, or approximately 430,000 broad emulations. It also is not necessarily 312 globally distinct molecules because the sources share drugs.

Bonferroni bounds the familywise error rate without requiring independence **when its individual p-values are valid for the specified family**. It does not fix confounding, an invalid bootstrap, post-selection inference, or undisclosed expansion of the hypothesis family. Repeated comparator analyses are inputs to the drug-level summary; multiplying the denominator by every repetition would answer a different testing-family question.

The filter based on balance is outcome-blind, whereas selecting reduced HRs, significant p-values, replication, and top-ranked effect sizes uses the outcomes. The same observed estimates determine which candidates are highlighted, creating potential winner's-curse exaggeration. Independent confirmatory evaluation remains valuable even after cross-source screening. Requiring significance in both databases is stronger than selecting in one source alone, but the final drug list is still selected using both sets of results.

## 15. The five candidates and what cross-database replication means
{: #results }

The primary analysis highlights the following mean adjusted HR summaries from balanced emulations, with the paper's 95% bootstrap intervals:

| Candidate | OneFlorida aHR (95% CI) | MarketScan aHR (95% CI) |
| --- | --- | --- |
| Pantoprazole | 0.81 (0.80–0.83) | 0.94 (0.92–0.96) |
| Gabapentin | 0.76 (0.73–0.77) | 0.79 (0.77–0.81) |
| Atorvastatin | 0.74 (0.73–0.76) | 0.92 (0.90–0.94) |
| Fluticasone | 0.92 (0.89–0.95) | 0.86 (0.84–0.87) |
| Omeprazole | 0.86 (0.84–0.88) | 0.91 (0.89–0.94) |

These are reported associations with AD diagnosis among the eligible, MCI-coded populations, using a five-year maximum follow-up. They should not be converted into treatment recommendations or described as proven disease-modifying effects. The study does not evaluate every candidate's safety, optimal dose, route, or net benefit for an MCI prevention population. [Main Figure 3 and pp. 6–7.](https://www.nature.com/articles/s41467-023-43929-1#Fig3)

<figure>
  <a href="{{ '/assets/rwe/high-throughput-ad/figure-3-drug-candidates.png' | relative_url }}"><img src="{{ '/assets/rwe/high-throughput-ad/figure-3-drug-candidates.png' | relative_url }}" alt="Original forest plots comparing five candidate drugs across OneFlorida and MarketScan with pooled, random-drug, and same-class comparator analyses" loading="lazy"></a>
  <figcaption>Figure 3 from Zang et al. (2023), cropped from the supplied PDF. “All” combines results from balanced random-comparator and same-class emulations; it is not an additional independent cohort. Narrow intervals summarize the published bootstrap procedure and must be interpreted with repeated patient reuse in mind. Reproduced under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; scientific content unchanged.</figcaption>
</figure>

Replication does not require identical effect sizes: pantoprazole and atorvastatin have smaller apparent associations in MarketScan than OneFlorida. This can reflect different populations, comparator composition, prescribing, measurement, residual confounding, or true heterogeneity. A common direction across sources is informative, but shared biases can also replicate.

The authors supplement the observational screen with rapid literature reviews. That contextualizes plausibility and prior findings; it is not part of the propensity-score adjustment and does not turn the observed association into causal confirmation. The note preserves the study's 2023 findings rather than presenting a current clinical assessment of these medications.

## 16. Sensitivity analyses and causal-discovery adjustment
{: #sensitivity }

### 16.1 Separate the two comparator families

The primary “All” result summarizes both random and same-class emulations; sensitivity analyses summarize each separately. Most directions were consistent, but **fluticasone in OneFlorida** is an important exception:

- Random comparators: aHR **0.84 (0.80–0.87)**.
- Same-class comparators: aHR **1.02 (1.00–1.04)**, described by the authors as nonsignificant.
- Combined result: aHR **0.92 (0.89–0.95)**.

This example shows why the comparator is part of the scientific question. A combined favorable result does not show benefit against every clinically relevant alternative. It also motivates reading the screening language about “all balanced trials” cautiously.

### 16.2 Knowledge-guided and graph-guided covariates

The sensitivity analysis first identifies likely AD risk factors using existing knowledge: age, gender, hypertension, hyperlipidemia, obesity, diabetes, heart failure, stroke, ischemic heart disease, traumatic brain injury, anxiety, sleep disorders, alcohol-use disorders, menopause, and periodontitis. It then applies the **stable PC algorithm**, implemented in `gcastle 1.0.3`, to each emulation.

The supplement states three prior constraints:

1. Age and gender have direct edges to both treatment and outcome.
2. Other covariates cannot point into age or gender.
3. Treatment cannot point into covariates measured before treatment initiation.

The authors use Fisher-z conditional-independence tests with a corrected significance level **$$2.9\times10^{-4}$$**, and separately examine **0.05**. They identify variables labeled as colliders, M-colliders, or mediators in inferred graphs and exclude them from adjustment. [Supplementary Method, p. 42; example graphs, pp. 43–54.](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-43929-1/MediaObjects/41467_2023_43929_MOESM1_ESM.pdf#page=42)

This should be understood as a **sensitivity analysis under learned graph assumptions**. Conditional-independence discovery depends on measurement, sample size, faithfulness, causal sufficiency or the algorithm's assumptions, and the supplied direction constraints. Fisher-z tests also require care when applied to many binary code variables. Removing a variable because an estimated graph labels it “bad” is not equivalent to expert confirmation of its causal role.

There are two source ambiguities worth retaining. The supplement prints its Bonferroni expression as `0.05/(k*(k-1))/2`, which is not algebraically the same as dividing by the number of unordered pairs, `0.05/(k*(k-1)/2)`. The stated numeric threshold is the clear reported setting. Also, example captions call some baseline conditions “mediators” despite the stated prohibition on treatment-to-baseline edges. A pretreatment condition cannot mediate the effect of a later initiation; it could mediate another relationship in the graph. The exact relationship being labeled requires graph-level inspection rather than a blanket removal rule.

### 16.3 What changed with the alternative adjustment set?

The five highlighted candidates retain generally similar directions. **Albuterol** becomes an additional candidate: with the graph-guided covariates, aHR is **0.85 (0.83–0.88)** in OneFlorida and **0.75 (0.73–0.76)** in MarketScan. In the primary analysis it is **1.09 (1.07–1.10)** in OneFlorida and **0.72 (0.71–0.73)** in MarketScan.

That direction change in OneFlorida is not merely a robustness success. It shows material sensitivity to adjustment choice. Without knowing the true graph, the analysis cannot determine solely from these results which adjustment set gives the less biased albuterol estimate.

### 16.4 Shorter follow-up

At a two-year horizon the authors report replication of the five main candidates and additionally albuterol: **0.80 (0.79–0.82)** in OneFlorida and **0.78 (0.75–0.80)** in MarketScan. Changing the horizon changes which events and censoring patterns enter the analysis; it can also change a Cox summary when hazards are not proportional.

Cross-source disagreement remains possible. The Discussion gives escitalopram at two years as **0.70 (0.63–0.79)** in OneFlorida versus **1.56 (1.49–1.62)** in MarketScan. The workflow is capable of exposing such instability, which is one reason not to screen from only one favorable database.

### 16.5 What was not a completed sensitivity analysis?

The paper discusses negative-control approaches, more explicit informative-censoring models, time-varying per-protocol analyses, ensembles, and additional databases as future directions. It does not report a completed negative-control calibration demonstrating absence of residual bias. Those proposed extensions should not be listed as if they were performed.

## 17. Simulation design, estimands, and limitations
{: #simulations }

The real data have no known true causal effect. Simulations therefore test whether improved SMD selection can also improve estimation under constructed mechanisms. The study uses 267 covariates to resemble the dimensionality of its clinical representation.

### 17.1 Covariate distributions

The reported generation rules are:

$$
X_1,X_3\sim\operatorname{Bernoulli}(0.5),\qquad
X_2\mid X_1\sim\operatorname{Bernoulli}(0.3+0.1X_1),
$$

$$
X_4,X_6\sim N(0,1),\qquad
X_5=0.3+0.1X_6+\epsilon,\quad\epsilon\sim N(0,1),
$$

$$
X_7,\ldots,X_{11}\sim\operatorname{Bernoulli}(0.4),\qquad
X_{12},\ldots,X_{267}\sim\operatorname{Bernoulli}(0.2).
$$

### 17.2 Treatment-assignment mechanisms

For the linear mechanism, $$Z\sim\operatorname{Bernoulli}\{\operatorname{expit}(\eta_L)\}$$ with:

$$
\eta_L=-6.84+\log(2)X_2+\log(3)X_3
+\log(2)X_5+\log(2)X_6
+\sum_{k=7}^{11}\log(1.5)X_k
+\sum_{k=12}^{267}\log(1.1)X_k.
$$

For the nonlinear mechanism, replace that predictor with:

$$
\eta_N=-5.72+\log(2)X_2^2X_1+\log(3)X_3X_2X_1
+\log(2)X_5X_1+\log(2)X_6X_1
+\sum_{k=7}^{11}\log(1.5)X_kX_1
+\sum_{k=12}^{267}\log(1.1)X_k.
$$

The nonlinear mechanism includes interactions that an unaugmented linear predictor does not generally represent. Because $$X_2$$ is binary, its squared term equals itself, but its interaction with $$X_1$$ can still matter.

### 17.3 Survival generation and the true HR

Let $$U\sim\operatorname{Uniform}(0,1)$$ and define:

$$
\eta_Y=-5.67-Z+\log(1.8)X_1+\log(1.8)X_2
+\log(1.8)X_4+\log(2.3)X_5^2
+\sum_{k=7}^{11}\log(1.5)X_k
+\sum_{k=12}^{267}\log(1.1)X_k.
$$

The event time is generated as:

$$
T=100\left\{\frac{-\log U}{\exp(\eta_Y)}\right\}^{1/2},
$$

and administratively censored at 200, with no other censoring mechanism. This is a Weibull-based proportional-hazards construction conditional on the covariates. The coefficient of $$Z$$ gives a conditional HR of $$e^{-1}\approx0.368$$. The study targets a **marginal** Cox HR, which need not equal that conditional coefficient because HRs are noncollapsible and marginal hazards mix different risk profiles.

The authors generate one million records with both potential outcomes, fit a Cox model following the cited procedure, and use **0.578** as the ground-truth marginal HR for both assignment mechanisms. This is a simulation-defined Cox summary, not a known clinical drug effect. Marginal proportional hazards also do not follow automatically from conditional proportional hazards under arbitrary mixing.

### 17.4 Scenarios and evaluation

The grid crosses five sample sizes (**3,000; 3,500; 4,000; 4,500; 5,000**), two assignment mechanisms, and correctly versus incorrectly specified estimation, for **20 scenarios**. Each is repeated **100 times** with different seeds. The same 80:20 split, tenfold selection, LR regularization grid, and comparison against validation-AUC and validation-loss selection are used.

Evaluation covers balance success, failing-covariate counts, estimated marginal HR, empirical variability, bias, mean squared error, and interval coverage. The paper reports better balance and favorable bias/MSE/coverage for its selection strategy in these settings. Those results support the method under the chosen mechanisms; they do not test arbitrary unmeasured confounding, competing death, informative censoring, nonproportional outcomes, or every clinically plausible treatment process.

### 17.5 Two details that limit how the simulation should be read

First, the stated misspecified **linear** predictor replaces $$X_1,X_2,X_3$$ by their squares while retaining other variables. All three are binary under the same Methods, so $$X_j^2=X_j$$. As written, that transformation does not create the advertised linear-model misspecification. The nonlinear misspecification—using raw covariates without the stated interactions—is substantively different. This apparent inconsistency should be resolved from the exact simulation script before reproducing the claims.

Second, the paper defines an **oracle** standard deviation from HR estimates across the repeated simulations and uses intervals $$\widehat\psi_b\pm1.96\sigma$$ to assess coverage. Such an empirical across-repetition standard deviation is not available to an analyst with one real dataset. Its coverage measures a particular simulation diagnostic, not automatically the calibration of the complete practical bootstrap/Wald procedure used for one observational study. [Main p. 13, Eqs. 6–8; Supplementary Figures S8–S10 and Table S7.](https://www.nature.com/articles/s41467-023-43929-1)

## 18. Causal assumptions and the remaining threats
{: #limitations }

### 18.1 Exchangeability is assumed, not demonstrated by balance

A causal initiation contrast requires sufficiently rich baseline information so that, conditional on it, treatment choice does not depend on potential outcomes. In this setting important unmeasured factors may include cognitive severity, functional status, socioeconomic circumstances, healthcare access, prescribing indication and severity, frailty, adherence propensity, and prodromal symptoms.

Measured balance is evidence about measured variables. It cannot show that people with and without a prescription have the same underlying disease trajectory. The broad MCI algorithm and lack of detailed cognition make this limitation particularly relevant.

### 18.2 Positivity and the target population

Both treatment strategies must be possible at the relevant baseline profiles. A gastrointestinal medication versus a heterogeneous random-drug pool can have weak clinical overlap even if a flexible model predicts the exposure well. Excluding poorly balanced emulations selects comparisons where adjustment succeeds by the chosen rule; the resulting results pertain to that selected set of comparisons.

Clipping can stabilize estimation but also alter the weighting target. The paper does not explicitly define an overlap-population estimand that resolves every weight truncation choice. The target population of a screened mean HR deserves separate specification.

### 18.3 Time-related and selection biases

The two-prescription confirmation condition uses post-baseline information. A variable baseline-history length can produce differential measurement. Patients with more encounters are more likely to have both MCI and AD coded. A drug may influence encounter frequency, diagnostic workup, or symptom recognition without changing disease pathology. These pathways can affect the recorded endpoint.

Baseline exposure classification also ignores later switching, discontinuation, and concomitant target use unless an exclusion rule explicitly addresses them. That is consistent with an initiation-style analysis, but its interpretation differs from sustained treatment. Excluding controls according to future target use would instead introduce another post-baseline selection mechanism, which is why the temporal scope must be audited.

### 18.4 Censoring and competing events

Observation can end because of insurance changes, care outside the network, worsening health, death, or administrative limits. If those mechanisms relate to AD risk after accounting for modeled information, the noninformative-censoring assumption can fail. Baseline treatment weights do not correct those processes. A lower rate of recorded AD is not necessarily a better clinical outcome if, for example, competing mortality or loss of diagnostic observation differs.

### 18.5 Model selection and uncertainty

The proposed balance-first criterion is outcome-blind and useful, but it optimizes a coarse count of mean imbalances. It may favor different regularization for different clinical comparisons, and exact ranking can depend on the finite grid, folds, clipping, and baseline representation. Repeating comparisons increases computational evidence about those choices without increasing the number of independent treated patients by a factor of 100.

A favorable screen can reflect both true effects and residual bias. Multiplicity correction, cross-database agreement, and sensitivity analyses are useful safeguards against particular failures; none substitutes for a well-defined intervention, credible exchangeability, valid follow-up, and complete uncertainty accounting.

## 19. Reproducibility details and source discrepancies
{: #reproducibility }

### 19.1 Reported computing environment

The paper reports Python **3.9**, PyTorch **1.8**, Adam for deep-model training, **two GeForce RTX 2080 Ti GPUs** and **16 CPU cores**. The packages include `lifelines 0.26`, `scikit-learn 0.23`, `lightgbm 3.2`, and `gcastle 1.0.3`. The code is archived at [Zenodo DOI 10.5281/zenodo.10070359](https://doi.org/10.5281/zenodo.10070359). Raw patient-level data require appropriate access agreements; open code does not mean the clinical data are publicly downloadable.

### 19.2 Important facts supplied by the supplement or implementation

| Detail | Main paper alone | Additional source |
| --- | --- | --- |
| MCI/AD phenotype codes | Refers to supplementary definitions | Table S3 gives the exact codes and broad MCI alternatives |
| Target comparator size | Does not emphasize a fixed ratio | S2 footnote specifies three controls per treated person; actual pools can be smaller |
| LSTM balance variables | Describes temporal histories | S2 explains attention-weighted diagnosis/medication summaries |
| Graph constraints | Describes graph-guided adjustment | Supplement p. 42 specifies prior edge constraints and Fisher-z settings |
| Weight trimming | Extreme 1% wording | Inspected `evaluation.py` uses percentile clipping and conditional fallbacks |
| Cox variance | Refers to robust Cox literature | Inspected outcome function requests `robust=True` |
| Neural architecture | High-level MLP/LSTM descriptions | Pinned model files expose streams, activations, masking, and heads |

### 19.3 Issues that should not be silently harmonized

| Issue | Careful interpretation |
| --- | --- |
| Figure 1 uses `>50`/`>1 year`, whereas Methods/Table 1 use inclusive thresholds | Follow the explicit Methods: age at least 50 and baseline at least one year |
| Approximately 4,300 “unique drugs” | Ingredient entries are counted across two databases; primary screened sets are 66 and 246 |
| First prescription baseline plus later refill confirmation | Retain and evaluate the post-baseline selection concern |
| “All balanced HRs below one” versus mean-HR testing and fluticasone subgroup findings | Report the screening wording and its ambiguity separately from clear aggregate results |
| Weight “trimming” versus code clipping/fallback variants | Pin the execution path; do not assume deleting the top/bottom 1% of patients |
| “Two-layered” LSTM versus two separate default-one-layer encoders | Distinguish manuscript architecture from the inspected implementation |
| LSTM balance uses learned attention summaries | Do not imply every model's balance metric is calculated on identical raw features |
| Printed weighted $$s$$ expression is a variance expression | Use explicit $$s_w^2$$ notation in explanation |
| DAG correction parentheses and baseline “mediators” | Preserve the reported numeric threshold and flag causal/temporal interpretation |
| Squaring binary variables called linear misspecification | As written it does not change those inputs; verify the simulation code |
| Some five-year supplementary-table columns retain two-year labels | Use table-level titles and footnotes; avoid silently extracting a horizon from a stale column heading |

A full reproduction should record exact code revision and script, cohort and drug-mapping versions, eligibility logic, treatment washout, index dates, baseline windows, control-sampling seeds, deduplication within comparator pools, model grids and fixed settings, all weight rules, overlap/ESS, balance gate decisions, event and censoring definitions, proportional-hazards diagnostics, bootstrap resampling units, and the testing family. These notes identify the relevant points but do not claim to rerun restricted patient data or reconcile every implementation variant.

## 20. A complete worked workflow and related reading
{: #workflow }

For one target medication, the full methodological sequence is:

1. **Specify the question:** compare initiation of the target ingredient with the defined alternative-initiation strategy among eligible MCI-coded patients, with an explicit horizon and endpoint.
2. **Build initiation cohorts:** apply phenotype, age, history, dementia-exclusion, and observed-new-use rules; audit the later-prescription confirmation condition.
3. **Anchor each record:** assign its own initiation index date, collect only pretreatment information, and derive follow-up time and event/censoring status.
4. **Construct 100 comparator emulations:** 50 random-drug and 50 same-class comparisons, seeking the reported 3:1 control ratio while excluding target-group overlap.
5. **Assemble covariates:** 267 fixed baseline variables for the primary workflow, with temporal inputs for the neural comparator and a separate graph-guided sensitivity set.
6. **Fit/select the propensity model:** split 80:20, run inner tenfold fits, minimize combined-inner-data imbalance count, use held-out AUC to break ties, then refit on the 80%.
7. **Construct the actual analysis weights:** stabilize, apply the documented clipping rule, and assess train/test/combined balance and overlap.
8. **Apply the balance gate:** retain emulations with no more than 2% failing covariates; require at least 10% of repetitions to pass for drug-level consideration.
9. **Estimate outcomes:** fit weighted Cox and adjusted KM analyses, keeping hazard ratios distinct from survival/risk differences.
10. **Summarize and screen:** average balanced-emulation estimates, obtain the specified bootstrap summaries, apply the 0.05/312 threshold, and require decreased associations in both databases.
11. **Challenge the result:** separate comparator families, shorten the horizon, change adjustment assumptions, examine model-selection sensitivity, and assess what simulations do and do not validate.
12. **Interpret as a hypothesis:** define the more precise intervention and confirmatory study needed to distinguish a therapeutic effect from remaining design, measurement, and selection biases.

The most transferable lesson is the separation of three tasks: **define a credible comparison, estimate weights that balance relevant baseline information, and interpret outcome estimates under explicit assumptions**. Optimizing a treatment classifier addresses only part of the second task. A large number of emulations cannot compensate for ambiguity in the first or third.

Related notes: [Federated target trial emulation]({{ '/rwe/federated-target-trial-emulation/' | relative_url }}) explains collaboration across institutions; [EmulatRx and agentic trial design]({{ '/rwe/emulatrx-agentic-trial-design/' | relative_url }}) examines how automated design support changes the workflow. The broader [high-throughput and federated TTE study companion]({{ '/causal-inference/high-throughput-federated-tte/' | relative_url }}) connects these ideas to IPTW and causal-inference foundations.

**Primary sources:** [Zang et al., journal article](https://www.nature.com/articles/s41467-023-43929-1); [Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-43929-1/MediaObjects/41467_2023_43929_MOESM1_ESM.pdf); [archived code record](https://doi.org/10.5281/zenodo.10070359); [inspected GitHub revision](https://github.com/calvin-zcx/RWD4Drug/tree/a783e8d86f60a3d9c7f7715419e90afb1cdb28c8).
