---
layout: "causal-guide"
title: "Causal Inference Study Guide"
description: "A guided reading route through 23 notes on causal inference, target trial emulation, estimation, and bias."
group: "Guide"
order: 0
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "Before you begin: understanding and remembering", "anchor": "section-1"}, {"title": "1. Recommended route: from causal questions to design and estimation", "anchor": "section-2"}, {"title": "2. Learning map", "anchor": "section-34"}, {"title": "3. Review by question", "anchor": "section-37"}, {"title": "4. Review by case", "anchor": "section-44"}, {"title": "5. A three-pass review method", "anchor": "section-49"}, {"title": "6. Maintaining the study guide", "anchor": "section-53"}]
permalink: "/causal-inference/"
---

<aside class="study-callout study-callout--abstract" markdown="1">

**One route for your first review**

**Read steps 1 through 21 below in order.** At each step, read only the indicated sections, then return here for the next step. You do not need to finish every formula, source passage, or advanced discussion first.

There are currently **23 topic notes**: 21 form the first-pass route, g-estimation is step 22 for a second pass, and a separate TTE extension note discusses the literature. New material is placed within this route with links to the preceding and following topics.

</aside>


## Before you begin: understanding and remembering
{: #section-1 }

**Start with [What exactly is a treatment effect?]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-1).** Use the blood-pressure example to understand what would happen to the same person under different treatments, then connect that meaning to notation in step 2. For familiar steps, use the self-check and move on; there is no need to recopy notes.

The entire route develops one question: **for the same eligible patients, what would happen under different treatment strategies, how can observational records answer that question, and how can we assess the credibility of the answer?**

Use each step’s “Read first” and “After reading” guidance to set the scope. You need not open every related link at once. Consult the glossary, question index, and case exercises as needed. Keep reported study findings separate from invented teaching numbers: the latter explain calculations and are not evidence of clinical efficacy.

## 1. Recommended route: from causal questions to design and estimation
{: #section-2 }

### Part 1: clarify what we want to know
{: #section-3 }

#### 1. [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }})
{: #section-4 }

**Read first:** “What exactly is a treatment effect?” and §§1–4. Focus on the intuitive examples and four identification assumptions. Return to the standardization calculation in §5 at step 13; leave §§6–7 for the second pass.

**After reading:** explain why a treatment effect is neither a before–after change nor simply a difference between existing groups. Next, connect those meanings to mathematical symbols.

#### 2. [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }})
{: #section-5 }

**Read first:** §§1–3. Use the five-year mortality question to understand strategies, potential outcomes, events, probabilities, and risk differences. Then use §§3.1–3.4 to distinguish observing A=1, intervening with do(A=1), and the potential outcome Y¹. §3.5 uses a separate one-year example to explain why the numbers differ; its expandable identification formula can wait until step 13. Consult §4 as needed.

**After reading:** explain superscripts, horizons, and event coding; why do is not selection of an existing treatment group; and how it relates to potential outcomes. Next, combine clearly defined intervention scenarios into the causal contrast of interest.

#### 3. [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }})
{: #section-6 }

**Read first:** §§1–6, especially §3’s symbol-by-symbol explanation of the five-year risk difference, then the results table in §5.

**After reading:** identify the two scenarios, population, outcome, horizon, and whether the comparison uses a risk difference or risk ratio. Next, separate two easily confused scenarios: assignment and adherence.

#### 4. [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }})
{: #section-7 }

**Read first:** §§1–4, §6, and §§7.2 and 7.4; use §8 for self-assessment. Leave §5’s full notation and the other source-passage discussions in §7 for the second pass.

**After reading:** explain that ITT concerns assignment to a strategy, whereas PP concerns following a specified rule, and why simply deleting nonadherers does not correctly estimate PP. Next, ask whether the protocol requires a single action or sustained adherence.

### Part 2: turn interventions into executable rules
{: #section-8 }

#### 5. [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }})
{: #section-9 }

**Read first:** §§2–3, §§5–7, and §10. In §7, first use the diagrams to understand how health and treatment can influence one another; calculation of longitudinal weights can wait.

**After reading:** explain why specifying initiation only and specifying sustained treatment define different PP effects, and when subsequent discontinuation constitutes deviation. Next, use biomarkers to test whether a rule actually specifies what should be done.

#### 6. [Biomarkers and Well-Defined Interventions]({{ "/causal-inference/biomarkers-well-defined-interventions/" | relative_url }})
{: #section-10 }

**Read first:** §§2–6, then the three questions in §7. Consult §1’s source-passage interpretation for comparison.

**After reading:** explain why setting hemoglobin to a value and using a defined treatment rule to pursue that target are not identical. You now have a population, outcome, and action rules; next, organize them into a trial protocol.

### Part 3: write the causal question as a trial
{: #section-11 }

#### 7. [Pragmatic Trials in Routine Care]({{ "/causal-inference/pragmatic-trials/" | relative_url }})
{: #section-12 }

**Read first:** §§1–6.

**After reading:** explain why routine-care conditions and random allocation can coexist, and why pragmatism does not by itself select ITT or PP. Next, consider how such a trial can guide an observational design.

#### 8. [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }})
{: #section-13 }

**Read first:** §§1–5, then §§6.2–6.5. Emphasize §3: determining eligibility, assigning strategies, and identifying deviations during follow-up are three separate operations.

**After reading:** explain who enters when, when strategies are assigned, and when outcome counting begins. A strategy can initially require waiting, with actual dialysis occurring later. Next, assemble these concepts in a complete protocol table.

#### 9. [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }})
{: #section-14 }

**Read first:** §§1–6 and the eligibility/loss-to-follow-up examples in §§8.2–8.4. Save §7’s analysis plan for an integration exercise after step 18.

**After reading:** explain how the seven design components constrain one another, and distinguish permitted safety discontinuation, protocol violation, loss to follow-up, and outcome events. Next, ask where direct data comparisons can still become unfair despite a written protocol.

### Part 4: understand why the comparison may be biased
{: #section-15 }

#### 10. [Confounding and Treatment Components: Kidney Transplantation]({{ "/causal-inference/confounding-treatment-components/" | relative_url }})
{: #section-16 }

**Read first:** §§2–6, and calculate §5’s kidney-quality mixture example yourself.

**After reading:** explain why recipient characteristics and donor-organ characteristics cannot all be adjusted for indiscriminately: variable roles depend on the treatment strategies. Next, examine errors from selecting the wrong people or placing the study clock incorrectly.

#### 11. [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }})
{: #section-17 }

**Read first:** §§1–4 and §6. Understand events, waiting time, and population selection first. Save §5’s longer three-investigator dialysis example until step 18, when it can be compared with correct CCW.

**After reading:** explain what immortal time, earlier timing, and depletion each change, and why waiting alone is not immortal time. Next, examine how these errors affect the people and time used by statistical models.

### Part 5: move from records and assumptions to effect estimation
{: #section-18 }

#### 12. [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }})
{: #section-19 }

**Read first:** §§1–6 and §8. Follow the sequence: why follow-up time matters → who is compared at each event → how relative scores form conditional probabilities → how an HR is selected. Calculate along with the four-person risk-set table in §4; leave the expandable derivative for the second pass.

**After reading:** distinguish risk, hazard, and HR; identify each event-time comparison; and explain why the model does not automatically repair earlier design biases. Next, move from HRs to direct calculation of target-population risks.

#### 13. [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }})
{: #section-20 }

**Read first:** §§1–4 → §§5–6 → §§8–9. With the 1,000-person example, trace the problem with a crude comparison, borrowing risks from people with the same health status, and predicting and averaging over one shared target population. Then see why repeated treatment requires modeling subsequent health. Expand §7’s long formula on the second pass. Revisit step 1, §5, for standardization if needed.

**After reading:** explain why predictions are averaged over the same baseline population, and why subsequent health must develop under the intervention in sustained-strategy analyses. Next, use the same table to learn another calculation targeting the same quantity.

#### 14. [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }})
{: #section-21 }

**Read first:** §§1–6 → §§7–11. Ask who is underrepresented in an observed treatment group, how much weight they need, and why the weight is precisely an inverse probability. Recalculate the same 12.5% and 25% risks as the g-formula. Then use two decisions to understand multiplication of weights and distinguish treatment from censoring weights. Leave ATT and more complex stabilized weights for the second pass.

**Research example:** continue with the [multivariable LR–IPTW example comparing initiation of drugs A and B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15). Substitute each patient’s features into LR, then inspect SMDs, stabilized weights, and one-year hospitalization risks. The single-variable example builds intuition; the A/B example connects to new-user comparisons in the next part.

**After reading:** explain what each probability predicts, why its inverse is used, and why sustained strategies and artificial censoring need longitudinal data and corresponding assumptions. You are ready to understand how observational records are organized—and why the weighting step in CCW is essential.

### Part 6: organize existing clinical records into a target trial
{: #section-22 }

#### 15. [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }})
{: #section-23 }

**Read first:** §§1–5.

**After reading:** distinguish three data situations: initiation of alternative drugs at baseline, repeated eligibility, and simultaneous compatibility with multiple strategies. Next, progress from new-user comparisons to repeated trials and strategy copies.

#### 16. [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }})
{: #section-24 }

**Read first:** §§1–4, especially the five enrollment decisions in §2; then read the integrated explanation in the source companion.

**After reading:** explain why enrollment begins with new users, why an active comparator is useful, and why later discontinuation should not undo earlier enrollment. Next, address the lack of a unique natural starting point for someone who does not initiate today.

#### 17. [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }})
{: #section-25 }

**Read first:** §§1–6. Follow Mr. Li’s January and March records to separate the baselines and subsequent treatment in different small trials.

**After reading:** explain why one person can enter different trials at multiple eligible times and why analysis must account for their correlated records. Next, replace multiple starting points with multiple compatible strategies at one starting point.

#### 18. [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }})
{: #section-26 }

**Read first:** §§1–6. Then, within §7, read why alignment can hold before dialysis starts, followed by the step-by-step enrollment and assignment process from a shared starting point. Finally revisit step 11, §5, to compare the three investigators.

**After reading:** explain baseline copies, censoring times, deaths while waiting, the need for weighting, and why the target is strategy PP. You can now take the dialysis example from question to analysis. Next, examine whether outcome recording and unmeasured confounding can still mislead.

### Part 7: examine remaining uncertainty
{: #section-27 }

#### 19. [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }})
{: #section-28 }

**Read first:** the definitions, numerical examples, and practical approaches in §§1–7. Save expandable mathematical extensions for the second pass. Then read the source discussion of blinded outcome ascertainment and breast surgery.

**After reading:** explain why disease occurrence, detection, and recording are separate processes, and why testing pathways can play different roles when studying disease versus demand for surgery. Next, look for signs of residual bias after efforts to address adjustment and measurement.

#### 20. [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }})
{: #section-29 }

**Read first:** §§2–4 and §§6–8, initially focusing on the noncollapsed mechanisms and examples. Leave calibration formulas and competing-event details for the second pass.

**After reading:** explain what negative controls hold fixed and what they replace; why a suspicious association does not reveal the amount of bias or justify direct correction. Next, consider adding information previously absent from the analysis.

#### 21. [From Clinical Records to Adjustment Variables: NLP, Imaging, and Machine Learning]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }})
{: #section-30 }

**Read first:** §§2–7.

**After reading:** explain which information NLP, imaging, and machine learning help extract, measure, or model, and why they cannot guarantee elimination of unmeasured confounding. The first-pass route ends here. Use the integration exercise to test the full logic, rather than memorizing method names.

**Literature extension:** after understanding the relationship between machine learning and adjustment, read [High-Throughput Drug Screening and Federated Target Trial Emulation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}). It adds discussion of the IPTW framework and Fig. 1/Boxes 1–2, including high-throughput cohorts, training/validation/test splits, model selection, and SMDs. Other discussions remain in development. Prerequisites are TTE, IPW, and Cox. Distinguish expansion of implementation scale from causal identification requirements, then return to the protocol exercise below.

### Finish the main route: explain a protocol from beginning to end
{: #section-31 }

Return to §7 of [the hormone-therapy target trial protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}) and explain each sentence of the analysis plan. Then choose the hormone or dialysis example and answer in your own words:

1. Who is the shared target population, and what are the two complete rules?
2. Is the contrast assignment or adherence, and what are the outcome, horizon, and effect scale?
3. How do eligibility, strategy grouping, and follow-up align, and which later actions trigger censoring?
4. Why use this data organization and estimator, and which variables require attention?
5. Which assumptions, measurement issues, and residual biases still affect interpretation?

### Advanced stop for the second pass
{: #section-32 }

#### 22. [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }})
{: #section-33 }

**Read after completing the main route.** §§1–4 use one 200-person blood-pressure example throughout: why crude comparisons fail → what should be equal after addressing confounding → why observed blood pressure can still differ because of treatment → why subtract a candidate effect → how −10 is selected. §5 expresses within-health-stratum mean comparisons as estimating equations. §§6–8 cover longitudinal extensions, differences between methods, and assumptions; §10 revisits “common treatment history.”

**After reading:** explain how common treatment history relates to treatment choice, how a transformed outcome helps estimate effect parameters, and why this differs from both the g-formula and recovering each individual’s counterfactual. It belongs on the second pass so that targets, assumptions, treatment probabilities, and longitudinal strategies are already familiar.

## 2. Learning map
{: #section-34 }

<pre class="mermaid">flowchart TD
    Q[&quot;1–4: causal questions, notation, estimands, ITT/PP&quot;] --&gt; R[&quot;5–6: initiation/sustained rules and defined interventions&quot;]
    R --&gt; T[&quot;7–9: trial purpose, TTE, complete protocol&quot;]
    T --&gt; B[&quot;10–11: variable roles, confounding, time-related bias&quot;]
    B --&gt; M[&quot;12–14: Cox, g-formula, IPW&quot;]
    M --&gt; D[&quot;15–18: design overview, ACNU, sequential trials, CCW&quot;]
    D --&gt; V[&quot;19–21: measurement, negative controls, additional confounding information&quot;]
    V --&gt; C[&quot;Return to the protocol: explain design and analysis&quot;]
    C -. Second pass .-&gt; G[&quot;22: g-estimation and advanced derivations&quot;]</pre>

This is a compact version of §1’s route. Arrows indicate learning order, not causal effects. Use the terminology and notation below as references.

### Quick glossary
{: #section-35 }

<details class="study-callout" markdown="1">
<summary>Expand when you encounter an unfamiliar term</summary>


| Term | A starting interpretation |
| --- | --- |
| Exposure / treatment | The factor or action whose effects are studied; these notes mostly use treatment examples |
| Outcome | The result of interest, such as death within one year; specify both its content and horizon |
| Baseline / time zero | The clinical decision point when the study begins; patients may reach it on different calendar dates |
| Follow-up | Observation of outcomes from the starting point onward |
| Censoring | Subsequent event information ceases to be used or available from a time onward; it does not mean an event occurs then |
| Association | A difference or statistical relationship between observed groups, without a causal explanation by itself |
| Causal effect | A contrast of outcomes for the same person or target population under different interventions |
| Causal contrast | Which two intervention scenarios are compared in the same target population, such as assignment or adherence |
| Estimand | The specific target quantity, defined by population, strategies, outcome, time, and comparison scale |
| Estimator / estimate | The calculation rule versus its realized numerical result, such as a risk difference of −3 percentage points |
| Confounder | A typical example is health status affecting treatment choice and outcome; the adjustment set must follow the causal structure |
| Risk | Probability of an event within a specified horizon, such as 10% one-year mortality risk |
| Incidence rate | Events divided by total at-risk person-time, such as 10 events per 1,000 person-years |
| Hazard / HR | Instantaneous event intensity among those still event-free, and a ratio of two hazards; an HR is not a fixed-horizon risk ratio |
| Bias / random error | Systematic departure from the target versus finite-sample variability; a larger sample does not automatically fix bias |
| CI: confidence interval | Statistical uncertainty depending on the method and its assumptions; it does not automatically include systematic errors such as unmeasured confounding |

</details>


### Connecting the notation
{: #section-36 }

Most notes use $$A$$ for treatment, $$L$$ for covariates, and $$Y$$ for outcome. The foundations note follows the textbook’s $$T$$ and $$X$$ for treatment and covariates, whereas survival analysis often uses $$T$$ for event time. **The same letter can have different definitions across notes; check the local notation first.** For example, subscripts in $$A_0,A_1$$ often denote decision times, those in $$g_0,g_1$$ label strategies, and the 5 in $$Y_5$$ can denote a five-year horizon. Superscripts $$a$$ or $$g$$ often identify a potential outcome under an intervention, not exponentiation. See the [full notation reference]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}#section-16).

## 3. Review by question
{: #section-37 }

Choose the group matching your current question; there is no need to reread the entire guide.

### Causal effects and estimands
{: #section-38 }

<details class="study-callout" markdown="1">
<summary>Expand: causal effects and estimands</summary>


| When you ask… | Return to… |
| --- | --- |
| Why does ATT retain treated people and weight only controls, and how does it differ from ATE? | [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-7) |
| Why is a causal effect not simply the difference between two observed group means? | [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}) |
| What exactly is a treatment effect, and why is it not the before–after change? | [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-1) |
| What do Delta, Y, g, subscript 5, P, and =1 mean in a five-year risk-difference formula? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}#section-7) |
| When are superscripts not powers, when are subscripts not time, and how do hats, bars, sums, and products work? | [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}) |
| What does do(A=1) mean, and why is everything after a conditional bar not necessarily a selection condition? | [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}#section-10) |
| Why do do and Y¹ correspond without automatically eliminating confounding? | [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}#section-11) |
| Why does do remove arrows into treatment while retaining the effect of health on the outcome? | [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}#section-12) |
| Why can treatment effects remain after confounding is controlled, and what does subtracting an effect mean? | [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-5) |
| Why is causal contrast a design component, and why is it often expressed as ITT or PP? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}) |
| What do ITT and PP each compare? Does contrast mean ITT minus PP? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}#section-3) |
| Why study ITT and PP, and must every TTE estimate both? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}#section-11) |
| What does an ITT/PP results table look like, and how does a risk difference translate to events per 1,000? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}#section-12) |
| If PP is more favorable than ITT, can their difference directly measure the benefit of improved adherence? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}#section-13) |
| Without random assignment in TTE, should a result be called ITT, an initiation effect, or sustained PP? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}#section-16) |
| How does a complete estimand differ from a causal contrast, risk difference, or Cox method? | [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}#section-6) |
| Does this study compare assignment, initiation, or sustained adherence? | [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}) |
| Why does randomized-trial ITT concern Z → Y while observational analysis often concerns A → Y? | [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-14) |
| How do prescribing, dispensing, and actual use define different groups, and why is prescribing closer to ITT? | [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-23) |
| If assignment and initiation coincide at baseline, does that require future adherence? | [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-29) |
| Even without unmeasured confounding and with correct models, why does sustained PP usually require g-methods? | [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-30) |
| Why can ITT require adjustment for later loss-to-follow-up factors even when original groups are retained? | [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-31) |

</details>


### Target trials and protocol components
{: #section-39 }

<details class="study-callout" markdown="1">
<summary>Expand: target trials and protocol components</summary>


| When you ask… | Return to… |
| --- | --- |
| What is a pragmatic trial, and how does it relate to randomization and ITT/PP? | [Pragmatic Trials in Routine Care]({{ "/causal-inference/pragmatic-trials/" | relative_url }}) |
| What exactly is T₀, and where does follow-up begin and end? | [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}) |
| Does TTE inspect future medication before deciding who enters? | [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-4) |
| How can an early/late dialysis TTE enroll and assign people before their future dialysis dates are known? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-18) |
| If alignment is required, how can a patient enter before dialysis starts? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-24) — distinguish eligibility, strategy assignment, follow-up, and actual dialysis; waiting is also part of the rule. |
| Is finding an initiation date and then checking prior eligibility a form of looking into the future? | [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-4) |
| How do enrollment, treatment grouping, and identifying deviations during follow-up differ? | [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-5) |
| Why is backfilling groups from future treatment wrong while later treatment can trigger censoring in CCW? | [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-6) |
| How do the seven hormone-therapy protocol components fit together? | [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}) |
| Why can safety-related discontinuation remain compatible with PP and not end follow-up? | [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}#section-7) |
| Can the original eligibility rule be retained with billing records for a test but no test result? | [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}#section-19) |
| Why use prior healthcare history but not require that people actually remain in records throughout the future? | [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}#section-21) |
| How does excluding a whole person differ from censoring at loss to follow-up, and does no bill imply loss? | [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}#section-22) |

</details>


### Interventions, confounding, and time-related bias
{: #section-40 }

<details class="study-callout" markdown="1">
<summary>Expand: interventions, confounding, and time-related bias</summary>


| When you ask… | Return to… |
| --- | --- |
| What is the intervention when studying a biomarker? | [Biomarkers and Well-Defined Interventions]({{ "/causal-inference/biomarkers-well-defined-interventions/" | relative_url }}) |
| Why do some PP protocols allow discontinuation while others require sustained use? | [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}#section-2) |
| Why does initiation generally require baseline treatment-confounding control while sustained strategies involve later decisions? | [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}#section-8) |
| How should a longitudinal DAG with L₀, A₀, L₁, and A₁ be read, and must it contain treatment–confounder feedback? | [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}#section-9) |
| If hospitals have different adherence and initiation effects, does that establish bias? | [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}#section-5) |
| Which variables should be adjusted for, and which are components of treatment? | [Confounding and Treatment Components: Kidney Transplantation]({{ "/causal-inference/confounding-treatment-components/" | relative_url }}) |
| Why can including only people who survive to treatment bias strategy comparisons? | [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}) |
| How can confounding and selection bias be distinguished when both make groups noncomparable? | [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}#section-28) |

</details>


### Survival analysis and g-methods
{: #section-41 }

<details class="study-callout" markdown="1">
<summary>Expand: survival analysis and g-methods</summary>


| When you ask… | Return to… |
| --- | --- |
| What is SW_i, why do stabilized weights multiply by the group proportion, and do they necessarily reduce variance? | [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-20) |
| When g-formula and IPTW compare A/B, which models do they fit and how do they calculate risks? | [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}#section-9) |
| At which TTE step is IPTW used, and how does it relate to randomization? | [High-Throughput Drug Screening and Federated Target Trial Emulation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-4) |
| Does classical IPTW need train/test splitting, and can someone contribute to fitting their own propensity score? | [High-Throughput Drug Screening and Federated Target Trial Emulation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-28) |
| How do several covariates jointly produce individual propensity scores and weights in an A/B comparison? | [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) |
| Why assess balance on combined training/validation data, and do combined data in Boxes 1 and 2 refer to the same people? | [High-Throughput Drug Screening and Federated Target Trial Emulation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-24); [High-Throughput Drug Screening and Federated Target Trial Emulation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-25) |
| Who is compared at each Cox event time, and why do censored people still contribute information? | [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-4) |
| Does correctly coding censoring prevent informative-censoring bias? | [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-3) |
| Why can immortal time, selection, and measurement biases persist after Cox adjustment? | [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-9) |
| Is an HR the same as a five-year mortality risk ratio? | [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-8) |
| How does the g-formula turn observational data into intervention risks? | [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}#section-2) |
| Why should post-treatment health not be forced to have the same distribution? | [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}#section-14) |
| Why invert probabilities in IPW, and why do untreated people receive 1/(1−e)? | [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-3) |
| Why are longitudinal weights multiplied, and how do IPTW and IPCW differ? | [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) |
| What does common treatment history mean, and why does the source connect it to g-estimation? | [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}#section-22) |
| How does subtracting candidate effects identify a causal parameter in g-estimation? | [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}#section-10) |
| What does each symbol in H(ψ)=Y−ψA mean, and why is subtraction applied only to treated people? | [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}#section-7) |
| Why does subtracting −10 add 10 back, and is H a true counterfactual? | [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}#section-8) |
| Why does multiplying a treatment residual by H correspond to comparing means within health strata? | [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}#section-16) |
| Are g-estimation, g-formula, and IPW the same method? | [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}#section-19) |

</details>


### Emulation designs for observational studies
{: #section-42 }

<details class="study-callout" markdown="1">
<summary>Expand: emulation designs for observational studies</summary>


| When you ask… | Return to… |
| --- | --- |
| When should ACNU, CCW, or sequential trials be used? | [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}) |
| Who are initiators, and why does a no-treatment strategy also have baseline strategy initiators? | [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-4) |
| How do later discontinuation, a refill today, and insufficient prior records affect new-user eligibility? | [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-6) |
| Why does comparing initiators reduce treatment-affected eligibility selection? | [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-13) |
| How can a baseline variable already have been affected by treatment? | [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-16) |
| Why cannot prevalent users versus never-users directly correspond to a randomized trial? | [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-21) |
| Why can a prevalent-user comparison miss early coronary risk after hormone initiation? | [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-18) |
| If a woman remains eligible from age 51 to 65, which time should be time zero? | [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}#section-2) |
| Does monthly trial emulation require every person to visit every month? | [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}#section-3) |
| When someone later initiates, what happens to their earlier control records? | [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}#section-6) |
| Why can repeated enrollment improve efficiency without creating independent patients for standard errors? | [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}#section-11); [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}#section-14) |
| Do first-eligible-time and all-eligible-time analyses necessarily estimate the same average effect? | [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}#section-15) |
| What is a grace period, and why can someone not yet treated within three months still follow an initiation strategy? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-2); [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-3) |
| Why is a death in month 2 counted in both copies rather than excluding the untreated person? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-7) |
| Is a predialysis death always counted in both early and late groups? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-22) |
| Does randomly assigning a record to one compatible strategy create a randomized trial? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-5) |
| Why does comparing clone labels without handling deviations give identical results? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-13) |
| If CCW usually targets PP, does a grace period make ITT impossible? | [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-15) |

</details>


### Outcome measurement and residual bias
{: #section-43 }

<details class="study-callout" markdown="1">
<summary>Expand: outcome measurement and residual bias</summary>


| When you ask… | Return to… |
| --- | --- |
| Could more outcomes in the treated group simply reflect more testing? | [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}) |
| What does systematic and blind outcome ascertainment mean? | [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-18) |
| Why cannot retrospective blinded expert review automatically repair unequal case detection? | [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-20) |
| Why can an independent death registry reduce ascertainment differences related to knowledge of treatment? | [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-21) |
| Why can extra testing be bias for cancer occurrence yet part of the treatment effect on surgery demand? | [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-14) |
| How can remaining residual bias be investigated after the main analysis? | [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}) |
| Why should negative controls share sufficiently similar confounders with the main outcome? | [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}#section-9) |
| Can an outcome with a known nonzero effect also help assess a study? | [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}#section-20) |
| What is a treatment control, and how does it differ from an active comparator? | [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}#section-21) |
| Is lack of a direct effect on stroke sufficient to make stroke a negative control? | [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}#section-13) |
| What can protective associations in both main and negative-control analyses tell us? | [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}#section-5) |
| If treatment does not affect true disease, why might it still affect recorded negative-control diagnoses? | [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}); [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-13) |
| How can NLP and image processing help address previously unmeasured confounding? | [From Clinical Records to Adjustment Variables: NLP, Imaging, and Machine Learning]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }}) |
| How does machine learning for combinations of variables relate to IPW and the g-formula? | [From Clinical Records to Adjustment Variables: NLP, Imaging, and Machine Learning]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }}#section-7) |
| Why do more variables and more accurate prediction still not prove absence of confounding? | [From Clinical Records to Adjustment Variables: NLP, Imaging, and Machine Learning]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }}#section-10) |

</details>


## 4. Review by case
{: #section-44 }

These integration exercises are for after the main route, or when a specific question causes difficulty. On a first reading, continue sequentially through §1.

### Methods route: calculate first, then connect to longitudinal questions
{: #section-45 }

<details class="study-callout" markdown="1">
<summary>Expand this review exercise</summary>


If treatment effects remain unclear, first read [What exactly is a treatment effect?]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-1), then begin the calculations below.

1. [Cox proportional hazards]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}), §§1–4: four people, three deaths, and a hand-calculated HR.
2. [G-formula]({{ "/causal-inference/g-formula/" | relative_url }}), §§1–4: standardized risks for a shared baseline population of 1,000 people.
3. [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}), §§1–5: weight the same table and verify the same 12.5% and 25% risks.
4. [G-estimation]({{ "/causal-inference/g-estimation/" | relative_url }}), §§1–5: use a separate 200-person blood-pressure example to move from crude comparisons to candidate effects, then understand why the estimating equation aggregates within-health-stratum differences.
5. Return to g-formula §§5–8, IPW §§7–9, and g-estimation §6 for two treatment decisions and sustained strategies.

</details>


### Postmenopausal hormone therapy and breast cancer
{: #section-46 }

<details class="study-callout" markdown="1">
<summary>Expand this review exercise</summary>


1. [Causal contrasts and estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}): separate assignment from protocol adherence.
2. [Pragmatic trials]({{ "/causal-inference/pragmatic-trials/" | relative_url }}): understand why target trials often use routine-care conditions.
3. [Hormone-therapy target trial protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}): read the source table component by component, especially no use throughout follow-up and safety exceptions for discontinuation. Use §§8.2–8.4 to practice missing eligibility information, baseline proxies, and loss-to-follow-up handling.

   Additional starting-point discussion: [Eligibility from ages 51 to 65]({{ "/causal-inference/sequential-trials/" | relative_url }}#section-2). Understand why a woman does not require one unique lifetime baseline and why her future health or survival cannot determine earlier enrollment.

4. [Point interventions and sustained strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}): decide whether later behavior violates the specific protocol.
5. [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) and [g-formula]({{ "/causal-inference/g-formula/" | relative_url }}): revisit the case’s analysis plan to understand adherence-related time-varying confounding and selection.

   Use [the three layers of the analysis plan]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-28) to distinguish baseline grouping, strategy deviations, and loss to follow-up.

   For grace periods, read [initiation, noninitiation, and death during a three-month grace period]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-7) and §6. Use the three treatment histories to examine early events, artificial censoring, and PP. For breast cancer, death is a competing event, not a breast-cancer event.

6. [Systematic, blinded ascertainment and breast surgery]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-17): distinguish cancer occurrence, diagnosis, and actual surgery, and explain why lack of blinding has different consequences for different targets.
7. [Outcome controls, known-effect controls, and treatment controls]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}#section-23): examine brain cancer and pneumonia as candidate outcomes and state the conditions for a valid negative control.
8. [Clinical records and adjustment variables]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }}): use pretreatment family-history records to distinguish detecting residual confounding from adding information for adjustment.

</details>


### Timing of dialysis initiation
{: #section-47 }

<details class="study-callout" markdown="1">
<summary>Expand this review exercise</summary>


1. [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}): begin with shared eligibility and $$T_0$$.
2. [Why alignment can hold before dialysis begins]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-24): distinguish starting a strategy from actually receiving dialysis. Then follow the [correct step-by-step workflow]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-18), from eGFR 18 to dialysis or death, separating baseline copies from subsequent deviations.
3. [The three-investigator thought experiment]({{ "/causal-inference/time-related-biases/" | relative_url }}#section-20): compare investigators 1, 2, and 3 and explain each design error.
4. [What the dialysis-timing causal contrast compares]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-17): connect the workflow to the PP contrast of early versus late initiation strategies.
5. [Surveillance and measurement bias]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}): consider how eGFR measurement frequency affects strategy classification and outcome records.
6. [Cox proportional hazards]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}), §§6–8: explain how incorrect inclusion, timing, and grouping alter risk-set comparisons.
7. [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}), §8: understand why artificial censoring after deviation from early or late initiation requires weighting.

</details>


### Comparing medications
{: #section-48 }

<details class="study-callout" markdown="1">
<summary>Expand this review exercise</summary>


1. [Active-comparator new-user design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}): start with initiators facing similar clinical options. Use the final prevalent-user example to check whether eligibility and covariates have already been affected by earlier treatment.
2. [ITT and PP]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}): separate random assignment from actual initiation.
3. [Point interventions and sustained strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}): examine discontinuation rules, time-varying confounding, and estimation methods.
4. [Sequential trials]({{ "/causal-inference/sequential-trials/" | relative_url }}): handle repeated decision points for initiating now versus not initiating now. Use §6 to distinguish unique people, enrollment records, and the population over which effects are averaged. If assignment at each enrollment is unclear, return to [the three separate operations of enrollment, grouping, and deviation assessment]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-5).
5. [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}): handle grace periods, treatment deviations, and sustained strategies.
6. [Negative controls]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}): investigate remaining systematic errors. Use §8 to distinguish additional checks changing outcomes or treatments from the active comparator in the main analysis.

Advanced companion: the source links common treatment history to [g-estimation]({{ "/causal-inference/g-estimation/" | relative_url }}#section-22). First distinguish initiation among nonusers from continuation/discontinuation among current users, then connect the methods.

Calculation exercise: use the shared [g-formula]({{ "/causal-inference/g-formula/" | relative_url }}) and [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) example, first for baseline initiation and then for sustained strategies.

</details>


## 5. A three-pass review method
{: #section-49 }

### First pass: explain the question in your own words
{: #section-50 }

Follow steps 1–21 and their reading ranges, then answer the five integration questions. Expandable derivations can wait, but their underlying assumptions and interpretive limits cannot be skipped.

### Second pass: identify errors in a data analysis
{: #section-51 }

Add step 22, g-estimation, and revisit formulas, source passages, and long examples skipped initially. Recalculate the numbers first, then use the case exercises to check that design, grouping, censoring, and estimation address the same question.

### Third pass: state the identification conditions
{: #section-52 }

Write a target trial protocol for your own question and describe how observational data map to each component. State exchangeability, positivity, consistency, measurement, and censoring conditions. When using potential outcomes or a DAG, explain the basis of every symbol and arrow.

## 6. Maintaining the study guide
{: #section-53 }

<aside class="study-callout study-callout--important" markdown="1">

**Keep one continuous reading route when adding material**

1. Identify the question answered and prerequisite concepts, then place the material appropriately in §1 rather than merely appending a link.
2. Revise the preceding step’s transition, the new step’s reading range and self-check objective, and the following step’s connection to maintain continuity.
3. Keep one numbering sequence for the first pass. When order changes, update the map, step references, and topic count together.
4. Place detailed derivations, narrow topics, and close source interpretations on the second pass or as supplements to relevant steps. Do not create a competing main route. G-estimation currently belongs on the second pass.
5. Add common questions to §3 and case-spanning additions to §4. These support reference and consolidation; §1 remains the first-pass entry point.
6. Explain every variable, parameter, subscript, superscript, operator, value, and unit alongside a new formula. Identify whether it is a definition, assumption, model, or estimation formula. Pair important formulas with a plain-language reading and checkable example, including inside expandable sections.
7. Develop technical sections as: concrete question → why the preceding step is insufficient → why the next step helps → calculation with the same example → corresponding formula → interpretation and conditions. Explain the purpose of every operation and symbol, link missing prerequisites, and reserve advanced derivations for the second pass. A glossary alone does not repair missing logical steps in the main text.
8. Update dates and check scientific accuracy, numbers, sources, links, and anchors. Mark unfinished topics explicitly; do not use empty links as though the notes already exist.

</aside>
