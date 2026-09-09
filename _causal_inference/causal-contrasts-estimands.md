---
layout: "causal-note"
title: "Causal Contrasts and Estimands"
description: "Define the population, strategies, outcome, horizon, and effect scale before choosing an estimator."
group: "Foundations"
order: 3
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Why is “drug A versus drug B” insufficient?", "anchor": "section-1"}, {"title": "2. Why are the ITT effect and PP effect causal contrasts?", "anchor": "section-2"}, {"title": "3. How do treatment strategies, causal contrasts, estimands, and methods differ?", "anchor": "section-6"}, {"title": "4. Why is it an element of study design?", "anchor": "section-8"}, {"title": "5. How does it help interpret study conclusions?", "anchor": "section-9"}, {"title": "6. How should ITT and PP be named in observational TTE?", "anchor": "section-15"}, {"title": "7. How can the protocol state this clearly?", "anchor": "section-17"}, {"title": "8. Self-check", "anchor": "section-18"}]
previous_note: "/causal-inference/reading-causal-formulas/"
next_note: "/causal-inference/intention-to-treat-per-protocol/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Remember one sentence first**

**The causal contrast of interest specifies which two intervention scenarios' outcomes we wish to compare for the same target population.**

In a target trial protocol, this field often uses ITT or PP to distinguish the effect of “being assigned to different strategies” from the effect of “following different strategies.” It must also state how differences are summarized, such as by a risk difference or risk ratio. Define what to compare before choosing how to estimate it.

</aside>


Prerequisite: potential outcomes in [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}). **This note introduces ITT and PP from the beginning: hold one question fixed → define two targets → understand causal contrasts → examine their design role and results → map them to observational TTE.** On a first reading, follow §1–§6 in order; §7 provides a protocol-writing template. For estimation methods, continue to [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).

A protocol exercise after reading: [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}) shows how the same sustained-treatment protocol can specify both ITT and PP.

## 1. Why is “drug A versus drug B” insufficient?
{: #section-1 }

Suppose we want to study whether drug A lowers five-year mortality risk compared with drug B. First hold the remaining elements fixed, so that changing the population and outcome along the way does not lead us to attribute those differences to ITT versus PP.

| Element | Common teaching setup in this note |
| --- | --- |
| Target population | Patients eligible at baseline for whom both strategies A and B are applicable |
| Strategy A | Initiate A at baseline and continue as specified; adjust or discontinue according to the rules if prespecified contraindications arise |
| Strategy B | Initiate B at baseline and continue as specified for B; likewise explicitly define permitted adjustment and discontinuation rules |
| Start and duration | Align eligibility confirmation and strategy assignment, then follow patients for five years from that point |
| Outcome | All-cause death within five years |
| Comparison direction | A relative to B; calculate risk differences as A minus B |

A and B are placeholders. This is an outline for teaching; a real protocol must specify doses, contraindications, monitoring, and other details. This note first considers **PP for these two sustained strategies**. PP for a strategy specifying only baseline initiation is a different target, distinguished in §6.

Now consider Wang: he is assigned A and starts that day, but stops in month three for personal reasons, contrary to this example's protocol. He dies in the second year.

“Comparing A and B” still does not tell us what the study actually wants to know:

- **Assignment question**: How would five-year mortality risk differ if everyone were assigned to group A rather than group B? Discontinuation such as Wang's occurs as part of the actual postassignment process.
- **Adherence question**: How would five-year mortality risk differ if everyone were assigned to A and followed A's protocol, rather than being assigned to B and following B's protocol? For Wang, we need to infer his outcome if this protocol deviation had not occurred.

These questions use the same drug names but posit different treatment courses. Their true answers may therefore differ.

“Causal” emphasizes comparing potential outcomes under interventions; “contrast” means comparison; “of interest” identifies the question researchers select in advance and seek to answer, rather than a statistically significant result selected afterward.

## 2. Why are the ITT effect and PP effect causal contrasts?
{: #section-2 }

Because they specify the two comparisons above.

Begin with a target randomized trial: **the ITT intervention specifies the strategy assigned; the sustained-strategy PP intervention additionally specifies that actual treatment follows that strategy's rules.** The “intention” in intention-to-treat preserves the original treatment assignment; it does not score patients' subjective willingness to be treated. “Per protocol” means “according to the study protocol.”

|  | Intention-to-treat effect, ITT | Per-protocol effect, PP |
| --- | --- | --- |
| First intervention scenario | Everyone is assigned strategy A, with subsequent adherence and care developing as in that trial | Everyone is assigned strategy A and follows A's protocol |
| Second intervention scenario | The same population is assigned strategy B, with subsequent adherence and care developing as in that trial | The same population is assigned strategy B and follows B's protocol |
| Main question | What outcomes result from assignment to different strategies? | What outcomes result when the different strategies are followed according to protocol? |
| Nonadherence in reality | Part of the actual postassignment process | Requires inference about outcomes if the protocol were followed |

We initially retain the randomized-trial definitions and their assignment and care context; §6 explains their correspondence to observational emulation. Both the classic TTE methods paper and the TARGET reporting guideline give ITT and PP as common examples of causal contrasts. [Hernán and Robins, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/); [TARGET, 2025, Table 1](https://www.bmj.com/content/390/bmj-2025-087179.full.pdf)

### The contrast here is not “ITT minus PP”
{: #section-3 }

Each target compares A with B:

- **ITT contrast:** compare the world with assignment to A against the world with assignment to B.
- **PP contrast:** compare the world with assignment to and adherence to A's protocol against the world with assignment to and adherence to B's protocol.

These are **causal** because they ask what would happen to the same population under different interventions. We want to explain differences caused by the interventions, rather than merely observe that the existing A and B groups have different outcomes; that observed difference may also contain preexisting differences in severity.

Thus, “ITT” and “PP” specify **the type of effect we want to estimate**. The outcome, time horizon, and scale such as a risk difference must also be specified to form a complete target quantity. They are not themselves two statistical models.

### An invented numerical example
{: #section-4 }

Suppose the same population has the following five-year mortality risks in a teaching world. These are potential-outcome risks specified to illustrate the issue, not drug-study findings or four values that can be read directly from an ordinary data table.

| Intervention scenario | Five-year mortality risk |
| --- | ---: |
| Assigned A, with subsequent events developing naturally | 12% |
| Assigned B, with subsequent events developing naturally | 15% |
| Assigned A and follows A's protocol | 8% |
| Assigned B and follows B's protocol | 14% |

Expressed as A-minus-B risk differences:

- ITT: $$12\%-15\%=-3$$ percentage points.
- PP: $$8\%-14\%=-6$$ percentage points.

Different values do not mean that one must be wrong; each may correctly answer a different question. **The PP cannot be calculated directly from the ITT value, and this example does not imply that PP is always larger than ITT.**

Both PP risks may differ from their corresponding ITT risks: requiring adherence can change the treatment course in both A and B groups. Adherence is not a concern only for group A.

### PP does not mean “compare only actual adherers”
{: #section-5 }

Both contrasts can concern the same initially defined target population, including people who later stop treatment in reality. PP asks what would happen if these people also followed the protocol.

Simply deleting everyone who stops treatment selects a population based on future behavior. If severity affects both adherence and mortality, this may introduce selection bias. **The PP effect is the target; naively deleting nonadherers is one potentially biased analysis.** See [The crucial pitfall: An effect definition is not an analysis method]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-6).

“Everyone follows the protocol” also does not require continuing medication despite contraindications. Stopping according to prespecified safety rules may constitute adherence. Death must still be recorded as an outcome, and a person must not be excluded for failing to complete five years of treatment because they died.

## 3. How do treatment strategies, causal contrasts, estimands, and methods differ?
{: #section-6 }

These concepts work together but should not be used interchangeably.

| Concept | What does it answer? | This example |
| --- | --- | --- |
| Treatment strategies | What exactly should be done, when, and with what permitted adjustments? | Initiate A and continue at the specified dose; stop according to the rules if predefined contraindications occur. Specify B equally clearly |
| Causal contrast | Which intervention scenarios are compared, and how are their outcome differences summarized? | Compare effects of assignment or adherence, then specify a scale such as the risk difference |
| Effect measure | What numerical measure describes the difference? | Five-year mortality risk difference or five-year mortality risk ratio |
| Causal estimand, the complete causal target quantity | In which population, from what starting point, over what duration, and for which outcome is a specific quantity estimated? | The five-year all-cause mortality PP risk difference for A versus B among people eligible today |
| Estimator, a calculation rule | What rule turns data into an estimate? | A risk-difference estimator constructed using standardization or IPW |
| Estimate | What number results when these particular data are put into the calculation rule? | For example, an estimated risk difference of −3 percentage points, reported with its confidence interval |

In a TTE table, the treatment-strategies field first specifies the full action rules; the causal-contrast field then states whether to compare assignment or adherence to those rules. Writing only “PP” remains incomplete because PP under different protocols can refer to different quantities.

Distinguish the last three terms in one sentence: **the estimand is the quantity we want to know, the estimator is the rule for calculating it, and the estimate is the number calculated this time.** Changing the estimation method need not change the target quantity. Changing “initiate” to “continue use” changes the target quantity even if both analyses use the same model.

**A causal contrast is part of a complete estimand.** The effect measure has its own row here to distinguish “what is compared” from “what quantity describes the difference,” not to imply that causal contrasts in the literature exclude the scale. TARGET explicitly requires stating the effect measure in the causal-contrast field. Terminology may vary somewhat across publications; follow the actual definitions. [TARGET, 2025, glossary and items 6f–6h](https://www.bmj.com/content/390/bmj-2025-087179)

### Reading the five-year risk-difference formula symbol by symbol
{: #section-7 }

First state the question in plain language: **For the same set of eligible patients at baseline, what is the five-year mortality risk if everyone follows A's protocol minus the risk if everyone follows B's protocol?**

To match the sustained-strategy PP example in §2, let $$g_1$$ temporarily mean “assignment to and adherence to A's complete protocol,” and $$g_0$$ mean “assignment to and adherence to B's complete protocol.” This sentence defines the intervention represented by each superscript; the formula does not specify the protocol for us.

$$
\Delta_5=P(Y_5^{g_1}=1)-P(Y_5^{g_0}=1).
$$

| Symbol | What exactly does it mean in this example? |
| --- | --- |
| $$g$$ | A complete intervention scenario or strategy; the name of a rule, not a number |
| $$g_1,g_0$$ | The A and B scenarios defined above; subscripts 1 and 0 label strategies, not years, and 0 need not mean no treatment |
| $$Y$$ | The outcome variable; here the outcome is death, not blood pressure, dialysis initiation, or survival duration |
| The 5 in $$Y_5$$ | Five years from the common follow-up origin; it concerns cumulative death within five years, not only new deaths in the fifth year |
| Superscript $$g_1$$ | “If scenario $$g_1$$ were followed”; this marks a potential outcome, not exponentiation or selection of people who actually adhere to A |
| $$Y_5^{g_1}=1$$ | Under this scenario, a person dies within five years; 1 codes “the outcome occurs,” not a count of deaths |
| $$Y_5^{g_1}=0$$ | Under this scenario, a person does not die within five years; actual loss to follow-up and an unknown outcome cannot simply be coded 0 |
| $$P(\cdot)$$ | The probability of the event in parentheses; here, five-year mortality risk in the original target population, between 0 and 1, not a significance-test p-value |
| $$P(Y_5^{g_0}=1)$$ | Five-year mortality risk if the same population were under scenario B; the two terms are not crude risks in two initially different patient groups |
| $$\Delta_5$$ | Read “Delta five”; defined here as the five-year A-minus-B risk difference. The 5 is a horizon, not the fifth patient, and Delta is not a derivative |
| The minus sign | Subtract the second risk from the first in the prespecified direction |

**Read the first probability from the inside out:** first “following A's protocol,” then “death within five years,” then “the probability of this event in the target population.” Read the second probability in the same way, replacing A with B.

Substitute the teaching risks specified in §2:

$$
\Delta_5=0.08-0.14=-0.06=-6\text{ percentage points}.
$$

Read this as: **in this teaching world, A lowers five-year mortality risk by 6 percentage points relative to B.** Among 1,000 patients of this same type, the expected death counts under the two scenarios are 80 and 140, a difference of 60. This is a population-average comparison; it does not mean that both outcomes have been observed for every person or that we know which people benefit.

A risk difference expressed as a probability has no physical unit; when converted to percentages, it is reported in “percentage points.” Here, the negative sign means lower mortality risk in the first scenario. If the outcome were “survival,” the same negative sign could not be interpreted as favorable.

**This defines a target quantity; it is not an algorithm that directly calculates a causal effect from raw data.** An estimate obtained from actual data is often written $$\widehat\Delta_5$$; the “hat” marks a sample estimate, which has uncertainty and may also be biased. Identifying these risks from observational data still requires defining the interventions and relevant identification assumptions, then choosing a method.

The two probabilities concern the same baseline target population. Redefining $$g_1,g_0$$ allows the same form to express other targets, such as ITT, which changes only assignment and allows subsequent events to develop naturally. The formula alone does not automatically identify it as ITT or PP. Naming two drugs alone does not make the intervention process clear. For more basic notation, see [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}).

For a risk ratio, use $$P(Y_5^{g_1}=1)/P(Y_5^{g_0}=1)$$: replace subtraction with division, with B's risk as the denominator, which must be greater than zero. Here, $$0.08/0.14\approx0.57$$, meaning A's risk is about 57% of B's. This and a reduction of 6 percentage points are different descriptions of the same scenario. **Choosing ITT or PP is not the same as choosing a risk difference, risk ratio, or HR.** The former specifies the intervention scenarios; the latter specifies how to summarize their difference. An HR is also not a fixed-horizon risk ratio; see [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}).

## 4. Why is it an element of study design?
{: #section-8 }

Because we must decide what result would answer the research question before seeing the analysis results. Even when data already exist, researchers must first design how to construct the comparison from them.

If the aim is an assignment effect, Wang's death after discontinuation remains an outcome in the A-assigned group. If the aim is PP for a sustained strategy, his postdiscontinuation experience cannot directly represent “continuing A according to protocol.”

This affects the entire study, rather than merely changing a label in a results table:

| Study component | How does the causal contrast affect it? |
| --- | --- |
| Data sufficiency | An assignment effect requires corresponding assignment information; sustained-strategy PP generally also requires longitudinal treatment, severity, and determinants of adherence |
| Which actions count as deviations | If the protocol specifies only initiation, subsequent discontinuation need not violate it; sustained protocols require determining when and why deviation occurs |
| Use of subsequent records | ITT continues recording outcomes under original assignment after discontinuation; sustained PP using censoring weights may end a record's further contribution to its corresponding strategy at the first prohibited deviation |
| Identification assumptions | Observational baseline treatment choice requires confounding control; sustained strategies may additionally require time-specific control of adherence-related time-varying confounding and selection |
| Analysis method | Select methods according to the target and causal structure; a method cannot substitute for defining the target |
| Interpretation and comparison | State whether the effect concerns assignment, initiation, or a sustained strategy; when comparing studies, verify that their targets agree |

For example, artificial censoring does not make a patient “disappear” from actual follow-up, and it is not the only way to estimate PP. Appropriate precensoring records should be retained, and the selection introduced by censoring usually requires handling. The longitudinal g-formula can estimate PP by simulating processes under the strategies; “using artificial censoring” should not be treated as the definition of PP. [Hernán and Robins, 2016, Analysis plan](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/); see [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) and [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}).

## 5. How does it help interpret study conclusions?
{: #section-9 }

### Why distinguish these two targets?
{: #section-10 }

Both questions matter for decisions:

| Question of interest | What information does the corresponding target provide? |
| --- | --- |
| In the setting studied, what happens overall if people are assigned A rather than B? | ITT describes the consequences of assignment, including actual postassignment initiation, discontinuation, switching, and related care |
| What happens overall if the same people are treated according to the rules for A versus B? | PP describes the consequences of adhering to each protocol, helping compare the effects of specified treatment rules in this population and care setting |

For example, ITT can inform treatment-assignment decisions; sustained PP can help explain outcomes when patients follow the specified treatment pathway. Both depend on the population and care environment. **ITT does not automatically represent “real-world effectiveness” everywhere; PP is not a “pure pharmacological effect” detached from clinical care.**

Considering both in one study can enrich understanding of “the consequences of assigning a strategy” and “the consequences of following its rules.” PP, however, is not a correction of ITT and need not be more favorable. Differences may reflect different intervention processes, estimation error, or bias; the numerical difference alone does not establish the reason.

### Must every TTE estimate both ITT and PP?
{: #section-11 }

**No.** First select the primary target based on the decision question, then assess whether the data support estimation. If both questions are valuable and the data and methods suffice, both can be reported. If sustained strategies alone are of interest, PP can be the primary target without first calculating something called ITT.

In particular, do not label a result grouped by actual initiation as the ITT of a real randomized trial merely to supply both names. See §6 for naming in observational emulation.

### What might a results table look like?
{: #section-12 }

Organize the four risks from §2 in a common reporting format. **All numbers below are teaching assumptions used to demonstrate interpretation, not actual analysis results.** A real study should report estimated risks and effects with confidence intervals in the corresponding places.

| Causal contrast in the target randomized trial | Five-year risk under strategy A's scenario | Five-year risk under strategy B's scenario | Risk difference, A minus B | Risk ratio, A divided by B |
| --- | ---: | ---: | ---: | ---: |
| ITT: compare assignment | 12% | 15% | −3 percentage points | 0.80 |
| PP: compare assignment and adherence to sustained protocols | 8% | 14% | −6 percentage points | Approximately 0.57 |

The ITT row could be interpreted as:

> In this population and the adherence and care setting studied, assignment to A rather than B lowers five-year mortality risk by 3 percentage points; per 1,000 people, the two assignment scenarios differ by an expected average of 30 deaths.

The PP row means:

> If the same population were assigned to and followed the sustained protocols for A versus B, the five-year mortality risk would be 6 percentage points lower under A, corresponding to an expected average difference of 60 deaths per 1,000 people.

The per-1,000 expression is a population-average difference and does not identify the particular 30 or 60 people who benefit. A risk difference of “3 percentage points” also differs from a “3% relative reduction”: the ITT RR of 0.80 corresponds to a 20% relative risk reduction. The PP RR is approximately 0.57; neither is an HR.

An actual paper would usually also describe the target population and starting point, strategy details, follow-up horizon, 95% confidence intervals for risks and effects, adjustment methods, loss-to-follow-up handling, and key assumptions. Reporting only “HR = some number, P < 0.05” does not let readers determine which causal contrast is being estimated.

### Why not call the difference between the effects “the benefit of improving adherence”?
{: #section-13 }

Here, the PP risk difference is −6 percentage points and the ITT risk difference is −3 percentage points. Their difference is 3 percentage points, but this compares **two A-versus-B contrasts**; it does not estimate the effect of a particular “adherence-improvement program.” The risks under both A and B may change with an adherence intervention, and specific programs such as medication reminders or additional clinic visits may affect outcomes through other pathways.

To ask “How many deaths would implementing an adherence-support intervention prevent?”, define that intervention and its comparator separately, then study their corresponding causal effect.

### Assess the research contribution by whether the question is answered
{: #section-14 }

If a study claims to estimate the effect of “continuing A for five years” but only groups patients by actual baseline initiation and never addresses discontinuation or switching, then under appropriate control of baseline confounding and other conditions, it generally answers an initiation-effect question. No degree of statistical-model complexity can turn that into a sustained-strategy effect by changing its name.

Distinguishing causal contrasts therefore **aligns the question, data, methods, and conclusion**. Targets should also be checked before comparing studies: a difference between initiation and sustained-strategy effects does not automatically mean that studies contradict one another. [Hernán and colleagues: The target trial framework—Why and when is it helpful?](https://pmc.ncbi.nlm.nih.gov/articles/PMC11936718/)

## 6. How should ITT and PP be named in observational TTE?
{: #section-15 }

Specify separately **what the target trial seeks to compare** and **what comparison the available data can actually support**.

§2 and §5 first presented ITT and PP in a target randomized trial. When moving to observational TTE, the same two row labels cannot be carried into a results table without justification.

Observational records usually contain actual dispensing, medication use, or surgery, rather than the original random-assignment variable of the target trial. Grouping by actual initiation of A or B at baseline and retaining the initial group thereafter therefore generally estimates an initiation effect. This analysis form alone does not establish recovery of a randomized trial's ITT.

If the protocol specifies only “initiate A today, then continue under usual care” or “initiate B today, then continue under usual care,” the initiation effect can also be defined as the PP effect of that point-intervention protocol. The target becomes sustained-strategy PP when the protocol specifies “initiate and continue medication according to the rules.” **The meaning of PP must be read together with the specific protocol.**

If the data also contain physician prescriptions, recommendations, or policy-assignment information, the effects of those decisions can be studied under appropriate identification assumptions. They still do not automatically equal the ITT of another randomized trial. [Matthews and colleagues, BMJ, 2022](https://www.bmj.com/content/378/bmj-2022-071108)

### How should results from ordinary observational TTE be named?
{: #section-16 }

When data mainly record actual treatment, a results table can explicitly use the two targets below rather than two broad abbreviations:

| Reportable target | Intervention scenarios compared | What should the conclusion say? |
| --- | --- | --- |
| Baseline initiation effect, optionally described as an observational analog of ITT | Initiate A versus initiate B at baseline, with subsequent events following their respective usual-care processes | “The effect of initiating A relative to initiating B on five-year mortality risk” |
| Sustained-strategy PP effect | Treatment according to the complete A rules versus the complete B rules | “The effect of following A relative to following B on five-year mortality risk” |

Both rows can report five-year risks, risk differences, and risk ratios, but the identification conditions and data requirements differ. The first generally emphasizes controlling baseline treatment confounding; the second may also require longitudinal treatment and severity records and methods for treatment–confounder feedback. Both require appropriate handling of loss to follow-up and measurement problems.

This table explains naming and interpretation; it does not automatically transfer the fictional RCT numbers from §5 to an observational study. Actual estimates must come from the corresponding data and methods, and their causal interpretation depends on the necessary assumptions.

This is why “ITT-like” or “PP” in a paper is insufficient for evaluation. Continue asking: Is the intervention on assignment, actual initiation, or the full treatment history? What subsequent actions are allowed? How do the data and methods correspond? See [ITT in observational studies: Initiation and assignment effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-12) and [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}).

## 7. How can the protocol state this clearly?
{: #section-17 }

The following is a learning template, not a clinical protocol with operational details such as doses and contraindications already supplied:

> Among patients eligible at baseline for whom both A and B are applicable, use the aligned time of eligibility confirmation and strategy assignment as the start of follow-up. Compare the five-year all-cause mortality risk if everyone followed A's protocol with that if everyone followed B's protocol, specifying A minus B as the comparison direction. The target is a PP effect. Specify dose, permitted treatment adjustments during follow-up, contraindications, and discontinuation rules individually in the treatment-strategies field.

If the target is randomized-trial ITT, replace the “everyone follows the protocol” contrast with “assignment to A versus assignment to B, with subsequent adherence and care developing as in that trial.” Then state the identification assumptions and estimation method for each estimand separately.

Returning to the familiar dialysis example, first define complete rules for “early initiation” and “late initiation,” then choose whether to compare assignment to the early versus late strategies or adherence to those strategies. The outcome could be the five-year all-cause mortality risk difference. Under either choice, deaths while awaiting dialysis that belong under the protocol must not be deleted because “dialysis has not yet started.” See [Dialysis timing in the figure: What exactly does the causal contrast compare?]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-17).

## 8. Self-check
{: #section-18 }

1. Does “use Cox to analyze A versus B” identify the causal contrast?
2. If two studies both report five-year mortality HRs, one for ITT and one for sustained PP, must they have the same estimand?
3. Why can PP not be estimated simply by retaining only people who ultimately complete treatment?
4. For a protocol specifying only baseline initiation, does later discontinuation necessarily violate the protocol?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. No. Cox is a model; the intervention processes, population, and outcome must also be specified.
2. No. Using the same effect measure does not imply the same intervention scenarios.
   More specifically, they define different intervention processes and cannot be treated as the same estimand merely because both report HRs; their numerical values may coincide in special cases.
3. PP usually concerns outcomes if the original target population followed the protocol; selecting people by future adherence and survival changes the population and may create bias.
4. Not necessarily. If subsequent events are allowed to follow usual care, discontinuation does not violate the baseline-initiation requirement.

</details>
