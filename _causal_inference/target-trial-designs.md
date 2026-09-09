---
layout: "causal-note"
title: "Comparing Three Target Trial Emulation Designs"
description: "Compare active-comparator new-user, sequential-trial, and clone–censor–weight designs by the data problems they address."
group: "Trial design"
order: 15
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Comparison table", "anchor": "section-1"}, {"title": "2. Three questions for selecting design components", "anchor": "section-2"}, {"title": "3. How do the two forms of “repeated records” differ?", "anchor": "section-3"}, {"title": "4. Connections to ITT, PP, and three time-related biases", "anchor": "section-4"}, {"title": "5. Judgments required by every design", "anchor": "section-5"}, {"title": "6. Self-check", "anchor": "section-6"}]
previous_note: "/causal-inference/inverse-probability-weighting/"
next_note: "/causal-inference/active-comparator-new-user/"
---

Study entry point: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Start with what each design addresses**

**ACNU: Who is compared, and how both groups enter at treatment initiation.**

**CCW: How to allocate records and handle later deviations when multiple strategies are compatible at baseline.**

**Sequential trials: Which times can serve as entry points when one person repeatedly meets eligibility criteria.**

They can be combined; they are not three mutually exclusive choices.

</aside>


First understand “align eligibility, strategies, and the start of follow-up” in [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}), then read this overview. The designs address different parts of the research process, so define the question before selecting components. None randomizes actual clinical care.

<aside class="study-callout study-callout--tip" markdown="1">

**Suggested reading order**

Begin with the intuitive ACNU design and its two new-user cohorts; then learn sequential trials, which establish different starting points for repeatedly eligible people; finally study CCW for multiple strategies compatible at a common starting point. The order of names below follows the original article, not their difficulty.

</aside>


## 1. Comparison table
{: #section-1 }

| Design | Common question | How is baseline established? | Main design issue addressed |
| --- | --- | --- | --- |
| [ACNU: Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}) | Start A or start B for a similar indication? | When each group initiates its respective treatment | Improve clinical comparability and avoid mixing users at different treatment stages |
| [CCW: Clone, Censor, Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) | Surgery within 30 days versus no surgery for 90 days; medication for 6 versus 12 months; different dynamic initiation rules | A common eligibility decision point when strategies can be chosen, potentially before actual treatment | Baseline strategy ambiguity, grace periods, and sustained-strategy compatibility; correct selection from artificial censoring |
| [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}) | At each eligible time, initiate now or not now? | A sequence of prespecified eligible decision times | Repeated eligibility, time zero for noninitiators, and use of information from multiple baselines |

These are typical applications. All three require alignment of eligibility, strategy grouping, and follow-up start, with corresponding confounding adjustment. **A “common starting point” means the same clinical decision point; different patients may reach it on different calendar dates.**

## 2. Three questions for selecting design components
{: #section-2 }

1. **Are you comparing initiation of two reasonable alternative treatments?**<br>
   Consider ACNU so both groups enter at similar clinical decisions and new-user stages.

2. **Is a patient's baseline treatment history compatible with several strategies?**<br>
   For “initiate within 30 days,” actual treatment on day 0 may not uniquely determine group membership. Consider CCW to use records according to strategy compatibility.

3. **Can a person be eligible at several times?**<br>
   Consider sequential trials at those times. Each trial still needs appropriate baseline assignment, grace-period handling, and management of subsequent deviations.

All three answers can be “yes.” For example, start a trial each month among eligible patients who have used neither A nor B, comparing “start A within 30 days” with “start B within 30 days.” A and B are reasonable alternatives, and before initiation a patient may be compatible with both. This combines the three design ideas; it extends them to initiation grace periods rather than standard ACNU grouping by first prescription. Timing within the window and handling of early death still need full definition.

## 3. How do the two forms of “repeated records” differ?
{: #section-3 }

| Repetition | Person | Baseline | Strategy |
| --- | --- | --- | --- |
| CCW cloning | Same person | Same time zero | One copy for each compatible strategy |
| Repeated entry in sequential trials | Same person | Several different time zeros | Grouped within each trial using information available then |

Neither increases the number of independent patients. In combined designs, “original patient ID—trial baseline—strategy copy” can identify records, with within-person dependence handled in statistical inference.

## 4. Connections to ITT, PP, and three time-related biases
{: #section-4 }

| Concept already studied | Connection here |
| --- | --- |
| [ITT and PP]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}) | Design names do not determine the effect. ACNU and sequential trials can compare natural processes after initiation or sustained strategies; CCW generally targets PP adherence effects. Observing initiation is not observing randomized assignment |
| [Immortal Time Bias]({{ "/causal-inference/time-related-biases/" | relative_url }}) | Do not backfill baseline groups using future treatment completion. CCW explicitly handles outcomes before treatment, while sequential trials establish baselines for current decisions |
| [Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}) | New-user designs avoid treating long-term tolerant users as new initiators, though risk-set selection can still occur during follow-up |
| [Lead Time Bias]({{ "/causal-inference/time-related-biases/" | relative_url }}) | Early-versus-late strategies still need a meaningful common baseline; survival durations starting at different disease stages do not directly establish life extension |

## 5. Judgments required by every design
{: #section-5 }

- Are interventions and the target population clearly defined?
- Which baseline or time-varying variables are needed for confounding control?
- Is there sufficient treatment-choice overlap or opportunity to adhere under relevant histories?
- Is the ordering of loss to follow-up, protocol deviations, and outcomes handled correctly?
- For which population, horizon, and strategies does the final analysis estimate a risk difference or other effect?

Return to [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}): these designs organize observational data sensibly, but causal interpretation still requires exchangeability, positivity, consistency, and other assumptions.

Once data are organized, estimation methods must also be chosen. For example, [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) can address treatment selection or censoring; the [g-formula]({{ "/causal-inference/g-formula/" | relative_url }}) can predict and average outcomes under different strategies; and a [Cox model]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}) can analyze outcomes. These occupy a different level from the three designs and cannot replace them.

For example, “emulate initiate-now versus do-not-initiate trials sequentially, use IPW for relevant treatment selection, and estimate one-year risk differences with a weighted outcome model” is an analysis approach that can be further specified. **Sequential trials arrange entry opportunities, IPW is an adjustment method, and the risk difference is an effect scale.** Saying only “I used Cox” or “I used CCW” does not fully specify the research question.

## 6. Self-check
{: #section-6 }

1. Why can ACNU not guarantee elimination of all confounding by indication?
2. Under “surgery within 30 days,” should a patient dying without surgery on day 5 be directly excluded from that strategy?
3. Why is cloning and censoring without considering weighting insufficient for CCW?
4. Can a patient belong to the noninitiation group in January's trial and the initiation group in March's?
5. Does starting a trial every month restrict each trial to one month of follow-up?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. Initiation of A or B still depends on disease and other factors; reasonable alternatives only make exchangeability more plausible.
2. No. If compatible until death, the death is an outcome that must be counted under that strategy.
3. Artificial censoring may select people by prognosis and requires correction under corresponding assumptions. A simple analysis may work if censoring is truly independent of relevant prognostic factors, but that cannot be assumed.
4. Yes; these are trials with different baselines. How the earlier trial handles later initiation depends on its subsequent strategy.
5. No. Each trial can have a longer prespecified follow-up, with overlapping intervals.

</details>


Overview source: [Fu EL. Target Trial Emulation to Improve Causal Inference from Observational Data: What, Why, and How? (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/). See each design's note for specific sources and examples.
