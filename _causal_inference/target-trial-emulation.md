---
layout: "causal-note"
title: "Target Trial Emulation"
description: "Align eligibility, strategy assignment, and follow-up to translate a causal question into an observational study."
group: "Trial design"
order: 8
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. First understand the symbols in the figure", "anchor": "section-1"}, {"title": "2. Upper panel: Why is aligning the three elements easier in a randomized trial?", "anchor": "section-2"}, {"title": "3. Lower panel: What is \\(A_S\\) in an observational study?", "anchor": "section-3"}, {"title": "4. What happens without alignment? An immortal-time-bias example", "anchor": "section-7"}, {"title": "5. Connection to ITT and PP: Two different levels of question", "anchor": "section-9"}, {"title": "6. Follow-up origins, endpoints, and censoring", "anchor": "section-10"}, {"title": "7. Seven questions to ask when revisiting the timing", "anchor": "section-20"}, {"title": "Sources", "anchor": "section-21"}]
previous_note: "/causal-inference/pragmatic-trials/"
next_note: "/causal-inference/hormone-therapy-target-trial/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

The first step in **target trial emulation (TTE)** is to express the research question as a hypothetical randomized-trial protocol: who can participate, which treatment strategies are compared, how they are assigned, when follow-up begins and ends, which outcomes are observed, which causal effect is targeted, and how it will be analyzed. The second step maps the available observational data to each protocol component, including conditions that cannot be faithfully implemented.

For example, “Does drug B work?” is insufficiently specific. “Among patients eligible today, what is the effect of initiating B versus A on one-year mortality risk?” describes a question for which a study can be designed. TTE organizes questions and data; it is not a particular statistical model and does not turn observational data into truly randomized data.

<aside class="study-callout study-callout--abstract" markdown="1">

**This note's focus: Put the study clock in the right place**

In the target trial and its observational emulation, align three things at **$$T_0$$, the start of follow-up**:

**Eligible at this time → assigned or mapped to a treatment strategy at this time → outcomes counted from this time.**

Align the clinical decision point for the two strategies, such as “deciding which drug to initiate when eligible.” This does not require everyone to enroll on the same calendar date. Time alignment prevents some design biases but does not automatically remove confounding.

**A strategy applying from $$T_0$$ does not require medication, surgery, or dialysis to begin immediately at $$T_0$$.** If the rule is “wait, then start dialysis when specified conditions are met,” waiting is already part of the strategy. Strategy assignment and follow-up origin must align, not necessarily the dates of every treatment action.

</aside>


<aside class="study-callout study-callout--tip" markdown="1">

**First reading**

Read §1–5 first: begin with the three timing elements in the figure, then examine observational grouping and incorrect grouping. If you wonder “Do we look at future treatment before enrolling people?”, focus on the three supplementary subsections in §3. Then read §6.2–§6.5 to distinguish events, loss to follow-up, and discontinuation. The passage translation in §6.1 and formula in §6.6 can wait until a second reading; the entire note need not be read consecutively before continuing.

</aside>


Prerequisite: [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}). For effect definitions, see [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}); for specific designs, see [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}).

For the meaning of pragmatic trial in the original passage, and why targets emulated with routine data often have pragmatic features, see [Pragmatic Trials in Routine Care]({{ "/causal-inference/pragmatic-trials/" | relative_url }}).

For a complete example, see [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}). It brings together the seven protocol elements to practice distinguishing safety-related discontinuation, protocol deviation, end of follow-up, and ITT/PP analysis requirements.

Read those seven elements in this logical sequence: **define the population and strategies; then define the effect, starting point, and outcome; finally assess whether existing data and analysis methods can support the target.** This is a checking aid. Actual design usually requires revisiting the question and data repeatedly; filling in a table once does not complete the emulation.

After reading, extend by topic: timing errors in [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}); intervention and adjustment-variable definitions in [Biomarkers and Well-Defined Interventions]({{ "/causal-inference/biomarkers-well-defined-interventions/" | relative_url }}) and [Confounding and Treatment Components: Kidney Transplantation]({{ "/causal-inference/confounding-treatment-components/" | relative_url }}); outcome measurement and bias checks in [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}) and [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}).

For literature extensions, see [High-Throughput Drug Screening and Federated Target Trial Emulation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}), which develops a discussion around two papers on high-throughput drug screening and multicenter federated TTE. Its [Placement of IPTW in the TTE workflow]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-4) explains why weighting is planned at the protocol stage, applied to confounding adjustment after observational grouping, and incorporated into outcome analysis.


Multivariable calculation example: [A complete multivariable LR-IPTW example comparing drugs A and B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) shows how baseline characteristics of 3,000 people enter one common logistic regression to produce propensity scores, both groups' weights, balance diagnostics, and one-year risks. Z=0 denotes drug B, not no treatment.

## 1. First understand the symbols in the figure
{: #section-1 }

![Time-zero alignment in a randomized trial and its observational emulation]({{ "/assets/causal-inference/target-trial-time-zero-alignment.png" | relative_url }})

This image corresponds to [Figure 1 in Fu (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/#F1), comparing the timing of randomized trials and observational emulations.

| Symbol in the figure | Meaning | Intuition |
| --- | --- | --- |
| $$E$$ | Meeting eligibility criteria | Does this person meet the study requirements at this time? |
| $$A_R$$ | Randomized treatment assignment | Randomly determine the treatment-strategy group |
| $$A_S$$ | The researcher determines the analysis group using records and prespecified strategies | Which strategy permits the patient's actions up to this point? Initially, more than one may be compatible |
| $$T_0$$ | Time zero, the follow-up origin, also called baseline | Start accumulating time at risk and counting outcomes here |
| Two lines after the split | Follow-up over time in the two strategy groups | For example, initiating B versus initiating A |
| Tombstone symbol | Death illustrates the study outcome | It does not mean every participant must die for the study to finish |

The line on the left can be understood as prebaseline experience and records used to assess medical history, medication history, and similar information. The branches schematically show follow-up for two groups; they do not show both potential outcomes observed in the same person, and they are not survival curves.

## 2. Upper panel: Why is aligning the three elements easier in a randomized trial?
{: #section-2 }

Suppose the target trial asks whether initiating B versus A changes one-year mortality risk among eligible patients not yet using either drug.

At randomization:

1. **$$E$$: Confirm eligibility at that time.**
2. **$$A_R$$: Randomize to strategy B or A.**
3. **$$T_0$$: Begin follow-up and count subsequent deaths.**

The figure therefore places $$E$$, $$A_R$$, and $$T_0$$ at the same position.

“Confirm eligibility” does not mean all examinations must occur that day. Earlier examinations and medical history can be used, but the patient must satisfy the criteria at $$T_0$$; eligibility cannot require surviving an additional future period.

<aside class="study-callout study-callout--important" markdown="1">

**Assignment to a strategy is not immediate receipt of treatment**

If the protocol allows “start medication within seven days after randomization,” the strategy is assigned at $$T_0$$, while the first dose may come later.

If death is the outcome, deaths after randomization but before medication initiation must also be counted. Waiting until medication is actually taken to begin follow-up would omit that period of risk.

</aside>


**Early versus late dialysis makes the distinction clearer:** patients may become trial-eligible at eGFR 18 and be assigned to “wait until the early-initiation range” or “wait until the late-initiation range.” Both rules apply today, while both currently require no dialysis. Eligibility asks “Who can participate in this decision now?” Initiation conditions ask “Under the assigned rule, when should dialysis start?” See [Why is time aligned even though dialysis has not begun at enrollment?]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-24).

## 3. Lower panel: What is $$A_S$$ in an observational study?
{: #section-3 }

Observational studies generally use clinical records of events that have already occurred. Researchers did not personally randomize patients to A or B; actual treatment may have been determined jointly by physicians, patients, severity, resources, and other factors.

Researchers **map existing records to target-trial strategy groups using predefined rules**.

For a simple new-user design comparing “initiate B versus initiate A,” the mapping can be:

| Target trial operation | Observational counterpart |
| --- | --- |
| Confirm eligibility at enrollment | On the day the patient starts A or B, check eligibility using records from that day and earlier |
| Randomly assign A or B | Map to the corresponding strategy using actual recorded treatment initiation |
| Begin follow-up at random assignment | Begin follow-up on the corresponding treatment-initiation date |
| Compare outcomes between groups | Estimate the target contrast after addressing appropriate confounders |

This is a simple implementation of $$A_S$$: a prespecified initiation rule determines the group. If baseline is compatible with several strategies, different strategy copies can first be created and assessed for deviation over time; see [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}).

**The most important similarity between the panels is their timing structure; the most important difference is their grouping mechanism.** Even with $$T_0$$ aligned in the lower panel, severity, age, or other factors may make the groups nonexchangeable, so confounding still requires consideration.

<aside class="study-callout study-callout--note" markdown="1">

**Align each person's study time, not calendar dates**

One person may enter on March 1 and another on May 1. For both, $$T_0$$ means “the time when this person is eligible, mapped to a strategy, and begins follow-up.”

$$T_0$$ also need not be the first eligible date in a person's lifetime; its selection depends on the target trial's enrollment rules.

</aside>


### Do we look at future treatment before deciding who enrolls? Distinguish two kinds of time
{: #section-4 }

**Researchers can inspect the complete historical clinical record, but cannot simply use a patient's later successful treatment to retroactively determine eligibility and group membership at an earlier starting point.** What matters is where information falls relative to the chosen $$T_0$$ and how it is used.

There are two different sequences:

- **The computer-query sequence**: which query is run or table read first;
- **The patient's timeline**: relative to this emulated trial's $$T_0$$, which events have occurred and which are still future.

TTE requires the second timeline to be appropriate; it does not require code to query eligibility before medication.

For example, researchers in 2026 analyzing 2020 records to compare “initiate A” with “initiate B” may first search the entire database for initiation dates, then look back before each date to assess eligibility. Suppose Li initiates A on March 1, 2020 and meets eligibility criteria immediately beforehand. **March 1 can serve as $$T_0$$ for this initiation comparison**, placing Li in group A with follow-up beginning then.

Although the medication record was found first, grouping uses **the initiation action at $$T_0$$**, not future medication after $$T_0$$.

Conversely, if the intended question is “From the clinical decision on January 1, what happens under initiation versus noninitiation?”, classifying Li as an A recipient from January because he successfully starts A in March uses future treatment success to backfill earlier group membership. These designs have different questions and starting points and are not interchangeable.

**Early versus late dialysis is an example requiring a common earlier start.** The analysis begins when patients are not on dialysis and first meet eligibility, using records according to their compatibility with the early and late strategies. It cannot restrict to future dialysis recipients and backfill groups using their eGFR at actual initiation. For the eGFR 18 → 12 → 9 → 6 timeline, see [Enrollment and assignment for early versus late dialysis, step by step from a common origin]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-18).

### Eligibility, strategy grouping, and subsequent deviation are three separate operations
{: #section-5 }

| Operation | What does it ask? | How is information used? |
| --- | --- | --- |
| Assess eligibility for this trial instance | At this $$T_0$$, does the patient belong to the target population? | Use criteria already met and prior history, such as age, previous diseases, and medication in the past two years |
| Determine the strategy group in the analysis | Which strategy's initial actions are compatible with the current record? | Use current actual initiation, prescriptions, or other protocol-defined information; if several strategies fit, create several strategy copies |
| Assess deviations during follow-up | Do later treatment actions violate this copy's rules? | Use follow-up treatment and relevant medical history to determine when deviation occurs, then decide artificial censoring and adjustment according to the target effect |

These cannot be collapsed into “see which treatment the patient ultimately receives, then decide whether to include them from the start.” In some new-user designs, initiating a candidate drug at that time also determines entry into that specific comparison; this is still an action condition at baseline, not a requirement to complete treatment successfully in the future.

Also distinguish two meanings of “assignment”: **assignment in a real randomized trial determines which treatment strategy is offered; grouping in observational TTE usually maps events that already occurred to analytical strategies**. The latter does not control actual care, so confounding between treatment choice and prognosis must still be addressed.

### Later treatment during a grace period can determine when compatibility ends
{: #section-6 }

Suppose $$T_0$$ is January 1, comparing “initiate A within the next three months” with “do not initiate A during study follow-up.” Li is eligible and untreated at $$T_0$$, so both strategies are compatible at this point.

Under CCW, create two copies at $$T_0$$, without needing to know whether Li eventually starts treatment:

| Actual course observed after baseline | Copy assigned to initiate within three months | Copy assigned never to initiate |
| --- | --- | --- |
| No initiation in month one | Retain | Retain |
| Actual initiation in month three before the deadline | Continue follow-up according to protocol | Artificially censor at actual initiation |
| Alternative course: death in month two, before initiation and without other deviation | Retain the death event if death is the outcome | Retain the death event here too |

The month-three medication information is used, but determines **which copy ceases to represent its strategy from that time onward**. It does not determine Li's January eligibility or erase his first two months of contribution. Selection following artificial censoring must also be adjusted appropriately; see [Reading the passage: Initiation, noninitiation, and death within a three-month grace period]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-7).

“Censor from this time” is an analysis rule, not a reassignment of actual treatment. If the target is a baseline-initiation effect with usual care thereafter, later initiation or discontinuation need not trigger protocol-deviation censoring. The rule depends on the [specific target strategy]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}).

Thus, **follow-up records may be inspected; future treatment success, survival, or adherence cannot be used as requirements for earlier enrollment**. Subsequent records still count outcomes, update treatment and confounder histories, determine censoring, and serve other purposes; the methods must match the target effect.

In a [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}), information from March can also become baseline information for a “new March trial,” but cannot be treated as known at baseline for the “January trial.” Whether information is future always depends on a particular emulated trial's $$T_0$$.

For the theoretical basis of these distinctions, see [Hernán and colleagues, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/); for the original discussion of grace periods and strategy compatibility, see [Hernán and Robins, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).

## 4. What happens without alignment? An immortal-time-bias example
{: #section-7 }

The following invented example asks whether drug B reduces 30-day mortality among hospitalized patients.

A problematic design would:

- Begin follow-up for everyone **on admission**.
- Then inspect records across the entire hospitalization.
- Classify everyone who “ever received B during hospitalization” as treated from the admission day.
- Classify those who “never received B during hospitalization” as untreated.

Consider two patients:

| Patient | Day 0 | Subsequent course | Group under this method |
| --- | --- | --- | --- |
| Patient A | Admitted and eligible | Starts B on day 7, dies on day 20 | Counted as treated from day 0 |
| Patient B | Admitted and eligible | Dies on day 3, before receiving B | Untreated |

**The problem is patient A's time from day 0 until just before day 7.**

Patient A must first survive until B initiation to qualify for the “ever-treated” group under this rule. If death occurred earlier, the patient would be classified as untreated. Under this grouping rule, therefore, no death before an individual's actual initiation can be counted in the treated group.

This is **immortal time**: patients are not literally unable to die; the analysis rule prevents those who die early from entering that group. Incorrectly assigning this period to treated follow-up may make B appear protective even if the drug has no effect. [Hernán and colleagues, 2016: Misaligned time and immortal time bias](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/).

### Compare this with $$T_0$$ in the figure
{: #section-8 }

The flawed design starts follow-up on day 0 but waits for the future to determine “who is treated.” In other words:

**Follow-up has begun, while group membership depends on what happens later.**

Placing the figure's three elements together is therefore not a layout detail. It reminds us not to use future successful treatment to backfill all prior time into treated follow-up while allowing early deaths only in the comparator group. The problem is this misuse of future information, not a prohibition on analyzing treatment history during follow-up.

<details class="study-callout" markdown="1">
<summary>What if the actual question is “start treatment within seven days”?</summary>

Define “initiate B within seven days” as a strategy with a **grace period**, rather than requiring everyone to start on day 0.

In observational data, however, early records may be compatible with multiple strategies, so groups cannot simply be backfilled according to eventual treatment. One approach is [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}): create copies for compatible strategies, censor a copy when it deviates from its strategy, then use appropriate weighting to address selection from censoring.

This approach still counts outcomes from a common $$T_0$$ and requires corresponding identification assumptions. The point is to define strategies and handle early risk correctly, not retrospectively delete the waiting period. [Hernán and colleagues, 2016: Handling grace periods](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/).

</details>


## 5. Connection to ITT and PP: Two different levels of question
{: #section-9 }

First read [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}) for why the causal contrast is a design element and how it affects data requirements, deviation handling, analysis, and interpretation.

[Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}) asks **which effect we want to estimate**:

- ITT: the effect of assignment to strategy B versus A.
- PP: the effect if the target population follows B's protocol versus A's; in a randomized trial, retain the protocol-defined assignment and care context as well.

This figure asks **at which time we define the study population, map it to strategies, and begin counting outcomes**.

In a randomized trial, someone may be assigned B at $$T_0$$ but die before the first dose. In an ITT analysis with death as the outcome, they remain in the original B group and the death must not be omitted. This differs precisely from the erroneous rule requiring future actual B use for B-group membership.

For PP, retaining only “people who survive and complete treatment” is also inappropriate because it selects on future survival and adherence. Proper handling of deviations requires the target strategy and appropriate analytical methods.

$$A_S$$ in panel B does not conjure up real random-assignment records. Adopting panel B's timing structure therefore does not establish identification of exactly the same ITT effect as a randomized trial; one must still specify what was actually observed and which causal contrast was emulated.

## 6. Follow-up origins, endpoints, and censoring
{: #section-10 }

For how follow-up records enter survival analysis, see [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}): from “time + event indicator” to risk sets and then HRs.

<aside class="study-callout study-callout--abstract" markdown="1">

**This passage connects three concepts already learned**

The **starting point** is jointly determined by eligibility and the strategy decision.

The **observation endpoint** follows the protocol. The study outcome, a competing event, loss to follow-up, administrative cutoff, or maximum follow-up horizon may end observation of the first outcome, but have different meanings.

**PP analysis of sustained strategies** must also handle subsequent deviations. With censoring-weight methods, the first deviation prohibited by the protocol triggers artificial censoring.

</aside>


### 6.1 Paragraph-by-paragraph translation
{: #section-11 }

This passage comes from [Fu (2023): Start and End of Follow-Up](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).

Terminology:

- **RASi**: renin–angiotensin system inhibitors.
- **CCB**: calcium channel blockers.
- **Filled prescription**: a record that a prescription was dispensed and collected, unlike merely issuing a prescription; it also does not directly establish that the patient swallowed the medication.
- **Administrative censoring**: for example, a study or data-collection period ending on a predetermined date.

**First paragraph: Basic starting and ending points of follow-up**

In the randomized trial envisioned in Table 1, follow-up begins at random assignment and ends at the study endpoint, administrative censoring, or five years of follow-up, whichever occurs first.

Observational data, however, do not arise from random assignment. In an observational emulation, follow-up therefore begins when both conditions hold: (1) the patient is eligible; and (2) the patient's data are compatible with initiating treatment.

<aside class="study-callout study-callout--note" markdown="1">

**How should “initiation” here be understood?**

This passage concerns “immediately initiate RASi or CCB,” so the initial action is actual drug initiation. More generally, assess whether records meet **the initial requirements of the strategy studied**. If the strategy specifies waiting before treatment, the initial requirement may be no treatment yet. Do not generalize this passage to mean all TTE follow-up must start at the first dose or first dialysis session.

</aside>


For the specified strategies “initiate RASi only” and “initiate CCB only,” follow-up begins clearly at treatment initiation, identified using filled-prescription records. The rules ending follow-up in the observational emulation also correspond to those in the specified target trial.

**Second paragraph: A modification to the start of follow-up**

The author next introduces two modifications concerning the beginning and end of follow-up.

First, when comparing “initiate RASi only” with “do not initiate RASi,” there is no clear moment when a patient begins the action “do not initiate RASi.”

One solution is a sequential trial design: whenever a patient is eligible at a particular time, they can be classified under “do not initiate RASi” in that time's emulated trial. This uses the fact that a patient may meet eligibility criteria repeatedly.〔Original references 59, 60〕

**Third paragraph: A modification to the end of follow-up**

Second, if investigators compare “initiate RASi only and always use it during follow-up” with “initiate CCB only and always use it during follow-up,” patients must additionally be censored when they discontinue the treatment corresponding to their baseline strategy, RASi or CCB. This ends their subsequent follow-up contribution to that strategy's analysis.

<aside class="study-callout study-callout--note" markdown="1">

**“Only” does not automatically prohibit every other medication**

Here, it primarily distinguishes the RASi and CCB initiation strategies. Whether other co-medications, dose adjustments, or later combination treatment are permitted requires the complete protocol.

“Initiate RASi only” also does not automatically require “never stop thereafter”; the later explicit phrase “always use during follow-up” introduces sustained treatment.

</aside>


### 6.2 Why not choose an arbitrary date to start counting?
{: #section-12 }

At the starting point, we need to answer:

1. Is the patient eligible then?
2. Which strategy is compatible with the treatment record then?
3. Which outcomes should be counted from this point onward?

In this ACNU example without an additional initiation grace period, the date an eligible patient first collects RASi or CCB provides a clear strategy-initiation time.

For example, someone may meet the disease criteria in January but start RASi only in March. If the question concerns “initiating RASi versus initiating CCB,” enrollment should occur at the corresponding eligible initiation time; March RASi use cannot retrospectively make the person a RASi initiator from January.

Nor should the researcher wait until six months of successful use to decide whether to include the person from the first dispensing date. That selects the baseline population using future adherence and survival.

See [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}) and §4 of this note.

<aside class="study-callout study-callout--important" markdown="1">

**“Start at dispensing” is not a universal TTE requirement**

If the target strategy is “initiate within 30 days from today's eligibility,” follow-up can begin before the actual dispensing date. Outcomes while waiting must be counted correctly, usually with formal handling of the grace period, such as [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}).

The dispensing-based origin in this passage applies to its defined initiation strategies and data implementation.

</aside>


### 6.3 When does follow-up end? What does “the earliest” mean?
{: #section-13 }

First consider a simplified design with **all-cause death as the outcome and no loss to follow-up**. Let:

- $$T_{\mathrm{event}}$$: time from baseline to the study outcome;
- $$T_{\mathrm{admin}}$$: time from baseline to the predetermined data cutoff;
- Five years: each person's maximum follow-up duration.

The observed follow-up duration in the analysis is:

$$
T_{\mathrm{obs}}
=
\min\{T_{\mathrm{event}},\,T_{\mathrm{admin}},\,5\text{ years}\}.
$$

**How to read it:** $$T_{\mathrm{obs}}$$ is the observation duration available for this analysis; obs abbreviates observed, and event and admin are text labels for the event and administrative cutoff. $$\min$$ selects the smallest value, the first ending condition reached. Every term is measured from the same $$T_0$$ and must use the same unit, such as years. $$T_0$$ is the origin, whereas $$T_{\mathrm{obs}}$$ is elapsed duration from that origin. For example, if the event occurs in year four, data end in year three, and maximum follow-up is five years, then $$\min\{4,3,5\}=3$$ years, with censoring at the data cutoff; the three times are not added. The complete trajectory is imagined only to explain the minimum. In reality, it suffices to know no event occurred through year three; the actual postcensoring event year need not be known.

We do not wait for all three conditions. Whichever happens first ends the record.

| First occurrence | Why does observation end? | What is known? |
| --- | --- | --- |
| Study outcome | The target event has been observed | The event occurred at this time |
| Predetermined data-collection cutoff | Later data are outside this observation window | The period before cutoff is known; this record no longer observes what follows |
| Five event-free years of follow-up | The target horizon has been reached | No event occurred within five years; later outcomes are outside this horizon's question |

Reaching maximum follow-up can itself be considered administrative censoring. The passage lists “data or study cutoff” separately from “five years for an individual” to make all ending rules explicit.

#### An event is not the same as censoring
{: #section-14 }

In this all-cause mortality example:

- Death in year two: record an event at year two.
- Two years of follow-up at data cutoff, still alive: right-censor at year two. This means neither death in year two nor established survival through year five.
- Fully observed for five years, alive throughout: the person's five-year mortality outcome is known not to have occurred; later time is outside the target horizon.

**“Administrative” describes the cutoff reason; it does not automatically establish the independent-censoring conditions needed for every analysis.** Calendar entry time, observation windows, and their relationship to prognosis may still require appropriate design and modeling. Actual loss to follow-up also needs separate assessment and cannot all be treated as a predetermined administrative cutoff.

If the outcome is breast-cancer diagnosis, death before diagnosis is a competing event: after death, a diagnosis during life can no longer occur. Loss to follow-up merely leaves us uncertain about what happens afterward. They cannot be handled identically. See the complete example in [Death and loss to follow-up must not be conflated]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}#section-9).

#### “The same as the target trial” does not mean equal record lengths for everyone
{: #section-15 }

It means conceptual correspondence in outcome definitions, target horizon, and ending rules. It does not require identical event dates or five complete years of observation before anyone can be included.

For example, suppose a database ends in late 2030:

- Someone enrolled in late 2025 and event-free throughout may contribute five years.
- Someone enrolled in late 2028 and event-free throughout can contribute only about two years by the same cutoff.

Whether the latter can inform a five-year risk estimate depends on data support, the censoring mechanism, and model assumptions. The missing three years cannot simply be coded “no event.”

### 6.4 When does follow-up begin for noninitiators? Sequential trials provide an origin
{: #section-16 }

“Not initiating” usually is not a recorded action, so the target trial must define a meaningful decision time.

Consider prespecified assessments at the start of each month, assuming treatment initiation can be clearly identified at that point:

| Trial origin | Eligible participants at that time | Comparison within this trial |
| --- | --- | --- |
| January 1 | Eligible that day, with no prior RASi use | Initiate now versus do not initiate now |
| February 1 | Those still meeting the relevant criteria that day | Initiate now versus do not initiate now |
| March 1 | Those still meeting the relevant criteria that day | Initiate now versus do not initiate now |

Both groups in each trial begin follow-up at the same decision time. One person can be a noninitiator in January and February, then an initiator in the March trial when they actually start.

This does not mean selecting an arbitrary “day without medication,” and entry into today's noninitiation group must not require remaining untreated in the future.

Whether “do not initiate now” permits later initiation depends on the complete strategy. If the comparator requires “never initiate during follow-up,” later initiation constitutes a deviation in that trial.

See [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}) for the full process and statistical handling of repeated records. If the strategy changes to “initiate on any day during the month,” the grace period from the month's start to initiation also needs handling; group membership cannot simply be backfilled to the month's start.

### 6.5 Why does a sustained strategy add censoring at discontinuation?
{: #section-17 }

Compare two different targets:

- **Initiation effect**: initiate RASi versus CCB at baseline, then follow usual care.
- **Sustained-strategy effect**: initiate and also follow specified use rules during follow-up.

Invented example: a patient initiates RASi on day 0, stops in month three, and dies in month nine. Assume this discontinuation is not a permitted exception under the sustained protocol.

| Analysis target | What happens in month three? | How is the actual death in month nine handled? |
| --- | --- | --- |
| Initiation effect | No protocol-deviation censoring because of this discontinuation | Continue to record death in the baseline RASi-initiation group |
| Sustained-strategy PP using censoring weights | Artificially censor the strategy record in month three | Do not directly count the postdiscontinuation death as an outcome contribution under “continued protocol-adherent treatment” |

Why?

After month three, the patient's actual treatment history is no longer “continued RASi use according to protocol.” The actual death in month nine does not directly tell us **what the outcome would have been without this protocol deviation**.

Artificial censoring does not declare that the patient did not die later or that drug effects vanish immediately on stopping. It ends the use of subsequent actual records that deviate from the target strategy as direct representatives of that strategy.

**Artificial censoring in research data also does not mean stopping clinical care.**

#### Stopping follow-up alone is insufficient
{: #section-18 }

If worsening illness leads to prohibited discontinuation, those who stop may already be more likely to die. Simply censoring them may leave an increasingly healthy group. Thus, “ending follow-up” here means ending the analysis record; the resulting selection still needs attention.

The target remains outcomes if the whole target population followed the strategy, not merely a description of remaining adherers. Censoring-weight approaches also require:

1. Recording relevant baseline and follow-up history affecting discontinuation and outcomes;
2. Appropriate correction for selection caused by artificial censoring, such as inverse probability of censoring weighting (IPCW);
3. Corresponding no-unmeasured-confounding, positivity, consistency, and estimation conditions.

See [Weighting after artificial censoring]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-9) and [Hernán (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6889975/) for the principles.

Censoring weights are a common implementation, not the only way to estimate sustained-strategy effects; other appropriate g-methods use different estimation steps.

This is a distinction between target effects, not a problem unique to observational studies. Randomized trials estimating sustained-strategy PP must also handle nonadherence appropriately; baseline randomization does not justify ignoring later selection.

<aside class="study-callout study-callout--note" markdown="1">

**When does “stopping medication” count as deviation?**

It depends on the protocol. If stopping for a specified contraindication is permitted, stopping under that rule remains adherence. Pharmacy data also require definitions of days supplied and permitted refill gaps; no new prescription on a particular day does not automatically mean discontinuation.

If the outcome occurs first, record it first; later discontinuation cannot erase the event. Same-day outcomes and discontinuation also require a defined temporal order or prespecified handling rule.

</aside>


### 6.6 Adding extra censoring to the end time
{: #section-19 }

Under the sustained-strategy implementation using censoring weights above, write:

$$
T_{\mathrm{obs}}^{\mathrm{PP}}
=
\min\{T_{\mathrm{event}},\,T_{\mathrm{admin}},\,5\text{ years},\,T_{\mathrm{deviation}}\},
$$

where $$T_{\mathrm{deviation}}$$ is elapsed time from baseline to the first violation of the defined treatment strategy; $$T_{\mathrm{event}}$$ is time to the outcome and $$T_{\mathrm{admin}}$$ time to data cutoff, all in years. Superscript PP on the left labels “record duration used in this sustained-strategy PP analysis,” not exponentiation; obs still means observation. $$\min$$ selects the earliest candidate ending condition. For example, if the event is in year four and data cutoff in year three, but strategy deviation occurs in year one, that copy's record contributes only through year one. If loss to follow-up occurs, its observation-ending time must also be included. The rule does not require knowing the actual postcensoring event time.

The formula states only where a record ends; **calculating the risk among patients remaining after censoring does not by itself produce the PP effect**. For both artificial censoring and loss to follow-up, distinguish “when to stop using records” from “how to address outcome information missing as a result.”

Read alongside [Initiation effects and sustained-strategy effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-12): follow-up rules should follow the target strategy, not be changed arbitrarily after analysis.

## 7. Seven questions to ask when revisiting the timing
{: #section-20 }

1. At $$T_0$$, does the patient satisfy target-trial eligibility?
2. What determines enrollment and grouping? Is subsequent information used for compatibility at that later time, or to backfill earlier eligibility and group membership based on future successful treatment or survival?
3. Do both groups begin counting outcomes at corresponding versions of the same clinical decision point?
4. Beyond time alignment, is confounding between treatment choice and outcomes appropriately addressed?
5. Does this record end because of the outcome, a competing event, administrative cutoff, loss to follow-up, or protocol deviation?
6. Is later discontinuation allowed? Is the target an initiation effect or a sustained-treatment effect?
7. If artificial censoring follows protocol deviations, is the resulting selection also handled appropriately?

<details class="study-callout" markdown="1">
<summary>Self-check: Why might “dying before taking any medication” still count in a treatment group?</summary>

If the comparison concerns assignment to two strategies from $$T_0$$, all relevant deaths after assignment belong to the research question, including deaths while awaiting treatment. Group membership must follow the target strategy and valid assignment or emulation rules, not whether someone later survives until medication initiation.

</details>


## Sources
{: #section-21 }

- [Fu EL. Target Trial Emulation to Improve Causal Inference from Observational Data: What, Why, and How? (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).
- [Hernán MA, Robins JM. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).
- [Hernán MA et al. Specifying a Target Trial Prevents Immortal Time Bias and Other Self-Inflicted Injuries in Observational Analyses (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/).
- [Hernán MA. How to Estimate the Effect of Treatment Duration on Survival Outcomes Using Observational Data (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6889975/).

The admission-medication example, specific dates, and postdiscontinuation death timings are teaching assumptions illustrating record rules, not clinical research results.
