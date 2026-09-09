---
layout: "causal-note"
title: "Biomarkers and Well-Defined Interventions"
description: "Distinguish changing a biomarker from implementing a clearly specified treatment strategy."
group: "Foundations"
order: 6
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Paragraph-by-paragraph translation", "anchor": "section-1"}, {"title": "2. First distinguish three questions", "anchor": "section-2"}, {"title": "3. The amalgamation problem: What exactly is being mixed?", "anchor": "section-3"}, {"title": "4. Why can “targeting a particular Hb level” be randomized?", "anchor": "section-5"}, {"title": "5. Why is “set the biomarker to X” still insufficient?", "anchor": "section-8"}, {"title": "6. Unmeasured time-varying confounding: Why is baseline adjustment insufficient?", "anchor": "section-9"}, {"title": "7. Three questions to check your understanding", "anchor": "section-10"}]
previous_note: "/causal-inference/point-sustained-strategies/"
next_note: "/causal-inference/pragmatic-trials/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

Notation support: [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}). §4 explains the strategy-effect formula term by term; do not treat the symbols as new biological mechanisms.

<aside class="study-callout study-callout--abstract" markdown="1">

**The main thread**

“What level a biomarker reaches” does not fully specify “what was done.”

To make a causal question useful for action, specify: **Through which intervention and according to which rules is the biomarker adjusted toward which target?**

Then assess whether the observed data suffice to control confounding that affects treatment, the biomarker, and the outcome.

</aside>


Related notes: [Consistency and treatment versions]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-20), [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}), and [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).

<aside class="study-callout study-callout--tip" markdown="1">

**A route for the first reading**

Start with **the three questions in §2**, then read **§3–§4**: identical biomarker levels need not correspond to identical treatments, and treatment strategies—not bodily responses—are randomized. §1 retains the passage translation; §5 explains the context of “cannot” and “only option,” which should not be memorized as “no biomarkers can be studied causally.”

</aside>


## 1. Paragraph-by-paragraph translation
{: #section-1 }

The original passage is from [Fu, 2023: Target Trial Emulation to Improve Causal Inference from Observational Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/). Reference numbers below follow the original text supplied by the user.

**First paragraph: Reformulate a biomarker question as an intervention question.**

The inability to study the causal effect of biomarkers directly does not necessarily make the target trial emulation framework overly restrictive. Investigators can reformulate the question in terms of an intervention, as actual randomized trials of biomarker targets have done.〔34–37〕For example, randomized trials in patients with anemia and chronic kidney disease (CKD) have studied the effects of erythropoietin treatment strategies aimed at a particular hemoglobin level.〔34〕Such trials can also be emulated using observational data.〔15,38〕

**Second paragraph: Specify how the biomarker changes so that results can guide action.**

Framing causal questions about biomarkers as questions about interventions has another major advantage: the results become easier to interpret and more useful for decisions because the means of raising hemoglobin is now specified precisely.

**Third paragraph: Merely “setting a biomarker value” remains difficult.**

However, this approach works less well when interventions that modify the biomarker are unavailable. In that situation, the only option within the target trial emulation framework is to “set” the biomarker to a particular level—for example, comparing “adjust the biomarker to X mg/dL and maintain that level during follow-up” with “adjust the biomarker to Y mg/dL and maintain that level during follow-up.”

X and Y in the original passage are **placeholders for two target concentrations**, not the outcome $$Y$$ in later formulas; mg/dL means milligrams per deciliter. The original passage uses this unit for a generic biomarker, and it should not be indiscriminately applied to every measure. For example, clinical publications often report Hb in g/dL, and g differs from mg by a factor of 1,000.

Investigators should interpret such results causally with caution because the design retains the previously described amalgamation problem: mixing different ways of intervening. Unmeasured time-varying confounding may also be an insurmountable obstacle, since the biological processes that influence a biomarker are often incompletely understood.

<details class="study-callout" markdown="1">
<summary>Original English passage supplied by the user</summary>

The fact that the causal effect of biomarkers cannot be directly studied does not necessarily mean that the target trial emulation is restrictive—the investigator just needs to reformulate the question in terms of an intervention, just as has been performed to research biomarker targets in real randomized trials.34–37 For instance, randomized trials have examined the effects of targeting a certain hemoglobin level through erythropoietin use in patients with anemia and CKD.34 This can be emulated in an observational target trial emulation analysis.15,38 Phrasing causal questions on biomarkers in terms of interventions also has the large benefit of giving interpretable results that are useful for decision-making, since we now precisely specify how the increase in hemoglobin level is achieved. However, this approach works less well when interventions that modify a biomarker are lacking. In that case, the only option in the target trial emulation framework is to “set” biomarker values to a certain level, for example, comparing treatment strategies “change biomarker level to X mg/dl and keep at this level during follow-up” versus “change biomarker level to Y mg/dl and keep at this level during follow-up.” The investigator should be careful to interpret the results causally because the design suffers from the same amalgamation problem highlighted above. Furthermore, unmeasured time-varying confounding may be an unsurmountable problem because we often do not have a full understanding of all biological processes that influence the biomarker level.

</details>


## 2. First distinguish three questions
{: #section-2 }

Using hemoglobin (Hb) as an example:

| Wording | What does it actually ask? | What is still missing? |
| --- | --- | --- |
| Do people with higher Hb have lower mortality risk? | An association between a measure and an outcome, potentially useful for prediction | The association alone cannot determine whether to intervene to raise Hb |
| What would happen to mortality risk if Hb were raised? | A proposed causal question | Specify how it is raised, when, and for how long |
| What would happen under specified medication and monitoring rules targeting higher rather than lower Hb? | A causal contrast between two concrete treatment strategies | The protocol still needs a complete definition and identification conditions must hold |

**A biomarker is a measured biological characteristic; an intervention is an action or strategy that actively changes some process.**

The same biomarker can signal disease status, participate in disease mechanisms, and reflect treatment response. Its predictive value does not automatically imply that “changing it by any means will improve outcomes.”

## 3. The amalgamation problem: What exactly is being mixed?
{: #section-3 }

This is **the problem of mixing different intervention versions or implementation pathways**.

The same Hb level may result from different processes, such as erythropoietin use, correction of iron deficiency, or transfusion; Hb is also affected by underlying disease. For background on anemia treatment and contributing factors, see [NIDDK: Anemia in Chronic Kidney Disease](https://www.niddk.nih.gov/health-information/kidney-disease/anemia).

Even if different methods raise the same person's Hb to the same level, their other effects, accompanying measures, and risks need not be identical. Therefore:

> Pooling everyone who “reaches this Hb level” may lose information about which intervention was actually performed.

The problem does not imply that no average effect can ever be defined. Rather, **the broad description “raise Hb” can correspond to several clinical procedures with different outcomes.** Interpreting a result as the effect of an action requires specifying the procedure or rules for implementing its versions, or justifying that the versions are sufficiently equivalent for the target outcome.

This corresponds to **consistency and treatment versions** in the preceding note. Hernán and Taubman's analysis of BMI explicitly points out that different ways of changing BMI may correspond to different potential outcomes even when the same BMI is reached. [Hernán and Taubman, 2008](https://pubmed.ncbi.nlm.nih.gov/18695657/).

### It is not synonymous with confounding
{: #section-4 }

| Problem | Central question |
| --- | --- |
| Amalgamation / unclear intervention versions | “What exactly is the procedure I want to compare?” |
| Confounding | “Were people receiving different procedures or having different biomarker levels initially comparable?” |

Even after controlling confounding, the intervention must still be specified. Conversely, a clear intervention definition does not guarantee an absence of confounding in observational data.

## 4. Why can “targeting a particular Hb level” be randomized?
{: #section-5 }

Researchers can randomize **a treatment protocol intended to achieve a target**, rather than guarantee that a patient's body will exhibit an exact value.

For example, define two complete strategies:

- $$g_H$$: use erythropoietin according to prespecified monitoring, dose-adjustment, and discontinuation rules, guided by a higher Hb target.
- $$g_L$$: use explicitly specified rules guided by a lower Hb target.

Here, $$g$$ names a complete treatment rule; subscript $$H$$ stands for high and $$L$$ for low. These are **strategy labels, not time, actual biomarker values, or multipliers**. This $$L$$ also differs from the disease-status variable in a later causal diagram.

The actual CHOIR trial randomized epoetin alfa protocols guided by different Hb targets. [Singh and colleagues, 2006](https://pubmed.ncbi.nlm.nih.gov/17108343/). This supports a strategy comparison of “using this treatment to achieve different targets”; it does not automatically identify the effect of “changing Hb alone, independent of the treatment method.”

“Use EPO” plus a target remains only a protocol outline. A complete study must specify monitoring frequency, dose-adjustment rules, co-treatments, follow-up duration, and other details. These determine the strategy's meaning.

### The estimate concerns a strategy effect, not a biomarker effect independent of how it is achieved
{: #section-6 }

Writing a complete intervention as $$g$$, we can study:

$$
\mathbb{E}[Y^{g_H}]-\mathbb{E}[Y^{g_L}]
$$

This asks: for the same target population, how do average outcomes differ under these two specified strategies?

$$Y$$ is the outcome researchers ultimately care about, not necessarily Hb itself. For example, if $$Y=1$$ denotes death within five years and $$Y=0$$ no death, the expectations are the strategies' five-year mortality risks and the expression is a risk difference. **Hb may guide medication adjustment while death is the outcome being compared.**

Break down the expression again:

| Symbol | Meaning |
| --- | --- |
| $$Y^{g_H}$$ | Whether a person would die within five years if they followed the full treatment rules for the higher target; the superscript identifies an intervention scenario, not exponentiation |
| $$Y^{g_L}$$ | Whether the same person would die within five years if they followed the lower-target rules |
| $$\mathbb E[\cdot]$$ | Average over the same target population; the dot merely holds the place of a variable. The mean of a 0/1 death indicator is mortality risk |
| The minus sign between terms | Fix the direction as “risk under the higher-target rules” minus “risk under the lower-target rules” |

For example, **solely to practice reading the formula**, suppose the two strategies' five-year mortality risks are 18% and 15%. The expression is $$0.18-0.15=0.03$$, or +3 percentage points, meaning higher risk under the higher-target rules. This is not an actual CHOIR result, nor does it mean risk rises by 3 percentage points for each unit increase in Hb. If the outcome were blood pressure, $$\mathbb E$$ would mean average blood pressure and the difference would instead be measured in mmHg.

This formula compares **outcomes for the entire target population under two sets of rules**, rather than directly comparing actual groups that “happen to reach high Hb” and “happen to reach low Hb.”

The following hypothetical causal diagram illustrates why a strategy effect may differ from an isolated biomarker effect:

<pre class="mermaid">flowchart LR
    A[&quot;A: Specific treatment strategy&quot;] --&gt; M[&quot;M: Hemoglobin&quot;]
    M --&gt; Y[&quot;Y: Study outcome&quot;]
    A --&gt; Y
    U[&quot;U: Other physiological or disease processes&quot;] --&gt; M
    U --&gt; Y</pre>

Here, $$A$$ is strategy implementation, $$M$$ the Hb biomarker, $$Y$$ the study outcome, and $$U$$ other physiological or disease processes not elaborated in this simplified diagram. Arrows represent assumed causal effects, not numerical addition or subtraction. $$U$$ does not automatically denote a measured variable available for adjustment. Read the three paths as:

- $$A\to M\to Y$$: the strategy may affect the outcome through Hb.
- $$A\to Y$$: the strategy may also affect the outcome through pathways other than Hb.
- $$M\leftarrow U\to Y$$: the Hb–outcome relationship may also be confounded.

These arrows specify a possible structure to explain the concept; they do not establish that every path exists in any particular study.

### Connection to ITT and PP
{: #section-7 }

For “higher-target strategy versus lower-target strategy”:

- **ITT**: compare effects of assignment to the two strategies.
- **PP**: compare effects of assignment and adherence to each protocol.
- **Actually achieved high Hb versus actually achieved low Hb**: regrouping by posttreatment response, which cannot directly be interpreted as either effect above.

Someone can follow the dose-adjustment protocol perfectly yet fail to reach the target because of their individual response. Thus, **achieving a biomarker target is not the same as adhering to a treatment protocol; missing the target does not automatically imply nonadherence.**

Place this distinction in three hypothetical patient records. No clinical target values or doses are specified below; the purpose is only to illustrate reading a protocol:

| Patients all assigned to $$g_H$$ | What happens later? | How should it be understood? |
| --- | --- | --- |
| Patient A | Monitoring and dose adjustments follow the protocol; Hb reaches the target | Adheres to the strategy and reaches the biomarker target |
| Patient B | Monitoring and dose adjustments follow the protocol, but Hb remains below target | A different biological response; failure to reach target alone cannot establish protocol deviation |
| Patient C | A protocol-defined stopping condition occurs, and medication is stopped according to the rules | Follows a safety rule within the strategy; this is not automatically a deviation |

All three remain in the $$g_H$$ assignment group in an ITT analysis. For PP, patient A alone cannot represent $$g_H$$ either. Adherence must be judged by **whether treatment actions follow the rules**, not by the final biological response. Comparing only people who “successfully reach the target at the end” may also select the population by posttreatment disease status and survival.

This follows the distinction among “assignment, adherence, and actual results” in [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).

## 5. Why is “set the biomarker to X” still insufficient?
{: #section-8 }

“Set the biomarker to X and maintain it” specifies a desired physiological state but may leave unspecified the actual procedure used to achieve it.

It can be defined and studied as an idealized intervention, but requires explaining:

- What this ideal operation represents, or which mechanistic assumptions it relies on.
- Which processes in the observational data can represent it.
- Whether effects of different implementation methods can be ignored, or whether rules for mixing those methods have been specified.

In an explicit structural causal model, $$do(M=m)$$ can be defined as the ideal operation “replace the mechanism generating $$M$$ with the fixed value $$m$$.” This mathematical definition does not first require finding a real drug that can achieve it exactly.

$$do$$ is an intervention operator, $$M$$ the biomarker variable, and lowercase $$m$$ the specific value to set, which must have suitable units. For example, if $$M$$ denotes Hb here, $$m$$ must specify an Hb concentration. $$M=m$$ inside $$do(\cdot)$$ denotes active setting; simply observing “people with $$M=m$$” selects people whose current biomarker values agree. These are different questions.

However, **defining an ideal intervention, identifying it from data, and establishing whether it represents an actual treatment are three different questions**. Actual procedures such as EPO and transfusion may affect processes beyond Hb, so the fact that both raise Hb does not make them equivalent to this ideal operation. [Discussion of idealized interventions and real procedures](https://doi.org/10.1515/jci-2018-2001)

<aside class="study-callout study-callout--note" markdown="1">

**How should “cannot be directly studied” and “only option” in the original passage be understood?**

Read them in the author's context of target trials and interpretable interventions: a biomarker value alone is often insufficient to define treatment strategies that a target trial can compare clearly.

Do not extend them into “causal questions about all biomarkers are impossible in every framework.” Likewise, immediately after proposing idealized “setting of biomarker values,” the original passage stresses the difficulties of interpretation and identification.

</aside>


## 6. Unmeasured time-varying confounding: Why is baseline adjustment insufficient?
{: #section-9 }

A typical **time-varying confounder** is a factor such as disease status that changes during follow-up and affects both subsequent exposure or treatment decisions and the outcome. Since the strategy here continually modifies the biomarker, baseline values and disease status alone are insufficient considerations.

Consider a simplified hypothetical situation: in month three, a patient develops inflammatory activity that is inadequately recorded. Suppose it both lowers Hb and increases subsequent adverse-outcome risk:

$$
M_t\leftarrow L_t\to Y
$$

- $$M_t$$: Hb at time $$t$$.
- $$L_t$$: disease processes such as inflammation that develop or exist before that time.
- $$Y$$: the subsequent outcome.

Subscript $$t$$ denotes a follow-up time, such as month three, not a treatment label. $$M_t$$ has Hb concentration units; $$L_t$$ may include several variables such as presence or severity of inflammation, whose values and units require specific measurement definitions. If $$Y$$ continues to mean five-year death, it remains a 0/1 indicator. $$M_t\leftarrow L_t\to Y$$ says that $$L_t$$ is a common cause of Hb and the outcome; it does not mean “subtract inflammation from Hb to obtain the outcome.”

The data may therefore show an association between low Hb and worse outcomes, part of which arises from the common cause $$L_t$$. This does not establish that raising Hb through some procedure would remove that part of the risk.

**Adjusting for age and disease status at enrollment does not guarantee control of disease processes emerging later during follow-up.** Repeated Hb measurement also does not mean that every factor affecting Hb and the outcome has been measured.

NIDDK lists inflammation, infection, blood loss, and nutritional problems among factors contributing to CKD anemia. The diagram above is a simplified teaching structure for confounding. [Biological background](https://www.niddk.nih.gov/health-information/kidney-disease/anemia).

<details class="study-callout" markdown="1">
<summary>Advanced: What if these factors are also affected by previous treatment?</summary>

Treatment–confounder feedback can arise: previous treatment affects current disease status, which in turn affects the next treatment and final outcome.

Simply placing every follow-up variable into ordinary regression then does not guarantee the total causal effect. Longitudinal [g-computation]({{ "/causal-inference/g-formula/" | relative_url }}), [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}), and related methods can handle measured confounding of this type under appropriate conditions. [An original research application of the g-formula](https://pmc.ncbi.nlm.nih.gov/articles/PMC3641816/).

If key common causes were never measured, however, these methods do not automatically fill in the information. The challenge concerns the data and assumptions supporting identification, not merely model choice.

</details>


## 7. Three questions to check your understanding
{: #section-10 }

1. Why do identical Hb values in two people not establish that they received the same causal intervention?
2. If someone is assigned the higher-Hb-target strategy but never reaches the target, which group do they belong to in an ITT analysis?
3. Why may unmeasured time-varying confounding remain even when Hb is measured monthly?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. The ways of reaching the value and the underlying physiological processes may differ, as may the methods' other effects on outcomes.
2. The originally assigned higher-target strategy group. Actual Hb is a posttreatment result.
3. Hb is the biomarker itself; common causes of Hb and the outcome, such as inflammation or blood loss, may remain inadequately recorded.

</details>
