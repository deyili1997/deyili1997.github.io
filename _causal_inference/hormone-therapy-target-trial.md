---
layout: "causal-note"
title: "Hormone Therapy and Breast Cancer: A Target Trial Protocol"
description: "Work through the seven target-trial components using hormone therapy and five-year breast-cancer risk."
group: "Trial design"
order: 9
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. First, establish what this is: a target trial protocol, not a results table", "anchor": "section-1"}, {"title": "2. Eligibility criteria: Who can participate?", "anchor": "section-2"}, {"title": "3. Treatment strategies: Which two sets of action rules are compared?", "anchor": "section-3"}, {"title": "4. Assignment procedures: Random assignment, with participants aware of their group", "anchor": "section-6"}, {"title": "5. Follow-up and outcome: When do we observe, and what do we record?", "anchor": "section-7"}, {"title": "6. Causal contrasts: ITT and PP in the same protocol", "anchor": "section-10"}, {"title": "7. Analysis plan: What does the final long paragraph mean?", "anchor": "section-12"}, {"title": "8. What must change when using observational data?", "anchor": "section-17"}, {"title": "9. Self-check", "anchor": "section-27"}]
previous_note: "/causal-inference/target-trial-emulation/"
next_note: "/causal-inference/confounding-treatment-components/"
---

Study entry point: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

Prerequisites: [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}), [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}), and [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}). On a first reading, follow §1–§6 through “who enrolls → which strategies are assigned → when outcomes are recorded → which effects are compared”; then read §8.2–§8.4 to see how existing data constrain emulation. Return to the analysis details in §7 after studying IPW and the g-formula.

On your first reading, following one woman is enough: **eligible at baseline → assigned to the treatment strategy → subsequently develops DVT and stops treatment under the exception → continues to be observed for breast cancer.** Sections 3, 5, and 6 explain, respectively, whether she follows the treatment rules, whether follow-up ends, and how her experience enters ITT and PP analyses. Differences between the two analyses arise from the research question and its rules, rather than an arbitrary retrospective decision about retaining her.

<aside class="study-callout study-callout--abstract" markdown="1">

**What question will this study answer?**

Among eligible postmenopausal women, what is the effect on the five-year risk of a breast cancer diagnosis of comparing “no hormone therapy throughout follow-up” with “start estrogen plus progestin at baseline, then continue according to rules with safety exceptions”?

The same protocol prespecifies two targets: **the ITT effect of assignment to the two strategies**, and **the PP effect of following the two strategies**.

</aside>



A worked multivariable example: [Complete multivariable LR-IPTW example comparing drug A with drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) shows how baseline characteristics for 3,000 people enter one shared LR model to produce propensity scores, weights for both groups, balance diagnostics, and one-year risks. Z=0 denotes drug B, rather than no treatment. This is a separate teaching supplement; it does not change this note's original hormone-versus-no-hormone strategies.

## 1. First, establish what this is: a target trial protocol, not a results table
{: #section-1 }

The table comes from [Hernán and Robins (2016), Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/). Its title describes a **summary of the target trial protocol for estimating the effect of postmenopausal hormone therapy on five-year breast cancer risk**.

![Postmenopausal hormone target trial protocol]({{ "/assets/causal-inference/postmenopausal-hormone-target-trial-protocol.png" | relative_url }})

The authors first describe how a randomized trial would be designed if one could be conducted, then discuss how to emulate it using existing observational data. “Random assignment” in the table belongs to the hypothetical target trial; it does not mean that the subsequent database study actually randomized patients.

The table provides neither efficacy nor safety estimates, nor all the clinical implementation details, such as drug doses. This note first explains the rules the table contains. Details that the table leaves unspecified but a formal study would need to establish are identified separately.

For the connection between this type of design and routine care, see [Pragmatic Trials in Routine Care]({{ "/causal-inference/pragmatic-trials/" | relative_url }}). A pragmatic approach does not rule out randomization or limit research to ITT effects.

## 2. Eligibility criteria: Who can participate?
{: #section-2 }

At enrollment, all of the following must hold:

1. The woman is postmenopausal and within five years of menopause.
2. She enters the study during the 2005–2010 enrollment window.
3. She has no history of cancer.
4. She has not used hormone therapy during the preceding two years.

There are three different clocks here:

| Time period | What does it restrict? |
| --- | --- |
| Within five years after menopause | Physiological stage at enrollment |
| 2005–2010 | Calendar window during which enrollment is possible |
| Five years after baseline | Each person's maximum follow-up duration |

For example, a woman who reached menopause in 2004 and enrolls in 2007 is three years past menopause. If she meets the other criteria, she can enroll and begin follow-up in 2007, potentially continuing until 2012. Another woman who enrolls in 2010 can have five years of follow-up extending to 2015. **2005–2010 is not a common start and end period for everyone's follow-up.**

“No use in the preceding two years” also does not mean “never used in her lifetime”: someone who used treatment earlier may still satisfy this criterion. A pretreatment window defines current nonusers, but a two-year window alone cannot establish that all effects of earlier treatment have disappeared. See [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}) for new users and washout periods; the comparator in this table is no hormone use, rather than another active drug.

Eligibility should be assessed at baseline, without adding requirements such as “must remain alive and cancer-free for the next five years” or “must never switch drugs afterward.”

## 3. Treatment strategies: Which two sets of action rules are compared?
{: #section-3 }

### Strategy 0: No hormone therapy throughout follow-up
{: #section-4 }

The original phrase *Refrain from taking hormone therapy during the follow-up* means **no hormone therapy throughout follow-up**.

It does not merely require “no use on the enrollment day.” A woman who is untreated initially but starts at month eight deviates from this sustained nonuse strategy.

### Strategy 1: Start combination therapy at baseline and continue, with safety exceptions
{: #section-5 }

Start **estrogen plus progestin** at baseline and continue during follow-up, with exceptions to the requirement for continued treatment after the following diagnoses:

| Original term | Meaning |
| --- | --- |
| Deep vein thrombosis, DVT | Formation of a blood clot in a deep vein |
| Pulmonary embolism, PE | Embolism in the pulmonary circulation |
| Myocardial infarction, MI | Heart attack |
| Cancer | Cancer, not limited to breast cancer |

This is a **sustained treatment strategy with safety exceptions**. Sustained treatment does not mean forcing treatment for five years regardless of what happens clinically.

<aside class="study-callout study-callout--important" markdown="1">

**Stopping treatment for a specified safety reason can be adherence to the protocol**

Stopping after DVT under this exception should not automatically be treated as ordinary nonadherence. The PP effect must respect this rule within the strategy.

This summary table does not specify how soon to stop after diagnosis, whether discontinuation must be permanent, whether restarting is allowed, or the dose, route, and allowable gaps in use. We cannot supply “immediate permanent discontinuation” ourselves; these details must be specified before formal implementation or emulation.

</aside>


Both strategies govern later behavior. In particular, “no use throughout follow-up” is itself a sustained rule and cannot be replaced by “do not initiate at baseline, with no restrictions afterward.” See [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}).

## 4. Assignment procedures: Random assignment, with participants aware of their group
{: #section-6 }

At baseline, eligible women are randomly assigned to strategy 0 or strategy 1, and participants know their assigned group. Participants are therefore unblinded, and the table does not specify a placebo.

What is randomized is **group assignment**, not each subsequent decision to take or stop treatment. Therefore:

- A woman assigned to the treatment strategy may never start or may later stop on her own.
- A woman assigned to the no-treatment strategy may subsequently start treatment.

This is why the same randomized trial can address both ITT and PP.

Participants' awareness of their assignment does not automatically mean that outcome assessors are unblinded; the table does not address this. A breast cancer diagnosis can also be affected by the examination process, so a complete protocol should specify monitoring and outcome ascertainment. See [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}).

## 5. Follow-up and outcome: When do we observe, and what do we record?
{: #section-7 }

Follow-up begins at random assignment, $$T_0$$. This period of a woman's follow-up ends at the earliest of four events:

| What occurs first? | Its role in the study |
| --- | --- |
| Breast cancer diagnosis | The outcome of interest occurs |
| Death before breast cancer diagnosis | A competing event: a subsequent breast cancer diagnosis during life is no longer possible |
| Loss to follow-up | Subsequent outcome information is missing: a censoring issue |
| Five years since baseline | The planned follow-up horizon is reached: administrative censoring |

The outcome is **breast cancer diagnosed by an oncologist within five years after baseline**. The table does not further specify subtypes, pathological criteria, or a screening schedule.

The original paper subsequently distinguishes two questions. If the goal is to monitor and ascertain breast cancer using common rules unaffected by treatment history, we need to consider whether hormone users undergo more examinations; blinding only the final diagnostician may not eliminate earlier differences in examination opportunities. If the question concerns actual demand for breast surgery under usual care, additional examinations, diagnoses, and operations caused by treatment may form part of the total effect of interest. See [Translation of the original passage: Systematic, blinded outcome ascertainment and breast surgery]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-17) and §7 of that note for the full explanation. Unblinded clinical care can fit the latter target, but does not remove the need for confounding control and reliable records.

### Stopping treatment does not mean stopping follow-up
{: #section-8 }

Suppose a woman stops treatment under the exception after a DVT diagnosis at month twelve, then receives a breast cancer diagnosis at month thirty-six. Neither DVT nor treatment discontinuation appears in the table's list of follow-up endpoints. If no endpoint such as death or loss to follow-up occurs, breast cancer outcomes should continue to be observed.

Similarly, if she is first diagnosed with another cancer, this may trigger a safety exception in the treatment strategy, but **this table alone does not justify treating it as an endpoint of follow-up in the breast cancer study**. Treatments and changes in monitoring after another cancer may also affect the outcome; a full protocol needs to consider these processes.

If the first cancer is breast cancer, record the breast cancer event and end that period of outcome follow-up. The outcome that has already occurred must not be deleted because the diagnosis also meets a treatment-stopping exception.

### Death and loss to follow-up must be distinguished
{: #section-9 }

After loss to follow-up, we do not know whether the patient is subsequently diagnosed with breast cancer; after death, we know that she no longer has an opportunity for that diagnosis during life.

<details class="study-callout" markdown="1">
<summary>On a second reading: Follow-up stopping rules do not fully specify the analysis of competing events</summary>

If the target is “the probability of a breast cancer diagnosis within five years while allowing death to occur naturally,” estimate a cumulative incidence risk that accounts for competing death. This differs from “breast cancer risk if death were eliminated,” which requires additional definitions and identification assumptions.

The table says only that follow-up ends at death and does not fully specify this choice. If death is treated as ordinary censoring when constructing a breast cancer Kaplan–Meier curve, the resulting $$1-\widehat S(5)$$ cannot be directly interpreted as the cumulative probability of breast cancer in the presence of competing death. This adds an element that a formal analysis must clarify; it does not claim that the original table already selected a particular competing-event estimand. [Young et al. (2020): Causal estimands with competing events](https://onlinelibrary.wiley.com/doi/10.1002/sim.8471)

In the expression, S is the breast-cancer-event-free survival function constructed by this calculation; the hat denotes a sample estimate, and 5 in parentheses means five years after baseline. The initial 1 is total probability. Subtracting the curve's five-year value from 1 gives its event-probability complement. For example, if the curve equals 0.92, its complement is 0.08, or 8%. Correct arithmetic does not guarantee that this 8% equals breast cancer risk in the presence of competing death; the distinction between those targets is precisely the point. It is also not “92% overall survival.”

</details>


## 6. Causal contrasts: ITT and PP in the same protocol
{: #section-10 }

Let $$Z=1$$ denote assignment to the hormone therapy strategy and $$Z=0$$ assignment to the sustained nonuse strategy.

**ITT asks:** For the same eligible population, how does five-year breast cancer risk differ between assignment to strategy 1 and assignment to strategy 0, under the adherence and care processes that subsequently occur in this trial?

**PP asks:** For the same eligible population, how would five-year breast cancer risk differ if everyone were assigned to and followed strategy 1 versus strategy 0? Following strategy 1 includes the safety exceptions listed in the table.

This PP question does not ask, “What if everyone used hormones continuously for five years regardless of contraindications?” That is a different treatment strategy.

### How does the same person's experience enter the two analyses?
{: #section-11 }

To make the operations concrete, the PP column below uses **artificial censoring and weighting** as an example; other methods, including the g-formula, may also be considered.

| Actual experience | ITT analysis | Sustained-strategy PP analysis |
| --- | --- | --- |
| Assigned to treatment; stops at month six without a protocol-permitted reason | Continue tracking outcomes in the original treatment-assignment group | Subsequent contributions may be artificially censored at the first strategy deviation; retain earlier records and address the resulting selection |
| Assigned to treatment; stops after DVT at month twelve under the safety exception | Remains in the original treatment-assignment group | Do not censor for nonadherence solely because of this permitted discontinuation; she may continue to follow the strategy |
| Assigned to no treatment; starts treatment at month eight | Remains in the original no-treatment-assignment group | Deviates from “no use throughout follow-up,” requiring appropriate handling |
| Follows the treatment rules; breast cancer diagnosed in year two | Record the breast cancer event | Also record the event; do not exclude her for failing to complete five years of treatment |

The PP target remains the originally specified eligible population, including people who later deviate in reality. It is not an analysis restricted to people who eventually complete treatment or survive to year five. See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}) and [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}).

The table specifies a comparison of five-year breast cancer risks. Specifying a scale such as the risk difference or risk ratio completes the expression of the estimand. An HR compares instantaneous event rates and cannot be treated directly as a five-year risk ratio; see [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}).

## 7. Analysis plan: What does the final long paragraph mean?
{: #section-12 }

### First level: ITT compares risks by randomized assignment
{: #section-13 }

With randomization actually implemented, complete outcome observation, correct analysis, and the other relevant conditions, a comparison of five-year breast cancer risks between assignment groups can estimate ITT. Randomization protects comparability of baseline assignment.

This does not mean that loss to follow-up or outcome measurement problems can be ignored, or that one only needs to divide the observed number of breast cancer cases by the number of people still observed.

### Second level: PP must address prognostic factors related to adherence
{: #section-14 }

*Prognostic factors* are factors associated with subsequent outcomes. Here the original passage focuses on those also associated with adherence and requires consideration of information both before and after baseline.

Why are these data needed even in a randomized trial? Randomization determines the initial assignment, but subsequent initiation, discontinuation, and continued treatment are not repeatedly randomized. Health status, symptoms, or test results may jointly affect treatment decisions and breast cancer diagnosis risk. Comparing only actual adherers, or censoring at deviation without correcting for selection, may destroy the original comparability.

For example, if women who develop a symptom are more likely to stop treatment on their own, and that symptom is also related to a subsequent cancer diagnosis, simply deleting those who stop changes the prognostic composition of the treatment group. This concerns **discontinuation that deviates from the specified strategy**; stopping under the table's safety exceptions may still follow the strategy.

Suppose, further, that prior treatment itself affects this symptom. We then have **prior treatment → a prognostic factor during follow-up → subsequent treatment continuation**, while the factor also affects the outcome. This is treatment–confounder feedback. Ignoring it may leave confounding between later treatment and outcome. Directly including the factor as an ordinary regression covariate may block the pathway through which prior treatment affects the outcome and, in some structures, introduce selection bias.

This explains why the original passage says g-methods are generally required even in the absence of unmeasured confounding and model misspecification. Measuring a confounder does not remove the need to handle it appropriately; **accurately describing conditional relationships in observed data does not mean that we have already calculated the risk if everyone followed the entire strategy.** We cannot simply put all postbaseline factors into an ordinary Cox model and read the treatment coefficient as the total effect of a sustained strategy. The g-formula additionally derives distributions of follow-up factors under each strategy and averages over them; longitudinal IPW addresses treatment selection through appropriate weighting. These methods still rely on exchangeability, positivity, consistency, and the relevant estimation conditions. [Hernán and Robins, What If, Chapters 20–21](https://miguelhernan.org/whatifbook)

“Generally required” concerns sustained strategies and structures such as feedback here; it does not mean that every PP question unconditionally requires complex longitudinal methods. For example, if a strategy specifies only baseline initiation and there is no outcome loss to follow-up, sufficient baseline confounding control may estimate its effect. That answers a different PP question. See [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}); [Hernán and Robins (2017): Per-Protocol Analyses of Pragmatic Trials](https://pubmed.ncbi.nlm.nih.gov/28976864/).

### Third level: Both ITT and PP must address informative loss to follow-up
{: #section-15 }

*All analyses* in the table means that both analyses plan to address factors related to loss to follow-up and prognosis.

If women at higher risk are more likely to be lost, those remaining may no longer represent the original population. Analyzing according to original random assignment does not restore missing outcomes. Handling loss to follow-up may therefore require clinical and healthcare-use information during follow-up, beyond baseline information alone.

This differs from “artificial censoring for violating a treatment strategy”: the former concerns missing outcome data, while the latter is an analytical rule imposed to estimate a specified strategy. **Stopping treatment does not automatically mean loss to follow-up**. If outcomes remain observable after treatment stops, the ITT analysis should continue to use those outcome data.

If treatment also affects follow-up factors used to adjust for loss to follow-up, directly adding those factors to an ordinary outcome regression does not by itself solve the problem. Appropriate approaches include inverse probability of censoring weighting (IPCW): use information preceding loss to follow-up to estimate the probability of remaining observed, and use contributions from people still observed to correct selection. Its validity depends on sufficient relevant history and the corresponding assumptions; weights do not turn unobserved outcomes into measurements. See [8. IPTW and IPCW: Distinguishing Two Types of Probabilities]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-29).

### Fourth level: The analysis plan determines what must be collected
{: #section-16 }

The table's final sentence emphasizes that investigators must identify these adjustment factors in advance and collect the corresponding data.

They cannot wait until a study ends to discover, “We want to estimate sustained-strategy PP, but have no idea who stopped treatment, when, or why.” Naming a method cannot compensate for this data gap.

## 8. What must change when using observational data?
{: #section-17 }

### 8.1 Mapping the target trial to existing records
{: #section-18 }

The preceding sections describe the target randomized trial. When emulating it, investigators have no actual random assignment and must explain how existing records correspond to it:

1. At each person's appropriate $$T_0$$, use prior information to verify menopause timing, cancer history, and hormone use during the preceding two years.
2. Determine analytical contributions from the compatibility of contemporaneous initiation or noninitiation records with the strategies, and address confounding of baseline treatment choice. Prescribing, dispensing, and actual ingestion must be distinguished.
3. Track subsequent treatment and safety exceptions for sustained strategies, and handle deviations according to the strategy. A comparison of first-day treatment alone cannot be called sustained PP.
4. Record outcomes, competing deaths, and loss to follow-up, using methods aligned with the estimand.

In particular, do not retrospectively select “women who never use hormones in the next five years” as baseline controls or “women who successfully use them continuously for five years” as the baseline treatment group. That uses future behavior, and potentially future survival, to determine enrollment. Specifying what a strategy calls for in the future does not mean that enrollment must wait until all of that future adherence has been observed.

Without original random-assignment information, grouping by actual initiation generally estimates an initiation effect. Retaining initial groups cannot recover the randomized-assignment ITT in this target trial table. If data record assignment decisions such as prescriptions, an observational analog can be discussed, but additional assumptions still need to be explicit. See [7. ITT in Observational Studies: Initiation Effects and Assignment Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-12).

If there are multiple eligible starting points or an initiation grace period, continue to [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}) and [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}), respectively. These notes change how existing records are used for emulation; the population, treatment rules, and target effects specified in this table still need to be defined first.

### 8.2 Having a mammogram does not mean knowing its result
{: #section-19 }

The following two examples come from the [Eligibility criteria section of Hernán and Robins (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/). The authors imagine two additional enrollment requirements to illustrate why ideal eligibility criteria may be impossible to implement accurately in a database. **These extend Table 1; they are not eligibility criteria already specified by Table 1.**

**Paraphrase of the first example:** Suppose a target trial requires candidates to undergo baseline mammography, then excludes women with breast calcifications. The database may record “mammography performed” for billing while omitting the result. The original target trial may then be impossible to emulate. Investigators need to consider whether another target trial that allows women with calcifications would still answer a useful question.

*Mammography* means X-ray imaging of the breast. This example involves two distinct pieces of information:

| Information needed | Can it be determined from an examination billing record alone? |
| --- | --- |
| Was baseline mammography performed? | Possibly, though record validity still needs checking |
| Did it reveal calcifications? | Not without a report or reliable alternative information |

Thus, **“no recorded calcification result” cannot be treated as “the examination confirmed no calcifications.”** What is missing is clinical information needed to assess eligibility. Adding a regression variable for “examination performed” does not restore its result.

Linking imaging reports or other reliable information may help implement the original criterion. If the information truly cannot be obtained, investigators must transparently decide whether to modify the target population. The original passage does not claim that recovery is absolutely impossible in every setting; it says that these data alone may not faithfully emulate the original trial.

#### Changing inclusion criteria also changes the target of estimation
{: #section-20 }

Holding the remaining conditions constant:

- Original target: women who underwent baseline mammography and were confirmed to have no calcifications.
- Modified target: women who underwent baseline mammography, without exclusion based on calcification results.

The latter includes women both with and without calcifications in the target population. Even if both studies compare the same treatments, outcome, and five-year horizon, the full estimand has changed. If treatment effects vary with calcification status, the average effects in the two populations may also differ.

This does not mean that the modified study is necessarily biased. It can produce a valid estimate for the new target population, provided the new question is scientifically meaningful, identification conditions hold, and the change is reported honestly. We cannot estimate an effect for the expanded population and announce it as the effect in the original “women without calcifications.” See [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}).

Furthermore, **dropping calcifications as an exclusion criterion does not mean that all their causal roles can be ignored.** If calcifications are also an unmeasured common cause of treatment choice and outcome, confounding may remain in the expanded population; removing an eligibility condition does not automatically solve that problem.

### 8.3 Expecting continued healthcare contact does not mean requiring actual future contact
{: #section-21 }

**Paraphrase of the second example:** Suppose a trial relies on participants' connection with a healthcare system to track outcomes, and therefore seeks people expected to maintain contact during follow-up. An actual trial can ask at recruitment about plans to move, change jobs, and so forth; historical databases often lack this information. Investigators may approximate it using prebaseline healthcare records, such as routine examinations or medication dispensing during the previous two years, hoping these people are more likely to maintain contact later.

The key is **using information known at baseline to assess whether future follow-up is likely to remain possible**. In an actual trial, someone who answers “I do not plan to move” may later move; that does not make her ineligible on her enrollment day.

Healthcare contact in the original passage broadly means receiving care or maintaining a connection with the healthcare system. It does not mean adherence to the study's hormone therapy. A control participant can avoid hormones throughout follow-up while remaining in continuous contact with care.

| Operation | Which period supplies the information? | What does it mean for the target trial? |
| --- | --- | --- |
| Ask at enrollment about plans to move in the next two years | Plans known at baseline | Assess expected continued observation, without guaranteeing it |
| Require specified healthcare or dispensing records in the preceding two years | Prebaseline history | Approximate expected contact with a measurable proxy criterion |
| Retrospectively retain only people with records throughout the next five years | Actual postbaseline experience | Use future information to decide retrospectively who can enter the baseline cohort |

Prior healthcare use is a **proxy criterion**. It may help identify people who are easier to keep under observation, but cannot guarantee no loss to follow-up. It also restricts the population to people satisfying that historical condition. Investigators should clarify whether this population still corresponds to the question, and continue examining confounding and selection structures. A change in representativeness alone does not establish selection bias affecting internal validity. Conversely, using only baseline information does not automatically guarantee an unbiased study.

### 8.4 Exclude versus censor: Delete the person, or retain earlier follow-up?
{: #section-22 }

The original passage finally emphasizes that a woman must not be removed from the entire study because she later disappears from the database. If she is eligible at baseline and becomes unobservable only later, this should generally be treated as loss to follow-up, with censoring at an appropriate time.

Suppose Lin is eligible and enrolls at baseline. We reliably observe her for fourteen months, with no breast cancer diagnosis. She then changes insurance, the study database no longer covers her, and no other source supplies outcomes.

| Handling | What does it do? | Problem or implication |
| --- | --- | --- |
| Exclude her entirely because of later loss to follow-up | Delete the first fourteen months too, as if she never enrolled | Reselect the baseline population using future observability |
| Censor at loss to follow-up | Retain valid earlier follow-up, ending the record when observation becomes impossible | Acknowledge unknown later outcomes without discarding earlier information |
| Record her as breast-cancer-free for all five years | Fill unknown subsequent outcomes with no event | Mistake missing data for absence of disease |

In this simplified example with known observation coverage for fourteen months, if no study outcome or competing event occurred earlier, the survival record can be $$T_{\mathrm{obs}}=14$$ months with a breast cancer event indicator of 0. **This means only that no event has occurred by fourteen months; it does not mean no breast cancer within five years.**

Here T is duration since this study's baseline, and the subscript obs means observed. The unit of 14 is months, not years or age. The accompanying event indicator of 0 means that this record ends in censoring; it cannot be treated as 0 for a fully observed five-year death or cancer indicator.

If she was already diagnosed with breast cancer in month eight, record the event in month eight. Changing insurance in month fourteen should not erase this observed outcome. See [3. Why Do the Data Need Both Time and an Event Indicator?]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-3).

#### Why can selecting people by whether they remain in the future introduce bias?
{: #section-23 }

People who remain in a database may differ from those who leave in health, insurance, finances, and healthcare behavior. If these factors relate to outcomes, or if treatment also affects continued database presence, restricting analysis to future stayers may destroy comparability between the populations being compared.

This is primarily a future-selection and missing-data problem; not every such situation needs to be called immortal time bias. A guaranteed-survival-time mechanism arises if the rule additionally requires survival to some future time to qualify for enrollment. See [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}).

#### What else is needed beyond marking censoring correctly?
{: #section-24 }

If loss to follow-up is related to subsequent outcome risk, filling in a “censored” indicator does not suffice to eliminate bias. Prior clinical history may be needed to address informative loss, for example through inverse probability of censoring weighting (IPCW). Its validity depends on sufficient relevant history, conditional exchangeability, positivity of remaining observable, appropriate probability models, and other conditions. Weighting does not cause the unobserved later outcomes of censored people to be measured. See [8. IPTW and IPCW: Distinguishing Two Types of Probabilities]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-29); [Hernán and Robins, What If, Chapter 8](https://miguelhernan.org/whatifbook).

#### In a real database, does the absence of new bills necessarily mean loss to follow-up?
{: #section-25 }

No. This is an operational addition to the original brief description: **a temporary absence of medical bills may simply mean that no care was received.** Use continuous enrollment records, healthcare-system coverage, and outcome data sources to prespecify when relevant outcomes become unobservable; do not mechanically use the date of the last bill as the loss-to-follow-up date.

For example, if reliable cancer registry linkage still provides breast cancer outcomes after someone leaves an insurer, disappearance of that insurer's bills alone should not establish loss to breast cancer follow-up. Conversely, observable outcomes do not imply complete treatment and confounder information; sustained-strategy PP also requires a separate assessment of whether those data are sufficient.

### 8.5 How do the two examples connect?
{: #section-26 }

|  | Mammography example | Continued healthcare contact example |
| --- | --- | --- |
| What is missing? | Examination results needed to assess baseline eligibility | Reliable baseline expectations about future healthcare contact |
| What response does the original passage suggest? | Assess whether to switch to a new target trial allowing women with calcifications | Approximate with prebaseline healthcare history, then handle actual subsequent loss to follow-up correctly |
| What substitution is invalid? | No recorded result means no calcifications | Only people who later remain in the database were initially eligible |
| What else needs checking? | Whether the new target is meaningful and identifiable, and whether unmeasured confounding remains | The population defined by the proxy, and whether loss to follow-up or other selection is biased |

Here TTE makes the gap between data and the ideal protocol explicit: which conditions can be implemented, which can only be approximated, and which change the question. It cannot automatically supply information that a database never collected.

## 9. Self-check
{: #section-27 }

1. A woman is not using hormones at enrollment but starts at month eight. Has she followed strategy 0 in this table?
2. Does stopping after a protocol-specified pulmonary embolism diagnosis necessarily violate PP?
3. After stopping under the DVT exception, must breast cancer still be observed?
4. Do other cancers and breast cancer have exactly the same roles in this protocol?
5. Can randomization remove the need to handle loss to follow-up in both analyses?
6. If a database contains only a mammography billing record, can we conclude that a participant has no calcifications?
7. How does screening on two years of prior healthcare history differ from requiring database presence throughout the next five years?
8. If a woman is lost at month fourteen without prior breast cancer, should she be deleted entirely or recorded as cancer-free for five years?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. No; strategy 0 requires nonuse throughout follow-up.
2. Not necessarily; stopping under a specified safety exception can follow the strategy.
3. Yes, unless an actual follow-up endpoint has been reached.
4. No. Both may trigger a treatment exception, but the target outcome and explicitly listed cancer endpoint of follow-up are breast cancer.
5. No; informative loss to follow-up creates missing outcomes and selection problems.
6. No; undergoing an examination and its results are different information.
7. The former uses information known at baseline to define or approximate eligibility; the latter reselects the baseline population using future experience. The former also does not automatically ensure an unbiased study.
8. Neither. In the example with known fourteen-month observation coverage, retain valid earlier records, censor at loss to follow-up, and assess the censoring mechanism.

</details>
