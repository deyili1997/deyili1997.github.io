---
layout: "causal-note"
title: "Active-Comparator New-User Design"
description: "Choose comparable treatment initiators, align baseline, and understand how prevalent-user selection can distort comparisons."
group: "Trial design"
order: 16
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Why does the name have two parts?", "anchor": "section-1"}, {"title": "2. A complete teaching example", "anchor": "section-5"}, {"title": "3. What happens after stopping or switching?", "anchor": "section-7"}, {"title": "4. Common misconceptions", "anchor": "section-10"}, {"title": "5. Relationship to the other two designs", "anchor": "section-11"}, {"title": "Companion to the original text: Eligibility and treatment history", "anchor": "section-12"}, {"title": "Sources", "anchor": "section-24"}]
previous_note: "/causal-inference/target-trial-designs/"
next_note: "/causal-inference/sequential-trials/"
---

Study entry point: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**The idea in one sentence**

**Compare people just starting treatment A with people just starting a reasonable alternative B, and begin follow-up when each initiates treatment.**

An active comparator brings the comparison closer to one clinical choice; new users ensure both groups enter at treatment initiation.

</aside>


**ACNU (active-comparator new-user design)** primarily improves the choice of comparison groups and enrollment time; it does not itself eliminate confounding.

<aside class="study-callout study-callout--tip" markdown="1">

**First reading**

Read §1–§3 first: distinguish active comparator from new user, practice eligibility, grouping, and baseline with the five patients in §2, then decide what happens after discontinuation. Once you can explain those steps, continue to [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}). On a second reading, use §4 to check your understanding, then read the “companion to the original text” on post-treatment selection and the hormone therapy history example.

</aside>


Prerequisite: the start of follow-up in [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}). Design overview: [Comparing Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}).


A worked multivariable example: [Complete multivariable LR-IPTW example comparing drug A with drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) shows how baseline characteristics for 3,000 people enter one shared LR model to produce propensity scores, weights for both groups, balance diagnostics, and one-year risks. Z=0 denotes drug B, rather than no treatment.

## 1. Why does the name have two parts?
{: #section-1 }

### Active comparator: An active treatment control
{: #section-2 }

“Active” means that controls receive another actual treatment, rather than placebo or no treatment. For example, A and B treat the same disease at similar treatment stages and are reasonable clinical alternatives.

Suppose we want to study an antihypertensive treatment. Directly comparing people who start treatment with those who do not may encounter:

- More severe disease among users, giving them higher outcome risk beforehand;
- Milder disease among nonusers, or nonuse due to frailty, contraindications, or other reasons;
- Different opportunities to seek care and receive monitoring.

These differences make treated-group outcomes reflect both treatment effects and prior disease. **Confounding by indication** is one mechanism: the condition prompting treatment also affects the outcome. Choosing treatment B for a similar indication generally more closely reflects “which treatment should be chosen?” than selecting all untreated people.

**An active comparator does not guarantee no confounding.** Physicians may still choose A or B based on disease, contraindications, and other factors, so appropriate baseline confounding adjustment and examination of treatment-choice overlap remain necessary.

Methodological source: [Active-comparator design and new-user design in observational studies](https://pubmed.ncbi.nlm.nih.gov/25800216/).

### New user: A person starting treatment
{: #section-3 }

Both groups enter when initiating their respective treatments, avoiding a direct comparison of “people just starting A” with “people who have used and tolerated B for years.”

The latter have already passed through early risk; people who experienced early events or could not tolerate treatment may be absent from a current-user cohort. This connects to [Depletion of Susceptibles and Prevalent-User Bias]({{ "/causal-inference/time-related-biases/" | relative_url }}#section-15).

A new-user design also allows:

- Observation of events soon after treatment begins;
- Measurement of confounders before treatment where possible, avoiding treatment-affected measurements as baseline variables;
- Alignment of initiation and the start of follow-up.

Eligibility should be determined at initiation, without waiting to learn whether someone later survives, tolerates, or persists with treatment before selecting them. The companion at the end explains this in detail. New-user designs do not eliminate all selection bias.

Methodological source: [Lund et al.: Historical foundations and implementation of ACNU](https://pmc.ncbi.nlm.nih.gov/articles/PMC4778958/).

### Initiators: Who exactly are they?
{: #section-4 }

**To initiate means to begin; initiators are people who begin a treatment or strategy.** In medication studies, they are often called “treatment initiators” or “new users.” This describes what they do at baseline, not their subsequent persistence.

| Situation at baseline | Interpretation |
| --- | --- |
| No use during the specified prior period; starts A now | May meet the study definition of an A initiator |
| Has used A continuously for two years; now enters a database study | A prevalent user, not a new A initiator merely because enrollment occurs now |
| Starts A at baseline; stops two months later | Still an initial initiator; subsequent analysis depends on whether the target is initiation or a sustained strategy |
| Eligible but does not start A now | A noninitiator at this decision point; future treatment cannot retrospectively redefine baseline status |

“New” is defined by the study's specified prior treatment history and observation window, not necessarily first-ever use; see the washout period in §2.

In Hernán and Robins' hormone example, **initiators of different treatment strategies** is broader than “new medication users”: starting combined hormones at baseline makes a record compatible with the treatment strategy, while not starting makes it compatible with the initial requirements of the nonuse strategy. Comparing strategy initiators therefore does not necessarily mean both groups take a drug.

But not starting at baseline establishes only compatibility then, **not that the woman will avoid medication for five years**. Initiation analyses and sustained-strategy PP handle subsequent initiation differently; see §3. The original text explicitly codes eligible women who do not start hormones as initiating the first strategy. [Hernán and Robins (2016), Treatment strategies](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf)

Evidence of “starting” may also be a prescription, dispensing, or actual administration record; distinguish them. See [Prescribing, Dispensing, and Actual Use: Why Do the Groups Differ?]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-23).

## 2. A complete teaching example
{: #section-5 }

Suppose the question is **the effect on one-year mortality risk of starting A rather than B** among patients with the same disease for whom both drugs are appropriate. A and B are placeholders, not specific clinical recommendations.

| Design element | Teaching specification |
| --- | --- |
| Eligibility | Meets diagnostic and other baseline criteria on initiation day; sufficient observation during the prior 12 months, with no A or B use |
| A group | Starts A now |
| B group | Starts B now |
| Time zero | Each person's A or B initiation date |
| Baseline variables | Appropriate confounders such as age, disease, and comorbidities from pre-initiation records |
| Outcome | Death within one year from time zero |
| Initial comparison | Compare one-year mortality risks after handling baseline confounding, loss to follow-up, and other issues |

The stipulated “12 months without use” is a **washout period (observed nonuse window)**. In observational data it is a historical window for identifying new users, not an instruction to make patients stop medication.

Its length depends on the drug, data coverage, and research question. Without lifetime records, “no recent use” does not mean “never used.”

Also specify whether database “initiation” means prescribing, pharmacy dispensing or pickup, or recorded administration. These are different events. For example, a pickup record may define initiation operationally but does not prove ingestion that day. Both groups should use consistent definitions aligned with the target question.

<pre class="mermaid">flowchart LR
    H[&quot;Before initiation: Confirm eligibility, treatment history, and confounders&quot;] --&gt; A[&quot;Start A: time zero&quot;]
    H --&gt; B[&quot;Start B: time zero&quot;]
    A --&gt; YA[&quot;Count outcomes after initiation&quot;]
    B --&gt; YB[&quot;Count outcomes after initiation&quot;]</pre>

The baselines align clinically without having to fall on the same calendar date. Calendar time still requires design or analytical attention if it affects treatment and outcomes.

### Applying the rules to five patients
{: #section-6 }

All patients below meet diagnostic and other clinical conditions; only treatment history, observable records, and later events differ. To avoid conflating three forms of “initiation,” this example uniformly uses **the first eligible pharmacy dispensing record**.

In the table, $$T_0$$ is this study's start of follow-up; 0 marks baseline, not a treatment-group code or event count.

| Patient record | Eligible to enter now? | Why this group and baseline? |
| --- | --- | --- |
| Patient 1: Observed without A or B use for the preceding 12 months; first A dispensing on March 1 | Yes | A group; $$T_0$$ is March 1 |
| Patient 2: Same prior conditions; first B dispensing on April 1 | Yes | B group; $$T_0$$ is April 1, aligned clinically with Patient 1 |
| Patient 3: Continuous A use for eight months; another A dispensing today | Cannot enter as a new user today | Today is continuation; to study original initiation, check eligibility at that earlier time |
| Patient 4: Eligible first A dispensing on June 1; stops in July for a nonpermitted reason | Yes | Remains an A initiator on June 1; later stopping cannot erase initial enrollment; see §3 |
| Patient 5: First observed B dispensing today, but only two months of reliable prior records | Available data alone cannot confirm eligibility in this example | “No visible use” does not mean “confirmed no use for 12 months”; obtain more data or transparently modify the rules |

Investigators may search dispensing dates first and then examine history. Alignment depends on information's position relative to $$T_0$$, not the order of computer queries; see [Are We Looking at Future Treatment Before Choosing Participants? Distinguish Two Types of Time]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-4).

After including Patients 1 and 2, their outcome difference cannot directly be called a treatment effect. Their ages and disease may still differ. New users and an active comparator first improve **who is compared and when the comparison begins**; appropriate confounding adjustment and outcome analysis for the target population remain necessary.

## 3. What happens after stopping or switching?
{: #section-7 }

A design name does not choose the target effect for you. Specify subsequent strategies first.

For the distinction between follow-up endpoints and censoring, see [The Start, End, and Censoring of Follow-up]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-10).

### Question one: Start A versus B, then follow usual care
{: #section-8 }

Continue follow-up according to the initially started medication even if the patient later stops or switches.

This can target a **treatment initiation effect**. Some publications call it an observational analog of ITT, but actual initiation rather than randomized assignment defines the initial groups, so confounding still needs attention. Retaining subsequent group membership is the follow-up rule for this initiation question; it does not automatically confer randomization protection.

If the protocol specifies only baseline initiation, the initiation effect may also be called the **per-protocol (PP) effect** of that baseline intervention. Here adherence requires only the specified initial action, not sustained use. See [The ITT Terminology Problem in Observational Studies]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}#section-12).

### Question two: After initiation, continue A or B according to protocol
{: #section-9 }

This targets sustained-strategy PP. One approach uses **artificial censoring** at the first deviation: retain earlier compatible follow-up, but stop letting subsequent actual records directly represent outcomes under continued adherence. Then address censoring-induced selection appropriately, for example with [inverse probability of censoring weighting]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}).

**Deleting people who stop or switch does not automatically yield a valid PP estimate.** Stopping may relate to disease, side effects, and prognosis; permitted stopping rules must also be prespecified.

See [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}) and [Artificial Censoring and Weighting]({{ "/causal-inference/clone-censor-weight/" | relative_url }}#section-9). In standard ACNU, actual A versus B initiation already distinguishes baseline groups. Sustained-strategy analysis can handle later deviations directly; using censoring weights does not require additionally cloning everyone.

## 4. Common misconceptions
{: #section-10 }

| Statement | How to interpret it |
| --- | --- |
| Any other drug works as a comparator | It must be a reasonable alternative at a similar clinical decision; very different indications can leave severe confounding |
| Both groups are new users, so no adjustment is needed | Initiating A or B is still not random |
| No record in the past year guarantees first use | It may be reinitiation or incomplete records |
| Require six months of future continuous use, then start follow-up at the first dose | Future adherence and survival select the population, potentially creating immortal time and selection bias |
| Censor every switch to estimate PP | Reasons for censoring and their relationship with outcomes also matter |
| Research is impossible without an active comparator | Other strategies such as noninitiation can be defined; [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}) is one common option |

## 5. Relationship to the other two designs
{: #section-11 }

- **ACNU** focuses on who is compared and how both groups enter at similar treatment starting points.
- **CCW** handles a baseline treatment history compatible with multiple strategies and subsequent deviations.
- **Sequential trials** use multiple eligible decision times.

They can be combined—for example, compare new A and B initiation at several calendar times, then censor and weight deviations from sustained-treatment protocols.

## Companion to the original text: Eligibility and treatment history
{: #section-12 }

Return now to Hernán and Robins (2016). The central question is: **To estimate an initiation effect, why can we not first observe two years of treatment and then decide who is eligible?**

### Interpreting the passage: Why does comparing initiators reduce post-treatment eligibility selection?
{: #section-13 }

The original sentence can be rendered as:

> Comparing people who are just beginning the treatment strategies of interest—sometimes called a new-user design—is a simple way to avoid a particular selection bias. This bias arises when eligibility is defined using states after initiation, and only eligible people are selected, even though the strategies themselves may already have affected those states.

Here **initiators** are people beginning the relevant strategy; **prevalent users** have already used treatment for some time. The key is whether treatment initiation and study entry coincide. [Hernán and Robins (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).

#### Treatment changes who can still meet the rules, rather than the wording of the rules
{: #section-14 }

Suppose eligibility requires “still alive, no specified adverse event, still using the drug, and adequate kidney function.” These may look like descriptions of study participants, but if assessed two years after initiation, treatment may already have affected them.

| Same condition | Assessed before the treatment of interest starts | Assessed after two years of treatment |
| --- | --- | --- |
| Adequate kidney function | Defines the population appropriate for studying initiation | May exclude people whose kidney function worsened after treatment |
| No adverse event of interest yet | Excludes prior-event history and defines the target population | May also exclude early events after treatment |
| Still alive and using treatment | At initiation, future survival and persistence cannot be required | Retains only people who survive and remain treated until then |

The key question is therefore not merely “are eligibility criteria explicit?” but **does eligibility information precede the study strategy, or is it already a consequence of receiving it?**

#### A constructed example: Who is lost when treatment precedes selection?
{: #section-15 }

The target question is: among people all eligible now, **does starting A or starting B cause more adverse events?**

Instead, investigators include only people who “have used A or B for two years, still use it, and have not yet had the event,” then compare later outcomes.

Suppose A causes adverse reactions in some susceptible people during the first months. They may stop because of the reaction or become ineligible because the event has occurred. When investigators seek current users two years later, those people do not enter A's group. Remaining A users may be relatively tolerant of A.

**Better outcomes among people still using A two years later do not prove that initially starting A is safer.** Early events are omitted and the groups may have undergone different selection; bias direction depends on the mechanism.

Enrollment at A or B initiation captures early events without omitting patients at entry because they later stop. See §3 for use of post-discontinuation records.

#### An easily missed distinction: Before study baseline does not necessarily mean before treatment
{: #section-16 }

```text
Start A in 2020 ── Receive treatment for two years ── Enter the study in 2022 and measure “baseline kidney function”
```

Although labeled “baseline,” kidney function may already be affected by the previous two years of A. **Naming a measurement time baseline does not turn a post-treatment variable into a pretreatment one.**

If the target remains “the effect of initial A initiation in 2020,” selecting or adjusting on 2022 kidney function is not equivalent to controlling pre-initiation confounding. It may condition on a post-treatment intermediate, changing the estimated effect or introducing bias; assessment depends on the causal structure.

This is also why [Ray (2003)](https://pubmed.ncbi.nlm.nih.gov/14585769/) emphasizes observation from treatment initiation and pretreatment covariate measurement.

<details class="study-callout" markdown="1">
<summary>Advanced: Which selection path might open?</summary>

Let $$A$$ be treatment initiated earlier, $$U$$ individual susceptibility, $$S=1$$ continued eligibility two years later, and $$Y$$ the subsequent outcome. One possible structure is $$A \rightarrow S \leftarrow U \rightarrow Y$$. Both treatment and susceptibility affect sample entry; restricting to $$S=1$$ can induce an association between treatment and susceptibility, biasing subsequent outcome comparisons. Even initial randomized A can lose its comparability through post-treatment selection. This is one illustrative selection structure, not a claim that every prevalent-user study has the same DAG.

</details>


#### What does this statement not promise?
{: #section-17 }

1. **New-user design is not randomization.** Disease may still determine A versus B initiation, so baseline confounding requires handling; loss to follow-up, measurement error, and other issues do not automatically disappear.
2. **New-user does not necessarily require an active comparator.** The sentence emphasizes comparison from strategy initiation. “Start A today” versus “do not start A today” can also be studied with comparable decision points; “not today” does not mean “never.” See [Sequential Trial Design]({{ "/causal-inference/sequential-trials/" | relative_url }}).
3. **An initiation study cannot retain only new users who will complete six months of treatment.** That again selects on future adherence and survival; a sustained six-month question needs its own strategy and deviation handling, as in §3.
4. **Prevalent users can be studied.** If the question is “among people who have already used and tolerated A for two years, continue or stop now?”, two years of treatment history can be a baseline condition for this new decision. The target is continuation versus stopping, not original initiation.
5. **Not all post-treatment selection is immortal time bias.** If follow-up starts two years later, the main problem may be survivor selection and omitted early events. If the previous two years that must be survived for group eligibility are also incorrectly counted as that group's follow-up, [immortal time bias]({{ "/causal-inference/time-related-biases/" | relative_url }}) may arise.

Remember the design principle: **To answer an initiation question, determine eligibility, form the comparison, and begin follow-up at initiation where possible, rather than letting treatment first select a surviving group.** More complex strategies with initiation grace periods require protocol-specific time-zero choices; not everyone's actual first-use date should mechanically become baseline.

### Reading the whole passage: Hormone therapy, depletion of susceptibles, and history that cannot be randomized
{: #section-18 }

The authors next use “estrogen plus progestin and coronary heart disease” to show how this selection can affect actual research.

#### The passage's overall logic
{: #section-19 }

```text
Some women start estrogen plus progestin
          ↓
Treatment increases early coronary heart disease risk
          ↓
Some susceptible women experience early events, die, or stop use
          ↓
Months or years later, only still-treated eligible women are enrolled
          ↓
Susceptible women may form a smaller share of prevalent users, and early events may be omitted
          ↓
Comparing subsequent outcomes with never users may fail to identify the early risk of initiation
```

This chain describes a possible mechanism. In a first-coronary-event study, pre-enrollment events violate eligibility requiring no prior event; if current use is required, former users also cannot enter the prevalent-user group.

**Susceptible women** are more likely to experience the relevant outcome or early adverse treatment effects. **Depleted** means a relative reduction of such women among later selected current users, not that treatment made all of them “less susceptible.” Never users also undergo selection through aging, disease, and death; the point is that the groups have not experienced the same treatment and consequences.

#### How far should the historical example be interpreted?
{: #section-20 }

The authors discuss estrogen plus progestin and coronary heart disease in a specific context, not identical risks across all hormone formulations, routes, and populations. In WHI-related comparisons, increased coronary risk with combined hormones was more pronounced early. Hernán and colleagues later emulated initiation-versus-noninitiation trials with Nurses' Health Study data; their results show how aligning observational design and follow-up with trials helps explain differences between earlier estimates. [Hernán et al. (2008), original reanalysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC3731075/).

The original uses **may have contributed** and **might have been**; retain those qualifications. Depletion of susceptibles is one emphasized explanation, not a proven sole cause of historical discrepancies. Confounding, age at initiation, time since menopause, treatment duration, and other factors may also affect comparisons.

#### Why can “current users versus never users” not directly represent a randomized trial?
{: #section-21 }

A randomized trial assigns strategies going forward from a common decision point; it cannot randomize history that has already occurred. The authors criticize forming groups by existing treatment histories, then using later comparisons to answer an initial-initiation question.

Suppose study baseline is 2022:

| Group observed in 2022 | Pre-enrollment information included | Can this history be randomized in 2022? |
| --- | --- | --- |
| Has used treatment for two years and still uses it | Prior initiation plus two years of survival, tolerability, and adherence | No; today cannot assign “already used for two years and survived until now” |
| Never used treatment so far | No past use of that treatment | A person with prior use cannot be randomly turned into a never user |

Thus, **current user and never user describe existing history; those labels alone do not define a strategy contrast assignable at the current baseline.** “Never used” also does not automatically specify whether future initiation is allowed.

Moving randomization back to 2020 permits assignment to initiation or noninitiation with follow-up then. It still does not permit only two-year survivors who remain event-free and treated to represent the original treatment group.

#### Two clearly definable target trials
{: #section-22 }

| Target question | Who enters at baseline? | Strategies compared from baseline |
| --- | --- | --- |
| Effect of initiation | Eligible people currently not using treatment | Initiate now or do not initiate now; specify subsequent rules separately |
| Effect of continuation | Eligible people currently using treatment | Continue or stop; specify subsequent rules separately |

The stopping group in the second trial still has prior treatment history, so its members are discontinuers, not never users. The populations, interventions, and causal questions differ. “Current users versus never users” cannot replace either explicit protocol.

In the subsequent **Assignment procedures** section, the original paper explicitly proposes the latter continuation-versus-stopping “reversed target trial.” The authors therefore do not reject studies of prevalent users; the key is redefining population, strategies, and follow-up around the current decision. [Hernán and Robins (2016), page 760](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf).

Define [the treatment contrast and target effect]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}) before choosing matching, weighting, or other methods.

#### A note on the original text: Common treatment histories and g-estimation
{: #section-23 }

The authors then explain that the original trial compares initiation versus noninitiation among baseline nonusers, while the reversed trial compares continuation versus stopping among baseline users. Both compare the next action against a common prior treatment background. This captures a design intuition behind g-estimation.

“Common history” does not mean identical disease in everyone, and creating these groups does not complete g-estimation. The latter also requires a structural model for the causal effect and use of the treatment-choice mechanism to solve for effect parameters. See [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}) for the explanation and hand calculations.

## Sources
{: #section-24 }

- [Hernán MA, Robins JM. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).
- [Ray WA. Evaluating medication effects outside of clinical trials: new-user designs (2003)](https://pubmed.ncbi.nlm.nih.gov/14585769/).
- [Hernán MA et al. Observational studies analyzed like randomized experiments: an application to postmenopausal hormone therapy and coronary heart disease (2008)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3731075/).
- [Lund JL, Richardson DB, Stürmer T. The active comparator, new user study design in pharmacoepidemiology: historical foundations and contemporary application (2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4778958/).
- [Active-comparator design and new-user design in observational studies (2015)](https://pubmed.ncbi.nlm.nih.gov/25800216/).
- [Fu EL. Target Trial Emulation to Improve Causal Inference from Observational Data: What, Why, and How? (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/).

Examples are teaching scenarios, not efficacy conclusions about specific drugs.
