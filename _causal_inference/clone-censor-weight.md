---
layout: "causal-note"
title: "Clone–Censor–Weight"
description: "Represent compatible strategies with copies, censor at deviations, and weight appropriately for grace periods and sustained strategies."
group: "Trial design"
order: 18
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Why is this design needed?", "anchor": "section-1"}, {"title": "2. Clone: Copy records and assign strategies at baseline", "anchor": "section-4"}, {"title": "3. Censor: Censor the copy at its first strategy deviation", "anchor": "section-6"}, {"title": "4. Weight: Why is weighting needed after censoring?", "anchor": "section-9"}, {"title": "5. Which assumptions does weighting require?", "anchor": "section-11"}, {"title": "6. Why does it generally estimate a per-protocol strategy effect?", "anchor": "section-12"}, {"title": "7. Three applications: Dialysis timing, treatment duration, and dynamic rules", "anchor": "section-16"}, {"title": "8. Difference from sequential trials", "anchor": "section-33"}, {"title": "Sources", "anchor": "section-34"}]
previous_note: "/causal-inference/sequential-trials/"
next_note: "/causal-inference/surveillance-measurement-bias/"
---

Study entry point: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

Suppose today we want to compare “surgery within 30 days” with “no surgery within 90 days.” A patient without surgery today cannot yet be assigned uniquely to either group: both rules currently permit no surgery. **Clone–censor–weight (CCW)** starts from this temporary ambiguity and organizes which records may contribute to each strategy's analysis.

<aside class="study-callout study-callout--abstract" markdown="1">

**What do the three actions solve?**

**Clone:** Create strategy copies when baseline records are compatible with multiple strategies.

**Censor:** When actual treatment history first deviates from a copy's strategy, stop that copy's subsequent contribution under the strategy.

**Weight:** Under the required assumptions, address selection bias introduced by artificial censoring.

</aside>


“**Compatible**” means that, up to the current time, the actual record has not violated the strategy's required actions. Compatibility updates with the record; it does not require advance knowledge of future survival or treatment completion.

<aside class="study-callout study-callout--tip" markdown="1">

**First reading**

Read §1–4 and §6 first, following “surgery within 30 days versus no surgery for 90 days.” Establish what happens to each copy before treatment, at actual surgery, and at early death, then understand weighting and PP. The three-month hormone example illustrates the same mechanism from the original text and can wait until a second reading. Assumptions in §5 and dialysis, duration, and dynamic-rule applications in §7 extend the basics; leave §4's collapsed formula and §7's within-window initiation distribution until last.

</aside>


Overview: [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}). Related: [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}), [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}), and [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}).

If you wonder “is looking into the future forbidden, so how can later treatment determine censoring?”, read [Eligibility, Strategy Grouping, and Later Deviation Are Three Actions]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-5) and the following subsection. Eligibility and strategy copies are established at baseline; later information determines when compatibility ends, not whether earlier enrollment and risk records are deleted.


A worked multivariable example: [Complete multivariable LR-IPTW example comparing drug A with drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) shows how baseline characteristics for 3,000 people enter one shared LR model to produce propensity scores, weights for both groups, balance diagnostics, and one-year risks. Z=0 denotes drug B, rather than no treatment. Those are baseline treatment weights and cannot directly replace this note's censoring weights for continued strategy compatibility.

## 1. Why is this design needed?
{: #section-1 }

Some strategies cannot be distinguished at baseline using current treatment alone:

- “Surgery within 30 days after enrollment” versus “no surgery within 90 days”;
- “Medication for 6 months, then stop” versus “medication for 12 months, then stop”;
- “Initiate when a measurement first falls below threshold X” versus “initiate when it first falls below Y.”

Before the surgical window ends, both strategies may permit no surgery yet. In duration comparisons, both require the same actions initially. In threshold comparisons, both may require waiting while neither threshold has been reached.

**No surgery yet does not mean violation of “surgery within 30 days.”** Before the grace period ends, time remains to follow that strategy.

Waiting to observe the future and then grouping retrospectively by “the treatment actually completed” can require survival for some groups, causing [immortal time bias]({{ "/causal-inference/time-related-biases/" | relative_url }}#section-2).

Theory: [Hernán and Robins, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/). Treatment durations: [Hernán, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6889975/).

### Grace period: Initiation may be delayed, but follow-up still begins at time zero
{: #section-2 }

A **grace period** is the protocol-permitted window for completing an action. For example, the original text changes “initiate hormone therapy at baseline” to “initiate within three months of $$T_0$$, when eligibility is met and follow-up starts.” Examinations, dispensing, and treatment arrangements take time, making this more realistic than requiring everyone to start immediately at $$T_0$$.

A grace period changes **the initiation time permitted by the protocol**, not the start of follow-up to three months later. Time before actual medication remains trial follow-up. Outcomes during the grace period must be retained according to the protocol; enrollment cannot be restricted to three-month survivors.

It also makes more observed histories compatible. Initiation at month 2 violates an immediate-initiation rule but may contribute to a within-three-month strategy. This does not relax all clinical eligibility or mean that more records automatically reduce bias. Extending the window may change the strategy's effect and should follow the clinical question.

### What does “temporarily compatible with both strategies” mean?
{: #section-3 }

The original compares:

- **Initiation strategy:** start treatment within three months after $$T_0$$;
- **Noninitiation strategy:** never initiate during study follow-up.

Suppose a woman begins treatment only in month 3. During months 1 and 2, her nonuse violates neither “do not initiate” nor “initiate within three months,” because the deadline has not arrived. **Her treatment history so far therefore rules out neither strategy.**

Compatibility does not mean she has completed both protocols or simultaneously intends to choose both treatments. Investigators only assess whether recorded actions have already violated a rule.

If investigators wait until month 3 and classify “eventual initiators” as treated from $$T_0$$, that group must survive to initiation. Earlier deaths cannot become eventual initiators and may all be assigned to noninitiation or excluded, mishandling waiting-period risk and causing immortal time bias. CCW retains compatible records from baseline and updates compatibility as events unfold.

These short rules summarize only initiation requirements. A full protocol must specify scheduling within the window, continued treatment after initiation, and permitted stopping exceptions. “Within three months” does not mean “immediately.” See §7 for within-window scheduling.

## 2. Clone: Copy records and assign strategies at baseline
{: #section-4 }

The following constructed teaching example concerns one-time surgery, 90 days of follow-up, and mortality:

- **Strategy S:** undergo surgery within 30 days after enrollment while still alive.
- **Strategy N:** do not undergo that surgery within 90 days after enrollment.

Surgery type and medical exceptions are omitted to emphasize record structure. **30 days is the initiation grace period**, not a requirement to survive 30 days before becoming eligible. An actual protocol must also specify scheduling within the window; see the advanced discussion at the end of §7.

On day 0, everyone is eligible, has not undergone surgery, and has a history compatible with S and N. Create two copies per person:

| Original patient | Copy | Strategy assigned from day 0 |
| --- | --- | --- |
| Zhang | Zhang-S | Surgery within 30 days |
| Zhang | Zhang-N | No surgery within 90 days |

The copies carry identical actual records. In this example, where everyone is compatible with both strategies, the groups therefore have identical baseline composition.

**Cloning creates neither two real patients nor two potential outcomes, and does not randomize actual treatment.** It initially lets each person's records contribute to compatible strategies, with later compatibility determining when contributions stop.

Only **strategies compatible with baseline data** can receive valid follow-up contributions from that time. Implementations may create compatible copies only, or create copies and immediately censor incompatible ones at baseline; clearly violating records cannot continue representing a strategy.

<aside class="study-callout study-callout--note" markdown="1">

**What is required for identical baseline groups?**

This example makes everyone compatible with S and N, so baseline composition is identical. If some patients are compatible with only one strategy, “both groups must be perfectly balanced” no longer follows. Recheck whether the comparison targets a common population and whether each strategy has sufficient data support.

</aside>


Also distinguish **a person did not take the required action** from **people with that baseline history cannot possibly take it**. The former may be addressed through appropriate selection weighting under overlap, exchangeability, and other conditions; the latter concerns feasibility or positivity. If a group's compatibility probability is zero, censoring its copies immediately and weighting cannot recover its outcomes under that strategy. Redefine a common target population, modify strategies, or explicitly rely on additional extrapolation assumptions. See positivity in [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}).

### Another option in the original text: Randomly allocate to one compatible strategy
{: #section-5 }

The original also suggests randomly assigning a woman's record to one compatible strategy instead of creating every compatible copy. For example, randomly label Ms. Li's record “initiate within three months”; if she survives to the deadline without initiation, handle that as a deviation.

What is randomized is **the strategy label assigned during analysis**. It does not change when Ms. Li actually took medication or make her actual treatment independent of disease. Censoring at deviation and appropriate correction of the resulting selection remain necessary; random labels cannot replace them.

Cloning instead retains contributions to every compatible strategy rather than only one randomly selected strategy. Both approaches require correct subsequent handling; neither artificial label recovers an actual randomized trial's ITT effect. See [Hernán et al., 2016: Specifying a target trial prevents immortal time bias](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/).

## 3. Censor: Censor the copy at its first strategy deviation
{: #section-6 }

**Artificial censoring** is a strategy-based analytical rule: retain earlier follow-up, but stop using later factual records to directly represent that strategy after deviation. The original patient and other compatible copies may continue to contribute; censoring does not mean death.

| Actual event | S copy: Surgery within 30 days | N copy: No surgery for 90 days |
| --- | --- | --- |
| Patient A has surgery on day 10 | Continue follow-up; surgery fits the strategy | Artificially censor at surgery on day 10 |
| Patient B is alive without surgery at the end of day 30 and remains untreated afterward | Artificially censor when the 30-day grace period ends | Continue follow-up |
| Patient C dies on day 5 without prior surgery | Record day-5 death | Also record day-5 death |
| Patient D has surgery on day 45 | Already censored at the end of day 30 | Censor at surgery on day 45 |

Patient A's N copy must not be censored on day 0: the history before surgery was still compatible with “no surgery.”

For Patient C, day 5 precedes S's deadline, and no prior deviation occurred. Death is the study outcome and cannot be recoded as deviation for “failure to complete surgery.” **Early deaths belong in copies still compatible and uncensored before death.** This does not imply a zero effect for “immediate surgery”; the strategy here permits surgery within 30 days.

<pre class="mermaid">flowchart LR
    O[&quot;Patient A: Eligible, no surgery on day 0&quot;] --&gt; S[&quot;S copy: Surgery within 30 days&quot;]
    O --&gt; N[&quot;N copy: No surgery for 90 days&quot;]
    S --&gt; ST[&quot;Surgery on day 10: Continue follow-up&quot;]
    N --&gt; NT[&quot;Surgery on day 10: Artificially censor&quot;]</pre>

“An early event can contribute to multiple compatible strategies” is central to avoiding allocation of all pretreatment deaths to the untreated group. See [Hernán and Robins, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).

<aside class="study-callout study-callout--note" markdown="1">

**Why does recording one death in two copies not claim two independent deaths?**

Copies are correlated records in different strategy analyses. They do not increase independent patient counts and cannot be treated as independent observations for standard errors. Retain original patient IDs and use inference suited to this dependence.

</aside>


### Reading the original text: Initiation, noninitiation, and death during a three-month grace period
{: #section-7 }

Return from surgery to hormones: H denotes “initiate within three months” and N “never initiate throughout follow-up.” This illustrates grace-period handling only; the full protocol still determines post-initiation continuation. **To highlight early-death handling, the table uses mortality as a teaching outcome.**

| Actual course | H copy | N copy | Reason |
| --- | --- | --- | --- |
| Alive and untreated during months 1 and 2 | Retain follow-up | Retain follow-up | Neither rule has been violated |
| Initiates in month 3 before the deadline | Retain and continue according to post-initiation rules | Artificially censor at actual initiation | Only N's noninitiation rule is violated |
| Alive but untreated at the three-month deadline | Artificially censor at the deadline | Retain follow-up | H's initiation deadline has been missed |
| Dies in month 2 without prior initiation | Record the death | Also record the death | Both strategies were compatible before death; this is not deviation after surviving to the deadline |

The crucial distinction is that **“alive without initiation at the deadline” and “dies before the deadline without an opportunity to initiate” cannot use the same censoring rationale.** The latter cannot be deleted from H using retrospective knowledge that “she never managed to begin treatment.”

Retaining one early death in two copies uses the same observed event in two strategy analyses. It does not observe both complete potential outcomes or prove that “she would certainly also die if treated immediately.” The estimand concerns a strategy permitting waiting arrangements, different from immediate treatment.

Assigning every early untreated death to N would artificially shield H from early risk. Retaining deaths in both compatible copies avoids this specific error; weighting is still needed for selection from later deviations. Other patients may already have initiated and some copies been censored, so final weighted early risks need not mechanically match.

<aside class="study-callout study-callout--note" markdown="1">

**If the outcome remains the original breast cancer outcome, how is death counted?**

The original uses death to illustrate grace-period event allocation, but death is not breast cancer. For five-year breast cancer cumulative incidence under real-world conditions, death before diagnosis is a competing event. Handle it in still-compatible copies using the outcome's analytical rules, neither as breast cancer nor as deviation censoring solely for failure to initiate.

</aside>


### Censoring rules must follow the strategy definition
{: #section-8 }

If N means “no surgery for 30 days, then usual care,” Patient D's day-45 surgery does not violate N. The table censors on day 45 because this example explicitly requires **90 days without surgery**.

“No treatment for 30 days,” “do not initiate now,” and “no treatment throughout follow-up” are different strategies and cannot be interchanged.

## 4. Weight: Why is weighting needed after censoring?
{: #section-9 }

For inverse probabilities, period-by-period products, and IPTW versus IPCW, begin with [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}).

Although baseline copies are identical, the copies remaining later may differ.

Suppose milder patients obtain surgery within 30 days more readily, while severe patients often do not. At the deadline, S artificially censors more still-living severe patients. Direct analysis of those remaining may mistake “healthier retained patients” for a strategy effect. This selection comes from actual treatment decisions, so the weight model must include baseline disease affecting those decisions; apparent balance from cloning has not randomized actual treatment.

This is **informative censoring**: censoring is associated with subsequent outcome risk.

The intuition of inverse probability of censoring weighting (IPCW) is:

> Among people with the same measured history, records less likely to remain strategy-compatible and retained should receive greater weight, representing comparable people who became incompatible through treatment choices.

### A one-step numerical example
{: #section-10 }

Before a treatment decision that can trigger censoring, among people alive and previously compatible:

| Population | Probability of remaining compatible and uncensored at this step | Illustrative weight among those retained |
| --- | ---: | ---: |
| A type of severe patient | 20% | $$1/0.2=5$$ |
| A type of mild patient | 80% | $$1/0.8=1.25$$ |

Among 100 similar severe patients, if only 20 remain on average because of actual choices, each retained person receives a weight of approximately 5 to represent that original patient type in the weighted analysis.

This requires a key assumption: after controlling the necessary history, those remaining represent comparable censored patients' subsequent outcomes under the specified strategy. **It does not assign fictional future outcomes to people who died, or unconditionally turn one person into five.**

For step-by-step implementation and censoring weighting, see [De-Mystifying the Clone-Censor-Weight Method](https://pmc.ncbi.nlm.nih.gov/articles/PMC11623977/).

<details class="study-callout" markdown="1">
<summary>Advanced: Why are weights generally products of period-specific probabilities?</summary>

For original patient $$i$$'s copy assigned to strategy $$g$$, let

$$
q_{igk}=P(\text{still not artificially censored at step }k\mid
\text{previously uncensored, still alive, relevant predecision history, strategy }g).
$$

**Reading each symbol:** $$i$$ identifies the original patient; $$g$$ labels the copy's strategy; $$k$$ indexes discrete assessment steps, such as months. $$q_{igk}$$ is the conditional noncensoring probability for that patient, strategy, and step. $$P(\cdot)$$ denotes probability. Conditions to the right of $$\mid$$ are already known and imposed when calculating it; the bar is not division. The subscript igk combines three labels, not their product. q is a unitless probability between 0 and 1.

An illustrative unstabilized weight is:

$$
W_{ig}(K)=\prod_{k=0}^{K}\frac{1}{q_{igk}}.
$$

$$W_{ig}(K)$$ is the copy's cumulative weight through step $$K$$. $$K$$ is the final step considered, and $$k=0$$ the first included step, so $$K+1$$ factors are multiplied. $$\prod$$ means multiply across terms; $$1/q_{igk}$$ is each probability's inverse, not a sum. Parenthetical K indicates how far weighting extends, not W times K. Weights are unitless multipliers; denominators must be positive. Division by zero cannot represent strategy histories with no data support.

If two consecutive conditional compatibility probabilities along a history are 0.8 and 0.5, their product is 0.4 and the weight 2.5. This product is not the joint probability of the complete disease and treatment history.

“History” includes relevant baseline variables, changing disease, and prior treatment; information after a decision cannot predict that decision. The probability concerns strategy compatibility, not outcome survival.

Actual analyses may use stabilized weights and handle loss to follow-up separately. Weight processes for different histories within a grace period must also match strategies precisely. This equation explains the principle, not a model recipe for every CCW dataset.

</details>


## 5. Which assumptions does weighting require?
{: #section-11 }

| Condition | Intuition here |
| --- | --- |
| Well-defined strategies and consistency | Treatment, initiation timing, and exceptions must be sufficiently explicit so actual compatible treatment corresponds to the intervention |
| Conditional exchangeability | Sufficient confounding information affecting treatment selection, deviations, and outcomes, generally updated over time |
| Positivity | Nonzero chance of observing the strategy-required action under relevant target-population histories, with sufficient practical support |
| Appropriate probability and outcome estimation | Models and measurements must support estimation; incorrect weights do not establish removal of bias |

If a type of severe patient can never receive a strategy, enormous weights on another type cannot supply the missing evidence.

Examine censoring proportions, weight distributions, and effective remaining information. Large weights can make results depend strongly on a few patients. Truncating extreme weights may improve stability at a bias cost; it does not repair structural positivity violations.

These conditions follow [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}). Crucial unmeasured time-varying confounding does not disappear through cloning or more complex models.

## 6. Why does it generally estimate a per-protocol strategy effect?
{: #section-12 }

### First, why comparing clone labels alone provides no ITT information
{: #section-13 }

ITT concerns the effect of assignment to a strategy. Here H and N are labels analysts add retrospectively to copied records, not randomized assignments that caused different actual care arrangements.

A constructed numerical example: among 100 patients, 20 deaths are actually observed within five years. Clone everyone into H and N, retain identical complete factual follow-up, apply no deviation handling and no between-group weight differences. Then:

| Label-only comparison | Records | Factual deaths | Crude mortality proportion |
| --- | ---: | ---: | ---: |
| H copies | 100 | 20 | 20% |
| N copies | 100 | 20 | 20% |

Equality results from copying, **not a discovery that hormone therapy has no effect**. Relabeling provides no information about “what would happen under another assignment.” Complete factual follow-up is assumed for illustration; these are not clinical results.

### Why does censoring and weighting target PP?
{: #section-14 }

CCW artificially censors deviations, then uses weighting under assumptions to correct that selection. Its usual target is:

> What would happen if everyone in the target population followed their respective specified strategy?

This is the **per-protocol (PP) effect**: compatible real records, supported by assumptions, estimate outcomes if the entire target population followed the strategy. The target population does not shrink to eventual treatment completers.

For hormones, compare outcomes if the target population follows the full within-three-month initiation strategy versus if the same population follows sustained noninitiation. Deaths during the grace period remain; PP does not require survival until treatment completion to contribute an outcome.

See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}). Allowing usual care after a grace-period strategy does not remove the requirement to follow its rules during the grace period.

### A real randomized trial with a grace period can still estimate ITT
{: #section-15 }

The original conclusion “ITT cannot be emulated” has a specific context: **this observational analysis reconstructed from clone labels and strategy compatibility lacks actual assignment information to support that ITT contrast**. It does not mean that every study with a grace period can estimate only PP.

A real trial can randomize participants at $$T_0$$ to “initiate within three months” or “never initiate during follow-up.” Each person has a real assigned group. If a woman assigned initiation dies in month 2 before using treatment, ITT retains her event in the original initiation group; it neither regroups her for nonuse nor copies her into the other group.

The issue is therefore **whether real assignment information exists and how analysis corresponds to it**. Retrospective labels cannot manufacture an assignment effect, and grace-period presence alone cannot determine ITT estimability. If prescriptions, recommendations, or other assignment proxies exist, assess the specific question separately; see [7.6. Interpreting the Limitation “Only PP Can Be Estimated”]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-26).

For how initiation and sustained protocols determine deviation rules, and why IPW and the g-formula address treatment–confounder feedback, see [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}).

## 7. Three applications: Dialysis timing, treatment duration, and dynamic rules
{: #section-16 }

### Dialysis timing in the figure: What does the causal contrast compare?
{: #section-17 }

A [Swedish Renal Registry study](https://www.bmj.com/content/375/bmj-2021-066306) examined dialysis initiation strategies at different eGFR levels. The simplified course comparison is:

- $$g_E$$: initiate dialysis according to protocol in the eGFR range $$10$$–$$14\ \mathrm{mL/min/1.73m^2}$$;
- $$g_L$$: initiate according to protocol in the range $$5$$–$$7\ \mathrm{mL/min/1.73m^2}$$.

eGFR is estimated glomerular filtration rate, a measure of kidney function. The action depends on subsequent measurement states, making these **dynamic strategies**.

<aside class="study-callout study-callout--important" markdown="1">

**Range labels in the figure are not complete implementation rules**

“Initiate at 10–14” does not automatically mean “dialysis must begin on the first day eGFR reaches 14.” A full protocol must specify measurement frequency, allowed initiation timing, what happens if measurements skip the entire range, and handling of people already within or below it at baseline. A schematic alone cannot determine censoring dates.

The original BMJ study primarily analyzed 15 narrower eGFR ranges and separately compared broader ranges. Some high-threshold strategy copies were immediately censored because they were already incompatible at baseline. Thus, “all patients can keep contributing to all strategies” is false. Study strategies defined by eGFR also do not encompass every basis for clinical dialysis timing decisions.

</aside>


The **causal contrast** places the same eligible target population in two hypothetical intervention worlds and compares outcomes:

| Hypothetical world | Rules everyone follows | Outcomes to compare |
| --- | --- | --- |
| Early-initiation world | The target population follows $$g_E$$ | All-cause mortality within five years; major cardiovascular events analyzed separately |
| Late-initiation world | The same population follows $$g_L$$ | The same outcomes and horizon |

For five-year all-cause mortality, let $$Y^{g_E}(5)$$ and $$Y^{g_L}(5)$$ denote five-year death indicators for the same target population under the two strategies. A per-protocol risk-difference contrast is:

$$
\Pr\{Y^{g_E}(5)=1\}-\Pr\{Y^{g_L}(5)=1\}.
$$

**Symbol by symbol:** $$g_E$$ is the early rule and $$g_L$$ the late rule. E and L label early and late, not eligibility E or a covariate L. $$Y$$ is a death indicator; superscript g means “if this rule were followed,” not exponentiation. Parenthetical 5 means five years from the common baseline, not multiplication by 5. $$Y^g(5)=1$$ indicates death within five years under g, and 0 no death within five years; unknown actual outcomes cannot simply be set to 0. $$\Pr$$ and P both denote event probabilities, so each term is five-year mortality risk in the same target population. Subtraction fixes the direction as “early minus late.”

This has the same structure as $$P(Y_5^{g_1}=1)-P(Y_5^{g_0}=1)$$ in [Reading Causal Formulas]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}), merely placing the horizon in parentheses and replacing labels 1/0 with E/L. **The same mathematical form does not imply equal effects across different medication and dialysis studies.**

For example, suppose solely for teaching that early and late five-year mortality risks are 20% and 25%. Early minus late is $$0.20-0.25=-0.05$$, or 5 percentage points lower. For 1,000 comparable people, that means 50 fewer expected deaths; these are not the dialysis paper's results. The expression defines the target, not an estimate completed by subtracting mortality proportions among actual early and late initiators.

A risk ratio, five-year survival-probability difference, or another prespecified scale can also be used. Thus, “causal contrast = per-protocol effect” identifies **which counterfactual worlds are compared**; a complete estimand also requires the target population, outcome, horizon, effect scale, and handling of other events.

A hypothetical randomized trial can define another contrast:

- **ITT:** compare random assignment to early versus late initiation without regrouping for later deviations;
- **PP:** compare everyone following the early strategy versus everyone following the late strategy.

With nonadherence, they answer different questions. ITT includes the overall effects of randomized assignment, communicating the protocol, and actual adherence patterns; PP targets executing the two prescribed dialysis strategies.

The Swedish registry lacks a real randomized-assignment variable. For course-example patients compatible with both strategies at baseline, investigators can create early and late copies, censor a copy when actual history violates its strategy, and weight to address this selection. The target is therefore a **PP strategy effect**. Merely labeling identical records “early” and “late” without compatibility handling leaves identical factual outcomes and cannot estimate actual randomized-assignment effects.

The question is also not:

- Prognostic differences among eventual dialysis recipients who actually started at higher versus lower eGFR;
- “How long did people live after dialysis?” measured from each actual initiation date;
- The causal effect of the eGFR value itself on death.

Those questions differ in population, time zero, or intervention. “Post-dialysis prognosis among recipients” may be useful descriptively, but cannot substitute for early-versus-late strategy effects from a common decision time; doing so may involve lead time and survivor-selection biases. Outcome contrasts between strategies include earlier dialysis effects through different pathways; additional dialysis duration and treatment burden can be assessed separately as decision-relevant outcomes.

### Enrollment and assignment for early versus late dialysis: Working from a common baseline
{: #section-18 }

**The study does not first find future “early dialysis patients” and “late dialysis patients,” then enroll them retrospectively.** Patients enter when they first meet all eligibility criteria. Those untreated and compatible with both strategies at baseline can initially contribute to both copies, with actual events determining how long each contribution continues.

If you wonder “eligibility, strategy initiation, and follow-up must align, so why wait after enrollment?”, first read [Why Does Enrollment Before Dialysis Still Satisfy Time Alignment?]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-24) below, then return to assess censoring along individual records.

The Swedish study included **10,290** eligible patients, of whom **3,822** initiated dialysis during follow-up. This directly shows that **eventual actual dialysis was not an enrollment condition**. The primary analysis compared 15 narrower eGFR ranges; the course's 10–14 versus 5–7 contrast corresponds to a separate broader-range analysis. [Fu et al., 2021, Methods and Results](https://www.bmj.com/content/375/bmj-2021-066306)

#### Step one: Establish a common baseline before dialysis
{: #section-19 }

The original study's $$T_0$$ was the first date all eligibility criteria were simultaneously met: adulthood, current eGFR 10–20, a prior 10–30 measurement for confirmation, no kidney replacement therapy history, and other protocol-required measurements. A calendar enrollment window also applied; one eGFR value alone does not establish full eligibility.

Suppose Li first meets these conditions on January 1 with eGFR 18 and no dialysis. **That day is his $$T_0$$.** We need not know whether or when he will undergo dialysis or die before it.

The question concerns early versus late rules from this common decision stage, so both strategies begin counting risk that day. We cannot start the early group at actual dialysis with eGFR 12 and the late group at eGFR 6, then equate their post-dialysis survival with choosing early versus late strategies from a common baseline.

#### Step two: Assign rules to copies, rather than predict a patient's future actual group
{: #section-20 }

To assess compatibility clearly, use the course ranges in a **simplified teaching protocol**:

- E: wait while eGFR exceeds 14; permit initiation within 10–14; no initiation after falling below 10 deviates from the early strategy.
- L: wait while eGFR exceeds 7; permit initiation within 5–7; no initiation after falling below 5 deviates from the late strategy.

Assume measurements resolve these sequences and trajectories decline through the ranges without skipping, rebounding, or other medical exceptions; post-initiation care is omitted. These teaching rules support the table below; **they are neither the original study's full daily algorithm nor clinical advice on when to initiate dialysis**. Actual studies must specify measurements, scheduling within ranges, and exceptions; range labels alone cannot determine every censoring time.

At $$T_0$$ with eGFR 18, both E and L permit waiting. Create:

| Analytical record | Strategy specified from $$T_0$$ | Actual dialysis now? |
| --- | --- | --- |
| Li-E | Evaluate subsequent events using the early rule | No |
| Li-L | Evaluate subsequent events using the late rule | No |

Both labels are fixed at baseline. They indicate which rule a copy contributes to analytically, not that Li was actually randomly arranged to receive both treatments. The real Li still has one treatment history.

#### Step three: Follow the same person's records to identify deviations
{: #section-21 }

First consider a **constructed timeline** in which Li actually starts later:

| Observation time | Actual record | E copy | L copy |
| --- | --- | --- | --- |
| $$T_0$$ | eGFR 18, no dialysis | Retain; begin follow-up | Retain; begin follow-up |
| A later measurement | eGFR 12, still no dialysis | Compatible: still within this teaching rule's permitted initiation range | Compatible: late-initiation range not reached |
| Next measurement | eGFR 9, still no dialysis | Artificially censor: early range has been missed | Retain |
| A later measurement | eGFR 6, initiates dialysis | Already censored; no further contribution | Initiation follows the rule; continue follow-up |

Later eGFR and dialysis records are indeed examined, but used to **stop a copy's future contribution when deviation is observed**. Li is not placed exclusively in the late group from $$T_0$$ because he later starts at 6. Risk time contributed by E before deviation remains.

Under another actual course, if Li initiates at eGFR 12, E continues while L is censored at initiation. **His post-dialysis eGFR cannot be treated as the course of someone still untreated and waiting to start at 6.** Cloning has not produced that unobserved counterfactual trajectory.

#### Step four: People who never receive dialysis still have outcomes that must be retained
{: #section-22 }

Suppose another patient enters at eGFR 18 and dies later at eGFR 16 without dialysis. Under the teaching rules, neither strategy was violated before death, so the event remains in both uncensored E and L copies.

But if E was already censored at eGFR 9 for missing its window, and the patient then dies without dialysis, that factual death enters only the still-compatible L copy. **Not every predialysis death belongs in both groups; an event belongs in each copy still under that strategy's follow-up before the event.**

Likewise, a patient whose eGFR never reaches either range over five years and who never starts dialysis may adhere to both waiting rules throughout. PP requires trigger-based action, not eventual dialysis for everyone.

#### Finally: Compare weighted strategy risks, rather than simply compare remaining people
{: #section-23 }

Earlier dialysis and continued waiting often depend on disease, symptoms, and other prognostic factors. Copies retained after artificial censoring may therefore cease to be comparable. The original study assessed deviations monthly and used baseline and time-varying information for inverse probability weighting. Validity still requires sufficient confounder information, positivity, consistency, and appropriate estimation.

The final comparison asks: **For the same target population, how does five-year risk from common $$T_0$$ differ under the early versus late rule?** Weighting uses compatible records to estimate strategy risks; it does not recover each censored person's invisible counterfactual outcome. Confidence intervals must also account for dependence between copies of the same person.

The example chooses eGFR 18 to make both strategies clearly compatible at baseline. Actual entrants vary, so this cannot establish compatibility with all threshold strategies for all patients; some high-threshold copies in the original study were immediately censored. Follow the full protocol.

### Why does enrollment before dialysis still satisfy time alignment?
{: #section-24 }

**This example does not relax time alignment. “Starting to follow a treatment strategy” and “actually starting dialysis” are different actions.** A strategy is the full set of rules applying from baseline; actual dialysis is one action taken when its conditions are met. [Hernán et al., 2016: Aligning eligibility, assignment, and follow-up](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/)

#### 1. Eligibility and dialysis initiation conditions answer different questions
{: #section-25 }

| Condition | Question answered | Role here |
| --- | --- | --- |
| Eligibility, such as no dialysis, eGFR 10–20, and other criteria | Who can now enter a comparison of dialysis initiation rules? | Defines the target population and decision baseline |
| Early initiation range, such as eGFR 10–14 | Once following the early strategy, when should dialysis begin? | Specifies an action within the strategy |
| Late initiation range, such as eGFR 5–7 | Once following the late strategy, when should dialysis begin? | Specifies an action within the other strategy |

A patient at eGFR 18 can therefore qualify **to enter the strategy comparison** without yet meeting either strategy's **dialysis initiation condition**. There is no contradiction: the current decision is which future rule to use, not necessarily immediate dialysis.

These ranges continue the teaching protocol above. A full study must specify within-range initiation, monitoring, and exceptions; a range label does not automatically require dialysis on its entry day.

#### 2. Waiting already follows a rule; it is not empty time before the study
{: #section-26 }

Write out the strategies:

- **Early:** from today, withhold dialysis until the early condition is met; assess according to protocol and initiate when required.
- **Late:** from today, withhold dialysis until the late condition is met; assess according to protocol and initiate when required.

At eGFR 18, both require the same current action, “no dialysis yet,” but different later actions. **Strategies need not require different actions immediately at baseline to be defined and compared.** For example, two annual management protocols can share an initial phase and later diverge according to disease.

A hypothetical trial can randomize these rules today and begin implementation and follow-up today. Actual dialysis need not occur before the original assignment can be known.

<aside class="study-callout study-callout--important" markdown="1">

**“Following a strategy” does not mean dialysis has already produced a biological effect**

The current rule can require waiting. Including that time means it belongs to the full strategy being evaluated, not that unperformed dialysis already affects the body. Only if other care and relevant conditions also coincide can we discuss no dialysis-mediated difference before actions diverge. “Neither has started dialysis” alone does not establish identical care and outcome mechanisms.

</aside>


#### 3. The first three items must align; actual dialysis is a fourth item
{: #section-27 }

Let $$T_0$$ be the first eligible date with eGFR 18:

| Time element | Target trial | Corresponding CCW emulation |
| --- | --- | --- |
| Confirm current eligibility | Confirm at $$T_0$$ | Confirm from records through $$T_0$$ |
| Assign treatment strategy | Randomly assign early or late rules at $$T_0$$ | Create and label compatible early and late copies at $$T_0$$ |
| Begin follow-up and evaluate the strategy process | Count outcomes and assess adherence from $$T_0$$ | Count outcomes and assess copy compatibility from $$T_0$$ |
| Actually initiate dialysis | Initiate later when assigned-rule conditions are met | Observe actual initiation and assess compatibility with each copy's rules |

Thus, the correct relationship is:

$$
t_{\text{eligibility confirmed for this trial}}=t_{\text{strategy assignment or copy labeling}}=T_0,
$$

Lowercase $$t$$ with a text subscript denotes when the corresponding operation occurs; $$T_0$$ is this trial's follow-up start. Subscripts identify “which time,” not multiplication or effect parameters. Equality means alignment at a common clinical decision point, not identical calendar dates for every patient.

But we do not require:

$$
t_{\text{actual dialysis initiation}}=T_0.
$$

Eligibility confirmation does not require all tests on one day, nor does every TTE require the first eligible date in a lifetime. In the Swedish study, the protocol chose the first time all eligibility conditions were simultaneously met. [Fu et al., 2021](https://www.bmj.com/content/375/bmj-2021-066306)

Preserve the distinction between target trial and observational emulation: **in TTE, investigators evaluate existing records by rules from $$T_0$$; labels do not cause patients to receive care under investigators' instructions.** Actual care still comes from the original clinical process, requiring later censoring, weighting, and identification assumptions.

#### 4. Why should follow-up not begin only at actual dialysis?
{: #section-28 }

Suppose an illustrative randomized trial enrolls a patient at eGFR 18 and assigns the late strategy. The patient waits according to rules but dies before reaching its trigger.

For “what happens if the late strategy is chosen today?”, this death must be counted. Survival to actual dialysis is not required to represent the late strategy. **Dying before the trigger is reached is not protocol violation.**

**A waiting period is not itself immortal time.** Death while waiting is allowed and counted here; survival until dialysis is not required. Conversely, selecting only future successful dialysis recipients while beginning the clock at earlier eligibility creates a period between baseline and dialysis during which enrollment rules guarantee survival.

Starting at actual dialysis would exclude this patient entirely. The analysis would concern “people who survived to and received dialysis,” not the original population deciding between early and late strategies. In this illustrative setting, late starters undergo longer survival selection.

Even if both groups eventually enter, “the next five years” from each dialysis date differs from five years at a common decision stage: disease stage and observation windows change. This is the problem illustrated by [the Three-Researcher Thought Experiment]({{ "/causal-inference/time-related-biases/" | relative_url }}#section-20). Post-dialysis prognosis can be studied separately, but cannot directly replace the original strategy effect.

Counting waiting-period deaths also does not claim that waiting caused each death. Causal effects arise from **risk differences under two full strategies in the same target population**, not attributing individual causes of death.

#### 5. Why do new-user designs often begin at the first dose or dispensing?
{: #section-29 }

They may study another protocol: “start A now” versus “start B now.” If baseline initiation is required and contemporaneous initiation records emulate grouping, eligibility assessment, grouping, follow-up start, and actual initiation can coincide.

| Strategy question | Requirement at $$T_0$$ | Can actual treatment occur after $$T_0$$? |
| --- | --- | --- |
| Start A now versus B now | Eligible and perform the initial treatment action | In this setting without an additional grace period, initiation is at $$T_0$$ |
| Initiate within three months versus never during follow-up | Eligible; enter the specified window today | Yes, delayed initiation is permitted |
| Dialyze at the early versus late threshold | Eligible; follow threshold rules from today | Yes, action timing depends on subsequent triggers |

**Coincidence of medication initiation and follow-up start is required by particular strategies, not by the definition of every treatment strategy.** Grace periods often specify “within how much time”; dialysis thresholds specify “under what state,” generally without a predetermined number of waiting months. [Hernán and Robins, 2016: Grace periods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/)

#### 6. Does this allow arbitrary movement of $$T_0$$ earlier?
{: #section-30 }

No. Baseline must still correspond to a prespecified, clinically meaningful target trial at that time: patients are eligible, strategies apply then, early outcomes are retained, and grouping does not require future survival or successful dialysis.

For example, one could separately design a trial of “initiate immediately versus continue waiting at eGFR 12 while still untreated.” Its population consists of **people who survive to and remain eligible at that stage**, not everyone originally at eGFR 18, and its follow-up window differs. It may answer a meaningful new question, but must not be conflated with the original.

When reviewing, complete this sentence: **“From $$T_0$$, what does this strategy require now, and under which later conditions does the action change?”** If the current requirement is waiting, absence of dialysis does not mean the strategy has not started.

### Comparing treatment duration
{: #section-31 }

Compare “start now, use for 6 months, then stop” with “start now, use for 12 months, then stop.”

The strategies may be identical for the first 6 months, permitting two initial copies. Later compatibility follows actual stopping times, with censoring and weighting.

If a patient uses medication as specified until death in month 4, the death can enter both compatible copies. “Did not complete 12 months” cannot justify exclusion from the long-duration group.

“People who completed 12 months” and “people assigned to a 12-month strategy” are different concepts. This distinction is key to avoiding immortal time bias. [Hernán, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6889975/)

### Comparing dynamic treatment rules
{: #section-32 }

For example, measure a biomarker at fixed intervals and compare “initiate the first time it falls below X” with “initiate the first time it falls below Y.”

If neither threshold is reached initially, a person may be compatible with both strategies. Different requirements emerge as measurements and treatment change. Censor the corresponding copy at deviation.

Monitoring frequency, allowed initiation timing, and post-initiation rules must all be specified. See [Biomarkers and Well-Defined Interventions]({{ "/causal-inference/biomarkers-well-defined-interventions/" | relative_url }}).

<details class="study-callout" markdown="1">
<summary>Advanced: “Initiate within 30 days” alone may be insufficient</summary>

Initiating on day 1 versus day 29 may produce different outcomes. A within-30-day strategy also requires a rule or distribution for scheduling treatment inside the window.

Common CCW implementations may retain part of the observed within-window initiation process while defining intervention through deadline rules. Their results therefore neither automatically equal “immediate treatment” nor apply to every possible arrangement within 30 days.

Report explicitly how within-window initiation distributions and prior treatment histories enter weights. See [The Complex Estimand of Clone-Censor-Weighting When Studying Treatment Initiation Windows (preprint)](https://arxiv.org/abs/2404.15073).

</details>


## 8. Difference from sequential trials
{: #section-33 }

- Typical CCW copying: **same person, same time zero, multiple compatible strategy copies**.
- Typical [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}) repetition: **same person, multiple time zeros, entry into separate emulated trials**.

CCW can be implemented within each sequential trial; the designs are not mutually exclusive.

## Sources
{: #section-34 }

- [Hernán MA, Robins JM. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).
- [Hernán MA et al. Specifying a target trial prevents immortal time bias and other self-inflicted injuries in observational analyses (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/).
- [Hernán MA. How to estimate the effect of treatment duration on survival outcomes using observational data (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6889975/).
- [De-Mystifying the Clone-Censor-Weight Method for Causal Research Using Observational Data: A Primer for Cancer Researchers (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11623977/).
- [Fu et al. Timing of dialysis initiation to reduce mortality and cardiovascular events in advanced chronic kidney disease (BMJ, 2021)](https://www.bmj.com/content/375/bmj-2021-066306).
- [Webster-Clark et al. The Complex Estimand of Clone-Censor-Weighting When Studying Treatment Initiation Windows (2024, preprint)](https://arxiv.org/abs/2404.15073/).

People, the 30/90-day setting, the 100-person clone-label demonstration, and numerical weights are constructed teaching examples, not clinical conclusions; the three-month hormone initiation window comes from the original text.
