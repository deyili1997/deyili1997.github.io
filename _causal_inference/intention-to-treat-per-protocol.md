---
layout: "causal-note"
title: "Intention-to-Treat and Per-Protocol Effects"
description: "Separate assignment, treatment initiation, and sustained adherence, with examples of censoring and analysis plans."
group: "Trial design"
order: 4
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Why distinguish “assignment” from “receipt”?", "anchor": "section-1"}, {"title": "2. ITT effect: The effect of assignment to a treatment", "anchor": "section-2"}, {"title": "3. Per-protocol effect: The effect of following a treatment strategy", "anchor": "section-4"}, {"title": "4. The main pitfall: An effect definition is not an analysis method", "anchor": "section-6"}, {"title": "5. Connecting to potential-outcome notation", "anchor": "section-8"}, {"title": "6. Which is better? When are they equal?", "anchor": "section-11"}, {"title": "7. ITT in observational studies: Initiation effects and assignment effects", "anchor": "section-12"}, {"title": "8. Six self-check questions", "anchor": "section-32"}]
previous_note: "/causal-inference/causal-contrasts-estimands/"
next_note: "/causal-inference/point-sustained-strategies/"
---

Study entry point: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

Formula-reading support: [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}). Section 5 unpacks potential outcomes, averages, superscripts, and subscripts as they appear; the formulas are not definitions you must memorize first.

<aside class="study-callout study-callout--abstract" markdown="1">

**Start with two questions**

**ITT effect: What would happen if people were assigned to treatment B rather than treatment A?**

**Per-protocol effect: What would happen if people were assigned to B and followed its protocol, compared with being assigned to A and following its protocol?**

We begin with randomized trials: the target population can be the same; the distinction is whether we specify assignment alone or additionally require actual treatment to follow the protocol. A protocol may specify only the initial action or actions throughout follow-up. See §7 for the corresponding terminology in observational studies.

</aside>


<aside class="study-callout study-callout--tip" markdown="1">

**A first-reading route**

Read **§1–§4 → §6 → §7.2 → §7.4** first: assignment differs from actual treatment, and PP does not mean retaining only adherers. Then continue to [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}) to distinguish initiation-only rules from sustained adherence.

**Section 7 is a question-based companion to the original text; there is no need to read it all at once.** On a second pass, examine the formulas in §5 and the DAG in §7.1; consult §7.3 for prescribing and dispensing, §7.6 for different articles' uses of ITT, and §7.8 after beginning longitudinal adjustment.

</aside>


Prerequisite: [Potential Outcomes, Exchangeability, and Identification]({{ "/causal-inference/potential-outcomes/" | relative_url }}). This note is also a concrete example of selecting a “causal contrast” in [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}).

For an introduction to the targets of ITT and PP, why they are called causal contrasts, why they matter, and how to report results, first read §1–§6 of [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}). That note uses a single five-year mortality example to connect the question, design, and results; this note expands the grouping rules, formulas, and analyses. The numerical examples in the two notes are independent and should not be combined into one data table.

For implementing these target effects with observational data, see [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}). [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) explains why estimating the effect of following a protocol requires more than deleting nonadherers without addressing selection bias.

If you arrived with the question raised by the original text—“observational studies can only estimate PP, yet often call initiation effects ITT”—go directly to **§7.2**, then return to §7.1 for the explanation. Afterward, use [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}) to compare initiation-only and sustained-adherence rules further.


A worked multivariable example: [Complete multivariable LR-IPTW example comparing drug A with drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) shows how baseline characteristics for 3,000 people enter one shared LR model to produce propensity scores, weights for both groups, balance diagnostics, and one-year risks. Z=0 denotes drug B, rather than no treatment. The example compares baseline initiation strategies and does not automatically equal randomized-assignment ITT or sustained-treatment PP.

## 1. Why distinguish “assignment” from “receipt”?
{: #section-1 }

A randomized controlled trial (RCT) can determine a person's assigned group without necessarily ensuring that treatment follows the protocol afterward: some people never start, miss doses, stop, or switch drugs.

We therefore need separate records for “assigned group” and “actual treatment”:

| Symbol | Meaning | Example |
| --- | --- | --- |
| $$Z$$ | Randomly assigned group | $$Z=1$$: assigned B; $$Z=0$$: assigned A |
| $$A_k$$ | Treatment actually received at time $$k$$ | Someone assigned B may not take B this month |
| $$g_1,g_0$$ | Treatment strategies specified by the two protocols | Which drug, dose, when to start, and when stopping is permitted |
| $$Y$$ | Outcome within the specified horizon | Death within one year is 1; survival is 0 |

Here $$A_k$$ is a mathematical symbol for actual treatment, not the name “treatment A.”

$$k$$ indexes successive treatment decisions: $$k=0$$ is baseline and $$k=1$$ the next specified time; it need not be measured in years. Here $$A_k=1$$ may encode receiving B at that time and $$A_k=0$$ receiving A; if neither treatment or other treatments are possible, the coding must be expanded. The subscripts in $$g_1$$ and $$g_0$$ are **strategy labels, not time**: they identify the full rules for B and A, respectively. Independent initiation-versus-noninitiation examples later specify their own meanings of 1 and 0.

**Random assignment makes $$Z$$ random; it does not automatically make subsequent actual treatment $$A_k$$ random.**

## 2. ITT effect: The effect of assignment to a treatment
{: #section-2 }

The **intention-to-treat effect** compares outcomes after assignment to two treatment strategies, allowing subsequent adherence to follow the processes occurring in the trial. This effect includes subsequent treatment and care changes caused by assignment.

For example, ITT asks:

> If this population were all assigned to B rather than all assigned to A, how would one-year mortality risk differ? Some people would miss doses or stop; these later behaviors are part of the actual process following assignment.

The corresponding **ITT analysis** analyzes people according to their original randomized assignment. Someone assigned B who never takes it remains in B; someone assigned A who switches to B on their own remains in A. [Cochrane Handbook §8.2.2](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08).

### A constructed numerical example
{: #section-3 }

Suppose 200 people are randomized into two groups and everyone's one-year outcome is available:

| Original randomized assignment | Number | Protocol deviations | Deaths within one year |
| --- | --- | --- | --- |
| B | 100 | 20 never start B or do not use it according to protocol | 12 |
| A | 100 | 10 violate the protocol by switching to B | 20 |

Expressed as a risk difference, the ITT estimate is:

$$
\widehat{\mathrm{ITT}}
=
\frac{12}{100}-\frac{20}{100}
=
-8\text{ percentage points}
$$

It estimates **the average risk difference for assignment to B versus A under this trial's subsequent adherence behavior**.

The hat in $$\widehat{\mathrm{ITT}}$$ means “an estimate calculated from a sample.” This note expresses ITT as a risk difference, but ITT itself does not require a difference scale. 12/100 is one-year mortality in the B-assignment group and 20/100 in the A-assignment group, so $$0.12-0.20=-0.08$$, or −8 percentage points. The negative sign follows from the comparison order “B minus A.”

It does not tell us “how much risk would fall if everyone received B as required.” This summary table alone cannot also yield the per-protocol effect.

An ITT effect can be clearly defined, but “analyzing by original group” alone does not ensure an unbiased estimate: randomization must be correctly implemented, and missing outcomes, measurement errors, and other issues still require attention. Complete one-year outcomes are deliberately assumed here so that risks can be calculated directly.

<aside class="study-callout study-callout--note" markdown="1">

**The effect of “being randomly assigned,” not of “randomization itself”**

Both groups undergo randomization. The contrast is assignment to B versus A, not randomization versus no randomization.

</aside>


## 3. Per-protocol effect: The effect of following a treatment strategy
{: #section-4 }

The **per-protocol effect** asks:

> In the same target population, how would one-year mortality risk differ if everyone were assigned to B and followed B's protocol, compared with everyone being assigned to A and following A's protocol?

“Everyone” includes people who later fail to adhere in reality. We ask **what would happen if they also followed the protocol**, rather than shrinking the target population to actual adherers.

### “Per protocol” does not necessarily mean never stopping treatment
{: #section-5 }

Suppose B's protocol says:

> Use B daily at the prescribed dose; stop if protocol-defined severe toxicity develops.

Stopping as specified because of severe toxicity is still adherence. Per-protocol effects concern the full treatment rules, including permitted adjustments or discontinuation, rather than merely whether a person kept taking medication. [Cochrane Handbook §8.4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08).

## 4. The main pitfall: An effect definition is not an analysis method
{: #section-6 }

In [Identification and Estimation]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-12), we distinguished “the quantity we want to know” from “how to calculate it.” The same applies here:

- **Per-protocol effect** is the causal quantity of interest.
- **Per-protocol analysis** is an analysis label; the label itself does not guarantee a correct estimate.

### Why not simply delete nonadherers?
{: #section-7 }

Continuing the example, retaining only the 80 adherers in B and comparing them with adherers in A is a common **naïve per-protocol analysis**.

The problem is that health can affect adherence. For example:

1. People whose disease worsens are more likely to deviate from the protocol.
2. Worsening disease also increases mortality risk.
3. After selection on adherence, the people remaining in the groups may no longer be comparable.

The resulting difference may mix treatment effects with differences created by selection. **Original randomization does not guarantee that the two selected subgroups remain exchangeable.**

Make this concrete with numbers. The teaching records below agree with §2's total counts and deaths. “No deviation” means no protocol deviation before death or the end of one-year follow-up; **death itself is not nonadherence**:

| Original assignment | No deviation: people/deaths | Deviation: people/deaths | Total deaths |
| --- | --- | --- | ---: |
| B | 80/5 | 20/7 | 12 |
| A | 90/18 | 10/2 | 20 |

Retaining only those without deviations gives $$5/80-18/90=6.25\%-20\%=-13.75$$ percentage points. This differs from §2's ITT estimate of −8 percentage points, but **does not establish that “the PP effect is −13.75.”**

Why? The 20 deleted B patients and 10 deleted A patients remain part of the original target population, and the table does not tell us what would happen if they adhered. Higher observed mortality among B's deviators could reflect worsening disease prompting discontinuation, rather than discontinuation alone causing death. Naïve selection discards their contribution to the target and fails to address the reasons for deviation.

Another approach, **as-treated analysis**, reclassifies people by the drug actually used. This also does not automatically solve the problem, because actual treatment choice may be confounded.

Valid PP estimation generally requires data on adherence and prognostic factors, along with appropriate adjustment methods such as [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) or other g-methods. It also relies on the relevant no-unmeasured-confounding, positivity, consistency, and other conditions. [Hernán and Hernández-Díaz, 2012](https://pubmed.ncbi.nlm.nih.gov/21948059/).

<aside class="study-callout study-callout--important" markdown="1">

**When you see “per-protocol analysis,” ask one more question**

Does it merely delete nonadherers, or does it define a target causal effect and address confounding and selection involving adherence and outcomes?

</aside>


## 5. Connecting to potential-outcome notation
{: #section-8 }

Understand the preceding intuition before reading this section.

### 5.1 ITT: Specify assignment only
{: #section-9 }

Define $$Y^{Z=z}$$ as the potential outcome “if assigned to group $$z$$, with subsequent behavior unfolding according to this trial's actual processes.”

Read the symbols one at a time: $$Z$$ is the assignment variable, and lowercase $$z$$ is the specified group, either 1 (B) or 0 (A). In this note's main example, $$Y$$ indicates death within one year: 1 for death and 0 for no death. The superscript $$Z=z$$ is not exponentiation; it labels “under this assignment intervention.” The absence of a time subscript on $$Y$$ does not mean no follow-up horizon—the text has already specified one year.

Expressed as a difference in means:

$$
\mathrm{ITT}
=
\mathbb{E}[Y^{Z=1}]
-
\mathbb{E}[Y^{Z=0}]
$$

$$\mathbb E$$ means “expectation” or “population average”; the brackets contain the variable being averaged. For a 0/1 outcome such as death, its mean is the risk. The first term is therefore one-year mortality risk **if the entire same target population were assigned B**, and the second is its risk if assigned A. Their difference is reported as a proportion or in percentage points; we have not observed each patient twice.

Under simple random assignment, consistency, complete outcomes, and the other relevant conditions:

$$
\mathrm{ITT}
=
\mathbb{E}[Y\mid Z=1]
-
\mathbb{E}[Y\mid Z=0]
$$

Connecting to the preceding note's adjustment logic, randomization helps us directly identify **the effect of assignment $$Z$$**.

The vertical bar $$\mid$$ in the second equation means “among”: $$\mathbb E[Y\mid Z=1]$$ is the observed mean outcome **among people actually assigned B**. This differs in meaning from the counterfactual population in the first equation; equality holds only under the identification conditions above. The calculation $$12/100-20/100=-8$$ percentage points in §2 estimates these observed means with sample proportions. We cannot omit the conditions and call any difference between two group proportions ITT.

### 5.2 PP: Specify assignment and adherence to the corresponding strategy
{: #section-10 }

Let $$Y^{Z=z,g_z}$$ denote the potential outcome “if assigned to group $$z$$ and subsequently following that group's treatment strategy $$g_z$$”:

$$g_z$$ means “the full rules corresponding to group $$z$$”: $$g_1$$ when $$z=1$$ and $$g_0$$ when $$z=0$$. The comma in the superscript **lists assignment and adherence requirements together**; it is neither addition nor multiplication. The entire superscript is still a counterfactual scenario label. The outcome $$Y$$ and one-year horizon remain the same as for ITT.

$$
\mathrm{PP}
=
\mathbb{E}[Y^{Z=1,g_1}]
-
\mathbb{E}[Y^{Z=0,g_0}]
$$

This notation makes both “assigned group” and “subsequent treatment” explicit.

Here $$\mathbb E[Y^{Z=1,g_1}]$$ is one-year risk if the entire target population were assigned B and followed B's rules; the other term is the risk if that same population were assigned A and followed A's rules. This equation also expresses $$\mathrm{PP}$$ on the risk-difference scale. For example, **separately suppose** these risks have been appropriately estimated as 10% and 18%; the risk difference is then $$10\%-18\%=-8$$ percentage points. These are separate illustrative values for reading the formula; they cannot be calculated directly from the count tables in §2 or §4.

Randomization controls only the former requirement. For people who do not follow the protocol, we must still infer their potential outcomes **if they had followed it**, so we cannot simply replace the expression with “the mean difference between actual adherers.”

<details class="study-callout" markdown="1">
<summary>Advanced: Why retain \(Z\) in the PP formula?</summary>

In an open-label trial, knowing one's assigned group may change other behavior or care. Thus, the effect of “assignment to a strategy and following it” need not equal the effect of “actual treatment itself” without specifying the assignment context.

These concepts can be combined only under further assumptions, such as assignment affecting outcomes solely through the specified treatment. Retaining $$Z$$ while learning avoids equating PP directly with a “pure pharmacological effect.” [Dahabreh et al.: The role of assignment in defining causal effects](https://arxiv.org/abs/2408.14710).

</details>


## 6. Which is better? When are they equal?
{: #section-11 }

They answer different questions, so the choice depends on the research objective:

| Question | Closer target |
| --- | --- |
| What would assignment to B rather than A do in this trial's adherence and care setting? | ITT effect |
| How would B and A differ in the same population if both strategies were followed according to protocol? | Per-protocol effect |

If everyone would follow the corresponding protocol under either assignment, the target intervention processes coincide and so do ITT and PP. With nonadherence, the effects may differ, but need not.

**ITT is not necessarily closer to zero than PP.** Nonadherence can reduce treatment differences, but direction also depends on each group's treatment, adherence patterns, and other details. A smaller estimated ITT does not establish that a drug is ineffective when used according to protocol. [Hernán and Hernández-Díaz, 2012](https://pubmed.ncbi.nlm.nih.gov/21948059/).

ITT is the assignment effect in a particular trial setting. Calling it “real-world effectiveness” requires considering whether trial adherence and care resemble those in actual application. Even with analysis by original assignment, missing outcomes from loss to follow-up still need attention. [Murray et al.: A guide to estimating causal effects in pragmatic randomized trials](https://arxiv.org/abs/1911.06030).

## 7. ITT in observational studies: Initiation effects and assignment effects
{: #section-12 }

<aside class="study-callout study-callout--abstract" markdown="1">

**Three questions to distinguish in observational studies**

**RCT ITT: Compare assignment $$Z$$.**

**What observational studies often call ITT: Compare actual initial initiation $$A_0$$, retaining initial groups afterward.**

**Sustained-treatment PP: Compare outcomes under adherence to treatment rules throughout follow-up.**

Similar “no subsequent regrouping” analyses do not mean that the first two intervene on the same variable.

</aside>


### 7.1 Translation of the original passage and context
{: #section-13 }

The original passage supplied by the user comes from [Fu (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/):

Two causal contrasts often estimated in randomized trials are the effect of random assignment to a treatment strategy (the intention-to-treat effect) and the effect of receiving that strategy according to the protocol (the per-protocol effect). Because observational studies lack randomization, the author states that only per-protocol effects can be estimated in them. However, investigators often call the effect of treatment initiation the intention-to-treat effect in observational studies; this quantity differs from the effect bearing the same name in randomized trials.

The wording “only PP can be estimated” needs the author's setting: observational data that typically contain actual treatment records but lack original random-assignment information. It does not say that all observational data are incapable of studying prescriptions, recommendations, or assignment policies; see §7.6.

### How should we read Z, A, L, and Y in the figure?
{: #section-14 }

![Itt randomized vs observational point intervention dag]({{ "/assets/causal-inference/itt-randomized-vs-observational-point-intervention-dag.png" | relative_url }})

#### Translation of the original text and figure caption
{: #section-15 }

In randomized clinical trials, the intention-to-treat (ITT) effect is defined as the effect of **being assigned to a treatment**. Supplementary Figure 4 represents it as the total effect of $$Z$$ on $$Y$$. The author emphasizes that correctly implemented randomization protects the assignment effect from baseline confounding. The effect of treatment assignment need not equal the effect of actually initiating treatment; in this simplified figure, the latter is represented by the effect of $$A$$ on $$Y$$. The text then uses “everyone initiates their assigned treatment” to explain when the effects can correspond.

<aside class="study-callout study-callout--note" markdown="1">

**Two qualifications to the original wording**

Randomization protects comparability of assignment; it does not make an ITT analysis immune to other biases. Also, under conditions such as the absence of a direct assignment effect in the figure, complete initiation adherence is a **sufficient condition** for agreement of the two effects, not a necessary one. For example, both effects could be zero even if some people never initiate.

</aside>


Observational studies lack randomization, so in the usual data setting the author discusses, they cannot estimate that effect of randomized treatment assignment. When investigators use “intention-to-treat” in observational studies, they generally mean the effect of **initial treatment initiation**; in this article's terminology, it is the per-protocol effect of a point intervention.

The caption's variables are:

- $$Z$$: treatment assignment—which treatment group is assigned;
- $$A$$: which treatment is actually initiated at baseline;
- $$L$$: baseline confounders affecting both actual treatment and outcome;
- $$Y$$: the outcome.

In this section's initiation example, $$A=1$$ means initiating the treatment of interest at baseline, and $$A=0$$ means not initiating at baseline. They do not mean “follow-up 1” and “follow-up 0.” $$Z=1$$ and $$Z=0$$ denote assignment to initiation or noninitiation. $$L$$ contains pretreatment-decision characteristics and may include multiple variables. All arrows below indicate assumed causal effects; commas or wider spacing merely separate several relationships.

The left panel depicts a randomized trial, the right an observational study. Randomization-based identification of ITT in the left panel depends on actual randomized assignment $$Z$$; actual initiation $$A$$ in the right panel requires control of confounders $$L$$. The figure temporarily omits later treatment details and pathways by which assignment might affect outcomes without going through initiation; interpretation should remain within this setting.

#### Left panel: $$Z$$ is randomized; $$A$$ need not be
{: #section-16 }

The left panel has the structure:

$$
Z\rightarrow A\rightarrow Y,
\qquad
L\rightarrow A,
\qquad
L\rightarrow Y.
$$

The figure assumes simple random assignment: $$Z$$ is not determined by $$L$$, so the assignment mechanism gives:

$$
Z\perp L.
$$

Here $$\perp$$ abbreviates statistical independence, not geometric perpendicularity. It says that simple random assignment does not select groups based on $$L$$.

It does not require every characteristic to match exactly between groups in one finite sample. If assignment probabilities vary across baseline strata, conditional comparisons or weighting should follow the actual assignment mechanism; the expression cannot be applied unconditionally.

When comparing outcomes by randomized $$Z$$, the path

$$
Z\rightarrow A\leftarrow L\rightarrow Y
$$

has a collider at $$A$$ and is closed when we do not condition on $$A$$. Thus, although $$L$$ affects actual initiation and outcome, it does not confound the relationship between randomized assignment $$Z$$ and $$Y$$. This is the randomization protection of ITT analysis.

But $$A$$ itself receives an arrow from $$L$$. Actual initiation of assigned treatment may depend on disease, contraindications, health behavior, or physician decisions. If we abandon $$Z$$ and directly compare actual initiators with noninitiators, $$A\leftarrow L\rightarrow Y$$ is an open backdoor path. Confounding can therefore arise even when the data come from an RCT.

#### Why is the effect of $$Z\to Y$$ different from that of $$A\to Y$$?
{: #section-17 }

$$Z$$ means “give an assignment,” while $$A$$ means “actually initiate.” With nonadherence such as noninitiation or initiation of the other group's treatment, $$Z$$ and $$A$$ need not correspond one-to-one according to the protocol; changing assignment does not guarantee a corresponding change in actual initiation. Stopping or switching after initiation changes subsequent treatment history; it should not be equated with failing to initiate baseline $$A$$ as assigned.

A constructed example:

- 100 people are assigned to initiate; 80 actually do so.
- 100 are assigned not to initiate; 10 nevertheless do so.
- To make this simple mixture calculation valid, additionally assume that, regardless of adherence type, everyone has 10% risk if an intervention makes them initiate and 20% risk if it makes them not initiate, and assignment has no effect on outcome except through initiation.

Risk under assignment to initiate is then:

$$
0.8\times10\%+0.2\times20\%=12\%,
$$

and risk under assignment not to initiate is:

$$
0.1\times10\%+0.9\times20\%=19\%.
$$

Both calculations sum “the proportion following a path × the risk under that path.” The first equation's 0.8 and 0.2 are proportions actually initiating and not initiating after assignment to initiate; the second equation's 0.1 and 0.9 are the corresponding proportions after assignment not to initiate. The 10% and 20% are the initiation and noninitiation risks supplied by the additional assumptions above. Each equation's weights sum to 1, yielding an overall risk rather than a risk ratio.

Thus, in this constructed setting, the assignment risk difference is $$12\%-19\%=-7$$ percentage points, while the initiation risk difference is $$10\%-20\%=-10$$ percentage points. These are risks under a stipulated mechanism; the records “80 initiate” and “10 cross over” alone do not imply these causal risks.

In reality, actual initiators and noninitiators may already differ in prognosis. Their observed risks cannot simply be inserted into this mixture formula as causal initiation risks.

If everyone would initiate the corresponding treatment under each assignment, so $$Z$$ and $$A$$ correspond perfectly, and assignment cannot affect outcomes except through initiation while the subsequent care setting is the same, the two intervention processes correspond and their effects coincide. If assignment itself changes additional care, expectations, or behavior, assignment and initiation effects still need to be distinguished. [On the distinction between assignment and treatment effects](https://arxiv.org/abs/2408.14710)

#### Right panel: No $$Z$$; actual initiation $$A$$ is confounded
{: #section-18 }

The right panel contains no randomized-assignment node and has the structure:

$$
A\rightarrow Y,
\qquad
A\leftarrow L\rightarrow Y.
$$

Investigators seek the causal effect of initiation $$A$$ on outcome $$Y$$, but the backdoor path $$A\leftarrow L\rightarrow Y$$ is open. For example, patients with more severe disease may be more likely to start treatment, while severity itself increases mortality. Unadjusted differences between initiators and noninitiators can mix treatment effects with differences caused by $$L$$.

Only if baseline conditional exchangeability, positivity, consistency, outcome measurement conditions, and other requirements hold, and $$L$$ is appropriately controlled, can observational data identify the initiation effect of a point intervention:

$$
\mathbb E[Y^{A=1}]-\mathbb E[Y^{A=0}].
$$

Here $$Y$$ is the outcome within a specified horizon; for mortality, 1 indicates death and 0 no death. Superscripts $$A=1$$ and $$A=0$$ specify “initiate now” and “do not initiate now”; they neither select two observed groups nor denote exponentiation. $$\mathbb E$$ averages over the same target population. For binary mortality, the terms are risks under the two initiation interventions, and subtraction specifies “initiation minus noninitiation.” Subsequent treatment is allowed to occur naturally under each intervention.

#### Why does the author call it point-intervention PP?
{: #section-19 }

Suppose the target protocol specifies just one action at time zero:

- Strategy 1: initiate treatment now;
- Strategy 0: do not initiate treatment now;
- Subsequent stopping, switching, or initiation follows usual care naturally.

Adhering to this protocol requires only performing the specified baseline action. The effect if “everyone initiates or does not initiate at baseline according to their respective protocol” is therefore the per-protocol effect of a point intervention. PP does not require continued medication here, because continued behavior was never specified in this point-intervention protocol.

If the protocol changes to “initiate now and continue for one year,” it becomes a sustained strategy. Subsequent discontinuation may be a deviation, requiring later treatment tracking and handling of related confounding and selection. Artificial censoring and weighting is one implementation method, not part of PP's necessary definition. In that setting, the figure's baseline initiation $$A$$ cannot stand in for the full treatment history.

#### Similar names do not imply the same estimand
{: #section-20 }

| Term in the literature | Variable actually intervened on | Question answered |
| --- | --- | --- |
| RCT ITT | $$Z$$ | How does assignment to the treatment rather than control strategy affect outcomes? |
| Observational “ITT-like/as-started” | Actual baseline initiation $$A$$ | How does initiating now rather than not initiating now, with subsequent natural development, affect outcomes? |
| Sustained PP | Full treatment history $$\bar A$$ or strategy $$g$$ | How would outcomes change if everyone continued to follow their respective longitudinal rules? |

The bar in $$\bar A$$ denotes a sequence of treatment records—for example, treatment at baseline, first follow-up, and second follow-up—**not average treatment**. $$g$$ is the rule determining those actions, which need not be one fixed medication trajectory shared by everyone.

Retaining initial groups after discontinuation in an observational initiation analysis only makes its format similar to ITT. It still groups people by actual $$A$$ and does not create randomized assignment $$Z$$. Conversely, calling a result PP does not ensure control of $$L$$ or satisfaction of other identification assumptions.

### 7.2 Putting the three questions together
{: #section-21 }

All examples below compare drug B with not initiating B, with the same target population and outcome horizon.

| Question | Basis for intervention or grouping | Definition of later treatment |
| --- | --- | --- |
| RCT ITT | Random assignment to the “start B” strategy or the control strategy | Initiation, discontinuation, switching, and other behavior follow the trial's processes |
| Effect of treatment initiation | Actually initiate B at time zero or do not initiate B then | Subsequent behavior follows the usual processes in the care setting studied |
| Sustained-strategy PP | Follow “start B at baseline and continue as specified” or the corresponding control strategy | Follow specified rules throughout follow-up, including permitted adjustments or discontinuation |

“Do not initiate now” permits later initiation in usual care; “do not initiate throughout follow-up” does not. The protocol must specify this distinction; a shared “untreated group” label must not obscure it.

### 7.3 A grouping example that does not calculate an effect
{: #section-22 }

In §7.1, 100 people are assigned to initiate but only 80 start. ITT retains all 100; grouping by “actual initiation” removes the other 20 from the initiation group. If another study includes only new users of two drugs, people initiating neither may be excluded altogether, so the study's population must also be checked against the original target population.

This shows that **“people assigned to start” and “people who actually start” define different groups**. Those three numbers alone cannot yield a causal effect, and outcomes among the 80 initiators cannot substitute for the ITT result among the original 100.

Database records of prescription, dispensing, and actual first ingestion also represent different events. The record used to define “initiation” must be specified.

#### Prescribing, dispensing, and actual use: Why do the groups differ?
{: #section-23 }

**Initiators are people who begin the relevant treatment or strategy at baseline.** The term does not mean “people who persist forever afterward.” For a complete definition and the special usage with a nonuse strategy, see [Initiators: Who Exactly Are They?]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-4).

Medication treatment often includes the following stages, which need not occur on the same day:

| Stage | What does the record indicate? | What cannot be directly inferred? |
| --- | --- | --- |
| Prescription | A physician has decided to prescribe the drug | The patient necessarily obtained or took it |
| Dispensing | A pharmacy issued the medication, often used as a pickup record | The patient necessarily took it as directed |
| Treatment initiation | The patient began receiving the treatment of interest | The patient will continue following the strategy |

Without actual-ingestion data, a study may define observable “initiation” as first dispensing. It then needs to describe the operational definition, measurement limitations, and alignment with the target intervention.

Suppose that at a common baseline, 100 patients receive a prescription; 80 obtain a dispensing and 20 do not:

- Grouping by prescription places all 100 in the prescribed group.
- Grouping by dispensing places only 80 in the dispensing-defined initiation group. The analysis group or eligibility of the other 20 depends on the protocol and cannot be assumed.

This explains the original phrase **somewhat more analogous** for a prescription comparison: it retains people for whom “the physician has made a treatment decision, but the patient has not obtained the medication,” resembling “assigned but never initiated” in an RCT. A dispensing comparison already selects on whether the patient obtains the drug.

Physician prescribing nevertheless depends on disease, contraindications, and other factors: **a prescription is not randomized assignment**. Prescription effects and dispensing/actual-initiation effects are not automatically the same target. If dispensing occurs after prescribing, future pickup cannot be used to backdate treated status to the prescription day; time zero and any initiation grace period need separate design.

Original source: [Hernán and Robins (2016), Analysis plan](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf).

### 7.4 Why do observational studies still often call initiation effects ITT?
{: #section-24 }

A common approach imitates ITT in form:

1. Group people by the treatment actually initiated at baseline.
2. Retain initial groups even after treatment stops or switches.
3. Compare outcomes after addressing the appropriate baseline confounding.

This is often called an **observational analogue of ITT**, or more explicitly a **treatment initiation effect, as-initiated effect, or as-started effect**.

For example, Zhang starts B at baseline and stops two months later:

- In an analysis of “initiate B, then follow usual care,” Zhang remains in the original B-initiation group.
- In an analysis of “initiate B and continue as specified for one year,” if the discontinuation is not permitted by the protocol, the deviation requires handling, for example artificial censoring with correction for the corresponding selection bias.

**These are different treatment strategies, rather than lenient and strict scoring of the same question.**

For treatment initiation as an as-started effect, see the [NICE real-world evidence framework](https://www.nice.org.uk/corporate/ecd9/chapter/methods-for-real-world-studies-of-comparative-effects). Interpret “retain baseline groups” in [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}) and [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}) through this distinction.

### 7.5 The key: PP does not necessarily require sustained long-term treatment
{: #section-25 }

The original article's [supplement, pages 9–10](https://cdn-links.lww.com/permalink/jsn/e/jsn_34_8_2023_07_28_fu_jasn-2023-000583_sdc1.pdf#page=9) explicitly distinguishes two types of PP:

| Protocol | What does adherence require? | How should discontinuation after initiation be interpreted? |
| --- | --- | --- |
| Point intervention: intervene only on initial initiation | Perform the specified initiation action at baseline | If the protocol imposes no later treatment restrictions, later discontinuation does not violate this initiation protocol |
| Sustained strategy: ongoing treatment rules | Initiate and follow the rules during follow-up | Whether stopping is a deviation depends on whether the protocol permits it |

Thus, in the author's terminology:

> **The effect of initiating treatment is the PP effect of a point-intervention protocol that specifies only the act of initiation.**

“Intervene only at baseline” does not mean that the drug has no later effects or that follow-up lasts one day. It means only the initial action is specified, while subsequent treatment behavior develops naturally.

The same initiation action may produce different results in two settings with different later discontinuation, switching, and care patterns. It should not be interpreted as an invariant pure pharmacological effect.

This also explains why “observational studies can only estimate PP” does not mean “they can only study people who keep taking medication as prescribed”: PP requirements depend on the protocol, and its target population is not limited to actual adherers.

### 7.6 How should we interpret the limitation “only PP can be estimated”?
{: #section-26 }

In the original passage's usual setting, the central obstacle is:

> Without observing the original assignment $$Z$$ in the target randomized trial, actual treatment records $$A_0,A_1,\ldots$$ alone cannot recover that trial's assignment effect.

This cannot be generalized to “nonrandomized data cannot study any assignment or recommendation strategy.”

If data explicitly record a physician's initial prescription, treatment recommendation, or policy assignment, together with later outcomes, that well-defined decision can be treated as the exposure. Its effect may be studied under sufficient confounding control, positivity, consistency, and other conditions. This still provides no randomization guarantee and does not automatically equal another RCT's ITT.

For example, [Matthews et al. (BMJ, 2022)](https://www.bmj.com/content/378/bmj-2022-071108) discuss studying observational analogs of ITT when assignment information such as prescriptions is available. Different publications therefore use “observational ITT” somewhat differently.

When encountering this name, check:

- Is the initial exposure randomized assignment, a prescription, dispensing, or actual ingestion?
- Are people who were assigned or prescribed treatment but never actually initiated included?
- What rules govern later stopping and switching?
- Do the target population and confounding control support the causal interpretation?

**Absence of randomization does not automatically produce PP, and naming an analysis PP does not identify the corresponding effect.**

For grace periods, see [A Real Randomized Trial with a Grace Period Can Still Estimate ITT]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-15). An actual trial can randomize “initiate within three months” versus “do not initiate” and estimate ITT. Artificially copied labels in observational CCW do not carry the same assignment information, so compatibility censoring and weighting generally target PP.

### 7.7 Connecting to formulas and identification assumptions
{: #section-27 }

<details class="study-callout" markdown="1">
<summary>Advanced: Keep the three intervention variables separate</summary>

In this box, $$Y$$ is the outcome within one common specified horizon, for example 1 for death within one year and 0 otherwise. $$\mathbb E$$ averages over the same target population, so the expectation of a binary outcome is risk. $$\Delta$$, read “delta,” names a difference; its subscripts assignment, initiation, and sustained are **effect-type labels, not times or multipliers**. Superscripts specify intervention scenarios, not powers or observed groups.

The RCT assignment effect is:

$$
\Delta_{\mathrm{assignment}}
=\mathbb E[Y^{Z=1}]-\mathbb E[Y^{Z=0}].
$$

$$Z=1$$ means assignment to initiate, and $$Z=0$$ assignment not to initiate; both allow actual behavior after assignment to unfold naturally.

The initial initiation effect can be written as:

$$
\Delta_{\mathrm{initiation}}
=\mathbb E[Y^{A_0=1}]-\mathbb E[Y^{A_0=0}].
$$

The subscript 0 in $$A_0$$ is baseline; 1/0 after the equals sign are action values for initiation/noninitiation. The 1 and 2 in $$A_1,A_2$$ instead index subsequent times.

The second equation intervenes only on $$A_0$$. Under each initiation intervention, $$A_1,A_2,\ldots$$ follow subsequent processes in the setting studied; the same person's factual later medication is not mechanically held fixed.

For a sustained strategy, write:

$$
\Delta_{\mathrm{sustained}}
=\mathbb E[Y^{g_1}]-\mathbb E[Y^{g_0}],
$$

where $$g_1,g_0$$ are full longitudinal treatment rules.

Here $$g_1$$ might specify “initiate now and continue management according to rules with discontinuation exceptions,” and $$g_0$$ “never initiate throughout follow-up.” Subscripts 1/0 distinguish strategies, not year 1 and year 0. In any equation, if the left risk is 12% and the right risk 20%, the difference is −8 percentage points. Identical arithmetic does not mean that the three equations study the same intervention.

This strategy-effect notation does not explicitly specify an RCT assignment context. To connect it to $$Y^{Z=z,g_z}$$ in §5.2, clarify whether assignment itself affects the outcome through extra care or other pathways; the two cannot automatically be equated. [The role of assignment in defining causal effects](https://arxiv.org/abs/2408.14710)

</details>


For a simple initial initiation effect, under baseline conditional exchangeability, positivity, consistency, complete outcomes, and other conditions, the main treatment-confounding adjustment occurs at baseline. Do not directly adjust for all subsequent disease states affected by initiation merely to “control more thoroughly.”

Sustained-strategy effects often also require handling treatment selection and time-varying confounding during follow-up; longitudinal IPW, the g-formula, and other methods may be used under the relevant conditions. If early treatment records are compatible with multiple strategies, [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) explains how to construct and weight the corresponding records.

Both still face possible loss to follow-up and outcome measurement problems; see [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}). “Do not censor for discontinuation after initiation” does not mean “ignore all subsequent data problems.”

<details class="study-callout" markdown="1">
<summary>When might RCT ITT and initiation effects be similar or equal?</summary>

In the same target population and care setting, if everyone initiates their assigned treatment at baseline and assignment cannot affect the outcome through pathways other than initiation, the contrasts can correspond. This is a sufficient condition; nonadherence does not force their numerical values to differ.

Equating results from an RCT with those from another observational dataset additionally requires comparability in target populations, later treatment processes, care settings, and other aspects.

This differs from §6's question of “when ITT and sustained-strategy PP coincide,” which additionally concerns following the sustained protocol throughout the relevant follow-up.

</details>


### 7.8 Reading the original text: Three layers in the Analysis plan
{: #section-28 }

This passage from Hernán and Robins (2016) connects three different questions: **how to group people initially, how to handle later strategy deviations, and how to handle loss of outcome follow-up.**

#### First paragraph: Why is comparing initiators only an observational analog of ITT?
{: #section-29 }

The meaning is that actual randomized trials estimate ITT using randomized groups. Observational data generally lack equivalent random-assignment information, so a closer approach compares people who begin different strategies at baseline, with sufficient baseline confounding control. Retaining initial groups after stopping or switching resembles ITT in form.

Distinguish two stages of adherence:

| Stage of adherence | Example | Relevance to this paragraph |
| --- | --- | --- |
| Initiating the assigned strategy at baseline | After assignment to treatment, does the person actually begin that day? | Determines correspondence between assignment and actual-initiation groups at baseline |
| Continuing to follow the strategy later | Continue or stop according to rules at month six? | Determines whether ITT and sustained-strategy PP target different later behavior |

The original phrase **assignment and initiation always occur together at baseline** refers to the first stage: in the hypothetical target trial, everyone initiates the corresponding strategy at assignment. It does not say that nobody ever deviates afterward.

If initial assignment and initiation correspond perfectly, grouping by initiation and by original assignment may retain the same groups even if some people stop six months later. Equating the effects also requires compatible interventions, subsequent care, pathways from assignment to outcomes, and other conditions; see §7.7. “Everyone started at baseline” alone cannot equate estimates from all actual studies.

This observational comparison therefore generally targets an initiation effect, or an observational analog of ITT; it gains no randomization guarantee. See §7.3 for why grouping by prescription rather than dispensing is closer to an assignment-level comparison.

#### Second paragraph: Why does sustained-strategy PP generally require g-methods?
{: #section-30 }

The meaning is that an effect of sustained adherence requires addressing relevant factors determining initial and subsequent adherence. Follow-up factors may themselves be affected by earlier treatment, so ordinary adjustment is generally insufficient for the target total effect.

Consider a teaching scenario:

- $$A_0$$: early treatment.
- $$L_1$$: subsequent disease status before the next treatment decision.
- $$A_1$$: later continuation or discontinuation.
- $$Y$$: the final outcome.

Suppose $$A_0$$ changes $$L_1$$, and $$L_1$$ affects $$A_1$$ and $$Y$$. Then $$L_1$$ may both transmit the effect of early treatment and confound later treatment–outcome relationships:

$$
A_0\rightarrow L_1\rightarrow Y,
\qquad
A_1\leftarrow L_1\rightarrow Y.
$$

Ignoring $$L_1$$ may leave later treatment confounded. Holding $$L_1$$ fixed in an ordinary outcome regression and directly interpreting its treatment coefficient as the total effect of the full strategy may block early treatment's effect through disease changes or encounter other conditioning problems.

**Thus, measuring every relevant variable and correctly specifying the conditional regression model does not mean that its treatment coefficient is the sustained-strategy total effect we want.** This explains the original emphasis on *even in the absence of unmeasured confounding and model misspecification*.

G-methods organize estimation according to the temporal sequence of treatment and disease. For example, [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) uses clinical history to estimate each period's treatment or adherence probabilities. [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}) lets disease evolve under different strategies and summarizes outcomes. These methods still rely on the corresponding exchangeability, positivity, consistency, and estimation conditions. [Naimi et al.: An introduction to g methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6074945/)

This does not imply that initial assignment in a randomized trial was confounded. RCTs randomize assignment; subsequent adherence is generally not repeatedly randomized. Estimating sustained-adherence effects is what requires addressing baseline and time-varying factors associated with actual adherence. In special settings such as complete adherence, there is no need to create complex additional adjustment merely because the target is called “PP.”

#### Third paragraph: Loss to follow-up can make later information necessary for both ITT and PP
{: #section-31 }

The meaning is that if loss to follow-up creates selection bias, ITT and PP analyses in both actual trials and observational studies may need relevant follow-up factors to address it. When those factors are themselves treatment-affected, g-methods are generally needed for appropriate handling.

For example, people whose disease worsens may be more likely to be lost, and worsening also predicts poorer outcomes. Using only the outcomes of those remaining may make them unrepresentative of the original target population. **Retaining the original assignment label does not obtain the outcomes of those lost.**

If treatment also causes this disease change, directly controlling for it in an ordinary outcome regression may change the total treatment effect originally sought. Under the appropriate assumptions, inverse probability of censoring weighting and related methods can address the observation process: appropriately weight those still observed instead of forcing post-treatment disease status to have the same fixed distribution under both strategies.

Keep the distinction clear: discontinuation changes treatment behavior; loss to follow-up makes required outcome information unavailable. A person can stop medication yet remain followed, or still take medication while becoming lost from study data. Their mechanisms, records, and handling rules cannot be conflated.

| Target and setting | Treatment-related adjustment | Loss-to-follow-up adjustment |
| --- | --- | --- |
| RCT ITT | Randomization ensures baseline assignment comparability; no regrouping for discontinuation | Informative loss still requires handling, potentially using later clinical history |
| Observational initiation effect | Address baseline confounding of initial treatment choice; later treatment evolves naturally by definition | Relevant loss likewise requires handling |
| Sustained-strategy PP in an RCT or observational study | Address confounding and selection associated with actual adherence; treatment–confounder feedback generally requires longitudinal g-methods | Relevant loss likewise requires handling; avoid counting one mechanism twice in adherence and censoring weights |

For an analysis plan in a complete protocol, see [7. Analysis Plan: What Does the Final Long Paragraph Mean?]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}#section-12); for censoring weights, see [8. IPTW and IPCW: Distinguishing Two Types of Probabilities]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-29).

## 8. Six self-check questions
{: #section-32 }

1. Someone assigned to B never takes medication. Which group should contain them in an ITT analysis?
2. Is the PP effect simply an effect “among people who adhere in reality”?
3. The protocol requires stopping for severe toxicity. Is stopping according to that rule nonadherence?
4. Does an observational study that groups by actual initiation and retains groups after discontinuation automatically estimate RCT ITT?
5. If the protocol specifies only initiation at baseline, does later stopping necessarily violate it?
6. Does the absence of random assignment mean that simply comparing actual medication users yields a PP effect?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. Keep them in their original randomized B group and obtain their outcome as completely as possible.
2. No. This note's PP target is the entire target population and asks what would happen if everyone followed their respective strategy.
3. No; following discontinuation rules is part of adhering to the protocol.
4. No. One compares randomized assignment and the other actual initiation; retaining baseline groups gives only a similar analytical form.
5. Not necessarily. If later treatment is unrestricted, later discontinuation does not violate an initiation-only protocol.
6. No. Actual treatment may be confounded; PP identification and estimation still require the relevant assumptions, data, and methods.

</details>
