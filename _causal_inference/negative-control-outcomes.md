---
layout: "causal-note"
title: "Negative Control Outcomes and Residual Bias"
description: "Use negative controls to investigate residual bias while respecting their assumptions and limits for correction."
group: "Bias and measurement"
order: 20
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Translation of the source passage", "anchor": "section-1"}, {"title": "2. A negative-control outcome is not “another group of patients”", "anchor": "section-2"}, {"title": "3. Why can an outcome unaffected by treatment reveal bias?", "anchor": "section-3"}, {"title": "4. What makes a useful negative control?", "anchor": "section-6"}, {"title": "5. How should the SGLT2-inhibitor and stroke example be interpreted?", "anchor": "section-11"}, {"title": "6. What do an association and its absence each tell us?", "anchor": "section-14"}, {"title": "7. Detecting and adjusting are different tasks", "anchor": "section-15"}, {"title": "8. How does benchmarking differ from negative controls?", "anchor": "section-18"}, {"title": "9. Self-check", "anchor": "section-24"}, {"title": "Main sources", "anchor": "section-25"}]
previous_note: "/causal-inference/surveillance-measurement-bias/"
next_note: "/causal-inference/clinical-data-adjustment/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Begin with the core logic**

Find an outcome that there is good reason to believe **will not be changed by the treatment strategies being compared**, then ask whether the same observational analysis nevertheless estimates a “treatment effect” on it.

If the estimate clearly departs from the expected null value, investigate residual bias or problems with the negative-control assumptions, taking sampling uncertainty into account.

**Negative controls help detect problems; they do not automatically prove or repair everything.**

</aside>


<aside class="study-callout study-callout--tip" markdown="1">

**How to approach a first reading**

§1 introduces the source passage; §2–§4 cover the definition, a numerical example, and selection criteria. §6 explains interpretation. Leave adjustment methods in §7 for advanced reading; §8 distinguishes other controls and benchmarking.

</aside>


Prerequisite: confounding and exchangeability in [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}).

## 1. Translation of the source passage
{: #section-1 }

The passage comes from the concluding section of [Fu (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/). The translation follows its meaning; “detect” and “adjust” require different conditions, as discussed in §7.

> Negative-control outcomes can be used to detect and adjust for residual bias. Existing knowledge suggests that treatment should not affect these outcomes, so an association between treatment and a negative-control outcome suggests possible residual bias.
>
> For example, research on sodium–glucose cotransporter 2 inhibitors (SGLT2 inhibitors) can draw on randomized-trial evidence that did not show an effect on nonfatal stroke. Both benchmarking and negative controls require subject-matter knowledge, often obtained from previous trials; without trial evidence, observational research may be more difficult.

<aside class="study-callout study-callout--note" markdown="1">

**How should “showed no effect” be interpreted?**

**Failure to find a statistically significant effect does not prove that the true effect is exactly zero.** This describes the author’s reasoning for choosing a negative control at that time; it cannot be generalized to every drug, population, and comparator. §5 explains this using a specific estimate.

</aside>


## 2. A negative-control outcome is not “another group of patients”
{: #section-2 }

Let:

- $$A$$: treatment group, for example initiation of drug A or B.
- $$Y$$: the primary outcome of interest.
- $$N$$: a negative-control outcome (NCO).

Within the same treatment comparison, we originally analyze $$A$$–$$Y$$ and now additionally analyze $$A$$–$$N$$.

| Primary analysis | Negative-control analysis |
| --- | --- |
| What effect does treatment A versus B have on primary outcome Y? | Does the same treatment comparison also show an association with N, on which no effect is expected? |
| The true causal effect remains to be studied | Independent reasons support a zero or sufficiently near-zero causal effect of the compared strategies on N |

Usually retain comparable eligibility rules, treatment definitions, time zero, follow-up design, and relevant confounding control so the negative control can diagnose related analytical problems. Clearly explain any different handling required by the outcome’s characteristics.

“Negative” means neither harmful nor a negative numerical effect. It indicates a **control relationship expected to have no treatment effect**.

The null value depends on the effect scale: 0 for a risk difference, 1 for a risk ratio or HR. “Near-zero effect” below means approximately no causal effect, not that every ratio should approach the number 0.

A negative control is not a placebo group either. It usually means an additional analysis of N, not simply adding N to the primary regression as if adjustment were then complete.

## 3. Why can an outcome unaffected by treatment reveal bias?
{: #section-3 }

Suppose an inadequately measured factor $$U$$, such as health or healthcare-seeking behavior, affects:

- Whether a person receives A or B.
- Primary outcome Y.
- Negative-control outcome N.

But the treatments being compared do not affect N.

<pre class="mermaid">flowchart LR
    U[&quot;U: Inadequately controlled factor&quot;] --&gt; A[&quot;A: Treatment choice&quot;]
    U --&gt; Y[&quot;Y: Primary outcome&quot;]
    U --&gt; N[&quot;N: Negative-control outcome&quot;]
    A --&gt; Y</pre>

The diagram has no causal $$A\rightarrow N$$ pathway, but it has:

$$
A\leftarrow U\rightarrow N.
$$

A and N can therefore have a noncausal association. If the relevant U also affects Y, the primary analysis may contain similar confounding.

This diagram shows only confounding. Negative controls can also reflect selection bias, differential outcome detection, or other analytical problems. They do not identify the particular bias mechanism by themselves.

The basic approach is described by [Lipsitch, Tchetgen Tchetgen, and Cohen (2010)](https://pubmed.ncbi.nlm.nih.gov/20335814/).

### A fully invented numerical example
{: #section-4 }

Assume neither treatment A nor B causally affects N, and N is completely and accurately observed, but unmeasured health differs between groups:

| Health state U | Number in A | Number in B | N risk in this state, identical under both treatments |
| --- | ---: | ---: | ---: |
| Lower risk | 750 | 250 | 2% |
| Higher risk | 250 | 750 | 10% |
| Total | 1,000 | 1,000 | — |

Expected recorded events in A are:

$$
750\times 2\%+250\times10\%=40\text{ events},
$$

and in B:

$$
250\times2\%+750\times10\%=80\text{ events}.
$$

These expected risks give:

$$
RR_N=\frac{40/1000}{80/1000}=0.5.
$$

RR means risk ratio, and subscript N identifies the negative-control outcome. The numerator is A’s negative-control event risk over the specified period; the denominator is B’s. Each 1000 is the group’s total size, not its number of cases. A ratio of 0.5 means A’s negative-control risk is half B’s. Risk ratios are unitless and have null value 1. This is an association between observed groups, not proof that treatment halves negative-control risk.

A appears to halve N’s risk, but we specified identical A and B effects on N within the same health state. The difference arises because more A recipients are lower risk.

If $$U$$ later became accurately measured, standardizing both groups to a common “half lower risk, half higher risk” population would, under this example’s assumptions, give $$0.5\times2\%+0.5\times10\%=6\%$$ in both groups and return the ratio to 1. This is guaranteed by the complete confounding structure we specified. In a real study, a negative control does not identify $$U$$ automatically or guarantee that adjusting one variable is enough. See [The G-Formula]({{ "/causal-inference/g-formula/" | relative_url }}) for standardization.

If Y also depends on this uncontrolled factor, the primary analysis may have related confounding. U can represent factors remaining after routine adjustment, so “many variables were already adjusted” does not rule this out.

### Return this logic to the hormone-therapy source passage
{: #section-5 }

The source’s primary question is: **What effect do the defined hormone-therapy strategies have on breast cancer?** The authors then suggest brain cancer and pneumonia as candidate control outcomes. They are not replacing participants with another group of “control patients”; they add another outcome within as similar a design as possible.

To isolate the logic, let $$N$$ denote a justified, suitable negative control, without assuming brain cancer or pneumonia works in every setting. Suppose the analysis gives these teaching results:

| Analysis | Estimated risk ratio | Interpretation |
| --- | ---: | --- |
| Same hormone-strategy comparison, breast cancer $$Y$$ | 0.70 | Apparently associated with lower breast-cancer risk; causal interpretation still needs justification |
| Same hormone-strategy comparison, negative control $$N$$ | 0.50 | If the expected-null justification holds, this clear departure from 1 deserves investigation |

The second row prompts us to examine whether recipients of the different strategies had uncontrolled pre-existing differences. **Concern about related confounding in the primary analysis is justified only if those differences also affect breast cancer.** The 4% versus 8% example shows how composition differences can generate a spurious association; it does not establish identical factors or bias magnitudes in actual hormone research.

Actual analysis also requires confidence intervals, appropriate negative-control selection, and attention to selection and measurement. “Protective associations for both outcomes” cannot directly establish that hormones are ineffective, and $$0.70/0.50$$ cannot automatically correct the primary result.

## 4. What makes a useful negative control?
{: #section-6 }

### Condition 1: A justified expectation of no causal effect in the specific treatment contrast
{: #section-7 }

Independent subject-matter knowledge or external evidence must support the expected null effect of the compared strategies on N. “No direct pharmacological effect” alone is insufficient: consider indirect effects, population, follow-up period, and outcome definition. If N is “diagnosed disease,” strategy-induced testing changes may affect it; see [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}).

The negative control concerns a **contrast between treatment strategies**:

> No effect of A versus placebo on N does not guarantee no effect of A versus another drug B on N.

If B reduces N, the A–B difference may be a real effect. If external evidence supports only an approximately null effect, include that uncertainty rather than treating the reference value as precisely known.

<aside class="study-callout study-callout--note" markdown="1">

**If true disease is unaffected, why can diagnosis records still be associated?**

If treatment leaves true negative-control disease occurrence unchanged but increases testing and detection, it can genuinely affect “recorded disease.” This result may still signal surveillance problems in the primary study, but does not alone establish unmeasured confounding.

When using negative controls to assess measurement bias, distinguish true events from records: which outcome has the expected null effect, and which recording process is being investigated? One cannot define “diagnosis records” as the outcome and simultaneously declare treatment-induced diagnosis changes noncausal. See [What if surveillance is part of the treatment strategy?]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}#section-13).

</aside>


### Condition 2: It reflects the bias of concern in the primary analysis
{: #section-8 }

The negative control should share relevant uncontrolled causes, selection processes, or measurement processes with the primary analysis. State explicitly: **which bias is it expected to detect, and why does it reflect the primary analysis’s problem?**

#### Why does the source require “confounders sufficiently similar”?
{: #section-9 }

“Sufficiently similar” concerns relevant confounding sources, not merely similar disease names, organs, or incidence. Lipsitch and colleagues call this **U-comparability**: comparability between primary and negative-control analyses in relevant uncontrolled common causes $$U$$.

Two counterexamples clarify the limits:

- A factor affects treatment and the primary outcome but not the negative control: the primary analysis may be confounded, yet the negative control cannot detect it.
- Another factor affects treatment and the negative control but not the primary outcome: the negative control may be associated with treatment, without establishing the same bias in the primary outcome.

Thus “unaffected by treatment” is only the first condition. **Sharing confounding sources does not mean numerically equal bias**: relationship strength, direction, and measurement processes may differ. Numerical adjustment requires the additional conditions in §7. [Lipsitch et al. (2010), Figures 2–3 and discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/)

### Condition 3: Sufficient information and credible measurement
{: #section-10 }

An N that is rare, severely underdiagnosed, or estimated very imprecisely cannot provide a strong diagnostic.

A p-value above 0.05 does not mean a negative control “passed.” Examine the estimate, confidence interval, magnitudes of bias that can be excluded, and the suitability of the control mechanism. The p-value here is not a group’s disease risk denoted earlier by probability symbol P.

See [Negative controls: Concepts and caveats (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10515451/) for these limitations.

## 5. How should the SGLT2-inhibitor and stroke example be interpreted?
{: #section-11 }

Fu suggests using RCT evidence to consider nonfatal stroke as a candidate negative control when studying SGLT2 inhibitors’ primary outcomes. A clear association in the same analysis should prompt investigation of residual bias and the candidate’s applicability. It supplies a clue, not a definitive bias mechanism.

### Why retain the word “candidate”?
{: #section-12 }

As a supplementary example, a 2021 meta-analysis combining CREDENCE and other large trials reported a pooled nonfatal-stroke HR of 0.97, with 95% confidence interval (CI) 0.76–1.24. The point estimate is close to 1, but the interval remains compatible with some benefit or harm. It does not prove that the true effect is exactly zero.

Source: [Effect of SGLT2 Inhibitors on Stroke and Atrial Fibrillation in Diabetic Kidney Disease: Results From the CREDENCE Trial and Meta-Analysis](https://www.ahajournals.org/doi/pdf/10.1161/STROKEAHA.120.031623), pooled nonfatal-stroke results in Figure 3. This illustrates the evidence available then; actual negative-control selection must also check subsequent research and the current specific contrast.

In practice, verify:

- Are the drugs and comparators the same?
- Are the populations, observation periods, and outcome definitions compatible?
- Does RCT ITT evidence support the same “null effect” judgment as the observational initiation effect or sustained-strategy PP effect?
- Is there adequate mechanistic knowledge and precise evidence, rather than merely an RCT P-value above 0.05?

See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}). RCT evidence supports the choice; it does not replace an assessment of negative-control validity.

### Competing events also affect negative-control judgments
{: #section-13 }

**Death before stroke prevents a patient from subsequently having a nonfatal stroke.** Death is therefore a competing event for this outcome. A treatment reducing earlier death may leave more people alive with an opportunity to experience stroke. Even without directly changing stroke biology, the two strategies’ “cumulative probability of nonfatal stroke within five years” may differ.

Thus “no direct action on stroke” does not guarantee a valid negative control. The expected null must correspond to **the compared strategies, follow-up horizon, and specific effect scale**. An HR near 1 in one study does not establish a necessarily zero five-year risk difference in another. This is an inference applying the competing-event framework to the example, not a claim that SGLT2 inhibitors necessarily increase stroke through this mechanism. [Young et al.: Causal estimands with competing events](https://onlinelibrary.wiley.com/doi/10.1002/sim.8471)

## 6. What do an association and its absence each tell us?
{: #section-14 }

| Negative-control result | Reasonable interpretation | Conclusion not directly justified |
| --- | --- | --- |
| Clear departure from the expected null | Investigate residual bias, control validity, and random error | The primary analysis is necessarily invalid, or the bias’s source, magnitude, or direction is known |
| Near null and relatively precise | Under valid negative-control assumptions, reduces concern about some biases it can reflect | All unmeasured confounding and other biases have been excluded |
| Near null with a wide interval | Insufficient evidence; important bias may remain | The negative control “passed” |

Even valid negative controls can show chance associations in one sample; testing many controls also requires attention to multiple comparisons.

A null association can reflect low power, a weak link to the primary bias, or cancellation between opposing biases. **Negative controls are not universal tests proving exchangeability.**

For assumptions and limits, see [Negative controls: Concepts and caveats](https://pmc.ncbi.nlm.nih.gov/articles/PMC10515451/).

## 7. Detecting and adjusting are different tasks
{: #section-15 }

### Detect: Find clues to bias
{: #section-16 }

When an expected-null relationship shows an association, examine:

- Omitted or crudely measured important baseline factors.
- Alignment of time zero, eligibility, and treatment assignment.
- Selection based on future treatment, survival, or adherence.
- Differences in testing and recording opportunities.

Related notes: [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}), [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}), and [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}).

Negative-control selection should have an a priori justification and results should be reported transparently. Do not retain only controls matching expectations or arbitrarily change models to push them back to zero.

### Adjust: Additional identification or calibration conditions are needed
{: #section-17 }

One negative-control estimate usually cannot determine how much bias affects the primary outcome.

For example, suppose the observed primary-outcome RR is 0.70 and the negative-control RR is 0.60:

> One cannot simply calculate $$0.70/0.60$$ and declare it the corrected true treatment effect.

Unmeasured factors can affect the outcomes with different strengths, measurement processes, and bias directions.

Advanced approaches for a second reading may include:

- Correcting effects with negative controls under additional assumptions linking the biases.
- Combining negative-control exposures and outcomes to identify effects using information about unmeasured confounding.
- Estimating a systematic-error distribution from several negative controls to empirically calibrate P-values or confidence intervals.

For example, [double-negative-control methods](https://www.tandfonline.com/doi/full/10.1080/24754269.2024.2390748) use additional variables’ information about unmeasured confounding but require stronger identification conditions. [Empirical P-value calibration](https://pmc.ncbi.nlm.nih.gov/articles/PMC4285234/) requires a collection of negative controls representative of the target analysis’s systematic error. Initially, remember that detecting a suspicious association and numerically correcting the main effect are separate tasks with different requirements.

Calibrating statistical inference does not establish that the primary point estimate is unbiased.

<details class="study-callout" markdown="1">
<summary>Advanced: Why not simply subtract?</summary>

On a selected additive scale, such as a risk difference, an estimate can be represented schematically as:

$$
\widehat\Delta_Y=\Delta_Y+b_Y+\varepsilon_Y,
$$

$$
\widehat\Delta_N=0+b_N+\varepsilon_N.
$$

**Reading the symbols:** Y is the primary outcome and N the negative-control outcome; subscripts identify the analysis, not multiplication. $$\Delta_Y$$ is the true primary effect. $$\widehat\Delta_Y$$ and $$\widehat\Delta_N$$ are sample effect estimates, with hats indicating estimates rather than true values. $$b_Y,b_N$$ are their systematic biases; Greek letters $$\varepsilon_Y,\varepsilon_N$$ denote random sampling fluctuations. The 0 in the second equation comes from assuming a true null negative-control effect, not from observed data necessarily being zero.

All terms must use the same scale. For a risk difference, use probability differences throughout or percentage points throughout; do not add a risk ratio to percentage points. Read “estimate = true effect + systematic bias + this sample’s random fluctuation.” This explanatory decomposition does not imply its right-hand components are individually known.

Even knowing N’s true effect is zero mainly informs us about $$b_N$$. Justified numerical correction requires a further relationship between $$b_N$$ and $$b_Y$$.

Direct subtraction, for example, assumes equal biases on a particular scale—a strong condition not implied merely by calling something a negative control.

Invented example: the primary true risk difference is −4 percentage points, its systematic bias −3, and random fluctuation temporarily 0, giving an estimate of −7. The negative control has true effect 0 but bias −1, giving an estimate of −1. Subtraction yields −6, still not the true −4. The problem is unequal biases, not incorrect arithmetic.

</details>


## 8. How does benchmarking differ from negative controls?
{: #section-18 }

**Benchmarking** asks whether an observational study reproduces compatible results for a question with credible trial evidence, under compatible populations, strategies, outcomes, follow-up, and causal contrasts.

| Method | Reference | Main use |
| --- | --- | --- |
| Benchmarking | A credible existing RCT result, potentially nonzero | Assess observational data and methods on a previously studied question |
| Negative-control outcome | An outcome with a justified expected null causal effect | Check whether an analysis produces suspicious associations for null relationships |

Benchmarking should not merely ask whether two P-values are both significant. Compare effect estimates, uncertainty, and alignment of the research questions.

Reproducing one RCT does not guarantee absence of bias for a new drug, population, or outcome. A near-null negative control does not validate every identification assumption either.

### Why is it harder without an RCT?
{: #section-19 }

Two kinds of reference are missing:

- It is less clear whether the primary analysis performs reasonably on a question with a reliable existing answer.
- It is harder to judge confidently which outcomes are valid negative controls.

This does not mean “observational studies are impossible without RCTs.” Subject-matter knowledge can also come from biology, previous research, and temporal order; the corresponding assumptions simply need careful justification.

### Outcome controls with known nonzero effects
{: #section-20 }

Outcome controls can be broader than negative-control outcomes. A checking relationship may have either an expected null or a credible nonzero effect.

For example, in an **invented scenario**, the effect on primary outcome $$Y$$ is unknown, but independent evidence supports an approximately 0.70 risk ratio for the same treatment contrast on another outcome $$K$$ in a compatible population. An additional analysis of $$K$$ checks whether the data and methods produce compatible results.

| Observational estimate for $$K$$ | Interpretation relative to external evidence |
| --- | --- |
| RR = 0.72 with compatible uncertainty | Consistent with external evidence near 0.70, supporting the method’s performance on this question |
| RR = 1.40, difficult to explain by uncertainty or study differences | Clearly inconsistent with the reference; investigate confounding, measurement, or mismatched questions |

These numbers are not actual hormone-therapy evidence. They show that **when checking a known answer, the answer need not be “no effect.”**

The comparison is with a credible range around 0.70, not a requirement to return to 1. Nor can any “significantly nonzero” outcome be treated as a known-effect control: reference evidence must be independent and reliable, with an appropriate population, comparator, follow-up, ITT/PP contrast, and effect scale.

If the reference is an RCT and its trial is explicitly emulated, this connects to benchmarking. **A negative control is the expected-null special case; a known-nonzero-effect control checks another independently supported answer.** Agreement on one control still does not guarantee an unbiased primary analysis.

### Treatment controls: Keep the outcome and choose another control treatment
{: #section-21 }

Negative-control outcomes “keep treatment and change the outcome.” Here we “keep the primary outcome and choose another treatment contrast.” The source’s expected-null treatment control can be understood as applying a **negative-control exposure** to treatment research.

Suppose the main analysis studies treatment $$A$$’s effect on $$Y$$. Select treatment $$Z$$, specify its comparator strategy, and require no expected causal effect on $$Y$$ for that specific contrast. Ideally, causes of receiving $$Z$$ overlap relevantly with causes of receiving $$A$$.

**Why emphasize similar indications?** Treatment is often chosen according to diseases, symptoms, severity, and access to care. Treatments with similar indications may share those selection causes and thus reflect similar confounding by indication. Similar indications alone, however, guarantee neither identical confounding structures nor no effect on $$Y$$.

Returning to hormone therapy, consider this **purely hypothetical example**. $$Z$$ treats similar menopausal symptoms. Assume independent evidence supports no causal effect of initiating versus not initiating Z on breast-cancer diagnoses in the current population and follow-up period. This assumption also excludes pathways through altered subsequent hormone use or testing. No actual drug is specified.

| Analysis | Treatment contrast | Outcome | Null effect expected in advance? |
| --- | --- | --- | --- |
| Primary analysis | Defined hormone strategy one versus strategy zero | Breast cancer $$Y$$ | Unknown; this is the research question |
| Additional treatment-control analysis | Initiate Z versus do not initiate Z, with subsequent rules specified | The same breast cancer $$Y$$ | Yes, by assumption in this teaching example |

If the second row also shows a clear protective association, investigate whether people receiving such symptom treatments were healthier initially or had different healthcare-seeking behavior. If similar treatment-choice causes also affect the primary analysis, the result is informative. Shared indications are a clue to that connection, not proof of it.

#### How does this differ from an active comparator?
{: #section-22 }

| Use | Comparison task | Is no effect expected? |
| --- | --- | --- |
| Active comparator | Compare A with a reasonable alternative B on Y in the main analysis | No requirement that A and B have equal effects on Y |
| Negative-control treatment | Additionally analyze Z versus its specified control on the same Y to look for bias | A justified expectation of no causal effect for that additional contrast on Y |

**Calling Z a treatment control does not justify comparing A with Z and expecting a null effect.** If A affects Y and Z does not, their difference can be a genuine treatment effect. See [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}).

A Z–Y analysis must also specify how it handles primary treatment A. If treatments are often used together, their association may involve A’s real effect on Y. If Z changes A use and thereby Y, that may violate the requirement of no Z effect on Y. “No direct pharmacological effect” alone does not establish validity.

These controls provide an extra diagnostic, not an automatic replacement estimator of the primary effect. Interpret presence or absence of association as in §6; further correction still needs §7’s assumptions. [Lipsitch et al. (2010): Negative-control exposure framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/)

<details class="study-callout" markdown="1">
<summary>Advanced: Why do some papers allow Z to affect Y through A?</summary>

To explain an “additional expected-null relationship check,” the example above uses the simpler condition that Z has no total causal effect on Y. Some formal negative-control-exposure methods use broader definitions: Z may affect Y through primary treatment A, but that effect must disappear after fixing or appropriately handling A, with an analysis matching those conditions.

“No direct effect” and “no total effect” are therefore different assumptions. One cannot simply compare Z and Y crudely in those methods and expect no association. Check how the paper defines the control, handles A, and specifies additional identification assumptions. [Penning de Vries and Groenwold (2023), §2](https://pmc.ncbi.nlm.nih.gov/articles/PMC10515451/)

</details>


### Another source passage: Outcome controls, known-effect controls, and treatment controls
{: #section-23 }

Having distinguished these three control types, consider this passage from Hernán and Robins (2016):

> A second approach is to consider control outcomes on which treatment is not expected to have a causal effect—for example, brain cancer or pneumonia in our hormone-therapy example. Such control outcomes can help detect confounding when the confounders of the primary and control outcomes are sufficiently similar.
>
> One may also consider control outcomes with nonzero true effects whose magnitudes are approximately known. Likewise, treatment controls can use strategies with indications similar to those of the treatment under study but no expected effect on the outcome of interest.

Here **second approach** follows the “reversed target trial of starting and stopping treatment” as another way to examine study credibility. It does not require collecting a second group of randomized-trial participants.

The original paper’s main protocol concerns combined hormone therapy and breast cancer; its coronary-heart-disease discussion explains prevalent-user bias. The three checks can be summarized as:

| Analysis | What is mainly retained? | Additional check | Comparison reference |
| --- | --- | --- | --- |
| Negative-control outcome | Same treatment contrast $$A$$ | Another outcome $$N$$ | A justified expected null value |
| Known-nonzero-effect outcome control | Same treatment contrast $$A$$ | An outcome with credible existing effect evidence | Its known effect range and uncertainty |
| Negative-control treatment / exposure | Primary outcome $$Y$$ | Another treatment contrast $$Z$$ | The expected null value for $$Y$$ |

Brain cancer and pneumonia are the authors’ **candidate outcomes**. Their examples are retained here, without proving exact null effects across every hormone formulation, population, follow-up period, and strategy comparison. Apply §4’s conditions rather than choosing by outcome name alone.

Source: [Using Big Data to Emulate a Target Trial, p. 760](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf).

The next source paragraph addresses another task: extracting information from clinical text, imaging, and many existing variables to improve confounding adjustment. The present paragraph checks whether an analysis is suspicious; the next adds or better uses adjustment information. Both can be combined. See [From Clinical Records to Adjustment Variables: NLP, Imaging, and Machine Learning]({{ "/causal-inference/clinical-data-adjustment/" | relative_url }}).

## 9. Self-check
{: #section-24 }

1. Is a negative-control outcome a group of untreated patients?
2. Does negative-control RR = 0.6 mean the drug protects against that outcome?
3. Does a negative-control P-value above 0.05 prove no confounding in the primary analysis?
4. Can the negative-control estimate simply be subtracted from the primary result?
5. Does no effect of A versus placebo on an outcome guarantee no effect of A versus another drug B?
6. If an outcome is unaffected by treatment but does not reflect the main analysis’s confounding, is it necessarily useful?
7. If credible evidence puts a control outcome’s true RR near 0.70, must the result be near 1 to be reasonable?
8. Are a negative-control treatment and an active comparator the same concept?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. No. It is an additional outcome analyzed within the same treatment comparison.
2. If the null-effect assumption is credible, investigate noncausal explanations first, while checking control selection and sampling variability.
3. No. Power may be inadequate, bias mechanisms may not be shared, or biases may cancel.
4. Not automatically; additional bias-linking and identification assumptions are required.
5. No. B itself may affect that outcome.
6. Not necessarily; it may fail to detect the bias of concern.
7. No. Compare with the credible nonzero reference and its uncertainty.
8. No. The former checks an additional known-null relationship; the latter compares primary treatments’ relative effects.

</details>


## Main sources
{: #section-25 }

- [Hernán MA, Robins JM (2016): Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf).
- [Fu EL (2023): Target Trial Emulation to Improve Causal Inference from Observational Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).
- [Lipsitch M, Tchetgen Tchetgen E, Cohen T (2010): Negative controls: a tool for detecting confounding and bias in observational studies](https://pubmed.ncbi.nlm.nih.gov/20335814/).
- [Penning de Vries BBL, Groenwold RHH (2023): Negative controls: Concepts and caveats](https://pmc.ncbi.nlm.nih.gov/articles/PMC10515451/).
- [CREDENCE and trial meta-analysis: SGLT2 inhibitors and stroke](https://pmc.ncbi.nlm.nih.gov/articles/PMC8078131/).
- [A confounding bridge approach for double negative control inference on causal effects](https://www.tandfonline.com/doi/full/10.1080/24754269.2024.2390748).
- [Interpreting observational studies: why empirical calibration is needed to correct p-values](https://pmc.ncbi.nlm.nih.gov/articles/PMC4285234/).

Except for explicitly identified published data, all numbers, causal diagrams, and teaching examples are constructed.
