---
layout: "causal-note"
title: "Confounding and Treatment Components: Kidney Transplantation"
description: "Use kidney transplantation to distinguish confounders from components of the treatment being compared."
group: "Foundations"
order: 10
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. What does the original passage say?", "anchor": "section-1"}, {"title": "2. Who and what are randomized in the target trial?", "anchor": "section-2"}, {"title": "3. Why might recipient characteristics require adjustment?", "anchor": "section-3"}, {"title": "4. Why should kidney quality not be mechanically equalized?", "anchor": "section-4"}, {"title": "5. A numerical example: Adjustment may remove a real effect", "anchor": "section-6"}, {"title": "6. Boundaries of this passage's applicability", "anchor": "section-7"}, {"title": "7. Check your understanding after reading", "anchor": "section-11"}, {"title": "Sources", "anchor": "section-12"}]
previous_note: "/causal-inference/hormone-therapy-target-trial/"
next_note: "/causal-inference/time-related-biases/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Start with the core distinction**

When comparing living-donor with deceased-donor kidneys, distinguish:

- **How did the patients receiving the treatments differ to begin with?** These differences may cause confounding.
- **What different kidneys do the treatments themselves provide?** These differences may be part of the treatment effect.

The target trial helps clarify **which differences should be removed and which belong to the treatment being studied**.

</aside>


Prerequisites: [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}) and [Confounders, mediators, and colliders]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-34). Read alongside [Biomarkers and Well-Defined Interventions]({{ "/causal-inference/biomarkers-well-defined-interventions/" | relative_url }}) to understand why intervention definition should precede selection of adjustment variables.

<aside class="study-callout study-callout--tip" markdown="1">

**Which sections matter most on a first reading?**

Read **§2–§5** first: compare the same type of recipients while retaining the organ differences the two treatments naturally provide. Read “do not adjust for donor characteristics” together with **§6.1**: this is a conclusion for a particular total-effect question, not a universal rule for kidney-transplant studies.

</aside>


## 1. What does the original passage say?
{: #section-1 }

The passage comes from the section “Target Trial Emulation Helps to Identify Which Confounders to Adjust for” in [Fu (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).

The author asks:

> How does living-donor kidney transplantation, compared with deceased-donor kidney transplantation, affect survival of the transplanted kidney and the transplant recipient?

Here:

- **Donor**: the person providing the kidney.
- **Recipient**: the patient receiving the kidney transplant.
- **Graft survival**: concerns whether the transplanted kidney fails; a specific study must also define how recipient death is handled.
- **Recipient survival**: concerns whether the patient dies.

The reasoning is to imagine randomizing recipients to the two kidney-source strategies. Randomization makes the baseline characteristics of recipients comparable in distribution, but does not make the two donor types' characteristics identical. Possible differences in kidney quality are part of the treatment supplied by the strategies. When emulating this trial, donor characteristics therefore should not all be treated as confounders merely because they are imbalanced.

<aside class="study-callout study-callout--note" markdown="1">

**How should “randomization makes groups similar” be understood?**

Randomization creates independence between assignment and baseline characteristics; a finite sample may still have chance imbalances. It also does not guarantee equal posttreatment characteristics across groups.

</aside>


## 2. Who and what are randomized in the target trial?
{: #section-2 }

The people randomized are **patients receiving transplantation**; what is assigned is **a strategy for receiving a kidney from a particular source**.

| Target trial element | Meaning in this simplified example |
| --- | --- |
| Study population | Recipients eligible at the specified starting point for whom the two strategies can appropriately be compared |
| Strategy A | Receive a living-donor kidney according to the protocol |
| Strategy B | Receive a deceased-donor kidney according to the protocol |
| Outcome | Graft failure or recipient death within the specified follow-up period |
| Target contrast | How do outcomes differ if the same target recipient population receives each strategy? |

The key is that “living-donor kidney” and “deceased-donor kidney” represent two kidney-source strategies. The kidneys provided under each strategy have their own characteristic distributions, which need not match. We first use simplified strategies to understand the adjustment principle; an actual study must also define the starting point, organ availability, selection rules, and waiting arrangements so that both strategies have a clear meaning for target recipients.

**A randomized trial can have comparable patients while providing treatments that are inherently different.**

It does not randomly turn a donor into a “living” or “deceased” person, nor require the same kidney to come from two sources.

## 3. Why might recipient characteristics require adjustment?
{: #section-3 }

Imagine a teaching scenario in which younger recipients with less severe disease at baseline are more likely to receive strategy A. These recipients might also have better survival if they received B.

A direct survival comparison may then mix:

1. Outcome differences caused by the kidney-source strategy;
2. Prognostic differences present before recipients receive treatment.

In notation:

$$
A \leftarrow L \rightarrow Y
$$

- $$A$$: the kidney-source strategy.
- $$L$$: relevant recipient characteristics before strategy assignment.
- $$Y$$: the subsequent outcome.

This path says that $$L$$ affects both which strategy is received and the outcome, a typical confounding structure. Appropriate adjustment for $$L$$ aims to bring the comparison closer to “the same type of recipients receiving different strategies.”

But “recipient characteristics” does not mean “adjust for all of them”:

- Choose a set sufficient to control confounding without introducing new bias.
- A variable that merely predicts the outcome is not necessarily a confounder.
- Posttreatment recipient measures, such as posttransplant kidney function affected by treatment, cannot automatically be treated as baseline confounders.

Adjustment depends on **causal role and timing**, not whether a variable appears in a “patient table” or a “donor table.”

## 4. Why should kidney quality not be mechanically equalized?
{: #section-4 }

For the total-effect question in the original passage, one possible causal pathway is:

$$
\text{Assigned kidney-source strategy}
\rightarrow
\text{Characteristics of the kidney actually received}
\rightarrow
\text{Graft or recipient outcome}
$$

If a strategy improves outcomes by providing kidneys of different quality, that improvement belongs to the strategy's effect.

The following simplified diagram places both types of path together:

<pre class="mermaid">flowchart LR
    L[&quot;L: Recipient characteristics before assignment&quot;] --&gt; A[&quot;A: Kidney-source strategy&quot;]
    L --&gt; Y[&quot;Y: Subsequent outcome&quot;]
    A --&gt; K[&quot;K: Characteristics of the kidney actually received&quot;]
    K --&gt; Y
    A --&gt; Y</pre>

In the diagram:

- $$A \leftarrow L \rightarrow Y$$ is the confounding path to address.
- $$A \rightarrow K \rightarrow Y$$ is a causal path to retain in the total effect.
- $$A \rightarrow Y$$ represents other pathways not separately elaborated; it does not assert that a particular independent mechanism has been demonstrated.

This is a **teaching diagram** for understanding the passage, not a complete causal model of kidney transplantation.

### An important detail: Donor age does not arise after surgery
{: #section-5 }

The donor's age and previous health clearly existed beforehand. We cannot simply say, “The transplantation strategy changes this donor's age, so donor age is always a mediator.”

$$K$$ in the diagram denotes **the characteristics of the particular kidney a recipient ultimately receives**. Assigning a different kidney-source strategy changes which kind of kidney they might receive; it does not change any particular donor's preexisting age.

A more precise reading of the original passage is therefore:

> Under this treatment definition, characteristics of the organ received are treatment components or features of its implementation; imbalance alone does not justify controlling them as ordinary recipient baseline confounders.

Controlling intermediate steps when estimating a total effect may produce overadjustment bias; see the general principles in [Schisterman and colleagues (2009)](https://pubmed.ncbi.nlm.nih.gov/19525685/). This example additionally requires distinguishing “treatment components” from “the recipient's own pretreatment characteristics.”

## 5. A numerical example: Adjustment may remove a real effect
{: #section-6 }

All numbers below are invented for teaching, not clinical estimates for the two transplantation types.

Assume:

- Recipient baseline characteristics are fully comparable across groups, with no recipient confounding.
- For these comparable recipients, the graft-survival probability at a fixed follow-up horizon is 90% with a higher-quality kidney and 70% with a lower-quality kidney. Assume that this risk relationship does not vary by strategy or recipient subgroup.
- To isolate one mechanism, assume the strategy affects the outcome only by changing the mix of kidney quality.

| Kidney quality | Proportion supplied by strategy A | Proportion supplied by strategy B | Graft-survival probability at this quality |
| --- | ---: | ---: | ---: |
| Higher | 80% | 40% | 90% |
| Lower | 20% | 60% | 70% |

Overall survival under strategy A:

$$
0.8\times0.9+0.2\times0.7=86\%
$$

Read term by term: 0.8 is the proportion receiving higher-quality kidneys and 0.9 their survival probability; multiplying gives their contribution of 0.72 to overall survival. The 0.2 and 0.7 correspond to lower quality and multiply to 0.14. The categories are mutually exclusive and cover the group, so the sum is 0.86. All probabilities refer to the same fixed horizon above and have no time unit.

Overall survival under strategy B:

$$
0.4\times0.9+0.6\times0.7=78\%
$$

This changes only the supplied proportions of higher and lower quality to B's 0.4 and 0.6. Conditional survival probabilities remain 0.9 and 0.7 by assumption, giving 0.36+0.42=0.78.

The total effect of strategy A versus B is therefore:

$$
86\%-78\%=8\text{ percentage points}
$$

The entire difference arises because strategy A more often supplies higher-quality kidneys. Under our assumptions, this is a real strategy effect.

Express the same calculation for “1,000 recipients of the same type”: strategy A supplies 800 higher-quality and 200 lower-quality kidneys, with $$800\times90\%+200\times70\%=860$$ expected surviving grafts. Under B, the corresponding count is $$400\times90\%+600\times70\%=780$$. The difference is 80 additional surviving grafts per 1,000 recipients. **Eight percentage points is an absolute difference, not an 8% relative increase.** These expected counts only explain the example; they do not mean that both outcomes have been observed for the same person in reality.

Now suppose a researcher, seeking “fairness,” standardizes both groups to 60% higher-quality and 40% lower-quality kidneys. Both groups then have:

$$
0.6\times0.9+0.4\times0.7=82\%
$$

The new 0.6 and 0.4 are common kidney-quality weights imposed by the researcher, not the actual quality composition under either original strategy. Survival probabilities within the quality categories remain 0.9 and 0.7. The results match because the same composition and conditional probabilities have been inserted on both sides.

The standardized difference becomes 0.

The researcher has effectively made both strategies supply “600 higher-quality and 400 lower-quality kidneys,” each with 820 expected surviving grafts. This artificially unified mix differs from the two original kidney-source strategies of interest.

**The problem is that the researcher has removed the difference in kidney quality that the strategies themselves would provide.** There was no recipient confounding to remove in this example, yet the entire strategy effect was lost.

Compare this with standardization in the potential-outcomes note:

| What is equalized? | Why does it matter? |
| --- | --- |
| Composition of recipient baseline characteristics | Makes the strategies apply to the same target patient population |
| Composition of kidney quality supplied by the strategies | Removes part of the treatment difference between strategies and may therefore change the question |

<aside class="study-callout study-callout--warning" markdown="1">

**“The difference shrank after adjustment” does not automatically imply initial confounding**

It may also mean that an intermediate part of the treatment effect was controlled or that a different estimand is now being compared. Examine the causal structure first; numerical changes before and after adjustment alone are insufficient.

</aside>


## 6. Boundaries of this passage's applicability
{: #section-7 }

### 6.1 “Adjust only for recipient characteristics” is a simplified conclusion for this example
{: #section-8 }

It is not a universal database-operation rule.

For example, if preassignment center, calendar period, or resource conditions jointly affect the kidney-source strategy and outcome, those factors also warrant consideration under the corresponding causal structure, even though they are not recipient physiological attributes.

Likewise, whether a donor-related variable represents a preassignment selection mechanism, a treatment component, or a feature of the organ actually received must be assessed against an explicit target trial. TTE helps ask the right questions, but cannot replace subject-matter knowledge, causal diagrams, and identification assumptions.

### 6.2 What if the question is “Does source still matter at the same kidney quality?”
{: #section-9 }

This is a different research question. It attempts to separate the part of a source-strategy effect that does not operate through certain organ characteristics.

It may involve a **direct effect** (excluding effects transmitted through specified quality features), a **joint intervention** (specifying both source and quality), or a strategy comparison within a particular quality range. Further questions must be answered:

- Which characteristics are fixed, and at which values or distribution?
- Do kidneys of this type exist under both strategies?
- Is the intervention well defined?
- Is sufficient information available on relevant confounding?

**Adding kidney quality to a regression does not automatically yield a causally interpretable direct effect.**

### 6.3 The starting point changes which characteristics are “baseline”
{: #section-10 }

A comparison starting “at transplantation” is not the same target trial as one starting “at waitlist entry, when the kidney-source strategy is chosen.”

For example, the latter also concerns strategy implementation and outcomes during the wait. A comparison restricted to people who have completed transplantation cannot directly substitute for that earlier-start strategy effect. See [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}) and [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}).

<details class="study-callout" markdown="1">
<summary>Advanced: Using a variable in a model is not the same as forcing groups to match on it</summary>

Here, “do not adjust for kidney quality” mainly means not treating quality as an ordinary confounder and using a common quality composition to define the main between-group comparison.

More complex estimation approaches may model quality and outcomes, then average over **the quality distribution that each strategy would actually produce**, while still targeting the total effect. What matters is whether the strategy-induced quality difference is retained or removed in the final comparison, not simply whether the variable appears in a regression formula.

</details>


## 7. Check your understanding after reading
{: #section-11 }

1. Must a variable be adjusted for whenever its distribution differs between groups and it predicts the outcome?
2. Why can randomization make recipients comparable without requiring identical characteristics of the kidneys they receive?
3. Donor age exists before transplantation. Why is that fact alone insufficient to establish that it must be adjusted for as a confounder?
4. In the example above, why does a difference of 0 after quality standardization not show that the strategy has no effect?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. No. Examine its causal role between the explicitly defined intervention and outcome.
2. Recipients are randomized to strategies; the strategies are allowed to supply different treatment components.
3. Earlier existence does not make it a common cause of recipient strategy assignment and outcome; which donor's kidney is actually received and its characteristics may also be part of treatment.
4. Standardization removed the pathway through which the strategy acts by changing quality composition. The original total effect remains 8 percentage points.

</details>


## Sources
{: #section-12 }

- [Fu EL. Target Trial Emulation to Improve Causal Inference from Observational Data: What, Why, and How? (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/): the source of the user-supplied passage, introducing target-trial reasoning for kidney-source strategies.
- [Schisterman EF, Cole SR, Platt RW. Overadjustment Bias and Unnecessary Adjustment in Epidemiologic Studies (2009)](https://pubmed.ncbi.nlm.nih.gov/19525685/): distinguishes overadjustment bias from unnecessary adjustment and discusses controlling intermediate variables on causal pathways.

The numerical example, teaching diagrams, and reading tips were constructed for this note to explain these concepts; they are not actual estimates of kidney-transplant strategy effects.
