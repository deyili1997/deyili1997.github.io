---
layout: post
title: "EmulatRx: Agentic Trial Design, Computable Protocols, and Causal Analysis"
description: "A detailed methodological reading of EmulatRx: trial knowledge graphs, computable phenotyping, cohort construction, target-trial alignment, propensity scores, survival analysis, protocol refinement, and human feedback."
permalink: /rwe/emulatrx-agentic-trial-design/
date: 2026-09-13 13:00:00 -0400
research_area: real-world-evidence
math: true
tags: [Method, Real-World Evidence, Target Trial Emulation, Causal Inference, AI Agents, Clinical Trial Design]
---

**Paper:** Haoyang Li, Weishen Pan, Suraj Rajendran, Chengxi Zang, and Fei Wang. *Empowering clinical trial design with agentic intelligence and real-world data*. **Nature Communications 17, 5501 (2026)**, published July 7, 2026. [Journal article](https://doi.org/10.1038/s41467-026-74501-2).

These notes explain the supplied 19-page article, with particular attention to its Methods, and cross-check the official Supplementary Information. Page references identify the main PDF unless explicitly marked “Supplement.” The emphasis is on **what the agents actually construct, how the statistical analysis is supposed to work, and which assumptions remain outside the automation**. Equations introduced for teaching are labeled as such; unspecified implementation choices are not filled in with invented settings.

EmulatRx connects language-model agents to clinical-trial registries, biomedical literature, EHR queries, and statistical software. Its central idea is to automate the repeated translation between a clinical question, a computable trial protocol, an available patient cohort, and an analysis report. This is an ambitious workflow contribution. Whether a resulting treatment-effect estimate is causally valid remains a separate question requiring an explicit target trial, defensible measurements, and appropriate analysis of the resulting data.

<nav class="table-of-contents" aria-label="Contents" markdown="1">

**Contents**

1. [What problem is EmulatRx solving?](#problem)
2. [Data, agents, tools, and control flow](#architecture)
3. [The target-trial contract that connects all stages](#target-trial)
4. [Trialist: from registry text to a clinical-trial knowledge graph](#trialist)
5. [Informatician: from a computable protocol to an analytical cohort](#informatician)
6. [Eligibility from clinical notes](#clinical-notes)
7. [Covariates, missingness, and clinical refinement](#covariates)
8. [Propensity scores, matching, weighting, and balance](#balancing)
9. [Time zero, immortal time, and clone–censor–weight](#time-zero)
10. [Survival models, effect measures, and double robustness](#effect-estimation)
11. [Clinician: literature grounding and agent meetings](#clinician)
12. [Subgroup exploration and eligibility-criterion attribution](#refinement)
13. [Adverse events and prospective sample-size planning](#safety-planning)
14. [Human feedback, PPO, and the reported DPO objective](#rlhf)
15. [Evaluation of retrieval, parsing, SQL, and clinical responses](#agent-evaluation)
16. [What the synthetic experiments test](#synthetic-evaluation)
17. [Three end-to-end showcases](#showcases)
18. [Selective refinement and the reliability of generated reports](#interpretation)
19. [Reproducibility: reported settings and missing specifications](#reproducibility)
20. [Source map and reading connections](#sources)

</nav>

## 1. What problem is EmulatRx solving?
{: #problem }

A written clinical protocol is not an executable observational study. Consider a rule that a patient must develop septic shock within a specified interval after ICU admission. The implementation must identify the admission event, define septic shock from available measurements, preserve the direction of the temporal relationship, decide what missing measurements imply, and ensure that follow-up starts at an appropriate common time. A language model that produces plausible SQL has addressed only part of this problem.

The paper describes five core tasks:

1. Extract and standardize information from existing trials and literature.
2. Generate a target-trial protocol.
3. Map its elements to EHR records and construct cohorts.
4. Run statistical and causal analyses.
5. Review and iteratively refine the design.

EmulatRx organizes these tasks as interactions among specialized agents, with a Supervisor coordinating the process. It aims to produce evidence useful for **clinical trial design**, including feasibility, choice of eligibility criteria, possible effect heterogeneity, and prospective sample-size assumptions. A real randomized trial need not already exist for every use: the workflow can also develop hypotheses from observational data. [Overview, pp. 1–3; Methods, pp. 11–16.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=1)

Three distinctions help interpret the contribution. First, the “Trial Simulator” is an interface to statistical and machine-learning tools; the real-data showcases are analyses of observed EHR cohorts, not experiments that randomize simulated patients. Second, the system can change its protocol while inspecting data and results. That makes it useful for exploration, but also makes the eventual inferential target and selection process important. Third, a coherent final report is a communication artifact, not independent verification that its treatment groups are exchangeable or that its confidence intervals account for all preceding choices.

The study therefore has at least three different success criteria: **operational correctness** of extraction and execution, **clinical plausibility** of the proposed design, and **statistical validity** of an effect estimate. Strong performance on one does not automatically establish the other two.

## 2. Data, agents, tools, and control flow
{: #architecture }

### 2.1 Data environments and model backends

The acute-care experiments use **MIMIC-IV**, described in the paper as more than 299,000 patients treated at Beth Israel Deaconess Medical Center in Boston during **2008–2019**. Its dense timestamps, physiological measurements, and clinical narratives support questions about rapidly changing ICU conditions. The chronic-disease experiments use the **INSIGHT Clinical Research Network**, with **5,532,428 patients**, five New York City health systems, and records from **January 2007 through December 2023**. INSIGHT provides longer longitudinal histories for conditions such as Alzheimer's and Parkinson's disease. These are source-database sizes, not numbers of participants in each emulation. [Data, p. 11.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=11)

The agent evaluation includes **20 curated trials**: ten acute-condition trials associated with MIMIC-IV and ten chronic-condition trials associated with INSIGHT. The registry knowledge graph contains **1,363 trials** covering septic shock, acute kidney injury, acute heart failure, and acute pulmonary edema. The 1,363-trial retrieval corpus and 20-trial agent-evaluation set are different units.

The compared LLM backends are **GPT-4o**, **Phi-4**, **DeepSeek-R1:14b**, and **Gemma-3:12b**. The abbreviated “DeepSeek-R1” in the results means the specified 14B backend; it should not be read as a comparison against every or the largest DeepSeek-R1 configuration. The main clinical showcases use GPT-4o. A role name such as “Clinician” specifies a prompt, tools, and workflow responsibility; it does not mean that a licensed clinician is answering every intermediate request.

### 2.2 The five roles

| Agent | Main input | Main work | Output or handoff |
| --- | --- | --- | --- |
| Supervisor | User objective and shared workflow state | Dispatch tasks, coordinate discussions, integrate results, decide whether to iterate or finish | Next task or final report |
| Trialist | Clinical question, registry records, related literature | Retrieve and normalize trial components; assemble a proposed protocol | Structured eligibility, strategies, outcomes, and trial metadata |
| Informatician | Protocol, database schema, standardized concepts | Generate SQL, retrieve records, add note-derived eligibility information, check data quality | Patient-level analytical dataframe and diagnostics |
| Clinician | Clinical question, missing-data issue, proposed design, or analysis report | Retrieve literature, suggest covariates or substitutions, interpret and review | Structured recommendations and proposed revisions |
| Statistician | Protocol and analytical dataframe | Select and execute balancing and outcome methods; explore subgroups, criteria, and feasibility | Effect estimates, diagnostics, sensitivity outputs, draft report |

Three major tools support these roles: a **trial retriever** over registry knowledge, **retrieval-augmented generation** over biomedical literature, and a **trial simulator** that exposes statistical libraries. The LLM decides what to request; executable software performs database operations and numerical estimation. Identical tools and data can therefore return identical estimates even when different language models propose the analysis.

### 2.3 Adaptive interactions within a predefined graph

The overview gives a typical sequence, Supervisor → Trialist → Informatician → Clinician → Statistician → Supervisor, but also permits feedback paths. Missing data can send the Informatician back to the Clinician. Poor balance can trigger discussion between the Statistician and Clinician. The Supervisor can organize a broader meeting.

The paper also explicitly says that **LangGraph enforces a predefined graph with directed transitions governed by logic**. These descriptions are compatible if “adaptive” means choosing among permitted routes in response to state, rather than inventing an unrestricted software workflow. Each agent combines role-specific LLM reasoning, memory, and executable tools. Conversation history and transformations are stored in a centralized serializable state object. An LLM response cache and fixed seeds for downstream statistical tools support replay. This helps reproduce a recorded run; it does not establish stability under different prompts, uncached generations, model versions, or database snapshots.

<figure>
  <a href="{{ '/assets/rwe/emulatrx/article-page-03-framework.png' | relative_url }}"><img src="{{ '/assets/rwe/emulatrx/article-page-03-framework.png' | relative_url }}" alt="Original article page 3 containing Figure 1: EmulatRx agents, tools, interaction paths, refinement capabilities, and an example report." width="1355" height="1800" loading="lazy"></a>
  <figcaption>Original article page 3, containing Figure 1, reproduced as an unchanged page rendering from Li et al. (2026). The figure distinguishes role-specific work, shared tools, interactions, and optional analysis capabilities. Click for the full-size page. The miniature example report is illustrative; use the main results tables and case descriptions for reported estimates.</figcaption>
</figure>

## 3. The target-trial contract that connects all stages
{: #target-trial }

The most useful way to understand the pipeline is as a series of translations of one scientific question. A protocol component should retain the same meaning when represented as text, a graph node, a concept set, a SQL condition, and an analytical variable. Losing meaning at any translation can change the study even if every program runs successfully.

The following table is an **explanatory target-trial checklist**, not a claim that the paper completely reports every field for every showcase.

| Component | Scientific definition required | What its EHR implementation must resolve |
| --- | --- | --- |
| Eligibility | Who could enter the hypothetical trial? | Codes, measurements, age rules, histories, temporal windows, missingness, repeated eligible encounters |
| Strategies | Which intervention is compared with which alternative? | Initiation, dose, duration, treatment versions, comparator exposure, grace periods, switching or adherence |
| Assignment | How would the strategies be assigned? | Observational treatment processes and measured confounders used for adjustment |
| Time zero | When do eligibility, strategy assignment, and follow-up align? | Diagnosis/admission/treatment timestamps and avoidance of future information at baseline |
| Outcomes | Which events count, and over what horizon? | Event algorithms, timestamps, composite construction, and competing events |
| Follow-up | When does observation end? | Event, administrative end, loss of observation, discharge, and any artificial censoring |
| Estimand | Which causal contrast and target population? | For example, risk difference at a fixed horizon versus a hazard-ratio parameter, and ATE versus ATT |
| Analysis | How is the contrast identified and estimated? | Models, weights, balance diagnostics, uncertainty estimation, and sensitivity analyses |

For notation used below, let $$A$$ indicate treatment, $$X$$ denote baseline covariates, $$T$$ event time, and $$C$$ censoring time. The observed survival record is $$U=\min(T,C)$$ with event indicator $$\Delta=I(T\le C)$$. A possible causal risk estimand is

$$
\operatorname{RD}(\tau)=P(T^1\le\tau)-P(T^0\le\tau),
$$

where $$T^a$$ is the event time under strategy $$a$$. This pedagogical notation makes explicit that the target concerns counterfactual strategies, not simply observed treated and untreated labels.

Identification still requires assumptions such as sufficiently measured confounding, positivity, treatment consistency, and appropriate handling of censoring. A knowledge graph cannot establish these assumptions. Neither can a low standardized mean difference prove that unmeasured confounding is absent. The article invokes target-trial emulation and discusses key timing issues, but its main and supplementary reports do not provide a complete, auditable protocol-to-code specification for all these elements in every case.

## 4. Trialist: from registry text to a clinical-trial knowledge graph
{: #trialist }

### 4.1 Why a graph is useful here

A registry search can find trials mentioning a disease or drug. A more difficult query asks for trials of that drug in the disease **that exclude patients with a particular laboratory threshold**, perhaps with a minimum sample size. The exclusion is a logical and numerical statement buried in free text. EmulatRx preprocesses that information so that it can be queried as structured relations.

Its **Neo4j-backed knowledge graph** has three main node types:

- **Trial nodes:** study identifiers and metadata, including dates, sample size, phase, and baseline/follow-up information when available.
- **Component nodes:** eligibility criteria, treatment strategies, endpoints, and adverse-event information.
- **Clinical concept nodes:** normalized clinical entities that participate in those components.

A component also carries a design pattern and relevant logical, numerical, or temporal information. Edges encode relations between the trial, component, and concepts. This is a graph of **protocol information**, not a causal directed acyclic graph identifying confounding relations. [Trial information methods, pp. 12–13.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=12)

### 4.2 Extraction must preserve scope

The concept-extraction prompt builds on **Criteria2Query 3.0**. It identifies domains including demographics, conditions, devices, procedures, drugs, measurements, observations, and visits, together with values and temporal information. The prompt separates individual concepts and is augmented for compound statements and omitted concepts.

For example, an allergy statement listing several drugs must produce several complete allergy concepts. Extracting an isolated “allergy” plus independent drug names loses the scope that each drug is an allergen. Similarly, “patients under 18” implies the demographic variable age even if the word “age” is absent. These examples are small but consequential: the SQL generator cannot reliably recover a relation already lost during parsing.

The extraction stage therefore needs more than named-entity recognition. It needs the **entity, its role, the direction of the relation, its numerical restriction, and its temporal anchor**. A measurement concept without its comparison operator is not an eligibility rule; a time interval without an anchor does not identify a baseline window.

### 4.3 Normalization and temporal patterns

The pipeline uses **UMLS** and **OHDSI APIs** to reconcile synonyms such as ICU and intensive care unit. Criteria2Query normalization modules identify comparison operators, numbers, units, and temporal relations. Existing clinical-trial ontology design patterns represent the structured relation.

The paper lists ICD-9/ICD-10 for conditions, RxNorm for drugs, LOINC for measurements, and SNOMED CT for procedures while describing mapping into OMOP CDM concept identifiers. In practice, an implementation must distinguish source codes, standard concepts, and expanded concept sets; these labels alone do not provide the exact mapping tables or descendants included in a query.

Figure 5 uses a history of traumatic brain injury within three months before ICU admission. It separates the injury concept, the admission anchor, and the temporal relation. An explanatory translation is

$$
t_{\mathrm{admission}}-3\text{ months}\le t_{\mathrm{injury}}<t_{\mathrm{admission}},
$$

with the boundary convention requiring a protocol decision. If it is an exclusion criterion, finding a qualifying injury excludes the patient. Merely finding an injury at any point in the record would implement a different population restriction.

### 4.4 Retrieval and protocol assembly

Neo4j graph pattern matching combines structured metadata with normalized criteria. When several trials match, the Trialist can summarize how frequently particular criteria, strategies, or outcomes occur. Such frequency summaries can inform protocol construction, but a frequently used criterion is not automatically necessary or scientifically optimal. The article does not give a fully specified algorithm for converting those frequencies into a unique final protocol, resolving incompatible trial definitions, or deciding which historical trial is authoritative.

<figure>
  <a href="{{ '/assets/rwe/emulatrx/article-page-13-phenotyping.png' | relative_url }}"><img src="{{ '/assets/rwe/emulatrx/article-page-13-phenotyping.png' | relative_url }}" alt="Original article page 13 containing Figure 5: concept extraction, clinical and temporal normalization, and construction of a clinical-trial knowledge graph." width="1355" height="1800" loading="lazy"></a>
  <figcaption>Original article page 13, containing Figure 5, reproduced as an unchanged page rendering from Li et al. (2026). Read the pipeline as preservation of meaning across representations: text → concepts and modifiers → normalized component → graph. The colored annotations belong to the original figure. Click to enlarge.</figcaption>
</figure>

## 5. Informatician: from a computable protocol to an analytical cohort
{: #informatician }

### 5.1 SQL generation is a semantic translation task

The Informatician receives standardized trial information and the database schema. Each criterion becomes a **Common Table Expression (CTE)**, permitting modular query construction. Simple age restrictions become filters; compound conditions use nested logic and temporal joins. Treatment and outcome definitions must be translated alongside eligibility. [Dataframe construction, pp. 13–14.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=13)

An illustrative representation of inclusion and exclusion is

$$
\mathcal E=\left(\bigcap_j\mathcal I_j\right)\setminus\left(\bigcup_k\mathcal X_k\right),
$$

where $$\mathcal I_j$$ is the set satisfying inclusion rule $$j$$ and $$\mathcal X_k$$ the set meeting exclusion rule $$k$$. This is pedagogical, not the paper's SQL. Rules with explicit alternatives require their own internal unions; blindly intersecting every parsed concept would misread “either condition A or condition B.”

Temporal joins must also respect units of analysis. Joining all diagnoses to all admissions can duplicate a patient across unrelated encounters. Repeated admissions require a specified selection rule. A correct query must connect an event to the intended episode and maintain the required order relative to time zero. The article describes temporal handling but does not publish every episode-selection or tie-breaking rule in its prose Methods.

### 5.2 The analytical output

The dataframe includes patient identifiers, eligibility indicators, treatment indicators, time-to-event outcomes, and baseline covariates. Treatment extraction may involve administration records, dose schedules, and timing. Baseline covariates are described as coming from the **pre-intervention period**. Outcomes include endpoints such as 28-day mortality.

The intended temporal alignment is important, but “pre-intervention” and “baseline at a common eligibility time” are not interchangeable if treatment begins at different delays. For an untreated comparator, there is no observed intervention time to use automatically. The cohort construction and the subsequent timing strategy must jointly specify the reference time for both groups.

### 5.3 Quality assurance and execution boundaries

Checks cover completeness, logical consistency, and clinical plausibility. Examples include nonnegative outcome durations and missingness across important variables. Implausible values can lead to exclusion or imputation, depending on context. The Informatician can return to the Clinician for a substitute when a variable is insufficiently observed.

The paper states that **SQL generation sends database schema and protocol, not patient records, to the model**, and SQL executes locally behind the institutional firewall. This is a useful boundary for that route. The separate clinical-note pipeline subsequently supplies note content to models; the article does not fully describe the deployment and data-flow safeguards for every model involved in that route. One should not extend the SQL-specific claim into a blanket statement that no LLM ever processes patient-level information.

## 6. Eligibility from clinical notes
{: #clinical-notes }

Structured tables may not capture the history or nuance needed for a criterion. EmulatRx therefore adds a staged note-matching process rather than asking a large model to read every complete note immediately. [Methods, pp. 13–14.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=13)

1. **Keyword generation:** an LLM, with examples including Gemma 3 or Phi-4, generates terms, synonyms, and abbreviations from the inclusion and exclusion criteria.
2. **Prefiltering:** these terms select potentially relevant notes.
3. **Text preparation:** normalize text and expand abbreviations in criteria and candidate sentences.
4. **Semantic retrieval:** sentence embeddings, with S-PubMedBert given as an example, identify the snippets most relevant to each criterion.
5. **Natural-language inference:** a biomedical NLI model receives the snippet as premise and criterion as hypothesis, then predicts entailment, contradiction, or neutrality. Confidence thresholds determine whether a criterion is satisfied.
6. **Final review:** a general-purpose LLM considers the full note and complete criterion set before the patient is included.

The methods name example embedding/LLM families but do not give the exact NLI checkpoint, confidence thresholds, retrieval depth, or all inclusion/exclusion aggregation rules. Those settings materially affect the resulting cohort. In particular, **neutral evidence is not the same as evidence that an exclusion is absent**. A note that does not mention prior brain injury may simply lack that history. Negation, family history, hypothetical statements, and historical versus current diagnoses also require appropriate handling.

There is a second timing issue: a note written after treatment or after an outcome can reveal facts that were unavailable at baseline. Text-derived eligibility and covariates need the same temporal restrictions as structured records. A final LLM review of the “full note” does not itself establish that future information was excluded.

For trial **NCT03872011**, the paper reports **33 additional eligible patients** identified through notes, with a trial eligibility-complexity score of **0.64**. This demonstrates added retrieval yield in that example. Without an independently adjudicated patient-level precision/recall analysis, it does not by itself establish that all added patients were correctly classified or quantify how many eligible patients were still missed.

## 7. Covariates, missingness, and clinical refinement
{: #covariates }

The Clinician suggests covariates based on disease context, literature, and the objective. The Informatician maps them to fields and retrieves them. Examples include demographics, laboratory values, vital signs, diagnoses, medication histories, and organ-function scores. The showcases use high-dimensional sets of **87–89 covariates**.

The statistical purpose of this step is not simply to maximize the number of variables. A useful confounder helps explain both treatment selection and the outcome, using information measured before the strategy comparison begins. A variable measured after treatment can be a mediator or consequence of treatment. Adjusting for it may change the estimand or introduce bias. A variable that primarily predicts treatment can also worsen overlap without addressing meaningful confounding. The paper relies on domain-informed selection but does not report a complete causal graph or every variable's precise measurement window.

Missingness creates distinct problems. A criterion may be unobservable, a confounder may be incompletely measured, or absence of measurement may itself reflect clinical severity or care decisions. Dropping a criterion changes eligibility; replacing a covariate changes the adjustment set; imputing a covariate adds modeling assumptions. These should be separate recorded decisions.

The article illustrates discussion of replacing sparsely measured lactate with **base excess**. This is a proposed context-dependent substitution reviewed by the agents, not a general equivalence between the two measures. A valid substitute must capture enough of the relevant clinical information for the particular role—eligibility, severity adjustment, or outcome definition. Literature plausibility alone does not quantify residual confounding after substitution.

In the nesiritide showcase, the agent encounters imbalance in absolute eosinophils. The Clinician advises removing it because it is not considered a primary confounder for the relevant hemodynamic outcome. The resulting set meets the reported balance threshold. This example demonstrates the feedback mechanism, but it also exposes an important distinction: **removing an imbalanced variable makes its imbalance disappear from the diagnostic display; it does not establish that the variable is causally irrelevant**. The scientific justification for removing it must precede or be independent of a desire to improve the balance summary.

The main text does not specify missingness cutoffs, the complete imputation procedure, outlier thresholds, or the exact surrogate-validation process. These omissions constrain reproducibility and interpretation of the final cohorts.

## 8. Propensity scores, matching, weighting, and balance
{: #balancing }

### 8.1 What the Statistician chooses

The Statistician selects among **propensity score matching (PSM), inverse probability of treatment weighting (IPTW), and no balancing**, informed by sample size, covariate distribution, and the research objective. The article describes PSM as a common choice for moderately sized data and IPTW as a way to retain observations in large cohorts. These are agent decision tendencies, not a fully specified rule with numerical thresholds. [Statistical analysis, p. 14.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=14)

The propensity score is, conceptually,

$$
e(X)=P(A=1\mid X).
$$

This definition and the formulas below explain the named methods; the article does not provide a complete propensity-model specification for each case.

### 8.2 Matching

PSM pairs or groups treated and comparator subjects with similar estimated treatment probabilities. Its validity depends on the covariates, model, overlap, matching algorithm, and how the resulting population is defined. Matching may discard poorly comparable subjects, changing the target population. A matched analysis often targets a treated or overlap population rather than automatically estimating the full-cohort ATE.

The paper does not specify a universal matching ratio, caliper, distance scale, replacement policy, or handling of unmatched patients. Calling an effect an ATE after matching therefore requires clarification of the population over which it is averaged. No-balance analysis likewise needs a justified design or outcome-adjustment strategy; selecting that option is not equivalent to demonstrating an absence of confounding.

### 8.3 Weighting

For a conventional baseline ATE analysis, illustrative unstabilized treatment weights are

$$
w_i^A=\frac{A_i}{\widehat e(X_i)}+\frac{1-A_i}{1-\widehat e(X_i)}.
$$

The weighted data give more influence to subjects whose observed treatment was less likely given their covariates, creating a pseudo-population in which measured baseline covariates can be less associated with treatment. This is not randomization of the actual patients.

IPTW can retain records, but it does not automatically retain their full statistical information. Extreme weights can give a few people most of the influence. An explanatory effective sample size is

$$
\mathrm{ESS}=\frac{(\sum_i w_i)^2}{\sum_i w_i^2}.
$$

Thus a larger raw cohort may have a much smaller ESS. Reproduction would require the propensity model, stabilization, truncation or trimming, overlap diagnostics, and uncertainty calculation. The article does not give all these settings. Its claim that IPTW preserves statistical power should be understood as a motivation, not a universal property of weighting.

### 8.4 Balance diagnostics

The study aims for **standardized mean differences below 0.1**. An illustrative continuous-variable SMD is

$$
\mathrm{SMD}_j=\frac{\overline X_{1j}-\overline X_{0j}}{\sqrt{(s_{1j}^{2}+s_{0j}^{2})/2}},
$$

using appropriate weighted or matched summaries after adjustment. The article names the threshold but does not fully specify every standardization convention. Absolute SMDs assess measured-variable balance; they do not test the no-unmeasured-confounding assumption, verify measurement validity, or guarantee adequate positivity. Reporting distributions and higher-order features can matter even when mean differences are small.

## 9. Time zero, immortal time, and clone–censor–weight
{: #time-zero }

### 9.1 The bias that a treatment label can hide

Suppose eligibility begins at ICU admission, but treatment starts later. Classifying everyone who eventually receives treatment as “treated from admission” credits the treated group with time during which those patients had to remain alive long enough to receive it. That pre-treatment survival can create an apparent advantage unrelated to the drug. Baseline propensity weighting alone does not repair an exposure definition that uses future treatment to classify earlier person-time.

A target-trial design must align eligibility, strategy assignment, and the start of follow-up. Depending on the scientific question, it might compare immediate initiation, initiation within a grace period, sustained treatment strategies, or sequential decisions. These are different protocols.

### 9.2 What the paper reports

Before balancing and outcome estimation, the Methods describe an **extended clone–censor–weight procedure**:

1. Create always-treated and never-treated clones for each subject.
2. Artificially censor the never-treated clone when observed treatment begins.
3. Apply inverse probability of censoring weights to account for that artificial censoring.

The conceptual advantage of cloning is that, while a patient's observed history is compatible with more than one strategy, it can initially contribute to each strategy. Artificial censoring removes a clone when its observed history becomes incompatible with the assigned strategy. The weighting then seeks to address selection induced by this censoring.

### 9.3 What is not fully specified

The paper does not provide the full treated-clone adherence rule, treatment grace period, start-time definition for every showcase, time-varying predictors of artificial censoring, weight stabilization, or all ordinary censoring rules. It does not explain in detail how clone weights combine with treatment weights, or how correlation between clones from the same person enters variance estimation.

An illustrative censoring weight can be written as the reciprocal of the conditional probability of remaining uncensored through time $$t$$, given the relevant history. In discrete time, a basic form is

$$
w_i^C(t)=\prod_{u\le t}\frac{1}{P\{D_i(u)=0\mid D_i(u-1)=0,\overline L_i(u),\overline A_i(u)\}},
$$

where $$D_i(u)=1$$ denotes a censoring indicator and $$\overline L_i(u)$$ is covariate history. This is a teaching expression, not a recovered implementation; actual definitions, numerators for stabilization, and the distinction between artificial and natural censoring must be supplied by the study.

The defensible conclusion is that EmulatRx **includes a stated mechanism intended to address immortal-time bias**. The description alone does not demonstrate that all three showcases implement a complete valid strategy comparison. Clones also do not create additional independent patients. This matters when interpreting the doubled cohort counts discussed later.

## 10. Survival models, effect measures, and double robustness
{: #effect-estimation }

### 10.1 Choice of numerical model

The Statistician can choose **Cox proportional hazards, Kaplan–Meier estimation, parametric survival models, random survival forests, or doubly robust methods**. The paper links this selection to endpoint type, proportional-hazards checks, and a trade-off between interpretation and predictive flexibility. It describes a multi-turn loop in which the same Statistician plans, executes tools, retains results, and self-corrects when validation fails.

A conceptual Cox model is

$$
\lambda(t\mid A,X)=\lambda_0(t)\exp(\beta A+\gamma^\top X),
$$

with conditional hazard ratio $$\exp(\beta)$$ under its assumptions. A treatment-weighted model with treatment alone and an adjusted conditional Cox model need not estimate the same parameter. The article does not fully specify all outcome-model terms or whether every reported HR is marginal, conditional, or associated with a particular weighted population.

Kaplan–Meier estimates a survival curve under appropriate censoring assumptions; random survival forests can flexibly predict survival. Neither becomes a causal estimator merely because an agent selects it. Their predictions must be integrated into a design and adjustment procedure corresponding to the intended causal contrast.

### 10.2 A hazard ratio is not a risk ratio

The hazard at a time point concerns subjects who have not yet experienced the event. Cumulative risk concerns the proportion experiencing an event by a horizon. Consequently, an HR of 0.59 is not generally a 41% reduction in the probability of the event, and an HR of 1.30 is not generally a 30% increase in 28-day mortality risk.

The generated reports sometimes use “risk” for a hazard interpretation. These notes retain the distinction. If the analysis reports an absolute risk difference, it additionally needs a defined horizon and a standardized survival/risk estimation procedure. The synthetic experiment defines its ATE as a risk difference at ten time units; the same meaning cannot be assumed for every real-data ATE without further specification.

### 10.3 What “doubly robust” would require

The showcases describe IPTW combined with a Cox model as a doubly robust analysis. **Weighting plus an outcome regression is not, by itself, a complete specification or proof of double robustness.** The property belongs to a particular estimator for a particular estimand under stated assumptions.

For intuition, with a fully observed binary endpoint $$Y$$, a standard augmented inverse-probability expression for mean potential outcome is

$$
\widehat\mu_a=\frac1n\sum_{i=1}^n\left[\widehat m_a(X_i)+\frac{I(A_i=a)}{\widehat p_a(X_i)}\{Y_i-\widehat m_a(X_i)\}\right],
$$

where $$\widehat m_a(X)$$ predicts outcome under arm $$a$$ and $$\widehat p_a(X)$$ estimates treatment probability. The contrast $$\widehat\mu_1-\widehat\mu_0$$ illustrates the two components: outcome predictions and weighted residual correction. With appropriate conditions, correct specification of either nuisance component can suffice for consistency. This is a **pedagogical binary-outcome formula**, not the survival estimator reported by EmulatRx.

Time-to-event outcomes require additional treatment of censoring and a defined risk horizon; clone-based strategies add further structure. The article does not give the precise survival augmentation equation, nuisance models, cross-fitting scheme, or influence-function/variance calculation. It is therefore appropriate to report that the authors label their procedure doubly robust while distinguishing that label from an independently verified estimator specification. Double robustness, where established, would still not solve unmeasured confounding or an incorrectly aligned time zero.

## 11. Clinician: literature grounding and agent meetings
{: #clinician }

The Clinician has two main duties: review the Statistician's report and offer recommendations during earlier stages. Its literature interface uses **full-text PDFs or extracted abstracts**, sentence-transformer embeddings, and a **FAISS index**. Semantic search retrieves relevant passages, which are synthesized into responses about eligibility, covariates, plausible substitutes, or the interpretation of a result. [Clinician methods, pp. 15–16.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=15)

This is passage retrieval from a prepared corpus. Mentioning PubMed as a source does not imply that every request performs an exhaustive or continuously updated systematic review of PubMed. The article does not give a complete corpus inventory, retrieval depth, embedding configuration, or quantitative evidence-support audit.

Recommendations use machine-readable tags such as `<Condition>`, `<Drug>`, `<Measurement>`, and `<Temporal>`. If a proposed concept cannot be mapped to a valid OMOP identifier, the workflow is designed to stop or request clarification. Extreme sparsity or zero matching patients can also trigger reconsideration. These checks constrain representations and reveal some errors. A valid concept identifier can still encode an inappropriate restriction, and a well-populated cohort can still be biased. Structured output therefore does not itself prevent selection bias.

**Team meetings** bring all roles together around a high-level issue. The Supervisor defines the agenda; each agent contributes its perspective; discussion can proceed for multiple rounds; the Supervisor consolidates the decision and assigns implementation. The lactate/base-excess example combines missingness evidence, clinical literature, and implications for balancing.

**Individual meetings** focus on a single task, such as writing and debugging SQL, with optional feedback from other agents. Their purpose is iterative refinement within a specialty rather than a full-team discussion at every step. These meetings are computational interaction patterns, not necessarily meetings attended by human experts.

The persistent state makes it possible to ask why a criterion changed and which data or literature justified it. A scientifically useful audit trail should also preserve rejected alternatives and estimates from earlier analyses, especially if subsequent refinements respond to the significance or direction of an effect.

## 12. Subgroup exploration and eligibility-criterion attribution
{: #refinement }

### 12.1 Subgroup analysis after an overall result

After a nonsignificant overall estimate, the Statistician can ask the Clinician to propose a clinically meaningful covariate and threshold. The cohort is split, survival analysis is rerun in each subgroup, and HRs and confidence intervals are compared. The paper says exploration stops if no subgroup shows a significant effect or several attempted splits fail, but does not specify an exact attempt limit or statistical correction.

This can generate hypotheses about treatment heterogeneity. It does not establish heterogeneity merely because one subgroup's p-value is below 0.05 and another's is above it. A formal interaction contrast, with its uncertainty, addresses whether subgroup effects differ. Selection of variables or thresholds after inspecting outcomes also changes the inferential problem. A final ordinary confidence interval generally does not reflect the uncertainty from searching many splits.

### 12.2 Eligibility criteria as a cooperative game

EmulatRx implements an approach inspired by **Trial Pathfinder** to examine how eligibility rules affect the estimated HR. Let $$K$$ be the set of criteria and $$v(S)$$ the HR estimated using the subset $$S\subseteq K$$. A pedagogical Shapley expression is

$$
\phi_j=\sum_{S\subseteq K\setminus\{j\}}\frac{|S|!(|K|-|S|-1)!}{|K|!}\big[v(S\cup\{j\})-v(S)\big].
$$

The value averages the change from adding criterion $$j$$ over possible orders of adding all criteria. Positive values indicate an average upward shift in the chosen HR-valued function; negative values indicate a downward shift. The sign would depend on the value function and its scale. The article discusses shifts toward or away from significance, but an HR difference alone does not encode its standard error or p-value.

Computing every subset requires up to $$2^{\lvert K\rvert}$$ evaluations. Monte Carlo permutations approximate the Shapley average: randomly order criteria, compute successive changes from the empty to full rule set, and average each criterion's contribution across orders.

### 12.3 What the attribution means

A criterion changes the eligible population, treatment overlap, sample size, and potentially confounding. Its Shapley value is therefore a measure of **sensitivity of this analytical result to protocol restrictions**. It is not the causal effect of imposing the criterion, a patient-level treatment effect, or proof that deleting it improves validity.

The Clinician or Supervisor can use these results when deciding whether to retain, modify, or remove a rule. However, selecting the rule set because it produces an attractive HR risks selecting noise or residual bias. Essential clinical safety restrictions should not be removed just because their attribution is large. Exploring protocol variants is scientifically different from treating the most favorable variant as a prespecified confirmatory study.

The paper's method description does not completely specify the treatment of invalid or tiny subset cohorts, whether all causal models are refitted for each subset, or the policy governing a final criterion decision. These details matter because they define the game being explained.

## 13. Adverse events and prospective sample-size planning
{: #safety-planning }

### 13.1 Adverse-event definitions and competing risks

The Trialist can retrieve adverse events from the trial graph. The Clinician can extract safety endpoints or adverse reactions from associated literature. The resulting standardized definitions are mapped to EHR events. The Statistician then applies outcome models and balancing strategies analogous to those used for the main outcome. [Statistical analysis, pp. 14–15.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=14)

There is a technical inconsistency in the reporting: the Methods describe **standard Cox models**, then list **subdistribution HRs and cumulative incidence functions** among outputs. In competing-risk settings, cause-specific Cox hazards and Fine–Gray subdistribution hazards are different quantities with different risk sets. Death can prevent observation of a later nonfatal adverse event. The choice determines the meaning of a treatment association and how cumulative incidence is estimated; it cannot be resolved by relabeling an ordinary Cox coefficient. [Primary methodological discussion of cause-specific and subdistribution hazards](https://pmc.ncbi.nlm.nih.gov/articles/PMC7216972/).

The paper does not provide enough detail here to reconstruct a single definitive competing-risk implementation. Moreover, demonstrating an available adverse-event module is different from showing that the three main showcases conducted comprehensive safety analyses.

### 13.2 Schoenfeld-based planning

The sample-size utility translates a target HR, significance level, power, treatment allocation, and expected event fraction into a prospective requirement. The agent extracts information such as control event rate, median survival, censoring, and average follow-up from the analytical data.

A common **pedagogical** approximation for a two-arm proportional-hazards design is

$$
D\approx\frac{(z_{1-\alpha/2}+z_{1-\beta})^2}{p(1-p)[\log(\mathrm{HR}_*)]^2},\qquad
N\approx\frac{D}{q},
$$

where $$D$$ is required events, $$p$$ the allocation proportion, $$q$$ the expected event fraction, and $$\mathrm{HR}_*$$ the planning alternative. The main paper names the Schoenfeld method but does not print this full equation or all implementation details. The two-sided convention shown here is explanatory.

The reported nesiritide planning example uses **alpha 0.05**, **power 0.80**, and an expected HR informed by prior trial literature. It obtains **3,107 participants** from a source cohort of **6,971**, without reporting all numerical inputs needed to reproduce that result. The Supplement gives a different case-report planning number, discussed below.

“Adaptive” here means responding to observed feasibility inputs or revised assumptions. It should not be confused with a prospectively specified group-sequential trial or a formal adaptive randomization design. A favorable observational HR can also be an optimistic planning input, especially after protocol search. Sample-size calculations inherit uncertainty in event rates, treatment effects, follow-up, and future adherence; a single automatically generated number does not eliminate those uncertainties.

## 14. Human feedback, PPO, and the reported DPO objective
{: #rlhf }

### 14.1 Two different feedback loops

Operational feedback changes the current study: an agent revises SQL or a criterion after another agent flags a problem. **Parameter optimization** changes an LLM's future response probabilities using a training objective. The paper describes both, and they should not be conflated.

Its reinforcement-learning-from-human-feedback section describes three stages: experts rate or rank outputs; ratings train scalar reward models and rankings form preference pairs; policies are optimized using PPO or DPO according to the available feedback. Ratings may be on a 1–5 scale and may concern correctness, clinical validity, or fit to the research objective. [Optimization, p. 16, Eqs. 1–3.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=16)

### 14.2 PPO as reported

The scalar-reward objective maximizes expected reward for model outputs. Its clipped surrogate is written in the article as

$$
L^{\mathrm{PPO}}(\theta)=\mathbb E_t\left[\min\left(r_t(\theta)\widehat A_t,\operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\widehat A_t\right)\right],
$$

with

$$
r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\mathrm{old}}(a_t\mid s_t)}.
$$

The ratio measures how the new policy changes an action's probability relative to the policy that generated the training interaction. The advantage indicates how favorable it was relative to a baseline; the article mentions approximating it by reward minus a baseline. Clipping limits the incentive to change probabilities too aggressively in one update. This equation does not specify the full implementation, such as token-level versus response-level rewards, value estimation, reference-policy regularization, batching, or learning rate.

### 14.3 The printed DPO expression and its limitation

For preferred and nonpreferred outputs $$x^+$$ and $$x^-$$, the paper prints an objective to maximize:

$$
L^{\mathrm{DPO}}=\sum_{(x^+,x^-)}\log\sigma\left(\beta[\log\pi(x^+)-\log\pi(x^-)]\right).
$$

It increases relative probability of preferred outputs. However, this printed expression omits the explicit reference-policy ratios found in canonical DPO. A standard reference-relative preference logit, shown here **for comparison rather than as an EmulatRx implementation claim**, is

$$
\beta\left[\log\frac{\pi_\theta(y^+\mid q)}{\pi_{\mathrm{ref}}(y^+\mid q)}-\log\frac{\pi_\theta(y^-\mid q)}{\pi_{\mathrm{ref}}(y^-\mid q)}\right].
$$

The reference terms are part of the original formulation, so they should not be silently inserted into the paper's reported equation or assumed absent from its software without inspection. [Original DPO paper](https://arxiv.org/abs/2305.18290).

### 14.4 What the optimization evidence establishes

The article describes deploying RLHF, but the main text and Supplement do not report a reproducible feedback-dataset size, reward-model architecture, PPO clipping value, DPO beta, learning rate, epochs, exact optimized checkpoints, or a quantitative with/without-RLHF comparison. They also do not fully separate evaluation of off-the-shelf backends from performance attributable to specific optimized policies.

The three clinical experts who score generated responses are an evaluation resource; their presence alone is not a complete specification of the training-feedback process. Likewise, expert-preferred language does not establish correct causal identification. A report can be lucid and clinically plausible while using an inadequate adjustment set or failing to account for selective analysis.

## 15. Evaluation of retrieval, parsing, SQL, and clinical responses
{: #agent-evaluation }

### 15.1 Trial retrieval: three constrained queries

The graph is tested with progressively constrained hydrocortisone/septic-shock questions. The first specifies disease and intervention; the second adds G6PD-deficiency exclusion; the third asks about a platelet threshold. Reference trial sets are constructed by keyword search and manual review. The comparator API queries are manually written, while direct GPT-4o is a deliberately simple ungrounded chat baseline.

| Retrieval setting | Query 1: 34 reference trials | Query 2: 10 reference trials | Query 3: 1 reference trial |
| --- | --- | --- | --- |
| Knowledge graph | 34 returned; precision 100%, recall 100% | 10; 100%, 100% | 1; 100%, 100% |
| ClinicalTrials.gov API | 34; 100%, 100% | 8; 100%, 80% | 2; 50%, 100% |
| Direct GPT-4o | 5; 100%, 14.7% | 3; 100%, 30% | 1; 100%, 100% |

These results demonstrate the value of structured eligibility information for the tested queries. They do not establish perfect retrieval across arbitrary questions or a comprehensive superiority claim over all possible registry-search systems. The manually constructed reference set can also inherit the coverage limits of its keyword-search stage. [Table 1, p. 4.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=4)

### 15.2 Concept parsing: exact attribute matching

Two biomedical informatics experts annotate **266 concepts across 20 trials**. A parsed concept is correct only if the concept name, domain/category, temporal qualifier, and value match the annotation. The study reports a Cohen's-kappa target of at least **0.7**; a target should not be presented as the observed agreement value unless separately reported.

GPT-4o's reported precision is **96.7%** and recall **98.9%**, with **263 of 266** reference concepts recognized. Those precision/recall values imply an F1 of approximately **97.8%** using the usual harmonic mean. The Discussion instead reports **95.4%** F1. The prose also calls Gemma the strongest remaining parser while Figure 2's caption calls it the weakest. These source inconsistencies limit exact model ranking claims; the GPT-4o precision/recall values can be reported with their location rather than silently reconciled.

### 15.3 SQL evaluation: error-specific accuracy

Generated SQL is manually reviewed, executed, and compared with expected cohort-retrieval results. Seven error types are considered:

| Error | What can go wrong |
| --- | --- |
| Concept omission | A parsed concept never enters the query |
| Incorrect concept mapping | A concept is linked to the wrong identifier |
| Logical error | Boolean structure, temporal relation, or numerical comparison changes meaning |
| Function misuse | SQL functions are used incorrectly |
| Integrity violation | Types or data-consistency constraints are violated |
| Schema reference error | An incorrect table or column is referenced |
| Syntax error | The query is grammatically invalid |

Figure 2b defines accuracy as the fraction of trials with **no error of a particular type**, not the fraction with no errors of any type. These cannot be treated as interchangeable measures of end-to-end cohort correctness.

Eligibility complexity is the proportion of criteria classed as complex. A simple criterion expresses a single concept, its negation, or a single quantitative comparison; complex criteria include combinations, temporal constraints, and conditional statements. GPT-4o error count correlates with complexity: **Spearman rho 0.45, p = 0.043**. This describes an association across the evaluation set, not a causal estimate of complexity's effect or a calibrated predictor of future error rates.

### 15.4 Expert ratings and RAG ablation

Three clinical domain experts use a **five-point Likert questionnaire** covering readability, correctness, coherence, creativity, and usefulness. Overall means are **4.88 for GPT-4o, 4.78 for Phi-4, 4.71 for DeepSeek-R1, and 4.40 for Gemma 3**. Table 5 uses Kruskal–Wallis tests, reports p-values below 0.001, and explicitly states **no adjustment for multiple comparisons**. Evaluation should distinguish repeated ratings of outputs from independent participants and should not equate subjective correctness ratings with validated causal estimates.

The RAG ablation is described qualitatively: without retrieval, numerical outputs can still be stated; with retrieval, summaries contain richer biomedical context and more detailed effect discussion. The article does not provide a full quantitative ablation table isolating RAG's contribution to cohort validity or treatment-effect accuracy. It likewise does not give a matched single-agent comparison establishing that every improvement requires multiple agent roles.

## 16. What the synthetic experiments test
{: #synthetic-evaluation }

### 16.1 Recovering known survival effects

The first synthetic experiment has **1,000 subjects and ten standard-normal covariates**. Treatment is assigned through a logistic mechanism using SOFA and age. Event times follow an exponential proportional-hazards model with **baseline hazard 0.1**, under true HRs **0.5, 1, 2, and 3**. Censoring is exponentially distributed. The true ATE is defined as a **risk difference at a ten-time-unit horizon**. Full coefficients and all censoring parameters are not supplied in the text.

All backends choose PSM and use deterministic numerical tools. Their HRs and intervals are identical despite differences in additional suggested outcome models. The resulting comparison tests whether agents can choose and invoke tools in this setting; it does not supply four independent replications of effect recovery.

| True HR | Estimated HR | 95% CI | Estimated risk difference | True risk difference, rounded |
| ---: | ---: | --- | ---: | ---: |
| 0.5 | 0.6345 | 0.5448–0.7389 | −0.0997 | −0.1759 |
| 1.0 | 1.0383 | 0.8958–1.2034 | 0.0244 | 0 |
| 2.0 | 1.7524 | 1.5152–2.0267 | 0.1461 | 0.1633 |
| 3.0 | 2.8074 | 2.4330–3.2394 | 0.2225 | 0.2832 |

The estimates recover effect directions, but the first interval excludes its true HR of 0.5 and several risk differences depart materially from truth. A single dataset per scenario cannot characterize estimator bias, confidence-interval coverage, or Monte Carlo variability. Figure 2 explicitly states that the reported estimates are not based on biological or technical replicates. The evidence is therefore narrower than a general demonstration of statistically calibrated causal inference. [Table 3, p. 7; Figure 2, p. 5.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=7)

### 16.2 Detecting an engineered effect modifier

A second dataset has **1,000 subjects**, SOFA, age, and binary treatment. The treatment log-hazard contribution is constructed to differ by SOFA, with values described as +1 below a threshold and −1 above it, plus an offset intended to produce an overall null effect. The task is to recognize the null aggregate result and find clinically plausible strata with different responses.

GPT-4o and Phi-4 use **SOFA <8 versus ≥8**; DeepSeek-R1 and Gemma use **<7 versus ≥7**. The table reports one subgroup-analysis attempt for GPT-4o, DeepSeek-R1, and Gemma, and two for Phi-4.

| Cutoff and models | Lower-SOFA HR, 95% CI | Higher-SOFA HR, 95% CI |
| --- | --- | --- |
| 8; GPT-4o and Phi-4 | 1.3849, 1.2101–1.5850 | 0.7280, 0.5921–0.8950 |
| 7; DeepSeek-R1 and Gemma 3 | 1.3443, 1.1760–1.5366 | 0.8286, 0.6853–1.0019 |

The higher-SOFA interval at cutoff 7 includes 1. Thus not every listed stratum achieves conventional significance. This controlled example demonstrates the ability to explore a known modifier; it does not assess false discoveries when no heterogeneity exists, selection over many candidate variables, or transportability of a discovered threshold.

### 16.3 Shapley-estimator validation

The criterion-attribution experiment varies the number of rules from **2 to 20**. It samples true rule importances from an unspecified uniform range, constructs subset values from a baseline plus summed importances, and adds Gaussian noise with **standard deviation 0.5**. Random permutations estimate marginal contributions, stopping at **1,000 iterations** or when the standard error of the mean reaches **0.001**. Accuracy is evaluated with mean absolute error relative to the constructed importances.

This is a test of approximation in a synthetic additive value game. It does not validate the causal effect estimates produced by re-running a clinical emulation under alternative eligibility rules. In a real study, changing a rule can change positivity, confounding, treatment prevalence, and the estimand in nonadditive ways. Convergence of the Monte Carlo attribution does not certify validity of the HRs supplied as the value function.

## 17. Three end-to-end showcases
{: #showcases }

The showcases demonstrate the workflow with GPT-4o. Their estimates are **reported observational results**, not treatment recommendations. Figure 3's workflow text is itself described as GPT-4o-generated summaries of logs, which makes it useful for orientation but not a substitute for inspecting the underlying data and execution trace. [Showcases, pp. 9–10.](https://www.nature.com/articles/s41467-026-74501-2.pdf#page=9)

### 17.1 Nesiritide in acute decompensated heart failure

The source protocol is **NCT00475852**. The Trialist identifies hospitalization for ADHF, or diagnosis within 48 hours, with exclusions including high-risk hypotension, acute coronary syndromes, and specified structural heart conditions. The Clinician proposes **89 covariates**, including detailed laboratory measures, vital signs, and SOFA. The Informatician constructs a cohort reported in the showcase as **13,942 patients**.

The Statistician chooses IPTW rather than matching to retain observations. It detects persistent eosinophil imbalance, receives a Clinician recommendation to remove that variable, and reports balance below the 0.1 threshold. IPTW and a Cox-based analysis labeled doubly robust yield **HR 0.5913, 95% CI 0.46–0.76**, for rehospitalization/all-cause mortality, and a reported **2.8-percentage-point absolute risk reduction**.

The paper characterizes the direction as consistent with ASCEND-HF but stronger. A primary-source check is more informative: the original randomized trial reported **HR 0.93, 95% CI 0.80–1.08**, with 30-day rehospitalization/death **9.4% versus 10.1%, p = 0.31**. Both point estimates are below one, but the original trial did not establish the strong statistically significant benefit implied by the emulated estimate. Directional agreement therefore does not validate its magnitude or eliminate observational bias. [Original ASCEND-HF report](https://www.nejm.org/doi/full/10.1056/NEJMoa1100171).

### 17.2 Renal replacement therapy in severe acute kidney injury

For **NCT06091982**, the main text describes adults with severe AKI, excluding prior chronic dialysis and incomplete baseline data. The Clinician selects **88 covariates** and the Informatician reports **11,124 patients**. IPTW and the doubly robust-labeled analysis produce **HR 0.6443, p = 0.0008** for mortality.

The narrative contrasts this with earlier null findings and suggests that the revised analysis reveals a previously obscured benefit. Methodologically, a change from null to significant after cohort/model revision does not identify which result is closer to truth. It could reflect greater information, changed populations, different estimands, different residual bias, or analysis selection. The earlier design and result need to remain part of the record.

The supplied Supplement also contains a generated report for this case whose data-source description conflicts with the main article. That discrepancy is discussed in §18 because it directly illustrates why automated prose cannot be accepted as a verified study provenance record.

### 17.3 Hydrocortisone in septic shock

For **NCT04134403**, the main text describes persistent vasopressor dependence and lactate above **2.0 mmol/L**, with exclusions including major hemorrhage, burns, and prolonged vasopressor use before the trial's reference point. The Clinician specifies **87 covariates**. The reported cohort is **2,306 patients**, compared with **1,153 in a previous run**.

IPTW and doubly robust-labeled estimation yield **HR 1.2983, 95% CI 1.07–1.58, p = 0.0082**, for 28-day mortality. The agents flag a possible harm signal and suggest further stratification. This is a dataset- and design-specific association. Confounding by indication is especially relevant when sicker patients are more likely to receive rescue therapy; a statistically significant adjusted result does not by itself establish treatment harm.

### 17.4 Runtime as a workflow outcome

The main text reports runtimes of **5.75 ±1.52 minutes for GPT-4o**, **20.95 ±7.94 for Phi-4**, **25.87 ±4.38 for Gemma 3**, and **31.36 ±14.51 for DeepSeek-R1**. It calls the GPT-4o value a median but does not clearly define the accompanying ± statistic. These numbers measure the tested configured pipeline. They do not include a controlled demonstration that an equally rigorous complete manual study, including data access, phenotyping validation, and scientific adjudication, takes the cited comparison time of days to weeks.

## 18. Selective refinement and the reliability of generated reports
{: #interpretation }

### 18.1 Exploratory design versus confirmatory estimation

The ability to revise a protocol is part of EmulatRx's purpose. The causal concern is not iteration itself, but **using the same outcome data both to choose the analysis and to present the chosen result with ordinary confirmatory inference**.

Several decisions can respond to results: changing covariates after balance checks, relaxing criteria to enlarge a cohort, selecting a subgroup after an overall null, comparing many criterion subsets, or choosing a model after seeing an effect. These decisions can each be reasonable for exploration. Together, they create a selection process that a final conventional p-value usually does not account for.

A more rigorous separation would preserve an exploratory phase that develops a protocol, then freeze the protocol and test it on independent data or an appropriately designed validation sample. If independent validation is unavailable, the report should retain all tried analyses, distinguish prespecified from post hoc choices, and describe uncertainty from selection. These are methodological recommendations from these notes, not procedures demonstrated by the paper.

### 18.2 Supplement cross-check: substantive discrepancies

The official Supplement's generated RRT report names **Harapan Kita National Cardiovascular Center, 2020–2022**, while the main article identifies **MIMIC-IV, Boston, 2008–2019** for this showcase. This appears to mix source-protocol metadata with emulated-data provenance. Its nesiritide report gives a required sample size of **14,409**, versus **3,107** in the main planning example. The RRT report's ATE interval includes zero despite the significant HR. These are not interchangeable effect measures or necessarily contradictory estimates, but they require distinct interpretation. [Supplementary Notes 2–4](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-74501-2/MediaObjects/41467_2026_74501_MOESM1_ESM.pdf).

The main article also gives **6,971 versus 13,942** for the nesiritide cohort and **1,153 versus 2,306** for hydrocortisone. Both changes are exact doublings. Cloning is one conceivable explanation, but the article does not explicitly establish it. These notes therefore do not equate the larger counts with either new independent patients or clone rows. The relevant analytical report must distinguish unique persons, eligible episodes, clones, person-time rows, matched samples, and effective weighted sample size.

The presence of narrative mismatches matters even when a numerical tool ran correctly. Report generation can introduce a false study setting, overstate an outcome interpretation, or assert an unspecified sensitivity analysis. Automated reporting needs provenance checks linking each claim to the actual configuration and result object.

### 18.3 What the current evidence supports

The experiments support feasibility of joining trial retrieval, structured concept extraction, SQL generation, clinical-literature retrieval, and executable analyses in one adaptive workflow. They show useful component performance and demonstrate how different roles can surface data problems and coordinate revisions.

They do not establish that every generated emulation identifies a causal effect, that the clinically strongest-looking revision is the most valid, or that agent consensus replaces independent methodological review. Evaluation on two data environments also leaves broader transportability, federated operation, multimodal inputs, and institution-specific schema or practice differences open. The paper itself identifies several of these as future directions.

## 19. Reproducibility: reported settings and missing specifications
{: #reproducibility }

The journal links both a [GitHub repository](https://github.com/TrialLab/EmulatRx) and a [Zenodo archive](https://doi.org/10.5281/zenodo.20016649). A reproduction should identify the exact archived version and connect it to the evaluated runs. The table below concerns what can be reconstructed from the **main article and Supplement examined for these notes**, not a claim that no further information exists in software artifacts.

| Area | Reported | Needed for a complete reproduction or causal audit |
| --- | --- | --- |
| Models and orchestration | GPT-4o, Phi-4, DeepSeek-R1:14b, Gemma-3:12b; LangGraph; shared state; cache; fixed downstream seeds | Exact model versions, prompts for every role, decoding settings, graph transition rules, cache artifacts, seed values, termination limits |
| Trial graph | 1,363 registry trials; Neo4j; trial/component/concept schema; ontology patterns | Complete registry snapshot, graph build configuration, failed extractions, ambiguity resolution, concept-set versions |
| Phenotyping | Criteria2Query-derived extraction; UMLS/OHDSI; temporal/value normalization; modular SQL | Full concept sets, SQL, eligibility adjudication, unit conversions, episode handling, timing boundaries |
| Notes | Keyword filtering, embeddings, biomedical NLI, final LLM review | Exact checkpoints, thresholds, retrieved-snippet counts, missing-evidence rules, note-time restrictions, model deployment boundaries |
| Covariates and data quality | Clinical selection; pre-intervention information; missingness checks; adaptive substitutions | Complete pre-time-zero feature windows, imputation model, missingness/outlier thresholds, justification for removed variables |
| Matching/weighting | PSM/IPTW/no balancing; target SMD <0.1 | Propensity estimator, matching settings, estimand, stabilization/trimming, overlap plots, ESS, variance calculation |
| Timing and censoring | Always/never-treated cloning; censor never-treated at initiation; IPCW | Common time zero, grace period, treated-clone rules, time-varying censoring model, ordinary censoring, combined weights, clone-aware uncertainty |
| Outcomes | Cox/KM/parametric/RSF options; HR and ATE outputs | Exact endpoint algorithms, risk horizons, model terms, PH tests, censoring assumptions, explicit survival doubly robust estimator |
| Adaptive analyses | Subgroup proposals; criterion Shapley values; adverse-event and sample-size utilities | Search limits, stopping rules, multiplicity handling, treatment of invalid criterion subsets, competing-risk model, full planning inputs |
| RLHF | Human ratings/rankings; scalar reward model; PPO and DPO objectives | Feedback volume, split, reward architecture, optimized checkpoints, learning rates, PPO epsilon, DPO beta, training schedules, comparative ablations |
| Evaluation | 20 trials; 266 concepts; three clinical raters; synthetic scenarios; component metrics | Achieved annotation agreement, full adjudication protocol, independent replications, uncertainty over trial/model runs, single-agent comparison |

Two forms of reproducibility are worth separating. **Computational replay** means that the same cached responses, code, data, and seeds yield the same outputs. **Scientific robustness** means that reasonable alternative designs, samples, measurements, and analysis specifications lead to appropriately interpreted conclusions. The state/cache architecture helps the first; the second needs substantially broader validation.

## 20. Source map and reading connections
{: #sources }

| Topic | Location in the source |
| --- | --- |
| Motivation, five tasks, agent architecture, graph control, cache | Main pp. 1–3; Figure 1 |
| Trial-query and concept-extraction evaluation | Main p. 4; Table 1; Figure 2a |
| SQL error evaluation and criterion complexity | Main pp. 4–6; Figure 2b; Table 2 |
| Synthetic effect recovery, heterogeneity, attribution, sample size | Main pp. 6–8; Tables 3–4 |
| Clinician questionnaire and RAG discussion | Main pp. 7–9; Table 5 |
| Clinical showcases and runtime | Main pp. 9–10; Figure 3 |
| Datasets and agent responsibilities | Main pp. 11–12 |
| Knowledge graph and extraction/normalization pipeline | Main pp. 12–13; Figures 4–5 |
| SQL, clinical notes, baseline data, quality checks | Main pp. 13–14 |
| Statistical methods, cloning, subgroup analysis, adverse events | Main pp. 14–15 |
| Criterion attribution and sample-size planning | Main p. 15 |
| Clinician retrieval and structured recommendations | Main pp. 15–16 |
| PPO, DPO, and meeting structures | Main p. 16 |
| Generated case reports and extraction-prompt details | Supplementary Notes 2–5 |

This paper sits at the intersection of **computable phenotyping**, **target-trial emulation**, and **agentic workflow design**. The phenotyping layer asks whether the cohort represents the written protocol. The causal layer asks whether the protocol and analysis identify a meaningful treatment contrast. The agent layer asks whether tasks, feedback, state, and tools can be coordinated reliably. Keeping these layers distinct makes both the contribution and the remaining work easier to assess.

For related reading on this site, the [Causal Inference collection]({{ '/causal-inference/' | relative_url }}) provides the identification and estimation background. The [high-throughput Alzheimer's drug-repurposing note]({{ '/rwe/high-throughput-ad-target-trial-emulation/' | relative_url }}) examines scaling across many drug comparisons, while the [federated target-trial-emulation note]({{ '/rwe/federated-target-trial-emulation/' | relative_url }}) examines estimation across institutions. EmulatRx instead scales the coordination of protocol construction, data extraction, and analysis; automating that coordination does not remove the identification assumptions shared by all three. The [TxAgent methodology note]({{ '/txagent-therapeutic-reasoning/' | relative_url }}) discusses a different form of biomedical agent: retrieving source information to answer therapeutic questions. EmulatRx additionally creates an observational analytical dataset and estimates treatment contrasts, so its validity depends on study-design and causal assumptions beyond accurate tool use.

**Primary source:** Li, H., Pan, W., Rajendran, S., Zang, C., and Wang, F. (2026). *Empowering clinical trial design with agentic intelligence and real-world data*. [Nature Communications](https://doi.org/10.1038/s41467-026-74501-2) · [Official Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-74501-2/MediaObjects/41467_2026_74501_MOESM1_ESM.pdf) · [Archived code](https://doi.org/10.5281/zenodo.20016649) · [Repository](https://github.com/TrialLab/EmulatRx).

The two reproduced page images are unchanged renderings of the supplied article, attributed to Li et al. and the publisher. The article is distributed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). The explanatory prose, mathematical illustrations, and methodological critiques in these notes are separately written commentary; they should not be attributed to the authors as additional reported experiments or implementation details.
