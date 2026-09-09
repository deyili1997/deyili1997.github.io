---
layout: "causal-note"
title: "Surveillance Bias and Differential Measurement Error"
description: "Distinguish disease occurrence, detection, and recording, and examine how outcome definitions change the role of monitoring."
group: "Bias and measurement"
order: 19
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. What does the source article’s eGFR example mean?", "anchor": "section-1"}, {"title": "2. A numerical example: Equal true risks recorded as different risks", "anchor": "section-2"}, {"title": "3. What does “differential” mean in differential measurement error?", "anchor": "section-3"}, {"title": "4. Why does it distort risk mathematically?", "anchor": "section-6"}, {"title": "5. Differences from confounding and lead time", "anchor": "section-7"}, {"title": "6. How can the problem be assessed and reduced?", "anchor": "section-8"}, {"title": "7. What if surveillance is itself part of the treatment strategy?", "anchor": "section-13"}, {"title": "8. Self-check", "anchor": "section-15"}, {"title": "Reading companion: How are outcomes detected?", "anchor": "section-16"}, {"title": "Main sources", "anchor": "section-22"}]
previous_note: "/causal-inference/clone-censor-weight/"
next_note: "/causal-inference/negative-control-outcomes/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Distinguish actual occurrence from recording**

**Surveillance bias**: Differences between groups in opportunities for testing, follow-up, or diagnosis create different opportunities to detect and record outcomes, distorting comparisons of true outcomes.

**Differential measurement error**: Even given the true value, the measurement-error mechanism varies by comparison group or another relevant variable.

In this example, surveillance differences can cause differential outcome detection or misclassification. The terms overlap but are not exact synonyms in every setting.

</aside>


<aside class="study-callout study-callout--tip" markdown="1">

**How to approach a first reading**

Start with the examples and definitions in §1–§3, then the distinctions, responses, and target effects in §5–§7. Save the formulas in §4 and the “Reading companion” near the end for a second reading; the latter explains systematic and blinded outcome ascertainment and why death registries may be an exception.

</aside>


Prerequisite: outcome and follow-up definitions in [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}).

## 1. What does the source article’s eGFR example mean?
{: #section-1 }

In the Outcomes section of [Fu (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/), the author notes that outcomes in observational data usually are not assessed using a uniform, blinded protocol. One treatment group may be sicker, leading to more frequent eGFR testing during follow-up and easier detection of related outcomes.

eGFR is **estimated glomerular filtration rate**, a measure of kidney function. The key issue is **outcome ascertainment—detecting, confirming, and recording outcomes**. It describes how a study learns about an outcome, not the disease process itself.

Imagine two treatment groups:

- Group A receives frequent follow-up tests, making deterioration in kidney function more likely to be recorded promptly.
- Group B is tested less often, so the same abnormality may go unmeasured or be recorded later.

The database’s “number of people with worsening kidney function” then depends on both:

1. Actual changes in kidney function.
2. Whether and when testing occurs and how outcomes are confirmed and recorded.

**Surveillance bias can exist even if the laboratory instrument is perfectly accurate each time.** For continuous eGFR, the problem may be missing measurements or irregular measurement times. When the outcome is defined as “whether kidney function deteriorated,” it may appear as missed or delayed outcome detection.

No outcome record therefore does not mean no outcome occurred. Treating “unrecorded” as “did not occur” can cause misclassification; simply excluding unmeasured patients may introduce selection bias, as discussed in §6.

## 2. A numerical example: Equal true risks recorded as different risks
{: #section-2 }

These numbers are entirely invented for teaching. To isolate surveillance, assume the groups are comparable, have identical true one-year risks, and have no false positives.

| Item | Group A: more complete surveillance | Group B: less surveillance |
| --- | ---: | ---: |
| Total participants | 1,000 | 1,000 |
| True target outcomes within one year | 100 | 100 |
| Proportion of true cases detected and recorded | 90% | 50% |
| Cases recorded in the database | 90 | 50 |
| Recorded risk using all enrolled participants | 9% | 5% |

The true risk ratio is:

$$
RR_{\mathrm{true}}=\frac{100/1000}{100/1000}=1.
$$

The recorded risk ratio is:

$$
RR_{\mathrm{recorded}}=\frac{90/1000}{50/1000}=1.8.
$$

RR means risk ratio in both formulas: group A’s risk divided by group B’s. The subscripts true and recorded label the true and recorded outcomes; they are not new variables. Each 1000 is the corresponding group’s total size. A risk ratio has no physical unit: 1 means equal risks, and 1.8 means A’s recorded risk is 1.8 times B’s—not a difference of 1.8 percentage points.

Replacing true risk with recorded risk would suggest “80% higher relative risk and 4 percentage points higher absolute risk in A.” Yet both true risks were set to 10%; the entire difference comes from detection rates.

<aside class="study-callout study-callout--note" markdown="1">

**Does the source’s sicker-group example conflict with assuming equal groups here?**

No. The source describes several problems that may coexist in real research; this example deliberately fixes equal true risks to isolate surveillance.

In real data, a group may both experience more true outcomes and have better outcome detection. More testing therefore does not prove that the whole outcome difference is bias.

</aside>


## 3. What does “differential” mean in differential measurement error?
{: #section-3 }

“Differential” does not simply mean “some measurements are wrong and others are not.” It means **the error mechanism depends on study variables such as group membership**.

Let:

- $$A$$: treatment group, coded 1 or 0. The preceding example’s group A can be coded 1 and B coded 0; the numbers are only labels.
- $$Y$$: true outcome, 1 if it occurred and 0 otherwise.
- $$Y^*$$: the database-recorded outcome, 1 for recorded cases and 0 for recorded noncases. The star marks the “recorded version,” not an exponent or intervention superscript. For now assume everyone has an analyzable recorded classification; missing data require separate treatment.

A typical differential outcome-measurement mechanism is:

$$
P(Y^*=1\mid Y=1,A=1)
\neq
P(Y^*=1\mid Y=1,A=0).
$$

Read this as:

> Among people who truly experienced the outcome, the probability of being recorded as a case differs between A=1 and A=0.

The groups have different **sensitivities** of outcome detection. Different **specificities**—probabilities of correctly recording true noncases as noncases—also constitute differential misclassification.

Here P denotes probability, $$\mid$$ means “conditional on,” the comma simultaneously restricts true outcome and treatment group, and $$\neq$$ means not equal. Each denominator population consists of that group’s **true cases**, not everyone in the group. For example, $$P(Y^*=1\mid Y=1,A=1)=0.90$$ means 90 of 100 true cases are expected to be recorded; the other group’s probability is 0.50.

To assess “differential” error, compare recording mechanisms given the true status, not merely the number misclassified. If true case counts differ, misclassification counts can differ even with identical sensitivity and specificity.

### How are measurement error and misclassification related?
{: #section-4 }

- For continuous variables, such as an eGFR value, the usual term is **measurement error**.
- For categorical variables, such as “whether kidney function deteriorated,” the usual term is **misclassification**.
- Undetected, delayed, or duplicate events also involve the outcome ascertainment and capture process.

All can vary by group. For a systematic treatment of outcome assessment, see [Cochrane Handbook, §8.6](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08).

### Which differential errors involve more than surveillance frequency?
{: #section-5 }

| Mechanism | Teaching example |
| --- | --- |
| Different surveillance opportunities | Equal numbers of true cases, but more follow-up testing in A detects more |
| Different decision thresholds | Assessors who know treatment group apply different criteria to identical test findings |
| Different measurement tools or methods | One group receives systematic assessment, the other relies on patient-initiated reporting |
| Different exposure recall | Cases and noncases recall previous medication use with different accuracy |

The last row concerns **exposure misclassification**: error in measuring past treatment varies by outcome status. This note mainly concerns **outcome misclassification**: disease-recording errors vary by treatment group. When using “differential,” specify which variable is mismeasured and which variable the error depends on.

## 4. Why does it distort risk mathematically?
{: #section-6 }

For treatment group $$a$$, use the following notation. Lowercase a is a value of group variable A, here 0 or 1; all risks concern the same follow-up period specified in this section:

- $$p_a=P(Y=1\mid A=a)$$: true outcome risk.
- $$Se_a=P(Y^*=1\mid Y=1,A=a)$$: sensitivity in this group, the probability a true case is recorded as a case.
- $$Sp_a=P(Y^*=0\mid Y=0,A=a)$$: specificity in this group, the probability a true noncase is correctly recorded as a noncase.

All are unitless probabilities between 0 and 1. Subscript a identifies “group a,” not multiplication by a. $$1-Sp_a$$ is the probability of recording a true noncase as a case; $$1-p_a$$ is the true noncase proportion.

Then:

$$
P(Y^*=1\mid A=a)
=
Se_a\,p_a+(1-Sp_a)(1-p_a).
$$

The left is recorded risk. The right combines:

1. True cases that are correctly detected.
2. True noncases incorrectly recorded as cases.

Adjacent terms such as $$Se_a p_a$$ are multiplied. The full expression says: “recorded case proportion = true case proportion × detection probability + true noncase proportion × false-positive probability.” The two components do not overlap and are therefore added.

For another example, suppose a group has 1,000 people, 100 with true disease, sensitivity 90%, and specificity 98%. We expect $$100\times90\%=90$$ detected true cases and $$900\times2\%=18$$ noncases incorrectly recorded as cases, totaling 108 recorded cases and a risk of 10.8%. **The denominator for 90% is true cases; the denominator for 98% is true noncases.** Sensitivity cannot be read as the group’s overall disease risk. This too is an invented measurement-process example.

This is the law of total probability stratified by true status. It describes measurement, not causal identification. If treatment is not randomized, the true between-group risk comparison may also be confounded.

In §2, specificity equals 1 in both groups, with no false positives, so:

$$
P(Y^*=1\mid A=a)=Se_a\,p_a.
$$

Equal $$p_a$$ but different $$Se_a$$ produce different recorded risks.

**Differential error has no universal direction of bias.** It may exaggerate, attenuate, or reverse an association, depending on true risks and each group’s sensitivity and specificity. [Effects of Disease Misclassification on Exposure–Disease Association](https://pmc.ncbi.nlm.nih.gov/articles/PMC3698812/)

<details class="study-callout" markdown="1">
<summary>Advanced: A protective effect can even be recorded as harmful</summary>

Construct another example without confounding or false positives:

- Group A: true risk 8%, detection 90%, recorded risk $$8\%\times90\%=7.2\%$$.
- Group B: true risk 10%, detection 50%, recorded risk $$10\%\times50\%=5\%$$.

The true risk ratio is $$0.8$$, but the recorded ratio is $$1.44$$. A protective direction is reversed into a harmful one.

</details>


<details class="study-callout" markdown="1">
<summary>Advanced: Nondifferential error does not guarantee bias toward the null</summary>

Nondifferential outcome misclassification means equal sensitivity and specificity across groups. It does not mean no bias or guarantee movement toward the null for every effect measure.

For example, assume no false positives and common sensitivity $$s$$, with $$s>0$$ and true control risk $$p_0>0$$ so the risk ratio is defined. s is the shared detection probability; $$p_1,p_0$$ are true outcome risks in actual groups 1 and 0 over the same period. Then:

$$
RR_{\mathrm{recorded}}=\frac{s p_1}{s p_0}=\frac{p_1}{p_0},
$$

whereas:

$$
RD_{\mathrm{recorded}}=s(p_1-p_0).
$$

RR is risk ratio and RD risk difference; recorded indicates calculations using recorded outcomes. The common s cancels from numerator and denominator in the first formula. The second subtracts recorded risks $$s p_1$$ and $$s p_0$$, factoring out s. With s=0.5 and true risks 10% and 20%, recorded risks are 5% and 10%: the risk ratio remains 0.5, but the difference changes from −10 to −5 percentage points. At s=1 this missed-case attenuation disappears; for 0<s<1 a nonzero risk difference shrinks in magnitude.

A risk ratio can remain unchanged while a risk difference shrinks. More complex error structures involving exposures, outcomes, and covariates can produce other directions of bias.

See [Misconceptions About the Direction of Bias From Nondifferential Misclassification](https://academic.oup.com/aje/article/191/8/1485/6539983). Large samples also do not automatically repair systematic measurement problems; see [Five myths about measurement error](https://doi.org/10.1093/ije/dyz251).

</details>


## 5. Differences from confounding and lead time
{: #section-7 }

| Problem | Core mechanism | Teaching intuition |
| --- | --- | --- |
| Confounding | Treatment choice and the true outcome share causes | Sicker people are more likely to receive A and were already more likely to experience the event |
| Surveillance bias | True events have different opportunities to be detected and recorded | A users receive more follow-up testing, so the database contains more events |
| Lead time bias | Earlier detection or an earlier time origin lengthens recorded postdiagnosis survival | Diagnosis moves earlier without necessarily delaying death |

These can coexist. More intensive surveillance may both detect more cases and diagnose the same case earlier, affecting survival measured from diagnosis. See [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}).

This teaching diagram separates the true and recorded outcomes:

<pre class="mermaid">flowchart LR
    A[&quot;A: Treatment strategy&quot;] --&gt; Y[&quot;Y: True outcome&quot;]
    A --&gt; M[&quot;M: Surveillance and testing&quot;]
    Y --&gt; R[&quot;Y*: Recorded outcome&quot;]
    M --&gt; R</pre>

The arrow $$A\rightarrow Y$$ represents the effect on the true outcome we want to study; $$A\rightarrow M\rightarrow Y^*$$ shows that treatment may also alter detection opportunities.

This is one possible structure. Actual surveillance differences may instead arise from shared causes such as health or healthcare resources, rather than treatment itself.

## 6. How can the problem be assessed and reduced?
{: #section-8 }

### Prespecify a common outcome-assessment protocol in the target trial
{: #section-9 }

For example, assess both groups at the same scheduled times using the same tests, outcome thresholds, and confirmation rules. Where appropriate, assessors unaware of treatment group determine outcomes.

A common assessment schedule is a study protocol, not a post hoc restriction to people who happened to complete every assessment.

Randomization makes assignment independent of patient prognosis and balances baseline factors in the repeated-randomization sense. It does not guarantee exact balance in every finite sample or identical subsequent testing, reporting, and assessment. Randomized trials can therefore also have differential outcome measurement. [Cochrane Handbook, §8.6](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08)

### In observational data, first examine the observation process
{: #section-10 }

Compare the groups’:

- Testing frequency and intervals.
- Reasons for testing: routine follow-up or visits prompted by worsening symptoms.
- Tools, thresholds, and confirmation rules.
- Data sources and follow-up coverage.

Total test counts also depend on follow-up duration, loss, and death; do not compare counts without their time context. Different counts are a warning signal, not proof of bias. Equal counts do not ensure equal diagnostic practices or test timing.

When Cox analyzes disease-onset times, differences in detection timing also enter risk-set comparisons: the model uses recorded event times and cannot automatically recover true onset times. See [Why these biases affect Cox]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-9).

### Do not treat “adjusting for test counts” as a universal repair
{: #section-11 }

Restricting retrospectively to people with “at least four tests during follow-up” may:

- Exclude people who died or were lost earlier.
- Select patients according to follow-up health or healthcare-seeking behavior.
- Introduce collider bias in some structures.

For example, if treatment and underlying health both affect test frequency, conditioning on it may open:

$$
A\rightarrow M\leftarrow U\rightarrow Y,
$$

where $$U$$ is a disease factor affecting both testing and the outcome. This is a possible causal structure, not a claim that every frequency adjustment is biased.

[Fu (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/) specifically cautions against selecting the analysis population by requiring a certain number of follow-up eGFR tests.

Research also shows that adjusting for previous visit frequency alone does not always eliminate bias from an informative observation process. [Informative presence bias: Empirical and simulation research](https://pmc.ncbi.nlm.nih.gov/articles/PMC9196698/)

### Choose analysis methods for the specific mechanism
{: #section-12 }

First seek validated data sources with more complete outcome recording. If true outcomes can be independently checked for a subset, that validation sample can estimate sensitivity and specificity by group, allowing assessment of how varying missed-case or false-positive rates change results. This is quantitative bias analysis.

Irregular or informative observation may require observation-probability weighting or appropriate modeling under explicit assumptions. “Informative” means whether and when someone is observed relates to the health condition or outcome of interest. Simply adding a test count to regression does not automatically resolve that selection; dependence on unobserved true health makes the problem harder.

For a sensitivity-and-specificity-based sensitivity analysis, see [A quantitative bias analysis approach to informative presence bias in electronic health records](https://pmc.ncbi.nlm.nih.gov/articles/PMC11027938/).

## 7. What if surveillance is itself part of the treatment strategy?
{: #section-13 }

Distinguish the target outcome.

- If the question is “does the drug cause true kidney injury?”, an increase in records caused only by more testing obstructs that question.
- If the question is “how many more diagnosed cases will a screening strategy produce?”, increased detection is itself an effect on the diagnosis outcome and cannot universally be called bias.
- If intensive surveillance prompts timely intervention and thereby changes actual health outcomes, that pathway may belong to the total effect of the full care strategy.

Specify whether the comparison concerns **true disease occurrence, diagnosed or recorded events, or outcomes of a complete care strategy that includes surveillance**. Different surveillance does not automatically justify adjusting away every related effect.

This follows the principle in [Confounding and Treatment Components: Kidney Transplantation]({{ "/causal-inference/confounding-treatment-components/" | relative_url }}): define the target effect before deciding which differences represent bias to remove.

### Hormone therapy and breast surgery: Why can the same pathway change meaning?
{: #section-14 }

If the target is whether a drug increases true breast-cancer occurrence, additional diagnoses caused only by more active testing cannot directly establish that the drug promotes cancer.

But suppose a hospital asks: **Under usual care in which patients and clinicians know the treatment, how would different hormone-therapy strategies change actual breast-surgery volume?** The following process may then belong to the strategy’s effect on surgical demand:

$$
\text{Hormone-therapy strategy}
\rightarrow\text{Changed testing and diagnostic behavior}
\rightarrow\text{Changed diagnosis or surgical decisions}
\rightarrow\text{More actual surgery}.
$$

Actual surgery or another real healthcare service must change. If the same surgeries are simply more likely to be recorded in one group, that remains measurement error in the surgery outcome.

| Target question | How should treatment-induced testing and diagnosis changes be viewed? | Corresponding target-trial consideration |
| --- | --- | --- |
| Does the drug increase disease occurrence, or cancer diagnoses under common surveillance? | Extra diagnoses caused solely by additional case-finding should not directly be interpreted as biological harm | Specify clear, comparable outcome-detection and confirmation procedures |
| Under usual care, how many more breast cancers will be diagnosed? | If the strategy causes diagnosis changes, they can belong to its total effect on diagnosis | Include usual care and the surveillance environment in the question |
| Under usual care, how many more breast surgeries will actually occur? | Surgery changes through testing, diagnosis, and clinical decisions can belong to the strategy’s total effect on healthcare use | Clinical care can remain unblinded, while surgery records must remain reliable |

The key in the second and third rows is **caused by the strategy**. If greater testing arises only because treated people had higher underlying risk, confounding may remain; not every observed difference belongs to the “total treatment effect.”

Likewise, a common surveillance protocol does not automatically identify a purely biological direct effect. Diagnosis remains a clinically defined event, and testing and subsequent care may affect health. Specify strategies and outcomes instead of treating “diagnosis time” as an observed “time when the tumor began forming.”

The authors’ phrase **no difficulty would arise** means that unblinded usual care is compatible with that target question; it does not make confounding, loss to follow-up, selection, or surgery-recording error disappear. The translated passage and terminology are discussed in the “Reading companion” below.

For the full case, see [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}). It illustrates why the population, treatment context, outcome, and target effect in [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}) must be defined together.

## 8. Self-check
{: #section-15 }

1. Does using the same accurate laboratory equipment eliminate surveillance bias?
2. Do more recorded cases in A establish that A raises true disease risk?
3. Does restricting to patients with four follow-up tests necessarily make the comparison fairer?
4. Does differential measurement error always exaggerate treatment risk?
5. Does blinded expert review of detected cancers recover cases missed among untested people?
6. If the target is actual breast-surgery volume under usual care, should every treatment-induced additional-testing pathway be removed?
7. Does death ascertainment unaffected by treatment history mean treatment cannot affect death?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. Not necessarily; testing opportunities, timing, and outcome assessment may still differ.
2. No; distinguish true occurrence from detection probabilities and consider confounding and other problems.
3. No; this may select people by future health and survival.
4. No; it can exaggerate, attenuate, or reverse an association.
5. No; downstream adjudication cannot automatically recover case information never obtained upstream.
6. No; a treatment-strategy-induced pathway that changes actual surgery can be part of the total effect. Confounding and missed surgery records still need attention.
7. No; it means the confirmation and recording process does not depend on treatment history. Treatment can still affect mortality risk.

</details>


## Reading companion: How are outcomes detected?
{: #section-16 }

The following discussion accompanies the Outcome paragraph in Hernán and Robins (2016), adding the original context for §7’s point that “the meaning of surveillance pathways changes with the target outcome.”

### Translation of the source passage: Systematic, blinded ascertainment and breast surgery
{: #section-17 }

The following translates the Outcome paragraph in Hernán and Robins (2016):

> We generally prefer to emulate a target trial in which outcomes are sought and confirmed according to a prespecified process under blinded conditions, ensuring that physicians’ knowledge of treatment does not alter their decision to look for the outcome. In our example, even without a biological effect of hormone therapy, differential outcome ascertainment could increase the incidence of diagnosed breast cancer among hormone users.
>
> However, because physicians usually know patients’ treatments, such observational data cannot emulate a trial with systematic, blinded outcome ascertainment unless ascertainment is unaffected by treatment history—for example, when the outcome is death, independently confirmed through a death registry.
>
> If instead we are interested in how different hormone-therapy strategies affect rates of breast surgery, and consequently demand for breast surgeons, this difficulty would not arise: the target trial to be emulated would itself use unblinded outcome ascertainment.

The source’s “cannot” and “no difficulty” must be read in the context of the data and question discussed, not generalized into absolute statements about all observational research. Source: [Using Big Data to Emulate a Target Trial, p. 760](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf).

### What do ascertainment, systematic, and blind mean?
{: #section-18 }

**Outcome ascertainment** includes whether testing is arranged, how findings are judged, and whether an event enters the study record. Distinguish the terms as follows.

| Term | Meaning in this passage | Misreading to avoid |
| --- | --- | --- |
| Occurrence | A disease or event actually happens | Occurrence date need not equal diagnosis date |
| Ascertainment | Seeking, judging, and recording whether an outcome occurred | Cases can be missed or misjudged; reviewing existing diagnoses may not include missed cases |
| Systematic | Prespecified, comparable testing and confirmation procedures across groups | Does not require everyone ultimately to receive exactly the same number of tests |
| Blind / blinded | Outcome-assessment decisions should be protected from knowledge of treatment; relevant assessors do not know group assignment | Does not mean every clinician, patient, and assessor in the entire trial must be blinded |

A protocol may specify common scheduled assessments and rules triggering tests for particular symptoms. Actual test counts can differ with symptoms; the key is clear rules and avoiding extra differences in case-finding or judgment caused solely by knowledge of treatment group.

Blinding aims to reduce the influence of group knowledge on testing or assessment; systematic procedures specify how to seek outcomes. Neither substitutes for the other.

### Why can breast-cancer diagnoses increase without a biological effect?
{: #section-19 }

The authors describe this possible pathway:

```text
Knowing that the patient uses hormones
        ↓
Greater attention to breast problems, more testing, or more active further assessment
        ↓
Cancers that might otherwise remain undetected are diagnosed
        ↓
More breast-cancer diagnoses are recorded during study follow-up
```

“No biological effect” is a hypothetical condition used to isolate the mechanism, not a claim that hormone therapy necessarily has no biological effect on breast cancer. Actual disease changes and detection-opportunity changes can coexist.

As §2 shows, unequal detection rates can create differences even when every recorded case is genuine. **Surveillance bias does not require false positives.**

Cases may also simply be detected earlier and thus enter the current follow-up window. Cancers that would have been diagnosed later can enter study records sooner because of additional testing.

### Why cannot retrospective blinded review automatically fix this?
{: #section-20 }

Distinguish two stages:

1. **Upstream detection**: clinicians decide whether to test, determining whether a patient has the opportunity to become a detected case.
2. **Downstream adjudication**: experts examine existing imaging, pathology, and records to decide whether the outcome definition is met.

Hiding treatment information from downstream experts can reduce group-influenced judgment. But if a patient was never tested, experts generally lack the corresponding material to review. **Blinded outcome adjudication is therefore not automatically a fully systematic, blinded ascertainment process.**

The passage chiefly concerns routine clinical records without uniform blinded detection. Data from scheduled testing, independent assessment, or reliable registries should be evaluated according to their actual processes and the protocols they can emulate. Concealing group labels only during analysis cannot supply tests never performed. [Cochrane Handbook, §8.6](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08)

### Why is an independent death registry an exception?
{: #section-21 }

Cancer detection often depends on whether a clinician looks for it. All-cause deaths, however, can be captured by registries independent of the current clinical team. With adequate coverage and reliable linkage, a death’s inclusion need not depend on clinicians knowing the medication history or actively searching for a particular disease.

**The process unaffected by treatment history is ascertainment, not death itself.** More precisely, among people who truly died, capturing that death should not vary with treatment history. Treatment’s effect on mortality risk remains the research target.

Death registries do not guarantee perfect measurement: coverage, identity linkage, reporting delays, and migration can affect completeness. All-cause death status is also distinct from determining a specific cause. The example chiefly shows that some outcomes can be recorded with less dependence on clinical testing decisions.

## Main sources
{: #section-22 }

- [Hernán MA, Robins JM. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available (2016)](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf): context for systematic blinded ascertainment, death registries, and demand for breast surgery.
- [Fu EL. Target Trial Emulation to Improve Causal Inference from Observational Data: What, Why, and How? (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/): the eGFR-surveillance example.
- [Cochrane Handbook, §8.6](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08): outcome measurement, between-group assessment differences, and blinding.
- [Effects of Disease Misclassification on Exposure–Disease Association](https://pmc.ncbi.nlm.nih.gov/articles/PMC3698812/): differential outcome misclassification.
- [Informative presence bias in analyses of electronic health records-derived data: a cautionary note](https://pmc.ncbi.nlm.nih.gov/articles/PMC9196698/): the visit process and limitations of simple frequency adjustment.
- [A quantitative bias analysis approach to informative presence bias in electronic health records](https://pmc.ncbi.nlm.nih.gov/articles/PMC11027938/): quantitative bias analysis.

The numbers and causal diagram are constructed teaching examples, not effect estimates for a particular treatment.
