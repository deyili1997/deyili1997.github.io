---
layout: "causal-note"
title: "Immortal Time, Lead Time, and Depletion of Susceptibles"
description: "Separate immortal time, lead time, and survivor selection through numerical examples and dialysis initiation strategies."
group: "Bias and measurement"
order: 11
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Comparing the three biases", "anchor": "section-1"}, {"title": "2. Immortal time bias", "anchor": "section-2"}, {"title": "3. Lead time bias", "anchor": "section-7"}, {"title": "4. Depletion-of-susceptibles bias", "anchor": "section-13"}, {"title": "5. Three investigators’ thought experiment: early versus late dialysis", "anchor": "section-20"}, {"title": "6. Separating timing problems from population problems", "anchor": "section-37"}, {"title": "7. Self-check", "anchor": "section-38"}]
previous_note: "/causal-inference/confounding-treatment-components/"
next_note: "/causal-inference/cox-proportional-hazards/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Three distinct mechanisms**

**Immortal time bias:** membership in a group requires surviving to a future point, and the analysis mishandles the preceding period during which those members necessarily survived.

**Lead time bias:** starting the clock earlier lengthens recorded survival without necessarily postponing death.

**Depletion of susceptibles:** people more likely to experience the outcome have events or leave earlier, changing the composition of those remaining. Interpreting this selected population as the original population can bias conclusions about treatment effects.

</aside>


Related notes: [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}), [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}), and [Potential Outcomes and Exchangeability]({{ "/causal-inference/potential-outcomes/" | relative_url }}).

For corresponding design approaches—enrollment of new users, grace periods, and emulation at multiple eligible decision points—see [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}).

How these biases enter Cox risk sets, event comparisons, and hazard ratios is discussed in [How Bias Affects the Cox Model]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-9).

<aside class="study-callout study-callout--tip" markdown="1">

**How to read this note**

On the first pass, read §1 and the three numerical examples in §2.3, §3.2, and §4.3. Remember their separate mechanisms: grouping using future information, an earlier clock, and changes in survivor composition.

On the second pass, work through the dialysis example: start with the table in §5.1, then read §5.2–§5.4. Use the timelines and causal diagrams to check the mechanisms. Derivations and expandable advanced sections can wait.

**Except where explicitly described as an interpretation of a publication, the numerical examples below are invented for teaching and are not clinical study findings.**

</aside>


## 1. Comparing the three biases
{: #section-1 }

| Bias | What goes wrong? | A characteristic mistaken inference |
| --- | --- | --- |
| Immortal time bias | Future information determines past group membership, or future survival selects participants, with incorrect handling of the relevant risk time | “People who eventually received the drug were less likely to die even before receiving it, so the drug works.” |
| Lead time bias | Follow-up begins at different disease stages, but survival after diagnosis or treatment is interpreted as evidence of longer life | “People lived longer after an earlier diagnosis, so their lives were extended.” |
| Depletion-of-susceptibles bias | Earlier events or treatment tolerance have already selected the people entering the analysis or remaining in later risk sets | “Long-term users rarely have events, so starting the drug must also be safe.” |

These are different mechanisms, not mutually exclusive categories. A study can have two or all three problems, and the direction of the resulting bias depends on its design.

Bias is always relative to a target question. Here the principal question is: **starting when patients share eligibility and can make a treatment decision, how do two strategies affect outcomes in the original target population?** If the question instead concerns continuation versus discontinuation among people who have already tolerated a drug for a year, the appropriate population and starting point also change.

## 2. Immortal time bias
{: #section-2 }

### 2.1 What does “immortal” mean?
{: #section-3 }

**Immortal time** is a period created by an inclusion or exposure definition during which members of the relevant group must remain alive or free of the study event. People are not literally unable to die: dying earlier would make them unable to satisfy the group definition.

Immortal time bias arises when assigning, excluding, or selecting participants using that period systematically distorts the target effect. [Suissa, 2008](https://pubmed.ncbi.nlm.nih.gov/18056625/).

This section uses death as the outcome. For a nonfatal outcome, ask specifically whether experiencing it would prevent the person from satisfying the inclusion or group definition. Not all pretreatment time is immortal time.

### 2.2 An inpatient medication example
{: #section-4 }

Consider this problematic analysis rule:

> Follow patients from admission. After reviewing the entire hospitalization, classify everyone who ever received B as treated from the day of admission.

Patient A has this history:

```text
Day 0: admission ─────── Day 7: starts B ─────── Day 20: death
                 No B yet, but this period is retrospectively
                 assigned to the treated group because B starts on day 7.
```

Had the patient died on day 3, they could not have become someone who “ever received B.” Thus everyone classified as treated by this rule necessarily survived until their actual initiation of B.

We cannot say that B protected the patient during those first seven days: the patient had not received B yet.

If the investigator instead assessed eligibility on day 7 and began a properly designed new-user comparison when B was initiated that day, initiation would be **baseline information** for that trial. Whether information is used incorrectly depends on its position and use relative to that trial’s $$T_0$$, not on which record the computer retrieved first. See [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}) for the distinction between enrollment, strategy assignment, and subsequent compatibility.

### 2.3 A numerical example: a null effect becomes a protective association
{: #section-5 }

Suppose a randomized trial with complete follow-up includes 200 people:

- 100 are assigned to “start B on day 30 if still alive.”
- 100 are assigned to “do not use B.”
- To isolate design bias, B is assumed to have no effect on anyone’s time of death.
- In each group, exactly 10 people die before day 30 and another 9 die during the remaining follow-up.

**Comparison by original strategy assignment:**

| Original strategy | Initial number | Deaths before day 30 | Later deaths | Risk over full follow-up |
| --- | --- | --- | --- | --- |
| Start B on day 30 | 100 | 10 | 9 | 19 / 100 = 19% |
| Do not use B | 100 | 10 | 9 | 19 / 100 = 19% |

The risks are equal; the risk difference is zero.

**Now regroup people by whether they actually ever received B:**

| Incorrect retrospective group | Who is included? | Number | Deaths over full follow-up | Calculated proportion dying |
| --- | --- | --- | --- | --- |
| Ever received B | The 90 people assigned to B who survived to day 30 | 90 | 9 | 10.0% |
| Never received B | The 100 assigned to no B, plus 10 early deaths among those assigned to B | 110 | 29 | 26.4% |

The drug has no effect, yet the incorrect comparison gives:

$$
10.0\%-26.4\%\approx-16.4\text{ percentage points}.
$$

The distortion comes from two steps: **regrouping using future treatment and retrospectively assigning pretreatment follow-up to the treated group.** Early deaths originally assigned to the B strategy are consequently moved into the untreated group.

Even data from a randomized trial can therefore yield bias after an incorrect retrospective analysis.

### 2.4 How can it be avoided?
{: #section-6 }

Specify the target question before changing a statistical model:

- **Effect of strategy assignment:** when actual baseline assignment is observed, retain relevant outcomes after assignment and before actual treatment. See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).
- **Initiating A versus initiating B:** enroll at the corresponding new-user decision points, with compatible eligibility, strategy definitions, and follow-up starts in both groups.
- **Actual exposure changing over time:** record unexposed and exposed time when they occur, avoiding assignment of pretreatment time to exposure. This fixes time classification only; ordinary time-dependent Cox regression may be insufficient when confounding varies over time.
- **Strategies allowing a grace period:** a rule such as “start B within 30 days” requires an appropriate design, such as [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}), rather than simple retrospective grouping by completed initiation.

These approaches can target different estimands and require different assumptions. See [Hernán et al., 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/) on alignment and grace periods.

<aside class="study-callout study-callout--warning" markdown="1">

**Removing the waiting period may not solve the problem**

Retaining only those who survived to treatment and moving follow-up to treatment initiation may remove waiting time from the analysis, but survival has already selected the population. This can introduce the problem in §4.

Landmark analysis can study subsequent effects among people still eligible at a fixed point. It changes the target population and starting point; it does not automatically recover the effect in the original population from the original baseline.

</aside>


## 3. Lead time bias
{: #section-7 }

### 3.1 The starting point of survival has changed
{: #section-8 }

The familiar clinical quantity “survival after diagnosis” is:

$$
\text{Survival after diagnosis}
=\text{Time of death}-\text{Time of diagnosis}.
$$

If screening advances diagnosis, this difference increases even when death occurs at exactly the same time. Interpreting the increase as evidence of longer life creates lead time bias. [National Cancer Institute: screening statistics](https://www.cancer.gov/about-cancer/screening/research/what-screening-statistics-mean).

### 3.2 Two hypothetical scenarios for the same person
{: #section-9 }

Suppose screening and subsequent management do not affect this person’s time of death:

| Scenario | Age at diagnosis | Age at death | Survival after diagnosis |
| --- | --- | --- | --- |
| No screening; diagnosis after symptoms | 66 | 70 | 4 years |
| Screening; earlier detection | 60 | 70 | 10 years |

```text
Age              60                       66                  70
No screening     Not diagnosed ─────────── Diagnosis ───────── Death
Screening        Diagnosis ────────────────────────────────── Death
                 Clock starts six years earlier               Same age at death
```

Recorded survival rises from four to ten years, but lifespan does not increase.

In a hypothetical population consisting entirely of people like this, five-year survival after diagnosis could even rise from 0% to 100% without anyone living longer.

### 3.3 Earlier diagnosis and actual life extension can coexist
{: #section-10 }

Understanding this problem does not require assuming that treatment is ineffective.

For two hypothetical scenarios for one person, denote diagnosis times without and with screening by $$C_0,C_1$$, and death times by $$D_0,D_1$$. Assume the disease would be diagnosed before death in both scenarios.

Here $$C$$ denotes diagnosis time, not censoring time as in some survival-analysis notes; $$D$$ denotes death time. Subscripts 0 and 1 identify no-screening and screening scenarios, not years 0 and 1. All four times must share a reference and unit, such as age in years or years since a common calendar origin. Subtracting two time points then gives a duration.

$$
\begin{aligned}
&\text{Postdiagnosis survival with screening}
-\text{Postdiagnosis survival without screening}\\
&=(D_1-C_1)-(D_0-C_0)\\
&=\underbrace{(D_1-D_0)}_{\text{Actual postponement of death}}
+\underbrace{(C_0-C_1)}_{\text{Advance in diagnosis}}.
\end{aligned}
$$

This is an algebraic decomposition, not an estimation model. $$D_1-C_1$$ is death minus diagnosis under screening; $$D_0-C_0$$ is the corresponding duration without screening. Rearranging their difference separates life extension from earlier diagnosis. In the preceding example, $$D_1=D_0=70$$, $$C_1=60$$, and $$C_0=66$$, so $$(70-60)-(70-66)=6$$ years: life extension is $$70-70=0$$, and diagnosis advances by $$66-60=6$$ years.

An observed increase in survival after diagnosis can therefore combine actual life extension and an earlier clock. The difference alone cannot separate them, and both sets of potential times cannot be observed for the same person.

### 3.4 The issue is not confined to cancer screening
{: #section-11 }

It can also arise when comparing early versus late treatment initiation.

For example, suppose:

- Both strategies are available at a common clinical decision point.
- Early treatment starts in year 0.
- Late treatment starts in year 2.
- The person dies in year 5 under either strategy.

Survival from treatment initiation is five versus three years. Survival from the common decision point is five years under both strategies. The former comparison alone cannot show that early treatment extends life.

### 3.5 Avoiding misinterpretation
{: #section-12 }

To assess whether screening reduces mortality, compare mortality risk over a prespecified horizon from a common baseline in the **entire population** randomized to screening or control, rather than comparing postdiagnosis survival only among those subsequently diagnosed. [NCI: screening and mortality outcomes](https://www.cancer.gov/types/lung/research/nlst-qa).

Similarly, evaluate early versus late treatment from the common point when patients are eligible and strategies can be chosen, counting outcomes during the waiting period.

<aside class="study-callout study-callout--note" markdown="1">

**Longer survival after diagnosis need not be a calculation error**

The descriptive number may be perfectly correct. The error is interpreting “lived longer after diagnosis” as “lived longer because of screening.”

Lead time bias does not establish that screening or early treatment has no value. It establishes that this survival comparison alone cannot demonstrate its value.

</aside>


<details class="study-callout" markdown="1">
<summary>Distinction from length-time bias</summary>

**Lead-time bias:** the same disease is detected earlier, advancing the starting point of the clock.

**Length-time bias:** screening preferentially detects slower-progressing disease with a longer detectable window, selecting cases that already tend to have a better prognosis.

The former concerns when timing starts; the latter concerns which cases are more likely to be found. [NCI: definitions of screening biases](https://www.cancer.gov/types/lung/research/nlst-qa).

</details>


## 4. Depletion-of-susceptibles bias
{: #section-13 }

### 4.1 Who are the “susceptibles”?
{: #section-14 }

Here susceptible does not specifically mean prone to infection. It means **more likely to experience the outcome under study**. Among people receiving the same drug, some may be more likely to bleed, experience a serious adverse reaction, or die.

These people may experience events, discontinue treatment, or leave earlier. Long-term users and later event-free risk sets then increasingly consist of relatively tolerant, lower-risk people.

**Depletion describes this compositional change; bias arises when it leads to an incorrect inference about treatment effects in the original population.**

### 4.2 How can prevalent users mislead us about new users?
{: #section-15 }

Suppose the question is: “What is the risk of a serious adverse event when starting B?”

The investigator instead includes only people who have already used B for a year and are still using it.

They have already undergone selection:

```text
Everyone who initially started B
    ├── Early adverse event, death, or resulting discontinuation
    │       → May be absent from the prevalent-user sample
    └── Still alive and continuing treatment
            → Included by the investigator
```

The latter group can have a lower risk than all initial users because the people being described have changed.

This is an important source of **prevalent-user bias**. Long-term users have already passed through the early treatment period and cannot directly represent new users. See [Ray, 2003](https://doi.org/10.1093/aje/kwg231) on new-user designs.

### 4.3 A numerical example: unchanged individual-type risks, declining overall risk
{: #section-16 }

To isolate the mechanism, suppose 1,000 people start the same drug and the outcome is the **first serious adverse event**:

| Type | Initial number | Monthly event probability, conditional on remaining event-free |
| --- | --- | --- |
| Highly susceptible | 200 | 50% |
| Less susceptible | 800 | 0% |

These probabilities are deliberately extreme. Each type’s conditional risk remains constant, and the counts below are expected counts under these assumptions.

**First month:**

- 100 highly susceptible people are expected to experience their first event.
- No less-susceptible people experience an event.
- The monthly event risk is $$100/1000=10\%$$.
- Among the 900 event-free people at month-end, only 100 highly susceptible people remain.

**Second month, among those 900 event-free people:**

- Another $$100\times50\%=50$$ events are expected among the remaining highly susceptible people.
- The conditional event risk for that month is $$50/900\approx5.6\%$$.

Overall monthly risk falls from 10% to 5.6%, but:

- The highly susceptible group’s risk is still 50%.
- The less-susceptible group’s risk is still 0%.
- Nobody has become more tolerant with longer use in this example.

What changes is the proportion of highly susceptible people in the risk set: from $$200/1000=20\%$$ to $$100/900\approx11.1\%$$.

$$
\text{Overall risk in the current period}
=\text{Highly susceptible proportion}\times50\%
+\text{Less susceptible proportion}\times0\%.
$$

Thus **population selection can lower overall risk without any reduction in an individual’s risk.**

<aside class="study-callout study-callout--important" markdown="1">

**Declining current risk does not mean declining cumulative risk**

By the end of two months, $$100+50=150$$ people have experienced an event, giving a cumulative risk of:

$$\frac{150}{1000}=15\%.$$

The 10% and 5.6% are monthly probabilities in two different risk sets; 15% is cumulative risk through month 2 in the original 1,000 people.

Leaving the first-event risk set after a first event is appropriate. It does not mean those people and their early events should be deleted from the entire study.

</aside>


### 4.4 How can it distort a comparison of two drugs?
{: #section-17 }

Suppose A and B have identical risks for the same types of people, but the comparison uses:

- B: people just starting treatment.
- A: people who have already used treatment for some time, remain event-free, and continue using it.

The B sample retains more people at high early risk; the A sample has already been selected. More events in B cannot directly establish that B is more dangerous.

The direction depends on which group is more strongly selected and who experiences events or leaves earlier. This bias does not invariably inflate or attenuate an effect.

### 4.5 How does this differ from developing tolerance?
{: #section-18 }

| Explanation | What changes? |
| --- | --- |
| Actual individual tolerance or biological change | The same person’s risk declines with duration of treatment |
| Depletion of susceptibles | Higher-risk people leave earlier, increasing the lower-risk share of the later population |

Both can occur together. A low event rate among long-term users alone cannot distinguish them.

### 4.6 How can it be avoided or reduced?
{: #section-19 }

When the target is the effect of **starting treatment**, an [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}) can help:

- Include initiators of the respective treatments in both groups, rather than new users in one and long-term users in the other.
- Align time since initiation and retain early events.
- Assess appropriate confounders using pretreatment information.
- Compare cumulative risks or survival curves over a fixed horizon for the original enrolled population, rather than only later event rates among those remaining.

These measures do not guarantee freedom from other biases. They chiefly reduce the mismatch between starting with selected users and asking about initiation effects. [Ray: new-user designs](https://doi.org/10.1093/aje/kwg231).

<details class="study-callout" markdown="1">
<summary>Do randomized trials or new-user designs eliminate the issue entirely?</summary>

No. Even after baseline randomization, some people experience events earlier. If treatment affects early events, susceptibility distributions among later survivors can differ between groups.

Let $$U$$ denote susceptibility and $$S_t=1$$ indicate being alive and event-free at time $$t$$. Baseline $$A\perp U$$ does not guarantee $$A\perp U\mid S_t=1$$.

Here $$A$$ is randomized baseline treatment assignment, $$U$$ is preexisting risk, and $$t$$ is a follow-up time measured from baseline. $$S_t$$ is a binary indicator of remaining event-free then, with 1 meaning still present. $$\perp$$ denotes statistical independence, and $$\mid S_t=1$$ restricts attention to people remaining. In words: independence of baseline treatment assignment and susceptibility need not persist among later survivors. $$S_t$$ is not $$S$$ multiplied by $$t$$, and selection does not necessarily create an association in every case.

A later hazard ratio compares the people in each group’s own remaining risk set. It should not be interpreted as the treatment effect for one shared set of survivors. A declining HR alone cannot distinguish a changing treatment effect from a changing risk set. [Hernán: The Hazards of Hazard Ratios](https://pmc.ncbi.nlm.nih.gov/articles/PMC3653612/).

This does not mean the HR was necessarily estimated incorrectly, or that depletion explains all changes over time. A population-level causal HR can be defined from the survival distributions of the same baseline population under two interventions, but these interpretive limits still apply. See [A Correctly Estimated Cox Model Can Still Be Misinterpreted]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}#section-13).

</details>


<details class="study-callout" markdown="1">
<summary>Is a study of long-term users necessarily wrong?</summary>

Studying these people can be appropriate when the question is whether people who have already tolerated treatment for a year should continue or stop. Define the starting point and comparison strategies for that new decision.

The estimand is the key. The effect of continuing among people who have tolerated a year of treatment cannot be directly generalized to the effect of starting among all new users.

</details>


## 5. Three investigators’ thought experiment: early versus late dialysis
{: #section-20 }

This section develops the example in [Fu’s 2023 supplementary material](https://cdn-links.lww.com/permalink/jsn/e/jsn_34_8_2023_07_28_fu_jasn-2023-000583_sdc1.pdf). The author imagines a **perfectly conducted randomized trial**: an infinite sample, no loss to follow-up, and everyone adhering to their assigned strategy whenever alive and able to receive treatment. The two dynamic strategies are summarized as:

- Early initiation: start dialysis when eGFR reaches the specified $$10$$–$$14\ \mathrm{mL/min/1.73m^2}$$ range.
- Late initiation: start dialysis when eGFR reaches the specified $$5$$–$$7\ \mathrm{mL/min/1.73m^2}$$ range.

eGFR, the estimated glomerular filtration rate, describes kidney function. These ranges only summarize the strategies. An actual protocol must specify measurement frequency, when within the range to initiate, what to do when a measurement skips the range, and baseline compatibility with each strategy. The figure alone cannot determine precise deviation or censoring times.

The correct causal question is: **from shared eligibility and randomization, what would mortality risk be if the target population followed early initiation rather than late initiation?** See the [causal contrast]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-17) in the CCW note.

Investigator 1 retains everyone randomized, follows them from randomization, and counts deaths before dialysis. The source assumes no mortality effect and sets the correctly analyzed early-versus-late HR to 1.0. Investigators 2 and 3 change the design and obtain HR = 1.5, illustrating design-induced bias.

These are assumptions of the thought experiment. In an actual study, an estimated HR of 1.0 alone cannot establish no effect at every time or in every person; uncertainty, modeling, and the full survival process also matter.

<aside class="study-callout study-callout--note" markdown="1">

**Direction of the HR**

The reported mortality HR is **early initiation divided by late initiation**. HR = 1.5 indicates a higher analyzed mortality hazard in the early group, apparently favoring late initiation. The source uses 1.5 to illustrate bias; it is not a fixed consequence of this class of error.

</aside>


### How to read the timeline
{: #section-21 }

![Depletion vs immortal time dialysis]({{ "/assets/causal-inference/depletion-vs-immortal-time-dialysis.png" | relative_url }})

The legend uses:

- $$E$$: satisfaction of all eligibility criteria specified by the analysis.
- $$A_S$$: the strategy label selected by the investigator using observed treatment history, rather than actual randomized assignment.
- $$T_0$$: time zero, the start of analytical follow-up.
- eGFR 10–20 at the left: the shared clinical stage when an early-versus-late strategy decision should be made.
- Upper branch, eGFR 10–14: earlier dialysis initiation; lower branch, eGFR 5–7: later initiation.
- Vertical lines and dialysis icons: actual dialysis initiation; tombstones: deaths recorded by the analysis.

Horizontal position indicates time moving to the right. Spacing is schematic; it does not provide waiting times in months or effect sizes.

<aside class="study-callout study-callout--important" markdown="1">

**What does $$T_0$$ always mean?**

$$T_0$$ always means **start of follow-up**. In this target trial, eligibility should be confirmed, strategy assigned, and outcome recording started then. **Actual dialysis may begin later**, because assignment concerns a rule for future threshold-based action.

A shared starting point means the same eligibility and decision rules in both groups, not the same calendar enrollment date for every patient. Panels A and B show what goes wrong when investigators place this starting point at different clinical positions.

</aside>


#### Panel A: why is within-branch alignment still wrong?
{: #section-22 }

The upper panel places each group’s $$E$$, $$A_S$$, and $$T_0$$ at actual dialysis initiation:

$$
T_{0,E}=T_{dialysis,E},\qquad
T_{0,L}=T_{dialysis,L}.
$$

$$T_{0,E}$$ and $$T_{0,L}$$ are the follow-up starts assigned to analyzed members of the two groups; $$T_{dialysis,E}$$ and $$T_{dialysis,L}$$ are their actual initiation times. “Dialysis” is a text label. The equalities describe the incorrect design, not a principle to follow. Equality within each group does not put early and late groups at the same clinical decision stage.

The early group therefore starts follow-up at eGFR 10–14; the late group starts only at eGFR 5–7. The three red symbols appear aligned **within each group**, but different disease stages have been chosen according to strategy. The issue is not whether two patients have identical date values: a comparison that should begin at a common strategy decision has become a comparison after each patient’s actual dialysis initiation. Subscripts $$E,L$$ here mean early and late, unlike the eligibility symbol $$E$$ above.

In investigator 2’s analysis, the lines from the shared eGFR 10–20 stage to dialysis are outside follow-up. People who die while waiting cannot reach the dialysis icon, satisfy final inclusion, or appear among the tombstone outcomes.

Late initiation entails longer waiting in this example. Higher-risk people are more likely to die before initiation, so those reaching late initiation undergo stronger survival selection. The late group already contains a smaller high-risk proportion at its own $$T_0$$: selection bias through depletion of susceptibles.

Starting the clocks at different disease stages also creates lead time bias: early initiators begin accumulating postdialysis survival earlier. Thus panel A emphasizes depletion of susceptibles while the text also describes lead time bias for investigator 2.

#### Panel B: why is a shared $$T_0$$ still wrong?
{: #section-23 }

The lower panel puts $$T_0$$ at the shared eGFR 10–20 stage, but the investigator waits until future dialysis initiation to determine $$E$$ and $$A_S$$:

$$
T_0<T_E,\qquad T_0<T_{A_S}.
$$

$$T_E$$ is when final inclusion requirements are satisfied in the incorrect analysis; $$T_{A_S}$$ is when future actual dialysis determines analytical group membership. The less-than signs indicate that follow-up starts earlier. Here $$E$$ means eligibility, not early as in the preceding equation. The formula describes misalignment, not a recommendation to select people after follow-up begins.

Follow-up has started, yet inclusion and early-versus-late group membership remain undetermined. The investigator must observe survival to dialysis and eGFR at initiation before retrospectively filling in the strategy label at $$T_0$$.

The lines from $$T_0$$ to dialysis now count as follow-up. But among ultimately included people, no tombstone can appear on those lines: a death there prevents dialysis, prevents acquisition of a future initiation label, and leads to exclusion.

This person-time is therefore guaranteed death-free by the inclusion definition: immortal time. The longer lower branch to eGFR 5–7 gives late initiators more guaranteed death-free time and artificially lowers their mortality hazard.

#### Where should the three symbols actually be placed?
{: #section-24 }

The correct target trial aligns the three operations at one decision point. With lowercase $$t$$ denoting the time of each operation:

$$
t_{\text{Eligibility assessment}}=t_{\text{Strategy assignment}}=T_0.
$$

This aligns **times**. Eligibility status $$E$$, strategy label $$A_S$$, and time $$T_0$$ are different kinds of variables and should not simply be equated. In a randomized trial, randomization determines strategy. In an observational emulation, $$A_S$$ represents analytical assignment based on records compatible at that time. Neither requires immediate dialysis at baseline.

Without actual randomization, the investigator can create early- and late-strategy copies for the same patient at a shared $$T_0$$, then censor and weight according to ongoing compatibility with observed treatment history. Future survival to dialysis does not become a baseline eligibility requirement, and predialysis deaths do not disappear for lack of an actual treatment group.

### 5.1 Comparing the three analyses step by step
{: #section-25 }

| Investigator | Start of follow-up | Who is included? | Group assignment | Deaths before dialysis | Main issue |
| --- | --- | --- | --- | --- | --- |
| Investigator 1 | Shared randomization time | Everyone randomized | Baseline random assignment | Counted in original assigned group | Correct trial analysis |
| Investigator 2 | Each person’s actual dialysis date | Only those who eventually initiate | eGFR at actual initiation | All deleted | Depletion of susceptibles and lead time |
| Investigator 3 | Shared randomization time | Only those who later survive to and initiate dialysis | Future initiation eGFR retrospectively determines group | All deleted, but included patients’ predialysis person-time retained | Immortal time bias |

Investigators 2 and 3 both require eventual initiation and delete predialysis deaths. Their key difference is that **investigator 2 also deletes waiting time and restarts the clock at dialysis; investigator 3 retains included patients’ waiting time from randomization to dialysis.**

### 5.2 Investigator 2: why does starting at dialysis change the question?
{: #section-26 }

The analysis can be summarized as:

> Study only people who successfully survive to dialysis, and compare subsequent mortality starting on each person’s dialysis date.

This is no longer the original trial question. The target was all eligible people at randomization. The analysis instead concerns two conditional populations selected by survival over different durations:

- Those surviving to initiation at higher eGFR.
- Those surviving longer, until initiation at lower eGFR.

The latter wait longer in this example, and higher-risk people are more likely to die while waiting. Thus even with identical prognoses at randomization, composition differs by each group’s dialysis date.

#### Error 1: deleting predialysis deaths depletes susceptible people
{: #section-27 }

Let $$U$$ denote underlying susceptibility that may not be fully measurable, such as severe comorbidity, frailty, or higher short-term mortality risk. Its distribution is the same in the early and late groups at randomization.

Suppose each group initially has 100 people: 40 high-risk and 60 low-risk. The following numbers illustrate selection only:

| By the respective dialysis time | High-risk deaths deleted by investigator 2 | People finally entering the analysis from dialysis | High-risk proportion among those included |
| --- | ---: | ---: | ---: |
| Earlier initiation | 5 | $$35+60=95$$ | $$35/95=36.8\%$$ |
| Later initiation | 20 | $$20+60=80$$ | $$20/80=25.0\%$$ |

The late group was not healthier initially. Longer waiting removed more people prone to death, leaving more robust survivors. This is **depletion of susceptibles**.

When observed again at dialysis:

- The early group still contains more high-risk patients because fewer have had time to be selected out before initiation.
- The late group contains only people better able to survive the longer wait.

Comparing their postdialysis mortality gives the late group an artificial prognostic advantage. The source describes selection bias; a collider diagram also expresses it:

<pre class="mermaid">flowchart LR
    Z[&quot;Z: randomized early/late strategy&quot;] --&gt; I[&quot;I: survives to and starts dialysis; included&quot;]
    U[&quot;U: baseline susceptibility to death&quot;] --&gt; I
    U --&gt; Y[&quot;Y: death after dialysis&quot;]</pre>

Randomization guarantees baseline $$Z\perp U$$. Investigator 2 conditions on $$I=1$$, including only people who survive to and initiate dialysis. Strategy determines how long survival is required, while $$U$$ also affects survival; $$I$$ is therefore a collider. Selecting on it can induce an association between $$Z$$ and $$U$$ among included people.

This explains why randomization does not protect the analysis: **it balances the initially assigned population, but does not guarantee balance in a future survivor subset influenced jointly by assignment and prognosis.**

##### Diagram: why can groups become unbalanced at dialysis without baseline confounding?
{: #section-28 }

![Confounding vs selection randomized dialysis]({{ "/assets/causal-inference/confounding-vs-selection-randomized-dialysis.png" | relative_url }})

The central $$R$$ marks actual randomization. To distinguish the time point from assignment, use $$Z$$ for randomized strategy. The left-hand bars show that at randomization:

$$
P(U=\text{High risk}\mid Z=\text{Early})
=P(U=\text{High risk}\mid Z=\text{Late})
=0.5.
$$

$$P$$ means probability, $$U$$ denotes baseline risk category, $$Z$$ denotes randomized group, and the vertical bar means within the specified assigned group. The denominator of 0.5 is everyone randomized to the respective group, and the numerator is its high-risk members. It means 50% are high-risk, not that mortality risk is 50%.

Randomization is known to be the assignment mechanism, so $$U$$ did not determine assignment. The equal 50% shares illustrate baseline comparability. Conversely, balance on one variable alone cannot establish no confounding in an observational study. If $$U$$ affects both actual treatment choice and death, a typical confounding structure is:

<pre class="mermaid">flowchart LR
    U[&quot;U: common cause&quot;] --&gt; A[&quot;A: receives early or late strategy&quot;]
    U --&gt; Y[&quot;Y: death&quot;]</pre>

That is $$A\leftarrow U\rightarrow Y$$: when treatment is chosen, $$U$$ already affects both choice and outcome. Randomization prevents $$U$$ from determining assignment $$Z$$, but does not necessarily prevent it from affecting actual treatment $$A$$. This thought experiment additionally assumes full adherence. See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}) for the distinction.

The diagram’s bias arises **after** randomization. Red skulls mark people who died before dialysis and were excluded by the incorrect analysis. The longer late-initiation branch entails more mortality selection, disproportionately affecting high-risk people. The right-hand bars therefore show that among survivors at their respective dialysis dates:

$$
P(U=\text{High risk}\mid Z=\text{Early},S=1)
\neq P(U=\text{High risk}\mid Z=\text{Late},S=1),
$$

where $$S=1$$ denotes surviving to and starting dialysis. The early group remains close to half high-risk, while the late group is dominated by low-risk survivors. The difference emerges through selection, not before randomization.

Adding $$S=1$$ changes the denominator from everyone originally assigned to those in that group who survived to and initiated dialysis. The comma imposes both group and inclusion conditions; $$\neq$$ means the proportions differ. $$S$$ plays the same role as inclusion indicator $$I$$ in the preceding diagram: 1 means included and 0 means not included.

The mechanisms differ as follows:

| | Confounding | Selection bias in this diagram |
| --- | --- | --- |
| When does noncomparability arise? | Already at treatment assignment | During postassignment survivor selection |
| Typical structure | $$A\leftarrow U\rightarrow Y$$ | $$Z\rightarrow S\leftarrow U\rightarrow Y$$, restricting to $$S=1$$ |
| Can randomization prevent it? | It prevents confounding of assignment $$Z$$; actual treatment $$A$$ may still depend on $$U$$ | No guarantee; later selection can recreate imbalance |
| Evidence in this example | Randomization is known; $$U$$ does not determine strategy assignment | Explicit later selection on survival to the respective dialysis dates creates group differences |
| Primary remedy | Randomization, or identification and appropriate control of common causes in observational studies | Retain the original population and align time zero; model selection or censoring where necessary |

A difference in high-risk proportions at dialysis is an **imbalance**, but the cross-sectional observation does not identify its cause. Ask when and how it arose. If risk affected initial treatment choice, consider confounding. If groups were initially balanced and restricting to survivors created imbalance, consider selection bias.

This is not a simple rule that baseline variables imply confounding and follow-up variables imply selection. Baseline inclusion can create selection bias, and confounding can vary over time. Distinguish **noncomparability caused by common causes from noncomparability caused by conditioning on a selected population**. Classification is clear here because randomization provides a known comparable starting point, followed by explicit conditioning on survival to dialysis.

#### Error 2: different disease-stage origins create lead time bias
{: #section-29 }

Investigator 2 also makes each patient’s dialysis date a new time zero. Early initiators have higher kidney function and begin the clock earlier; late initiators are further along the disease course and begin later.

To isolate timing, suppose the same patient dies 24 months after original randomization under both hypothetical strategies:

| Hypothetical strategy for the same patient | Dialysis starts | Death | Randomization to death | Investigator 2’s recorded postdialysis survival |
| --- | ---: | ---: | ---: | ---: |
| Early | Month 6 | Month 24 | 24 months | 18 months |
| Late | Month 18 | Month 24 | 24 months | 6 months |

Neither strategy changes this person’s death time, yet starting the clock at dialysis adds 12 months of postdialysis survival in the early-treatment world. Those months reflect an earlier clock, not postponed death. Calling them life extension is **lead time bias**. Both outcomes cannot be observed for one person; two different patients dying on the same date would not establish that early initiation is ineffective.

#### Why does investigator 2 nevertheless conclude that early initiation is harmful?
{: #section-30 }

The two biases act in opposite directions:

- Depletion selects healthier late-initiation survivors, favoring late initiation.
- Lead time lets early initiators accumulate postdialysis survival earlier, favoring early initiation.

The source’s HR = 1.5 indicates that the first mechanism dominates in its thought experiment. The net result appears harmful for early initiation. The final HR’s direction cannot establish that lead time is absent, and the two biases cannot be assumed to cancel.

### 5.3 Investigator 3: why does timing from randomization still create immortal time?
{: #section-31 }

Investigator 3 appears to fix time zero by starting follow-up at randomization, but adds two future requirements:

1. Patients must later survive to dialysis to enter the dataset.
2. Only after their eGFR at initiation is observed are they retrospectively classified as early or late initiators.

Analytical groups are therefore not determined from information available at baseline. For someone dying after randomization but before dialysis, actual initiation eGFR is never observed, and the investigator deletes the person.

#### What does “immortal” mean here?
{: #section-32 }

Among ultimately included people, no death can be recorded between randomization and initiation:

- Dying then would prevent future dialysis.
- Failure to initiate would violate investigator 3’s inclusion and grouping requirements.
- The person would therefore be excluded.

This is not biological immortality. **The analysis definition guarantees zero deaths in that period for everyone retained in the dataset.** This conditionally guaranteed event-free period is immortal time.

#### Why does the late group receive a larger artificial advantage?
{: #section-33 }

Late initiators must wait for eGFR to reach 5–7, generally longer than early initiators. More waiting person-time guaranteed death-free by inclusion is therefore counted for the late group.

For a minimal person-time example, suppose each ultimately selected group has 100 people, identical subsequent postdialysis follow-up of 100 person-years, and 10 deaths, but:

| Group | Included death-free waiting time | Postdialysis time | Deaths | Crude mortality rate |
| --- | ---: | ---: | ---: | ---: |
| Early | 50 person-years | 100 person-years | 10 | $$(10/150)\times100\approx6.7$$ per 100 person-years |
| Late | 200 person-years | 100 person-years | 10 | $$(10/300)\times100\approx3.3$$ per 100 person-years |

Postdialysis time and deaths are identical, but the late group has 150 extra person-years of guaranteed death-free time in its denominator. Its crude rate is half the early group’s, giving an early-versus-late crude rate ratio of 2. This illustrates denominator dilution only; it cannot yield a Cox HR, which also depends on event times and risk sets.

The source separately specifies HR = 1.5 to show how longer immortal time makes the late group’s mortality hazard appear lower. That number is neither derived from this invented table nor a fixed magnitude for this bias.

<aside class="study-callout study-callout--note" markdown="1">

**Is using future information always wrong?**

No. Here the problem is that future group membership requires event-free survival to treatment, pretreatment time is assigned to those future groups, and people who fail to survive are deleted. Some valid designs use future information, but require a matching target population, landmark, and estimand. Their results cannot be interpreted as strategy effects for everyone at original randomization.

</aside>


### 5.4 The key difference between investigators 2 and 3
{: #section-34 }

Focus on the waiting period between randomization and dialysis:

| | Deaths while waiting | Waiting person-time of ultimately included people | Resulting main issue |
| --- | --- | --- | --- |
| Investigator 2 | Deleted | Also deleted; clock starts at dialysis | Survivor selection/depletion, plus lead time from different disease stages |
| Investigator 3 | Deleted | Retained and assigned by future dialysis group | More guaranteed death-free time in the late group: immortal time |

It is therefore insufficient to ask whether predialysis deaths were deleted. Also ask: **does waiting person-time enter the analysis, when does it enter, to which group is it assigned, and was grouping determined at time zero?**

In the source’s alignment terminology:

- Investigator 2: strategies were assigned at randomization, but follow-up is postponed to dialysis: $$T_0>T_{assignment}$$.
- Investigator 3: follow-up begins at randomization, but analytical early/late classification awaits dialysis: $$T_0<T_{classification}$$.

“Assignment” refers to original strategy assignment; “classification” refers to grouping by future actual treatment. Their $$T$$ values are the corresponding times. $$>$$ and $$<$$ mean later and earlier. These compare timing; they do not calculate treatment effects.

### 5.5 Why cannot additional covariate adjustment fix these errors?
{: #section-35 }

These are primarily design errors:

- Deleted predialysis deaths are absent from the outcome data.
- Investigator 2 changes the target population and time origin.
- Investigator 3 includes time guaranteed by future survival in the risk sets.
- Selecting survival to dialysis may also induce collider bias involving unmeasured susceptibility.

Adjusting age, comorbidities, or eGFR at dialysis cannot restore deleted deaths or turn two disease stages into a shared time zero. Indiscriminately adjusting predialysis follow-up variables may also condition on postbaseline variables affected by strategy, creating additional problems.

### 5.6 How does target trial emulation address this?
{: #section-36 }

The correct design aligns enrollment under common eligibility rules, strategy assignment, and follow-up at each patient’s corresponding time zero. It cannot wait for a group to survive to future treatment and then treat those survivors as the original enrolled population.

With observational data, [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) can be used:

1. At shared time zero, create copies for the early and late strategies compatible with each eligible patient.
2. Count deaths from that day, rather than from dialysis.
3. Artificially censor a copy only when observed treatment history first deviates from its strategy.
4. Appropriately weight for this potentially informative artificial censoring.

If a patient dies before reaching either initiation threshold and their prior history remains compatible with both strategies, count the death in both still-compatible copies. Do not delete it because the patient could not complete a future action.

See [Fu’s 2023 supplement, pp. 2–3](https://cdn-links.lww.com/permalink/jsn/e/jsn_34_8_2023_07_28_fu_jasn-2023-000583_sdc1.pdf) for the three-investigator thought experiment. The corresponding registry study shows that the two conventional incorrect analyses can produce early-versus-late HRs around 1.5, whereas target-trial-aligned results are close to the randomized IDEAL trial. [Main article and comparison table](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).

Agreement can support a design’s credibility, but cannot establish that an observational estimate is unbiased or that the studies target identical effects. Assignment effects in randomized trials and sustained-adherence effects in observational studies still need to be distinguished. See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).

## 6. Separating timing problems from population problems
{: #section-37 }

Ask these questions in sequence:

1. **Does group membership depend on the future?** If membership requires surviving to an event and that time is mishandled, consider immortal time bias.
2. **Do both groups use the same clinical definition of baseline?** If an earlier starting point is interpreted as life extension, consider lead time bias.
3. **Have the people now observed already passed through survival or tolerance selection?** If they are treated as the original population, consider depletion of susceptibles.
4. **Whose effect, starting when, is the target?** This defines the reference for calling something bias and cannot be omitted.

Additional covariates alone do not resolve these problems. Missing early deaths, future-dependent grouping, and inconsistent time origins must first be addressed through design and the estimand.

## 7. Self-check
{: #section-38 }

1. A study classifies people who collect at least three prescriptions during follow-up as treated from their first prescription. Why should this raise concern about immortal time bias?
2. Screening advances diagnosis by four years and actually postpones death by one year. How much longer is survival after diagnosis?
3. Does a low adverse-event rate among long-term users establish that longer use makes the same person safer?
4. In §4.3, second-month risk falls to 5.6%. What is cumulative risk over the two months?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. Receiving the third prescription requires surviving until then; early deaths cannot meet that definition. Retrospectively determining baseline groups from future prescriptions and mishandling risk time can induce bias.
2. Five years: four from earlier diagnosis and one from delayed death.
3. No. Higher-risk people may already have experienced events or stopped treatment, leaving more tolerant people.
4. 15%; cumulative risk retains the original population and the events already experienced.

</details>
