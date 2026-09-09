---
layout: "causal-note"
title: "Point Interventions and Sustained Strategies"
description: "Why initiating treatment once and following a sustained strategy define different per-protocol effects."
group: "Trial design"
order: 5
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Interpreting the original text: What is the author comparing?", "anchor": "section-1"}, {"title": "2. How is the same patient handled under different protocols?", "anchor": "section-2"}, {"title": "3. A point intervention does not mean “one dose” or “one day of follow-up”", "anchor": "section-3"}, {"title": "4. Why does an initiation effect require only baseline treatment-confounding adjustment?", "anchor": "section-4"}, {"title": "5. Why can different adherence rates produce different initiation effects?", "anchor": "section-5"}, {"title": "6. A sustained strategy means following ongoing rules, not never stopping", "anchor": "section-7"}, {"title": "7. Why do sustained strategies involve time-varying confounding?", "anchor": "section-8"}, {"title": "8. Why not just put all time-varying disease measurements into a Cox model?", "anchor": "section-16"}, {"title": "9. What can methods do, and what can they not guarantee?", "anchor": "section-19"}, {"title": "10. Use this table when reviewing", "anchor": "section-20"}, {"title": "Sources", "anchor": "section-21"}]
previous_note: "/causal-inference/intention-to-treat-per-protocol/"
next_note: "/causal-inference/biomarkers-well-defined-interventions/"
---

Study entry point: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

For difficulty reading formulas, use [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}). The notation for “initiation,” “sustained rules,” and “standardization” is unpacked separately below.

Prerequisites: §1–§4 and §7.2 of [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}), and the potential outcomes and identification assumptions in [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}). You need not finish the entire ITT companion or learn CCW first. For dynamic rules and treatment versions, see [Biomarkers and Well-Defined Interventions]({{ "/causal-inference/biomarkers-well-defined-interventions/" | relative_url }}); consult [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) when you reach artificial censoring.

<aside class="study-callout study-callout--abstract" markdown="1">

**PP requirements depend on what the protocol specifies**

**Point intervention: Specify the initial action; subsequent treatment develops naturally.**

**Sustained strategy: Specify how treatment decisions continue during follow-up, including when treatment should stop.**

Both can define per-protocol effects. Whether later discontinuation violates the protocol depends on whether later behavior is specified and whether stopping follows the rules.

</aside>


<aside class="study-callout study-callout--tip" markdown="1">

**Compare the questions before learning the methods**

First read **the patient-handling table in §2 → §3 → §5–§6 → §10** to understand what the strategies require. Section 1 interprets the original text; return after understanding the main thread. On a second pass, read **§4 and §7–§9** to connect initiation effects with baseline standardization, then learn time-varying confounding and how prior treatment changes confounders. Hand calculations for IPW and the g-formula are in their own notes; there is no need to master them here all at once.

</aside>


## 1. Interpreting the original text: What is the author comparing?
{: #section-1 }

The source is the [supplement to Fu (2023)](https://cdn-links.lww.com/permalink/jsn/e/jsn_34_8_2023_07_28_fu_jasn-2023-000583_sdc1.pdf), which compares two PP targets in observational studies. The interpretation below is divided by its logical sequence.

**First paragraph: An initiation effect is also a type of PP.**

A per-protocol effect (PP) is the effect of receiving treatment according to the trial protocol. If the protocol specifies only “initiate treatment at baseline,” the effect of following this single-time protocol is point-intervention PP. Actual initiators and noninitiators may differ in prognosis, so a sufficient set for baseline confounding adjustment is needed—not every measured baseline variable indiscriminately. Residual uncontrolled confounding may invalidate the causal interpretation. Without later selection problems such as loss to follow-up, identifying this total effect of initial initiation does not additionally require controlling time-varying confounding for subsequent treatment decisions.

**Second paragraph: Initiation effects include later usual treatment experiences.**

Patients remain in their original initiation group even if they later stop or switch medication. The same baseline initiation action may therefore yield different outcomes in healthcare systems with different later adherence behaviors. The original text illustrates this with 80% versus 60% adherence and HRs of 0.70 versus 0.90; this is not a formula deriving HR from adherence. Its mention of 60% discontinuation in a particular SGLT2 inhibitor safety study is likewise an observation from one study, not a universal discontinuation rate.

HR means hazard ratio, comparing instantaneous event rates among people who have not yet experienced the event. It is a dimensionless ratio. HR 0.70 cannot be read directly as “30% lower one-year mortality risk”; see [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}) for risks versus instantaneous rates.

**Third paragraph: Sustained strategies include later actions in the intervention definition.**

For example, compare “start medication now and continue unless a contraindication develops” with “do not initiate it throughout follow-up.” The target becomes the outcome difference if everyone follows their full respective rules. The target effect is therefore no longer defined by how many people in that healthcare system happen to stop on their own. Estimating it from real data with deviations, however, generally requires high-quality longitudinal treatment and confounder information. When confounders are also affected by prior treatment, methods such as g-methods that address this structure are often needed. Time-varying confounding alone does not make all ordinary regression invalid; see §7.

Reference 12 in the original article is [Hernán and Robins (2017): Per-Protocol Analyses of Pragmatic Trials](https://pubmed.ncbi.nlm.nih.gov/28976864/).

## 2. How is the same patient handled under different protocols?
{: #section-2 }

Specify a teaching study with the same target population, common time zero, and one-year mortality outcome. The two protocols are:

- **Initiation protocol:** initiate medication at baseline, then follow usual care; the comparator does not initiate at baseline and also follows usual care afterward.
- **Sustained protocol:** initiate at baseline and continue as specified while alive, stopping for protocol-defined contraindications; the comparator never initiates during follow-up.

| Event | Initiation protocol | Sustained protocol |
| --- | --- | --- |
| Initiates at baseline; stops independently at month 3 | Retain initiation group; stopping does not violate a baseline-only protocol | Deviates from this point if no protocol exception applies |
| Initiates at baseline; a specified contraindication develops at month 3 and the patient stops as required | Retain initiation group | Stopping is adherence and must not be censored as nonadherence |
| Does not initiate at baseline; starts at month 6 | Remains in the baseline noninitiation group; later initiation is allowed to occur naturally | Deviates from “no initiation throughout follow-up” |
| Uses medication according to rules until death at month 4 | Record death | Also record death; do not exclude for failing to complete a year of medication |

An actual protocol also needs to specify the drug, dose, allowable missed-dose intervals, monitoring, contraindication criteria, and restarting after discontinuation. This shows only the structure; “unless contraindicated” is not a fully specified set of operational rules.

<aside class="study-callout study-callout--important" markdown="1">

**Two contexts for nonadherence in the original text**

In discussing initiation effects, the author says “subsequent nonadherence affects PP.” Here nonadherence refers to clinical adherence to usual continued medication.

If the research protocol intervenes only at baseline, subsequent stopping does not violate that point-intervention protocol. This is not “PP allowing violations of its own protocol”; the two protocols impose different requirements on later behavior.

</aside>


## 3. A point intervention does not mean “one dose” or “one day of follow-up”
{: #section-3 }

Point refers to **when the intervention acts on a decision**, not the duration of pharmacological action.

A study can specify only whether to initiate an antihypertensive today, then observe outcomes over five years. Patients may continue, stop, or switch; these are processes that develop naturally after initiation in that healthcare system.

The next formula returns to §2's one-year mortality example. Let $$A_0$$ indicate baseline initiation, with 1 for initiation and 0 for no initiation at that time; $$Y$$ indicates death within one year, with 1 for death and 0 otherwise:

$$
\Delta_{\mathrm{initiation}}=E[Y^{A_0=1}]-E[Y^{A_0=0}].
$$

Read from the inside out:

| Symbol | Meaning in this formula |
| --- | --- |
| $$A_0$$ | Actual baseline initiation action; subscript 0 indexes time |
| $$Y^{A_0=1}$$ | Whether death occurs within one year if initiation occurs at baseline and later events develop naturally; the superscript is an intervention scenario, not a power |
| $$Y^{A_0=0}$$ | Whether death occurs within one year if no initiation occurs at baseline and later events develop naturally; treatment may still begin later |
| $$E[\cdot]$$ | Average over the same target population, synonymous with $$\mathbb E[\cdot]$$; the dot is a placeholder for the variable |
| $$\Delta_{\mathrm{initiation}}$$ | Greek delta names the initiation effect; initiation labels the effect type, not time |
| Subtraction between the terms | Fixes the direction as “initiation minus noninitiation” |

Because $$Y$$ is 0 or 1, the two means are one-year mortality risks under the two scenarios. If they are 12% and 20%, the initiation risk difference is $$0.12-0.20=-0.08$$, or −8 percentage points. These causal risks are stipulated to illustrate the formula; actual group proportions alone do not establish them.

The notation sets only $$A_0$$; subsequent $$A_1,A_2,\ldots$$ arise from disease and care processes in each intervention world. The same patient's factual later medication trajectory cannot be mechanically copied into another counterfactual world.

Subscripts in $$A_1,A_2$$ index the first and second later treatment decisions; the ellipsis allows more times. Each $$A$$'s value is that occasion's action, not the effect size discussed above.

For a sustained strategy, let $$g_1$$ be “initiate at baseline and continue management under rules that include stopping for contraindications,” and $$g_0$$ “do not initiate throughout follow-up.” A complete study must additionally specify dose, monitoring, restarting, and the other details in §2:

$$
\Delta_{\mathrm{sustained}}=E[Y^{g_1}]-E[Y^{g_0}].
$$

Here $$g$$ names treatment rules; subscripts in $$g_1,g_0$$ distinguish the two strategies, **not treatment times**. $$Y^{g_1}$$ is a target-population individual's one-year outcome when following the first set of rules; $$Y^{g_0}$$ corresponds to the second. They are not two observed subgroups who “happened to keep adhering.” $$E$$ still averages over the full target population, and $$\Delta_{\mathrm{sustained}}$$ is the sustained-strategy risk difference. Separately setting the risks to 10% and 20% gives −10 percentage points. This differs from the initiation effect of −8 because the contrasts impose different later treatment requirements; these are independent teaching values.

The equations intervene differently on later actions and therefore define different **causal estimands**. An actual RCT assignment context is omitted here; see [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}) for $$Z$$ versus actual treatment.

## 4. Why does an initiation effect require only baseline treatment-confounding adjustment?
{: #section-4 }

Let $$L_0$$ contain pre-initiation disease and other sufficient baseline confounding information. We need to address:

$$
A_0\leftarrow L_0\rightarrow Y.
$$

Subscript 0 denotes baseline: $$L_0$$ is information preceding the treatment decision, $$A_0$$ whether initiation occurs then, and $$Y$$ death within the following year. The two arrows mean $$L_0$$ affects both treatment choice and outcome; they are not numerical operations and do not provide an effect size by themselves.

Under conditional exchangeability, positivity, consistency, and complete reliable outcomes, baseline standardization can identify an initiation effect, for example:

$$
E[Y^{A_0=a}]=\sum_{l_0}E[Y\mid A_0=a,L_0=l_0]P(L_0=l_0).
$$

The equation means “compare within the same baseline characteristics, then average over the same target population.” Its components are:

| Symbol or component | Meaning |
| --- | --- |
| $$a$$ | Specified baseline action: 1 for initiation or 0 for no initiation now |
| $$l_0$$ | A particular value of baseline characteristics $$L_0$$, such as mild or severe disease; lowercase denotes a value and uppercase a variable |
| $$E[Y^{A_0=a}]$$ | One-year mortality risk if the entire target population performed baseline action $$a$$ |
| $$E[Y\mid A_0=a,L_0=l_0]$$ | Observed mean outcome among people with characteristics $$l_0$$ who actually performed $$a$$; the bar means “under these conditions,” and the comma means both conditions hold |
| $$P(L_0=l_0)$$ | Proportion of the full target population in that characteristic stratum; $$P$$ denotes probability |
| $$\sum_{l_0}$$ | Sum “risk × stratum proportion” over every stratum; adjacent terms are multiplied |

Here $$L_0$$ is written as discrete strata; continuous characteristics require the corresponding integration or prediction-and-averaging expression. Coding $$Y$$ as 0/1 permits interpreting $$E$$ as risk, expressed as a proportion or percentage.

An independent hand-calculation example: the target population is 50% mild and 50% severe disease. Among observed initiators, one-year risks are 5% and 20% in those strata; among noninitiators, 10% and 40%. If the identification conditions hold, standardization gives:

- Everyone initiates: $$0.5\times5\%+0.5\times20\%=12.5\%$$.
- Nobody initiates now: $$0.5\times10\%+0.5\times40\%=25\%$$.
- Initiation risk difference: $$12.5\%-25\%=-12.5$$ percentage points.

Each calculation uses the same 0.5 and 0.5—the mild/severe proportions of the entire target population. These values do not continue §3's risk scenario and are not actual clinical effects; they demonstrate where data enter the standardization formula.

Later disease $$L_1$$ may affect later treatment $$A_1$$ and outcome $$Y$$, even producing confounding $$A_1\leftarrow L_1\rightarrow Y$$. However, the initiation effect does not separately intervene on $$A_1$$: it allows later disease, discontinuation, and switching jointly to constitute consequences of initiation. Estimating the total effect of $$A_0$$ therefore does not require balancing away this whole later process.

For example, if $$A_0\rightarrow L_1\rightarrow Y$$ is the pathway by which early treatment improves disease, directly controlling $$L_1$$ as an ordinary covariate may block part of the initiation effect.

**“Baseline adjustment is sufficient” has explicit boundaries:**

- It concerns confounding control for the total initiation effect, not the importance of follow-up data.
- If follow-up disease affects both loss to follow-up and death, informative loss needs handling, potentially using time-varying history.
- Artificial censoring at discontinuation introduces another selection problem and no longer gives the original simple initiation comparison.
- If “initiation” is actually defined by treatment decisions during a future grace period, a single-$$A_0$$ approach cannot be applied indiscriminately; see [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}).

## 5. Why can different adherence rates produce different initiation effects?
{: #section-5 }

Suppose two healthcare systems offer the same medication to the same target population:

- System A provides more stable refills and support, so more patients continue after initiation.
- In system B, patients more often stop or switch.

The treatment experiences set in motion by initiation differ. The **true causal effect** of “initiate today” on later outcomes can therefore differ even if both studies correctly control confounding.

This concerns context dependence and generalizability, not automatic evidence of a biased estimate. A different issue arises if investigators interpret an estimated initiation effect as the effect of “everyone continuing treatment”: that misinterprets the estimand.

The original 80%→HR 0.70 and 60%→HR 0.90 are illustrative only. Overall adherence cannot determine HR, and lower adherence need not move an effect toward zero. Timing and reasons for discontinuation, later control-group treatment, and early versus late treatment benefits and harms can all affect direction.

<details class="study-callout" markdown="1">
<summary>An independent risk example: Illustrating a mechanism, not calculating HR</summary>

Suppose one-year risk is 10% under sustained medication, 20% under another rule that stops very early with no subsequent treatment, and 20% for a comparator that never initiates or uses medication. To mix these causal risks directly, additionally assume that selection of the “continue” or “stop very early” path after initiation is independent of potential outcomes under both paths, there is no crossover treatment, and the two systems differ only in path-selection proportions.

This teaching mechanism determines later treatment paths at baseline; **it does not wait until year-end to classify people by whether they survived and persisted for a full year**. Death partway along the sustained path remains part of that path's mortality risk.

With an 80% sustained-path proportion, among 1,000 initiators, 800 follow the sustained path with $$800\times10\%=80$$ expected deaths, and 200 follow the early-stopping path with $$200\times20\%=40$$ expected deaths. The total is 120, giving 12% risk.

With a 60% sustained-path proportion, the same calculation gives $$600\times10\%+400\times20\%=140$$ deaths, or 14% risk. As risk mixtures, these are $$0.8\times10\%+0.2\times20\%=12\%$$ and $$0.6\times10\%+0.4\times20\%=14\%$$.

Initiation-versus-control risk differences are −8 and −6 percentage points, respectively. In this constructed setting, sustained-strategy-versus-control risk differences are both −10 percentage points.

In real data, continuers and discontinuers often differ in prognosis. Their observed risks cannot simply be inserted into this weighted formula to obtain causal effects.

</details>


### Qualifications for a single vaccine dose or one-time surgery
{: #section-6 }

If the intervention truly consists of one completed injection or operation, there is no subsequent daily decision about continuing that same action. But nonreceipt, delayed implementation, loss to follow-up, and later care differences can still occur. A protocol with multiple vaccine doses, perioperative medication, or rehabilitation requirements cannot be classified as purely point-based simply because it concerns a “vaccine” or “surgery.”

## 6. A sustained strategy means following ongoing rules, not never stopping
{: #section-7 }

The original “continue unless a contraindication develops” is a dynamic strategy: the next action depends on disease status known at that time.

People following the same strategy can have different medication trajectories:

- Those without contraindications continue as specified.
- Those developing contraindications stop as specified.

Both may adhere fully. The target therefore cannot simply be written as “force $$A_t=1$$ for everyone.” PP concerns outcomes if the full target population followed the rule, not only people who happen to adhere long term in reality.

Here $$t$$ is a treatment-decision time during follow-up and $$A_t=1$$ means medication use then. “Set treatment to 1 at every time” is a fixed sustained-use rule, different from the dynamic rule “stop when a specified contraindication develops.” Do not confuse this time index $$t$$ with a treatment label $$t$$ in the potential-outcomes foundations note.

The precise meaning of “adherence patterns do not affect sustained PP” is: **the defined counterfactual world requires everyone to follow the specified rules; the target is not defined by arbitrary deviation proportions observed in reality.** Actual adherence still affects estimation difficulty, precision, weights, and positivity. Different populations, monitoring, dose versions, and other care can also change the effect of a strategy described with the same words. It does not automatically generalize across systems.

## 7. Why do sustained strategies involve time-varying confounding?
{: #section-8 }

### 7.1 Reading the figure: Time-varying confounding need not imply treatment–confounder feedback
{: #section-9 }

![Time varying confounding without treatment feedback]({{ "/assets/causal-inference/time-varying-confounding-without-treatment-feedback.png" | relative_url }})

This screenshot depicts actual treatment and patient characteristics at three times. The explanation below follows only the visible arrows; §7.2 separately adds the case where prior treatment changes later disease.

#### Time subscripts and the two rows of variables
{: #section-10 }

| Time | Characteristics observed before this treatment decision | Actual treatment at this decision |
| --- | --- | --- |
| Baseline 0 | $$L_0$$ | $$A_0$$ |
| First follow-up 1 | $$L_1$$ | $$A_1$$ |
| Second follow-up 2 | $$L_2$$ | $$A_2$$ |

$$Y$$ is the final outcome. $$A_k$$ may indicate use, drug choice, or dose at that occasion or observation interval; it does not mean the $$k$$th drug. $$L_k$$ generally contains multiple covariates, rather than necessarily one measurement. 0, 1, and 2 indicate sequence, not necessarily three particular dates or only three clinical examinations.

Here $$k$$ is a general time index, so $$k-1$$ denotes the previous time. With binary use coding, $$A_k=1$$ means use and $$A_k=0$$ nonuse. Units of $$L_k$$ depend on its variables: blood pressure in mmHg, age in years, comorbidity as present/absent. $$Y$$ may retain the one-year mortality 0/1 coding.

The data sequence is: measure $$L_0$$, then decide $$A_0$$; subsequently measure $$L_1$$, then decide $$A_1$$; and so forth. $$L_k$$ in the same column must contain relevant information known before that treatment decision.

#### Inventory of the screenshot's arrows
{: #section-11 }

| Visible arrow | Causal assumption expressed |
| --- | --- |
| $$L_0\to L_1\to L_2$$ | Earlier patient characteristics affect later characteristics |
| $$L_0\to A_0$$, $$L_1\to A_1$$, $$L_2\to A_2$$ | Each treatment choice depends on contemporaneous characteristics |
| $$A_0\to A_1\to A_2$$ | Prior treatment affects later continuation, stopping, or switching |
| $$L_0\to Y$$, $$L_1\to Y$$, $$L_2\to Y$$ | Characteristics at each time also affect the final outcome; the first two are the long upper arcs |
| $$A_2\to Y$$ | Later treatment affects the outcome; early treatment in the figure can also affect $$Y$$ through later treatment |

Arrows encode assumed causal relationships, not effect size or sign. Crossing arcs do not form a node; one cannot change from one edge to another at their crossing.

#### Why are these L variables confounders?
{: #section-12 }

Each time has a common-cause structure:

$$
A_0\leftarrow L_0\rightarrow Y,\qquad
A_1\leftarrow L_1\rightarrow Y,\qquad
A_2\leftarrow L_2\rightarrow Y.
$$

For example, $$L_1$$ affects both treatment choice at first follow-up and the outcome. Direct comparison of people with $$A_1=1$$ versus $$A_1=0$$ may therefore mix treatment effects with effects of $$L_1$$. Confounding recurs with each treatment decision; baseline balance does not make sustained treatment histories inherently comparable.

This does not imply adjusting only for the current $$L_k$$ each time. Actual analyses should address sufficient prior clinical and treatment history according to the causal structure. The three short paths are simply the most visible sources of confounding.

A deliberately simplified example consistent with this figure is a comorbidity $$L_k$$ unaffected by the study drug, whose progression affects continued drug use and independently affects mortality. $$L_k$$ is then a time-varying confounder. If the example instead uses drug-affected blood pressure or another measurement, the corresponding treatment-to-measurement arrows must be added, giving the next subsection's structure.

#### The key relationship absent from the screenshot
{: #section-13 }

**There are no $$A\to L$$ arrows in the figure**, particularly no $$A_0\to L_1$$ or $$A_1\to L_2$$.

Treating the figure strictly as a complete DAG:

- $$L_1$$ confounds subsequent treatment $$A_1$$.
- $$L_1$$ is not shown as a consequence of early treatment $$A_0$$, so the figure does not justify calling it a mediator of $$A_0$$.
- The figure has time-varying confounding but no treatment–confounder feedback.

If the author intended only a simplified diagram, clinically relevant paths may be omitted. Those should be stated and added to the model, rather than treated as arrows already present in the screenshot.

| Structure | Key relationship used to illustrate it | In this screenshot |
| --- | --- | --- |
| Time-varying confounding | $$L_k\to A_k$$ and $$L_k\to Y$$ | Present |
| Prior treatment affects later confounders | Additional paths such as $$A_{k-1}\to L_k$$ | Not shown |

#### Connection to initiation and sustained-strategy effects
{: #section-14 }

If the target is only the total effect of $$A_0$$, allowing later treatment to develop naturally, adjusting for $$L_0$$ blocks backdoor paths into $$A_0$$ under the screenshot's complete causal model and other identification conditions. $$A_1,A_2$$ lie on $$A_0\to A_1\to A_2\to Y$$ and should not simply be controlled away to “adjust thoroughly.”

<details class="study-callout" markdown="1">
<summary>Why can controlling subsequent treatment also introduce selection problems?</summary>

In the figure, $$A_1$$ is affected by both $$A_0$$ and $$L_1$$. Conditioning on $$A_1$$ alone can open the collider path $$A_0\to A_1\leftarrow L_1\to Y$$. Appropriate control of other variables may close some paths again, but does not alter the fact that controlling later treatment blocks part of the initiation-effect pathway. Collider bias depends on the full adjustment set; the presence of a post-treatment variable alone is not enough to determine it.

</details>


Studying the full treatment strategy requires addressing confounding of $$A_0$$ and each subsequent action. This generally needs $$L$$ measured before each decision and prior treatment information, beyond baseline variables alone.

However, **needing longitudinal confounding control does not mean this figure alone establishes that ordinary regression must fail**. If confounders are truly unaffected by prior treatment, appropriate regression adjustment and standardization may also work under the necessary assumptions; IPW and the g-formula can also be used. Models must still match the target strategy; an arbitrary treatment coefficient cannot simply be equated with the full strategy effect.

The more difficult case is the next section's $$A_0\to L_1$$: controlling $$L_1$$ then concerns both confounding of later treatment and mediation of prior treatment. [Naimi, Cole, and Kennedy: An introduction to g methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6074945/)

### 7.2 Adding an effect of prior treatment on later disease
{: #section-15 }

The following teaching extension adds feedback through $$A_0\to L_1$$, which the preceding screenshot does not show. Do not treat the two figures as identical models.

For a simplified chronic-disease medication example:

- $$A_0$$: medication use at baseline;
- $$L_1$$: disease status at month 3, before the next treatment decision;
- $$A_1$$: continued medication after month 3;
- $$Y$$: the one-year outcome.

Early medication affects month-3 disease, which in turn affects later medication and outcome. To highlight the key relationships, the diagram omits baseline $$L_0$$, which also requires adjustment:

<pre class="mermaid">flowchart LR
    A0[&quot;A₀: Early treatment&quot;] --&gt; L1[&quot;L₁: Disease at month 3&quot;]
    L1 --&gt; A1[&quot;A₁: Later treatment&quot;]
    L1 --&gt; Y[&quot;Y: One-year outcome&quot;]
    A0 --&gt; A1
    A0 --&gt; Y
    A1 --&gt; Y</pre>

The same $$L_1$$ has two roles:

1. For later treatment $$A_1$$, it is a confounder: $$A_1\leftarrow L_1\rightarrow Y$$.
2. For early treatment $$A_0$$, it is a post-treatment mediator: $$A_0\rightarrow L_1\rightarrow Y$$.

This is **treatment–confounder feedback: prior treatment affects a confounder of subsequent treatment**.

For example, worsening disease may make patients more likely to stop because of tolerability issues and more likely to die. Comparing eventual continuers with discontinuers may mistake health differences for a continued-treatment effect. Improving patients may also stop, so bias has no fixed direction.

## 8. Why not just put all time-varying disease measurements into a Cox model?
{: #section-16 }

For Cox risk sets, partial likelihood, and how biases enter comparisons, see [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}).

In the feedback structure above:

- Ignoring $$L_1$$ may fail to control confounding between $$A_1$$ and $$Y$$.
- Directly conditioning on $$L_1$$ in an ordinary outcome regression may block $$A_0$$'s effect on $$Y$$ through $$L_1$$. The treatment coefficient cannot be directly interpreted as the full strategy's total effect; some structures can also introduce collider bias.

Appropriate methods must control confounding at each treatment step while preserving treatment effects through subsequent disease. This is a major use of g-methods. The key is the identification and analysis structure, rather than simply including more covariates. See [Robins, Hernán, and Brumback (2000)](https://www.stat.ubc.ca/~john/papers/RobinsEpi2000.pdf).

### IPW and marginal structural models
{: #section-17 }

For step-by-step numerical calculations, see [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}): propensity scores, inverse weights, longitudinal treatment weights, and censoring weights.

Use treatment and disease history known before each decision to estimate the probability of the actual treatment choice. Under identification assumptions, inverse probability weights produce a comparison no longer driven by these measured histories, then permit outcome estimation under each strategy.

For an implementation using “artificial censoring at deviation,” estimate the probability of remaining compatible and uncensored. Compatible records less likely to remain receive larger weights, representing similar patients with the same known histories who were censored. Baseline comparability also needs attention when initial grouping is confounded.

An MSM (marginal structural model) is a causal model describing outcomes under interventions; IPW is a common estimation approach. They are related but distinct concepts. See [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) for implementation.

### G-formula / g-computation
{: #section-18 }

For step-by-step numerical calculations, see [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}): first calculate risks for a common baseline population, then sustained-strategy risks when treatment changes later disease.

Model changes in disease over time and the outcome. Simulate sequentially:

1. If everyone in the target population follows $$g_1$$, how does disease change at each step, what treatment do the rules require, and what is the final outcome?
2. If the same population follows $$g_0$$, how does that process unfold?
3. Summarize and compare outcomes under the two simulated strategies.

The g-formula allows disease to change with the corresponding treatment history in each strategy world, rather than forcing identical later disease. It can itself use regression models; the issue is not “regression” as a tool but whether standardization and comparison follow the correct longitudinal causal structure. For dynamic strategies, see [Estimating Effects of Dynamic Treatment Strategies…: A Primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC5710813/).

If time-varying confounders are unaffected by prior treatment, some simpler methods may also apply under suitable conditions. This does not mean “all sustained-treatment studies must use the same weight model.”

## 9. What can methods do, and what can they not guarantee?
{: #section-19 }

| Required condition | Meaning for sustained strategies |
| --- | --- |
| Consistency and well-defined interventions | Sufficiently explicit dose, continuation and stopping rules, and treatment versions |
| Sequential conditional exchangeability | Given sufficient clinical and treatment history before each decision, that treatment choice is independent of potential outcomes under the relevant strategies; intuitively, no residual treatment confounding at any step |
| Positivity | The required action can be observed under relevant histories; extreme weights cannot invent paths that never occur |
| Appropriate data and estimation | Reliable treatment coverage, disease, contraindication, ordering, outcome, and loss-to-follow-up measurements, with models adequate for estimation |

Administrative databases often lack symptoms, frailty, actual ingestion, patient preferences, or reasons for stopping. If missing factors create uncontrolled confounding, IPW or the g-formula cannot eliminate it from nothing. More complex machine learning also cannot automatically recover unmeasured causes.

Likewise, when actual adherence is very low, an “everyone adheres” effect may be well defined but difficult to identify or estimate precisely from available data. A clear target and data capable of answering it are different matters.

## 10. Use this table when reviewing
{: #section-20 }

| | Point-intervention PP | Sustained-strategy PP |
| --- | --- | --- |
| What is intervened on? | Actual initial action $$A_0$$ | Full follow-up rules $$g$$ |
| How does later treatment occur? | Through usual care after the intervention | According to rules, including specified stopping exceptions |
| Does stopping necessarily violate the protocol? | No; later behavior may be unspecified | No; distinguish permitted stopping from actual deviation |
| Usual treatment-confounding control | Sufficient baseline confounding adjustment | Generally baseline and longitudinal confounding adjustment |
| Loss to follow-up | Still needs assessment; may require time-varying information | Likewise requires handling |
| Role of the adherence setting | Can change actual consequences and effects of initiation | Does not define the effect by the actual deviation rate, but affects estimation and generalizability |
| Main question | In this care setting, what would initiating now do? | What would happen if everyone followed these long-term rules? |

1. Why is stopping at month 3 not necessarily nonadherence under an initiation protocol?
2. Why do different initiation effects in two systems not necessarily imply bias?
3. How can the same $$L_1$$ be both a mediator and a confounder?
4. Should stopping according to a contraindication rule be censored as deviation?
5. How can data from only actual adherers represent the whole target population?
6. Can IPW repair unmeasured disease that affects stopping and death?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. The protocol specifies only the baseline action; later stopping does not violate that rule.
2. Different subsequent treatment trajectories can produce different true consequences of initiation.
3. $$L_1$$ is affected by $$A_0$$ and affects $$A_1$$ and $$Y$$; its role depends on which treatment decision is being considered.
4. No; that is adherence to a dynamic rule.
5. Relevant conditional exchangeability, positivity, and appropriate adjustment are needed; remaining people cannot simply stand in for everyone.
6. No. It adjusts using available information and the required assumptions.

</details>


## Sources
{: #section-21 }

- [Fu (2023), supplement: PP for point interventions and sustained strategies](https://cdn-links.lww.com/permalink/jsn/e/jsn_34_8_2023_07_28_fu_jasn-2023-000583_sdc1.pdf).
- [Hernán MA, Robins JM (2017). Per-Protocol Analyses of Pragmatic Trials](https://pubmed.ncbi.nlm.nih.gov/28976864/).
- [Robins JM, Hernán MA, Brumback B (2000). Marginal Structural Models and Causal Inference in Epidemiology](https://www.stat.ubc.ca/~john/papers/RobinsEpi2000.pdf).
- [Li X, Young JG, Toh S (2017). Estimating Effects of Dynamic Treatment Strategies in Pharmacoepidemiologic Studies with Time-varying Confounding: A Primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC5710813/).
- [Naimi AI, Cole SR, Kennedy EH. An introduction to g methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6074945/): time-varying confounding, treatment–confounder feedback, and the limits of standard methods.

The one-year follow-up, patient-handling table, and risk-mixture examples are teaching scenarios, not clinical efficacy results.
