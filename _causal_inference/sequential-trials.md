---
layout: "causal-note"
title: "Sequential Trial Design"
description: "Emulate trials at repeated eligible decision points while accounting for multiple records from the same person."
group: "Trial design"
order: 17
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. What problem does it solve?", "anchor": "section-1"}, {"title": "2. Define each small trial's question first", "anchor": "section-4"}, {"title": "3. How can one person enter several trials?", "anchor": "section-5"}, {"title": "4. After Li starts in March, what happens to earlier trial records?", "anchor": "section-6"}, {"title": "5. Does repeated enrollment create immortal time?", "anchor": "section-9"}, {"title": "6. What is required when pooling trials?", "anchor": "section-10"}, {"title": "7. How can this combine with the other designs?", "anchor": "section-16"}, {"title": "Sources", "anchor": "section-17"}]
previous_note: "/causal-inference/active-comparator-new-user/"
next_note: "/causal-inference/clone-censor-weight/"
---

Study entry point: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**The idea in one sentence**

**A patient may be eligible at multiple times; emulate a new trial at each such decision point, then appropriately combine the information.**

A common example compares “initiate treatment now” with “do not initiate now” at every eligible visit.

</aside>


**Sequential trial design** organizes a longitudinal cohort into a sequence of emulated trials with explicit starting points. A person can enter trials with different baselines, but each trial assesses eligibility and strategies at its own baseline.

<aside class="study-callout study-callout--tip" markdown="1">

**First reading**

Read §1–5 first, following how Li contributes to three trials. Pay particular attention to why later treatment or early death does not rewrite earlier enrollment. On a second pass, read §6 to connect record structure, confounding adjustment, standard errors, and target populations; finish with §7 on combining designs.

</aside>


Overview: [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}). Prerequisite: [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}). Other designs: [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}) and [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}).

## 1. What problem does it solve?
{: #section-1 }

When comparing initiation of A with B, both groups have explicit initiation dates.

When comparing “initiate A” with “do not initiate A,” a noninitiator has no natural “first day of not using medication.” The person may also be eligible today, next month, and the month after.

One solution prespecifies meaningful decision times—for example, every eligible visit or a fixed monthly assessment—and constructs a trial at each time.

**Both groups within an emulated trial must assess eligibility and begin follow-up at corresponding clinical decision points.** Initiators cannot start at first use while noninitiators start at some arbitrary earlier disease stage. This note uses monthly examples, so each trial also has a common calendar baseline; the general alignment principle does not require different patients to enroll on the same calendar date.

Sequential trials commonly use multiple eligible times; if one meaningful common baseline exists, a single trial can also be emulated. They are not the only possible design for “initiate versus do not initiate.”

Original overview: [Fu, 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).

### Reading the original passage: Eligible from ages 51–65—when should follow-up start?
{: #section-2 }

Hernán and Robins' example requires postmenopausal women with no chronic disease history and no hormone use in the preceding two years. If a woman meets these criteria at ages 51, 52, and 53, each time permits a new clinical question: **For her as an eligible woman at that time, what would happen after initiating estrogen plus progestin now versus not initiating now?**

Eligibility criteria therefore need not select a unique baseline. Decisions at 51 and 53 are both meaningful, but differ in age, history, and subsequent observation windows. $$T_0$$ is **the start of follow-up for a particular trial**, not a marker a person can possess only once in life.

Two approaches are available:

| Approach | Implementation | Individual contribution |
| --- | --- | --- |
| Select one eligible time | For example, the first confirmably eligible time in the data, or one eligible time selected by a prespecified sampling rule | One enrollment with follow-up from that baseline |
| Use all or a large fraction of eligible times | For example, reassess eligibility yearly or monthly and emulate a trial starting each time | Potentially multiple enrollments, each with its own baseline, group, and follow-up |

“First eligible in the data” need not be first eligible in the person's lifetime; the protocol should specify which is meant. Randomly sampling a baseline **does not randomize treatment**. The sampling rule and corresponding target population must be explicit; later disease, eventual treatment, or completed follow-up cannot be used to choose favorable starting points.

The second approach creates **multiple nested trials—emulated trials embedded in the same cohort**, also called sequential trial emulation. Nested does not mean each later trial's population is a strict subset of its predecessor: new people can become eligible while earlier participants become ineligible. Investigators do not actually randomize patients repeatedly.

<aside class="study-callout study-callout--important" markdown="1">

**“Remains eligible” illustrates multiple possible baselines; it does not select on the future**

Do not interpret the original as “only women known to remain healthy and survive from 51 to 65 can enter the age-51 trial.” Age-51 entry uses only criteria already met then; subsequent death or disease cannot erase earlier enrollment and outcomes.

The original calls these “unbiased time-zero choices.” This means they can validly determine baseline when appropriately implemented, **not that the whole study is guaranteed unbiased**. Every emulation still needs aligned eligibility, strategy grouping, and follow-up, adequate confounding and censoring adjustment, and identification conditions. Different baselines can also change the population over which effects are averaged; see §6.

</aside>


Original source: [Hernán and Robins, 2016, Defining time zero](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf).

### How do biennial data collection and irregular medical records differ?
{: #section-3 }

The data must support emulated trial baselines.

| Data setting | Approach suggested in the original text | Limitation |
| --- | --- | --- |
| A cohort collects data at fixed rounds, such as every two years | Reassess eligibility and start a trial at each collection round | Biennial information does not justify pretending to know daily treatment and disease in between |
| Electronic records arise irregularly with visits | Prespecify a short fixed unit, such as months, and construct trials successively | Dividing time into months does not create complete monthly measurements; eligibility, treatment, and confounders must still be assessed from available information |

For example, at each month's start, investigators might assess chronic disease and treatment history from a preceding record window. Window length, whether older tests still reflect current state, and handling of insufficient information depend on the clinical question and data quality. Next month's examination cannot directly become information supposedly known at this month's baseline.

Distinguish three time concepts: **how often trials begin, how often variables are measured, and how long each trial follows participants.** Monthly trials do not imply monthly measurement or one-month follow-up. The examples below make these differences concrete.

## 2. Define each small trial's question first
{: #section-4 }

A constructed teaching setting:

- A clear clinical decision occurs at the start of each month.
- Entrants are alive, have not yet used A, and meet other clinical criteria then.
- Initiation is identifiable at that decision time, with relevant history measured beforehand.
- Each trial follows people for 12 months from its own baseline and records death.

Two different strategy contrasts are possible:

| Target question | Initiation group | Control group | Later A initiation or stopping |
| --- | --- | --- | --- |
| Effect of initiating now | Initiate A now, then follow usual care | Do not initiate A now, then follow usual care | Retain this trial's baseline groups; no protocol censoring for subsequent changes |
| Sustained-strategy PP | Initiate now and continue A according to protocol while alive | No A use during this trial's follow-up | Artificially censor at deviation from this trial's strategy and address the selection introduced |

“Do not initiate now” permits later initiation; “no use for the next 12 months” does not. **This changes the research question itself, not merely an analysis detail.**

The first may be called an observational analog of ITT, but grouping still uses actual initiation without the guarantee of real randomized assignment. See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).

The **per-protocol (PP) effect** depends on the protocol: when it specifies only the initial action, adherence requires only that action; when it specifies actions throughout follow-up, ongoing adherence to those rules is required. See [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}).

## 3. How can one person enter several trials?
{: #section-5 }

Suppose Li:

- Is eligible on January 1 but does not initiate A;
- Remains eligible on February 1 and still does not initiate;
- Remains eligible on March 1 and initiates A at that day's decision;
- Is already a user in April.

Then:

| Emulated trial | Can Li enter at this baseline? | Group within this trial | Follow-up starts |
| --- | --- | --- | --- |
| January | Yes | Do not initiate now | January 1 |
| February | Yes | Do not initiate now | February 1 |
| March | Yes; eligible before initiation | Initiate now | March 1 |
| April | No under this example's “has not yet used A” criterion | — | — |

Under the original “no hormones in the preceding two years” criterion, April would likewise be ineligible because use occurred during that period. This does not mean “once treated, never eligible again”: after stopping and again satisfying two years of nonuse plus other criteria, reentry depends on the protocol.

Each trial uses history available before its decision. Li's February disease can be baseline information for February, but must not be backfilled into January's baseline. The “trials” are investigator-created data structures; Li is not actually randomized repeatedly.

<pre class="mermaid">flowchart LR
    J[&quot;January: Eligible, no initiation&quot;] --&gt; J1[&quot;Trial 1: Noninitiation group; follow-up clock starts&quot;]
    F[&quot;February: Still eligible, no initiation&quot;] --&gt; F1[&quot;Trial 2: Noninitiation group; follow-up clock restarts&quot;]
    M[&quot;March: Eligible, initiates A&quot;] --&gt; M1[&quot;Trial 3: Initiation group; follow-up clock restarts&quot;]</pre>

**Starting a trial every month does not limit each trial to one month of follow-up.** Here every trial can follow participants for 12 months, producing overlapping intervals.

For example, January's trial does not automatically end when March's begins. It has observed two months and continues according to its own endpoint rules. **trial_id distinguishes questions with different baselines; it does not partition the calendar into nonoverlapping pieces.** This explains why a person's later outcome can appear in multiple trial records and why §6 must handle their dependence.

## 4. After Li starts in March, what happens to earlier trial records?
{: #section-6 }

### If the comparison is only “initiate now versus do not initiate now”
{: #section-7 }

Li remains in the noninitiation groups of January and February, because he truly did not initiate at those trials' time zeros. March initiation is part of later usual care.

In the separately defined March trial, he belongs to the initiation group from the start.

He is contributing to different baseline decisions, not simultaneously serving as treatment and control within one trial.

### If the comparison is “initiate and continue versus no use during follow-up”
{: #section-8 }

Li's March initiation violates the “no A use” strategies in January and February. Therefore:

- January trial: retain follow-up from January until just before March initiation; artificially censor at initiation.
- February trial: retain follow-up from February until just before March initiation; artificially censor at initiation.
- March trial: continue follow-up as an initiator; handle any later violation of sustained-use rules according to that trial's protocol.

This **artificial censoring** retains pre-deviation follow-up but stops using later factual records to directly represent the original strategy. If worsening disease prompts Li to initiate A, censored records may come from people with poorer prognosis. Appropriate correction, such as inverse probability of censoring weighting (IPCW), is needed. **Sequential construction solves enrollment timing; it does not automatically solve noncomparability from initial treatment selection or later protocol deviations.**

Likewise, if a March initiator later develops a protocol-permitted contraindication and stops, that is rule-following; “stopping” alone should not establish deviation.

Methodological source: [Keogh et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC7614580/).

## 5. Does repeated enrollment create immortal time?
{: #section-9 }

When implemented appropriately, repeated entry itself does not create immortal time.

Suppose Li dies on February 15:

- The death remains an outcome in January and February, which he already entered.
- He cannot enter March because he is no longer eligible then.
- Survival until March is not required to retain January or February records.

Each trial asks: **Among people eligible at this time, what would happen under different strategies?**

But to answer the effect of “delay treatment from January until March,” deaths while waiting need explicit handling; outcomes only among March survivors cannot substitute for that answer.

<aside class="study-callout study-callout--important" markdown="1">

**“Initiate at the start of the month” and “initiate during the month” are different strategies**

Looking across an entire month and labeling anyone who starts A on any day as an initiator from the month's start can again mishandle deaths between baseline and actual initiation.

Use sufficiently precise decision times; if the strategy intentionally allows initiation “within this month,” formally handle the grace period, for example using [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) within each small trial. Additional handling depends on data precision and strategy definition; monthly grouping alone does not establish alignment.

</aside>


## 6. What is required when pooling trials?
{: #section-10 }

### Why might multiple baselines improve efficiency?
{: #section-11 }

With only each person's first eligible time, Li contributes only January's noninitiation entry. Multiple times additionally use his continued noninitiation in February, initiation decision in March, and outcomes from those new baselines.

This uses more decision opportunities relevant to the question and generally increases information available for estimation. Here **statistical efficiency** means potentially greater precision for comparable estimation tasks, such as smaller standard errors—not faster computing.

It is not guaranteed. Record dependence, treatment and outcome distributions, weight stability, and model specification all affect precision. In particular, “1,000 people with 5 entries each” is not “5,000 independent patients.”

### Each trial must address its own baseline confounding
{: #section-12 }

A patient's disease changes, so each trial uses history before its corresponding baseline to address noncomparability of current initiators and noninitiators. At least two distinct stages matter:

| Stage | Potential problem | Common approach |
| --- | --- | --- |
| Each trial's baseline | Disease differs between initiators and noninitiators | Adjust, standardize, or apply treatment weights using confounders preceding that decision |
| Sustained-strategy follow-up | Artificially censored deviators differ in prognosis from those remaining | Estimate compatibility probabilities from prior history and use IPCW or another appropriate method |

Loss to follow-up requires separate attention to its selection mechanism. IPCW alone does not automatically control baseline treatment confounding in each trial; baseline adjustment alone does not handle later selection when disease leads to stopping. See [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) for the methods' roles.

### Distinguish two times
{: #section-13 }

- **Calendar time of trial baseline:** for example, January versus March trials.
- **Follow-up time within the trial:** for example, months 1, 2, and 3 after entry.

Calendar periods can correspond to different care settings; follow-up time measures elapsed time since the strategy decision. Common pooled models account for trial baseline and follow-up time and specify which parameters are shared across trials.

Pooling aims to use multiple eligible decision times more fully; it does not assume unconditionally that every trial has the same effect.

### Multiple records from one person are not independent patients
{: #section-14 }

Common data identifiers include:

| Field | Purpose |
| --- | --- |
| person_id | Original patient; used to handle within-person dependence |
| trial_id | Which baseline trial the person entered |
| followup_time | Time since that trial's time zero |
| baseline_history | History preceding that trial's assignment |
| strategy | Strategy assigned analytically at that trial's baseline |
| censor / outcome | Censoring and outcome within that trial follow-up |

For example, in §4's “initiate now” analysis, if Li dies on June 1, the death may appear in January, February, and March follow-up, at 5, 4, and 3 months after each respective baseline. These are outcome records for different starting points, **not three independent deaths among three people**. For sustained-strategy effects, §4 determines which records were already censored for deviation.

Records from one person share disease and outcomes, so uncertainty estimation must account for their dependence:

- **Appropriate variance estimation clustered by original patient:** permit correlation across one person's trials and follow-up times; the estimator must also appropriately account for steps such as weight estimation.
- **Bootstrap entire original patients:** sample patients with their full records, reconstruct emulated trials, estimate required weights and outcome models, and use variation across repeated estimates to measure uncertainty. Do not resample expanded trial records as independent patients.

The original's adjustment of the **variance estimator** concerns the reliability of standard errors and confidence intervals. A standard error is the square root of an estimator's sampling variance; 95% confidence intervals use this uncertainty information. Incorrectly treating all records as independent may overstate information and produce overly narrow intervals, depending on the correlation and estimator.

**Handling dependence does not replace confounding control.** A different standard-error algorithm cannot turn a confounded comparison into a causal effect. Report independent patient counts separately from patient–trial enrollment records.

Methodological source: [Keogh et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC7614580/). Performance of inference methods also depends on sample size, event counts, and other conditions; see [Limozin, Seaman, and Su, 2025](https://journals.sagepub.com/doi/abs/10.1177/09622802251356594).

### Specify the population to which results apply
{: #section-15 }

A person eligible for a long time may contribute many decisions, while another contributes once. Simply pooling all records therefore does not automatically yield an effect that weights each member of the original patient population equally.

For example, Patient A is eligible at 10 baselines and Patient B at 1. Equal averaging of eligible decision records gives A 10 contributions and B 1, unlike equal averaging over the two people at one specified baseline.

A first-eligible-time analysis is closer to “decide when first eligible”; multiple-baseline analysis can average decision effects across different ages, disease states, and calendar periods. If effects vary with these factors, the average effects may differ. We cannot promise “the same result, only more precise.” Patient-clustered standard errors do not change that target distribution.

Specify whether averaging concerns all eligible decision times or a particular baseline population. Where needed, **standardize** model predictions to a defined population: predict outcomes under each strategy for the same target people and average. See [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}) for the intuition.

For detailed pooling and standardization methods, see [Keogh et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC7614580/). For data expansion, weights, and marginal-risk estimation implementation, see the [TrialEmulation methods paper](https://arxiv.org/abs/2402.12083).

## 7. How can this combine with the other designs?
{: #section-16 }

- If each decision compares new A versus B initiation, combine [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}) with sequential trials.
- If each compares “initiate within 30 days” with “do not initiate,” clone, censor, and weight within every sequential trial.
- If current treatment already distinguishes groups but sustained adherence is required, protocol-deviation censoring and weighting may suffice without cloning.

Here sequential trials means **emulating trials at multiple baselines**. It is not a group-sequential randomized-trial design that permits early stopping after interim analyses, nor does it mean repeatedly randomizing the same patient in reality.

## Sources
{: #section-17 }

- [Hernán MA, Robins JM. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available (2016)](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf). See “Eligibility criteria are met at multiple times” on page 761.
- [Fu EL. Target Trial Emulation to Improve Causal Inference from Observational Data: What, Why, and How? (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).
- [Keogh RH et al. Causal inference in survival analysis using longitudinal observational data: Sequential trials and marginal structural models (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7614580/).
- [Su L et al. TrialEmulation: An R Package to Emulate Target Trials for Causal Analysis of Observational Time-to-event Data (2024, preprint)](https://arxiv.org/abs/2402.12083).
- [Limozin JM, Seaman SR, Su L. Inference procedures in sequential trial emulation with survival outcomes: Comparing confidence intervals based on the sandwich variance estimator, bootstrap and jackknife (2025)](https://journals.sagepub.com/doi/abs/10.1177/09622802251356594).

Li and the monthly decisions are constructed teaching examples; actual enrollment frequency should depend on real decision processes and data precision.
