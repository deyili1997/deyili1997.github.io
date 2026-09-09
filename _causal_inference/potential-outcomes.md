---
layout: "causal-note"
title: "Potential Outcomes and Identification Assumptions"
description: "Understand treatment effects, counterfactual outcomes, exchangeability, positivity, consistency, and standardization through worked examples."
group: "Foundations"
order: 1
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "Read this first: What is a treatment effect?", "anchor": "section-1"}, {"title": "1. Getting to know the notation: Observed and potential outcomes", "anchor": "section-7"}, {"title": "2. Why is causal inference difficult?", "anchor": "section-9"}, {"title": "3. An example: Why might a difference between groups fail to represent a treatment effect?", "anchor": "section-13"}, {"title": "4. Four assumptions: Why can this comparison receive a causal interpretation?", "anchor": "section-17"}, {"title": "5. The adjustment formula: Stratify first, then average over the target population", "anchor": "section-23"}, {"title": "6. A step-by-step derivation: How does counterfactual notation disappear?", "anchor": "section-26"}, {"title": "7. Advanced distinctions: Return on a second reading", "anchor": "section-31"}, {"title": "8. What should you study next?", "anchor": "section-36"}, {"title": "9. Five questions to check your understanding", "anchor": "section-40"}]
previous_note: "/causal-inference/"
next_note: "/causal-inference/reading-causal-formulas/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

When you encounter unfamiliar notation, read alongside [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}). This note also explains how to read each formula nearby; no prior course in probability is required.

<aside class="study-callout study-callout--abstract" markdown="1">

**Start with one question**

**For the same target population, how would the average outcome differ if everyone received one treatment rather than everyone receiving another?**

This is a causal question. In reality, we can observe only the treatment each person actually receives and the resulting outcome. Causal inference asks under what conditions these observed data can answer that “what if” question.

</aside>


<aside class="study-callout study-callout--tip" markdown="1">

**How to read this the first time**

Follow the sequence “two futures for one person → population averages → confounding → identification assumptions.” The blood-pressure example below builds intuition; **§1–§3** express it in notation and extend it to a population; **§4–§5** explain the conditions under which estimation is possible. **The derivation in §6 and advanced distinctions in §7** can wait until a second reading.

</aside>


## Read this first: What is a treatment effect?
{: #section-1 }

**A treatment effect is the difference in the outcome that would result from choosing one treatment strategy rather than another for the same person or the same target population.** It can represent benefit, harm, or no difference; the word “effect” does not itself mean that a treatment necessarily works.

Begin with “medication versus no medication,” without memorizing notation. All numbers below are invented for teaching and do not describe the effectiveness of a real drug.

### The same person, at the same future time, in two possible scenarios
{: #section-2 }

Suppose Li's systolic blood pressure today is **150 mmHg**. Starting from this same point today, imagine his situation one year later:

mmHg means millimeters of mercury; it is the unit for both blood-pressure values and differences here.

| Possible scenario | Blood pressure after one year |
| --- | ---: |
| Start the specified treatment strategy today | 130 mmHg |
| Do not start that treatment strategy today | 145 mmHg |

For now, interpret the strategies as “initiate today, then continue under usual care” and “do not initiate today, then continue under usual care.” In this thought experiment, we specify both potential outcomes so that the comparison is clear; in reality, the same Li can experience only one scenario.

Taking “treatment minus no treatment,” Li's treatment effect is:

$$
130-145=-15\text{ mmHg}.
$$

This means: **in this scenario, treatment lowers Li's blood pressure at one year by 15 mmHg compared with no treatment.** We compare the same future time in two scenarios, rather than two different people.

### Why not subtract the pretreatment value of 150 from 130?
{: #section-3 }

The actual before-and-after change is:

$$
130-150=-20\text{ mmHg}.
$$

But in this scenario, even without treatment, Li's blood pressure would fall from 150 to 145 over the year. We therefore cannot attribute the entire observed 20 mmHg reduction to treatment.

| Number | What question does it answer? |
| --- | --- |
| A before-and-after reduction of 20 | How much did Li's blood pressure change in total over the year after treatment? |
| A treatment effect of −15 | How much additional change did treatment cause compared with the same Li's outcome at one year without treatment? |

This example does not specify why blood pressure falls by 5 without treatment initiation. It illustrates that **blood pressure may change over time even without starting treatment; the outcome at one year under no treatment cannot simply be assumed to equal today's baseline value.**

### Why do real studies usually examine average treatment effects?
{: #section-4 }

If Li actually receives treatment, we may observe 130, but we cannot observe his blood pressure at one year if he had not received treatment from the same starting point. The 145 in the table is another potential outcome specified for teaching; it is not a number that can be read directly from his medical record.

Finding another person, Wang, whose blood pressure is 145 without treatment does not establish that “Wang's outcome is Li's outcome without treatment.” Their initial severity, ages, and future trajectories may differ.

Actual research therefore often shifts to a population: compare the average outcome **if everyone in the same target population were treated** with the average outcome **if everyone were untreated**. We still compare two intervention scenarios, but replace “one person's difference” with “the population's average difference.” With an appropriate study design and identification assumptions, we can estimate this using different people's observed records without knowing each person's missing potential outcome. See §2.2 for the formal definition.

### Controlling confounding does not remove the treatment's effect
{: #section-5 }

Suppose people with more severe illness are more likely to receive treatment and would also tend to have higher blood pressure at one year even without treatment. The difference between the actual treated and untreated groups may then mix treatment differences with preexisting differences in severity and prognosis.

**The goal of confounding control is to avoid mistaking these preexisting differences for differences caused by treatment.** It does not require the two groups to have identical outcomes after treatment. If treatment has a causal effect, average posttreatment blood pressure can still differ after appropriate confounding control.

For example, after appropriate adjustment, we want the actual treated and untreated groups to have comparable average outcomes **if neither group were treated**. In reality, however, one group is treated and the other is not, so treatment can still make their observed means differ. §4.1 expresses this “comparability under the same treatment” as the exchangeability assumption.

### Returning to g-estimation: What does “subtracting the effect” mean?
{: #section-6 }

<details class="study-callout" markdown="1">
<summary>A preview of the method: Skip this on a first reading and expand it after learning exchangeability</summary>

Continuing Li's thought experiment, treatment lowers blood pressure at one year by 15. To remove this negative effect algebraically, add 15 back:

$$
130-(-15)=145.
$$

In a real analysis, we do not know how much to add back, so we try candidate values based on an effect model. This mathematical operation is called “subtracting a candidate effect”: it changes the numbers used in the calculation, without changing the treatment the patient actually received or the blood-pressure record in the chart.

G-estimation uses conditional mean relationships across the entire sample, given medical history, to find a parameter; **it does not thereby recover every individual's true untreated outcome**. Continue with population comparisons and exchangeability here, then see [A step-by-step explanation of H(ψ)]({{ "/causal-inference/g-estimation/" | relative_url }}#section-3) for how this intuition becomes a calculation.

</details>


## 1. Getting to know the notation: Observed and potential outcomes
{: #section-7 }

This note focuses on the simplest setting: choosing between two treatments at a specified time and observing outcomes over the same follow-up period. We now switch to “treatment A versus treatment B, with death as the outcome.” The principle of comparing potential outcomes is the same as in the blood-pressure example. For these calculations, assume outcomes are observed completely and accurately; loss to follow-up and measurement error require additional handling.

To keep the formulas consistent with the examples below, let **$$T=1$$ denote treatment B and $$T=0$$ denote treatment A**. Here, 0 is just a label and does not necessarily mean “no treatment.”

| Symbol | Meaning | How to read it in the treatment example |
| --- | --- | --- |
| $$i$$ | A particular person | Patient $$i$$ |
| $$T_i$$ | The treatment this person actually receives | Whether the person actually receives A or B |
| $$Y_i$$ | This person's observed outcome | Death during follow-up is coded 1; survival is coded 0 |
| $$Y_i(1)$$ | This person's outcome if treated with B | “What would happen to this person on B?” |
| $$Y_i(0)$$ | This person's outcome if treated with A | “What would happen to this person on A?” |
| $$X$$ | Pretreatment characteristics used for adjustment; possibly a set of variables | For example, pretreatment severity and age |
| $$C$$ | A variable singled out in the example | Pretreatment severity: mild or severe |

Uppercase $$T$$ denotes the variable for actual treatment; lowercase $$t$$ denotes a specified treatment value, such as 0 or 1. Thus, $$Y_i(t)$$ is a unified notation for the two potential outcomes.

The subscript $$i$$ here is **a person identifier, not time**; the $$t$$ in parentheses is a specified treatment label, also not follow-up time. Omitting $$i$$ and writing $$Y(t)$$ refers to the same potential-outcome variable at the target-population level. Later, $$X=x$$ means that the characteristic variable takes a particular value: for example, $$X$$ is severity and $$x$$ is “mild.”

This note follows Neal's use of $$T,X$$; later medical-methods notes often use $$A$$ for treatment and $$L$$ for covariates. These letters serve the same roles, but should be read according to each note's definitions. **Treatment $$T$$ here is not the $$T_0$$ marking the start of follow-up in TTE diagrams**; $$Y(1)$$ and $$Y^{A=1}$$ are also two common notations for potential outcomes.

In the latter notation, the superscript $$A=1$$ is a label meaning “suppose treatment is set to 1,” **not exponentiation**. The same letter can have another meaning elsewhere: for example, $$T$$ often denotes event time in survival analysis, so an interpretation should not be carried over merely because the letter is the same.

$$Y_i(1)$$ and $$Y_i(0)$$ are called **potential outcomes**. “Potential” does not mean “model prediction”; it refers to an outcome defined under a specified treatment condition.

Suppose a patient actually receives B and survives:

| Patient | Actual treatment $$T_i$$ | Potential outcome on B, $$Y_i(1)$$ | Potential outcome on A, $$Y_i(0)$$ | Observed outcome $$Y_i$$ |
| --- | --- | --- | --- | --- |
| This patient | 1, meaning B | 0, observed | ?, unobserved | 0 |

Here we have already used **consistency**, which will be explained later: when B is actually received, the observed outcome is the potential outcome under B. The outcome under the other treatment, which did not occur, is called the **counterfactual outcome**.

### Three symbols needed to read the formulas
{: #section-8 }

- **$$\mathbb{E}[Y]$$**: the population mean of $$Y$$. If $$Y$$ is a 0/1 indicator of death, its mean is the risk of death.
- **$$\mid$$**: “conditional on.” $$\mathbb{E}[Y\mid T=1]$$ is the average outcome among people who actually receive B.
- **$$\perp\!\!\!\perp$$**: statistical independence. Later, it expresses that “treatment assignment is unrelated to potential outcomes.”

For example, if 12 of 100 people die, the sample mean of the 0/1 outcome is $$(12\times1+88\times0)/100=0.12=12\%$$. This explains why the “mean” of a binary outcome can be read as a “risk.” The population risk is written $$P(Y=1)$$, where $$P$$ denotes probability and $$Y=1$$ inside the parentheses denotes the event “death occurs.” Thus, for a binary outcome, $$\mathbb E[Y]=P(Y=1)$$. If $$Y$$ is blood pressure, the expectation is mean blood pressure in mmHg and cannot be interpreted as mortality risk.

<aside class="study-callout study-callout--important" markdown="1">

**The pair of expressions most easily confused**

$$\mathbb{E}[Y\mid T=1]$$: What is the average outcome **among the people who actually receive B**?

$$\mathbb{E}[Y(1)]$$: What would the average outcome be **if the entire target population received B**?

They concern different populations and therefore generally cannot be equated directly.

</aside>


## 2. Why is causal inference difficult?
{: #section-9 }

### 2.1 We cannot observe both potential outcomes for the same person
{: #section-10 }

The individual causal effect is defined as:

$$
\tau_i=Y_i(1)-Y_i(0)
$$

That is, the same person's outcome under B minus their outcome under A.

$$\tau$$ is pronounced “tau”; $$\tau_i$$ is person $$i$$'s causal effect, not a duration. Both outcomes here take values 0 or 1, so their difference can be −1, 0, or 1. For example, in a thought experiment, if this person would survive under B and die under A, then $$\tau_i=0-1=-1$$. This is the difference between two event indicators for that person; averaging across the population produces the risk difference below.

In the example above, we know that the patient survived after receiving B, but we do not know whether the patient would also have survived under A. Thus, **“the patient survived after receiving B” alone does not establish that B saved the patient**.

This is the fundamental problem of causal inference: for the same person in the same treatment-decision setting, we can observe the outcome under only one treatment. Adding data from other people does not directly reveal that person's missing outcome.

<details class="study-callout" markdown="1">
<summary>Can giving the same person A first and B later solve this?</summary>

It is still the same person, but the treatment time, physical condition, or effects of previous treatment may have changed. The two outcomes observed in sequence are not the two potential outcomes under the same decision setting.

Crossover trials can provide causal evidence, but require appropriate design and attention to period effects, carryover effects, and related issues.

</details>


### 2.2 Turning to population averages: ATE
{: #section-11 }

Although we cannot calculate an individual effect directly, we can change the question to: **What is the average effect of B versus A in the target population?**

This quantity is the **average treatment effect (ATE)**:

$$
\mathrm{ATE}
=\mathbb{E}[Y(1)-Y(0)]
=\mathbb{E}[Y(1)]-\mathbb{E}[Y(0)]
$$

The second equality follows from the linearity of expectation: **the average of differences equals the difference of averages**. It does not require $$Y(1)$$ and $$Y(0)$$ to be independent.

Read each term: $$\mathbb E[Y(1)]$$ is the risk if the entire target population received B; $$\mathbb E[Y(0)]$$ is the risk if the same population received A; the minus sign defines the direction as B minus A. Risk has no physical unit and is usually written as a proportion or percentage; a difference between percentages is reported in **percentage points**. For example, if the two risks are 12% and 20%, the ATE is $$0.12-0.20=-0.08$$, or −8 percentage points, not “an 8% relative reduction.”

The useful implication is that estimating the ATE does not require first knowing every individual's causal effect. We can try to estimate the mean outcome under “everyone receives B” and under “everyone receives A” separately. **Averaging alone, however, does not solve the problem: we still need assumptions connecting these two quantities to observed data.**

In this note, $$Y=1$$ denotes death, so:

- ATE below 0: B lowers average mortality risk compared with A.
- ATE above 0: B increases average mortality risk compared with A.
- ATE equal to 0: average risks do not differ; this does not mean that the effect is zero for everyone.

### 2.3 Identification and estimation are different steps
{: #section-12 }

| Step | Question to answer | Example in this note |
| --- | --- | --- |
| **Identification** | Under the stated assumptions, can the distribution of observed data uniquely determine the target causal quantity? | Can the ATE be written using only $$Y,T,X$$? |
| **Estimation** | How can that quantity be calculated from a finite sample, and how large is the error? | Use stratum-specific means or a regression model to obtain an ATE estimate |

Identification asks whether the information would suffice even if we knew the observed-data distribution perfectly. Estimation asks how to calculate accurately when we have only finite data. A large sample or an accurate prediction model alone cannot ensure correct identification of a causal effect.

## 3. An example: Why might a difference between groups fail to represent a treatment effect?
{: #section-13 }

We retain the **fictional COVID-27 teaching example** from the original note. Severity $$C$$ here is **pretreatment** severity, and $$Y$$ indicates whether death occurs during follow-up.

| Treatment | Mild: deaths / total | Severe: deaths / total | Overall proportion who die |
| --- | --- | --- | --- |
| A | 210 / 1400 = 15% | 30 / 100 = 30% | 240 / 1500 = **16.0%** |
| B | 5 / 50 = 10% | 100 / 500 = 20% | 105 / 550 ≈ **19.1%** |

The data come from [Brady Neal's teaching example (§1.1)](https://www.bradyneal.com/Introduction_to_Causal_Inference-Sep8_2020-Neal.pdf#page=7); calculations below are rounded to one decimal place.

### 3.1 The apparent contradiction
{: #section-14 }

In the pooled data, the proportion who die is lower under A; within both the mild and severe strata, however, it is lower under B. This reversal in the direction of an association between the overall and stratified results is called **Simpson's paradox**.

The key is that the groups have different severity compositions:

- Approximately **93.3% of group A have mild disease**.
- Approximately **90.9% of group B have severe disease**.

A direct comparison of 16.0% and 19.1% therefore mixes treatment differences with differences in severity composition.

### 3.2 How does severity cause confounding?
{: #section-15 }

Suppose physicians are more likely to give B to patients with severe disease and severe disease itself increases mortality risk. We represent these causal assumptions with the following diagram:

<pre class="mermaid">flowchart LR
    C[&quot;C: Pretreatment severity&quot;] --&gt; T[&quot;T: Treatment A or B&quot;]
    C --&gt; Y[&quot;Y: Death&quot;]
    T --&gt; Y</pre>

The arrows denote assumed causal effects. This diagram contains two paths connecting $$T$$ and $$Y$$:

- **$$T\to Y$$**: treatment affects the outcome, the causal path of interest.
- **$$T\leftarrow C\to Y$$**: severity affects both treatment choice and outcome, creating a noncausal association; this is a **backdoor path**.

Here, $$C$$ is a typical **confounder**. The diagram expresses assumptions about the data-generating process; it cannot be established from the table alone. When reading an arrow, remember that it denotes an assumed causal effect, without directly specifying its magnitude, sign, or statistical significance.

### 3.3 How can the comparison be made fairer?
{: #section-16 }

First compare people with the same severity, then average using **the severity composition of one common target population**. Here, the target population is all patients represented by the sample, and the weights are estimated using the full-sample proportions:

$$
\text{Weight for mild disease}=\frac{1450}{2050}\approx70.7\%,
\qquad
\text{Weight for severe disease}=\frac{600}{2050}\approx29.3\%
$$

Use this same set of weights when evaluating either A or B:

$$
\begin{aligned}
\text{Estimated risk if everyone receives A}
&=\frac{1450}{2050}\times0.15
+\frac{600}{2050}\times0.30\\
&\approx19.4\%
\end{aligned}
$$

$$
\begin{aligned}
\text{Estimated risk if everyone receives B}
&=\frac{1450}{2050}\times0.10
+\frac{600}{2050}\times0.20\\
&\approx12.9\%
\end{aligned}
$$

The estimated ATE of B versus A is therefore:

$$
\widehat{\mathrm{ATE}}\approx12.9\%-19.4\%=-6.5\text{ percentage points}
$$

The “hat” over $$\widehat{\mathrm{ATE}}$$ indicates an **estimate** calculated from sample data.

To express this as a more intuitive count, suppose there are 1,000 patients with the above mix of mild and severe disease. If everyone received A, approximately 194 deaths would be expected; if those same people all received B, approximately 129 deaths would be expected. The scenarios differ by about 65 deaths on average. **This is not a direct comparison of the 240 deaths in group A and the 105 deaths in group B in the original data**, because those groups differ in both size and severity composition. Nor does it identify which particular 65 people would be saved.

<aside class="study-callout study-callout--important" markdown="1">

**What does this step depend on?**

If, within each severity stratum, people receiving the two treatments are sufficiently comparable and the other conditions in the next section hold, the calculation above can estimate a causal effect.

**Common weights standardize severity composition; they do not automatically eliminate residual confounding within strata.** If other factors, such as age, still influence treatment choice and mortality risk, adjusting only for severity may be insufficient.

Likewise, if “severity” is measured after treatment and affected by it, the interpretation above cannot be applied directly. Simpson's paradox itself does not tell us whether adjustment is appropriate.

</aside>


## 4. Four assumptions: Why can this comparison receive a causal interpretation?
{: #section-17 }

The following conditions support the adjustment formula in this note. First remember the practical question behind each assumption.

| Assumption | Most intuitive question |
| --- | --- |
| Exchangeability | Within the same $$X$$, are the groups' potential outcomes comparable? |
| Positivity | Can every type of person in the target population receive either treatment? |
| Consistency | Does actual treatment correspond to the intervention we have defined? |
| No interference | Is one person's outcome unaffected by other people's treatments? |

### 4.1 Exchangeability: Are the groups comparable under the same conditions?
{: #section-18 }

Start with the unconditional version:

$$
Y(t)\perp\!\!\!\perp T,\qquad t\in\{0,1\}
$$

This means that the treatment a person actually receives is unrelated to their potential outcome under a specified treatment.

Here, $$Y(t)$$ is the potential outcome under the specified treatment, $$T$$ is actual treatment, and $$\perp\!\!\!\perp$$ denotes their statistical independence. Read $$t\in\{0,1\}$$ as “$$t$$ takes the value 0 or 1”: the independence must hold separately for each treatment. It does not state that $$Y(1)$$ and $$Y(0)$$ are independent of one another.

For observational data, we usually hope that **conditional exchangeability** holds after conditioning on appropriate $$X$$:

$$
Y(t)\perp\!\!\!\perp T\mid X,\qquad t\in\{0,1\}
$$

The additional $$\mid X$$ means “given the same pretreatment characteristics $$X$$.” If $$X$$ contains only mild versus severe disease, independence is considered separately within those two strata; if $$X$$ contains age and several other variables, it must be understood within combinations of those characteristics.

For example, among patients with mild disease, if the actual A and B groups **both received B**, their outcome distributions should be the same; if they **both received A**, their distributions should also be the same. This compares potential outcomes under the same treatment; **it does not require treatments A and B to have the same effects**.

This condition allows the outcomes of “patients with mild disease who actually receive B” to represent the outcomes of “all patients with mild disease if they received B.”

If, even among patients with mild disease, older patients are more likely to receive B and more likely to die, the groups may remain nonexchangeable after conditioning only on severity.

Common related terms are **unconfoundedness, conditional ignorability, and no unmeasured confounding**. For now, interpret them as “no remaining confounding after conditioning on the selected covariates.”

<details class="study-callout" markdown="1">
<summary>What does randomization guarantee?</summary>

Under simple random assignment, the assignment mechanism does not select treatment based on patients' potential outcomes, supporting exchangeability by design. Nevertheless, a particular finite sample may still show chance imbalances in age or severity.

We must also distinguish “randomly assigned treatment” from “treatment actually received.” If some participants do not adhere to their assignment, actual treatment need not retain the exchangeability provided by randomization. Randomization also does not automatically eliminate bias from loss to follow-up, outcome measurement, or subsequent selection; see [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).

</details>


### 4.2 Positivity: Does every type of person have a comparison available?
{: #section-19 }

For a binary treatment, require:

$$
0<P(T=1\mid X=x)<1
$$

Here, $$P$$ denotes probability, $$T=1$$ means receiving B, $$X=x$$ identifies a particular baseline stratum, and $$\mid$$ means within that stratum. The inequalities require the probability to be strictly above 0 and strictly below 1. If patients in the severe stratum have a 70% chance of receiving B, they have a 30% chance of receiving A, so both actions are possible. The 70% is a probability, not a requirement that every sample be allocated in an exact 7:3 ratio.

This condition applies to values of $$X$$ that occur in the target population—strictly speaking, almost everywhere under its distribution. For those characteristics, the probability of receiving B is neither 0 nor 1, so either treatment can occur.

For example, if the healthcare system **always assigns B to patients with severe disease**, the data cannot directly tell us their average outcome under A. Estimating it requires additional extrapolation assumptions or reconsidering the target population and research question.

Distinguish:

- **Structural impossibility**: a type of person cannot receive A at all, violating positivity.
- **Few or no such people in the sample**: A is possible in theory, but current data are insufficient and estimation will be unstable.

Positivity is a probability condition in the population, not a requirement that every exact $$X$$ value in a finite sample contain two people, one on A and one on B. This is particularly inappropriate as a check for continuous variables.

### 4.3 Consistency: Does treatment in reality match the defined intervention?
{: #section-20 }

$$
T=t\implies Y=Y(t)
$$

Read this as: if a person actually receives treatment $$t$$, their observed outcome is their potential outcome under that treatment.

$$\implies$$ means “if the statement on the left holds, the statement on the right holds”; it is not a treatment arrow in a causal diagram. $$T=t$$ means actual treatment equals the specified value, $$Y$$ is the actual outcome, and $$Y(t)$$ is the potential outcome under that treatment. For example, an actual B recipient has $$T=1$$, and consistency gives $$Y=Y(1)$$ without also revealing $$Y(0)$$.

The difficulty is that “treatment $$t$$” must be defined clearly enough. Does “use B” specify the drug, dose, starting time, and duration? If one label includes regimens with different effects, $$Y(1)$$ may be ambiguous.

Questions such as “What is the effect of obesity on mortality?” therefore require a clearer specification of the interventions being compared. Changing weight through diet, exercise, or surgery may produce different outcomes. The point is to clarify the intervention, rather than simply declaring that an exposure “cannot be studied.”

Measures such as hemoglobin raise the same “how is it changed?” question; see [Biomarkers and Well-Defined Interventions]({{ "/causal-inference/biomarkers-well-defined-interventions/" | relative_url }}), which distinguishes mixed intervention versions from confounding.

### 4.4 No interference: Can other people's treatment affect me?
{: #section-21 }

$$
Y_i(t_1,\ldots,t_n)=Y_i(t_i)
$$

The left side allows person $$i$$'s outcome to depend on everyone's treatment; the right side states that, under no interference, only their own treatment needs to be specified.

Here, $$n$$ is the number of people considered, $$i$$ identifies one of them, and $$t_1,\ldots,t_n$$ are their assigned treatment values. The ellipsis stands for the intervening individuals' values, and $$t_i$$ is person $$i$$'s own treatment. Subscripts identify people, not time. For example, with two people, holding one person's treatment at B while changing the other's from A to B must leave the first person's outcome unchanged for this relation to hold for that person.

For example, other people's vaccination may change my infection risk, so no interference may fail. This can still be studied as a causal question, but other people's treatments must be included in the intervention definition; the simple formulas in this note cannot be carried over directly.

**SUTVA (stable unit treatment value assumption)** typically summarizes “no hidden versions of treatment that affect outcomes” and “no interference.” Textbooks differ slightly in how they separate these from consistency. Following Neal's teaching approach, this note discusses treatment versions under consistency. [Terminological discussion of these conditions](https://doi.org/10.1177/0962280211398037).

### 4.5 Can data prove these assumptions?
{: #section-22 }

We can examine treatment counts within strata or inspect the distribution of the **propensity score**, $$e(X)=P(T=1\mid X)$$, to diagnose positivity and overlap problems. Finite data, however, cannot prove that sufficient overlap exists throughout the population.

$$e$$ names this probability function, and $$X$$ in parentheses supplies the baseline characteristics as inputs. Here, $$e(X)$$ is not a power of the mathematical constant $$e$$. For example, $$e(\text{severe})=0.7$$ means that patients with severe disease have a 70% probability of receiving B.

Conditional exchangeability generally cannot be verified from observed data alone because every person has unobserved potential outcomes. Consistency and no interference also require judgment informed by the intervention definition and subject-matter knowledge. Data, design, and sensitivity analyses can help reveal problems, but “passing checks” cannot replace justification of the assumptions.

## 5. The adjustment formula: Stratify first, then average over the target population
{: #section-23 }

The calculation in §3 can be written generally. If the conditions above hold and $$X$$ is an appropriate adjustment set:

$$
\boxed{
\mathbb{E}[Y(t)]
=
\mathbb{E}_X\!\left[\mathbb{E}[Y\mid T=t,X]\right]
}
$$

Read from the inside out:

1. **Inner expectation** $$\mathbb{E}[Y\mid T=t,X]$$: within each category of $$X$$, find the average outcome among people who actually receive $$t$$.
2. **Outer expectation** $$\mathbb{E}_X$$: average these outcomes using the proportions of the $$X$$ categories in the target population.

The left side, $$\mathbb E[Y(t)]$$, is the average “if everyone received the specified treatment $$t$$”; the inner expectation on the right is the observed mean among people with the same characteristics and treatment. The $$X$$ subscript on the outer $$\mathbb E$$ specifies **which distribution of characteristics is being averaged over, not time**. Square brackets simply group the quantity being averaged; the box emphasizes the formula without adding an operation.

Thus:

$$
\boxed{
\mathrm{ATE}
=
\mathbb{E}_X\!\left[
\mathbb{E}[Y\mid T=1,X]
-
\mathbb{E}[Y\mid T=0,X]
\right]
}
$$

When $$X$$ is discrete, the first formula expands to:

$$
\mathbb{E}[Y(t)]
=
\sum_x
\underbrace{\mathbb{E}[Y\mid T=t,X=x]}_{\text{Mean outcome in this stratum}}
\underbrace{P(X=x)}_{\text{Proportion of the target population in this stratum}}
$$

Read $$\sum_x$$ as “go through all characteristic strata $$x$$ and add their contributions”; adjacent terms are multiplied. $$P(X=x)$$ is the stratum's proportion of the target population, not its treatment probability. If $$X$$ has only the values mild and severe, the expression is “treatment risk among mild cases × overall proportion with mild disease, plus treatment risk among severe cases × overall proportion with severe disease.” The B-strategy calculation in §3 is exactly $$10\%\times70.7\%+20\%\times29.3\%\approx12.9\%$$. The text underbraces merely explain individual terms.

For continuous $$X$$, replace the sum with an integral; $$\mathbb{E}_X$$ accommodates either case. This note assumes that the data come from the target population of interest. If the target population is at another hospital, transportability requires additional consideration; see §7.4.

### 5.1 Why not use each treatment group's own weights?
{: #section-24 }

The ordinary within-group mean is:

$$
\mathbb{E}[Y\mid T=t]
=
\sum_x \mathbb{E}[Y\mid T=t,X=x]P(X=x\mid T=t)
$$

Under the conditions for the adjustment formula, the causal mean is:

$$
\mathbb{E}[Y(t)]
=
\sum_x \mathbb{E}[Y\mid T=t,X=x]P(X=x)
$$

| Comparison | Weights | What question does it answer? |
| --- | --- | --- |
| Unadjusted comparison | Each group's own $$P(X=x\mid T=t)$$ | What are the outcomes among people who actually receive this treatment? |
| Adjusted comparison | A common $$P(X=x)$$ for both groups | What would the outcomes be if the same target population received this treatment? |

In the sample, the first uses “number in this stratum receiving this treatment / total number receiving this treatment”; the second uses “total number in this stratum / total sample size.”

In both expressions, $$Y$$ is the observed outcome and $$Y(t)$$ the potential outcome under a specified treatment; $$T=t$$ indicates actually receiving that treatment, $$X=x$$ indicates membership in that characteristic stratum, and $$\sum_x$$ adds across all strata. The real change is in the final weight: the bar in $$P(X=x\mid T=t)$$ restricts the population to the actual treatment group, whereas $$P(X=x)$$ imposes no such restriction.

If $$T$$ here is randomly assigned treatment and everyone actually receives their assigned treatment, then under simple random assignment with an assignment probability that does not vary with $$X$$, $$T$$ and $$X$$ are independent and theoretically $$P(X\mid T=t)=P(X)$$. If the other identification conditions also hold, the difference between the two sample means can estimate the ATE. Finite samples still have random error; with nonadherence, the assignment effect must be distinguished from the actual-treatment effect.

### 5.2 What is $$do(T=t)$$?
{: #section-25 }

If this is your first encounter with do, start with [A step-by-step explanation of observation, intervention, and potential outcomes]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}#section-8). That note uses A for treatment, while this one uses T; follow each note's own treatment coding.

You will encounter another common notation:

$$
\mathbb{E}[Y\mid do(T=t)]=\mathbb{E}[Y(t)]
$$

Both sides describe the same well-defined intervention:

$$do$$ is mathematical notation for “perform an intervention,” not a measured variable; $$T=1$$ still means B and $$T=0$$ means A. $$\mathbb E$$ denotes an average, and both sides refer to the same target population's average outcome under the specified treatment. Although the left expression also contains a bar, $$do(T=t)$$ replaces the treatment-generating mechanism; it must not be read as simply selecting people who already received $$t$$.

- **Conditioning on $$T=t$$**: observe people who actually receive $$t$$.
- **Intervening with $$do(T=t)$$**: set the target population's treatment to $$t$$ and consider their resulting outcomes.

In the diagram in §3, intervention means that severity no longer determines treatment: the assignment mechanism $$C\to T$$ is replaced, while $$C\to Y$$ remains.

“Adjustment formula,” “standardization,” and the “point-treatment g-formula” refer here to the same weighted expression. **Backdoor adjustment** in graphical methods offers one way to determine whether an adjustment set is appropriate. S-learners and T-learners are estimation methods, not alternative names for this formula.

## 6. A step-by-step derivation: How does counterfactual notation disappear?
{: #section-26 }

First derive the average outcome for just one treatment level $$t$$, then set $$t=1$$ and $$t=0$$ and subtract. This makes each step easier to see than writing two sets of formulas from the outset.

All notation in this section is as follows: $$T$$ is actual treatment, $$t$$ a specified value, $$Y$$ the actual outcome, $$Y(t)$$ the potential outcome under that treatment, and $$X$$ baseline characteristics; $$\mid$$ means “given,” $$\mathbb E$$ takes an average, and $$\mathbb E_X$$ averages over the target population's characteristic distribution. A comma connects simultaneous conditions: for example, $$T=t,X$$ conditions on both treatment and characteristics. All outcomes are evaluated over the same specified follow-up period.

### Step 1: Decompose the overall average into stratum-specific averages
{: #section-27 }

By the law of iterated expectations:

$$
\mathbb{E}[Y(t)]
=
\mathbb{E}_X\!\left[\mathbb{E}[Y(t)\mid X]\right]
$$

This is simply a probability identity: the mean outcome for all patients can be obtained by first averaging within severity strata, then averaging using the severity proportions among all patients. The inner quantity is still a potential outcome and has not yet become an observed quantity that can be estimated directly.

### Step 2: Use exchangeability so that actual recipients of $$t$$ serve as representatives
{: #section-28 }

$$
\mathbb{E}[Y(t)\mid X]
=
\mathbb{E}[Y(t)\mid T=t,X]
$$

If actual treatment is unrelated to $$Y(t)$$ given $$X$$, additionally restricting to “actually received $$t$$” does not change the conditional mean of $$Y(t)$$.

**Exchangeability supports this equality; positivity ensures a possibility of receiving $$t$$ at these values of $$X$$**, so that the right side can be determined from the corresponding part of the observed distribution.

### Step 3: Use consistency to replace potential outcomes with observed outcomes
{: #section-29 }

$$
\mathbb{E}[Y(t)\mid T=t,X]
=
\mathbb{E}[Y\mid T=t,X]
$$

The conditioning already specifies $$T=t$$, so consistency tells us that these people's $$Y(t)$$ equals their observed $$Y$$.

<aside class="study-callout study-callout--tip" markdown="1">

**What does each assumption do?**

**Exchangeability** allows actual recipients of $$t$$ to represent everyone in the same stratum; **consistency** allows those people's potential outcomes to be replaced with observed outcomes.

Consistency alone does not let us directly replace $$Y(t)$$ with $$Y$$ in $$\mathbb{E}[Y(t)\mid X]$$: the stratum also includes people who actually receive the other treatment.

</aside>


### Put the steps together, then obtain the ATE
{: #section-30 }

$$
\begin{aligned}
\mathbb{E}[Y(t)]
&=\mathbb{E}_X\!\left[\mathbb{E}[Y(t)\mid X]\right]\\
&=\mathbb{E}_X\!\left[\mathbb{E}[Y(t)\mid T=t,X]\right]\\
&=\mathbb{E}_X\!\left[\mathbb{E}[Y\mid T=t,X]\right]
\end{aligned}
$$

Set $$t=1$$ and $$t=0$$ separately, then subtract to obtain:

$$
\mathrm{ATE}
=
\mathbb{E}_X\!\left[
\mathbb{E}[Y\mid T=1,X]
-
\mathbb{E}[Y\mid T=0,X]
\right]
$$

No interference allows us to define a potential outcome using only the person's own treatment $$t$$. It is not an algebraic operation in a particular line above. For the textbook material corresponding to this derivation and the original note, see [Neal §2.3.6](https://www.bradyneal.com/Introduction_to_Causal_Inference-Sep8_2020-Neal.pdf#page=20).

## 7. Advanced distinctions: Return on a second reading
{: #section-31 }

### 7.1 Do potential outcomes include the influence of severity?
{: #section-32 }

**Yes.** $$Y_i(t)$$ means “what would happen to this person if treatment were set to $$t$$”; it does not erase severity, age, or other characteristics.

A patient with severe disease may still have a higher mortality risk under B than a patient with mild disease under B. The difficulty is that when patients with severe disease receive B more often, the B group's outcomes cannot directly represent the outcomes if the whole population received B.

| Relationship | Meaning |
| --- | --- |
| $$C\to Y$$ | Severity affects the outcome, and that influence can be reflected in potential outcomes |
| Both $$C\to T$$ and $$C\to Y$$ exist | Treatment groups may bring together people with different underlying risks, creating confounding |

Exchangeability therefore concerns **the relationship between treatment assignment and potential outcomes**, not a requirement that other variables have no influence on potential outcomes.

### 7.2 Confounders, confounding bias, and other biases
{: #section-33 }

**A confounder is a variable; confounding bias is a systematic departure caused by confounding.**

A “pretreatment common cause” is a typical starting point for understanding confounders. In a complex causal graph, however, “associated with both treatment and outcome” alone cannot determine whether to adjust. The more useful question is: **Can this set of variables close the relevant backdoor paths while avoiding the introduction of new bias?**

To illustrate the gap between the unadjusted comparison and the target quantity, write:

$$
\Delta=
\underbrace{\left\{
\mathbb{E}[Y\mid T=1]-\mathbb{E}[Y\mid T=0]
\right\}}_{\text{Observed overall association}}
-
\underbrace{\left\{
\mathbb{E}[Y(1)]-\mathbb{E}[Y(0)]
\right\}}_{\text{Target causal effect}}
$$

$$\Delta$$ is pronounced “delta.” This subsection specifically uses it for “unadjusted association minus target causal effect”; **here it is not the treatment effect itself**. The first braces contain the risks in the actual B and A groups; the second contain the risks in the same target population under interventions B and A. Braces simply group the calculations. Using the rounded results in §3, the first term is $$19.1\%-16.0\%=3.1$$ percentage points, the second is $$12.9\%-19.4\%=-6.5$$ percentage points, and the gap is approximately $$3.1-(-6.5)=9.6$$ percentage points. Other notes may use $$\Delta$$ to name an effect directly, so the local definition always governs.

In a simplified setting that considers only confounding and meets the other relevant conditions, this difference can be interpreted as the confounding bias of the unadjusted comparison. If selection or measurement problems also exist, not every departure of an estimate from its target can be attributed to confounding.

For example, [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}) distinguishes the true outcome $$Y$$ from the recorded outcome $$Y^*$$: even if true risks are equal, different detection rates may create a difference in recorded risks.

The star $$*$$ here only marks “the recorded version”; it is not multiplication, exponentiation, or another treatment intervention.

Confounding effects can also happen to cancel on a particular measure. A difference that happens to equal zero does not prove an absence of confounding.

[Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}) introduces a diagnostic approach: check whether treatment remains associated with an outcome it is not expected to cause. This can provide clues about residual bias, but no association does not prove exchangeability, and an association does not automatically quantify bias in the main effect.

### 7.3 Why is adjusting for more variables not always better?
{: #section-34 }

The table below concerns common simple structures when **estimating a total effect**. It provides directional guidance but cannot replace evaluation of the complete causal graph.

The table continues to use $$T$$ for treatment, $$Y$$ for outcome, and $$C$$ for a pretreatment common cause. The new letter $$M$$ denotes a mediator, and $$S$$ a collider that might be conditioned on, such as inclusion in an analysis sample. Arrows run from cause to effect and specify an assumed structure; they do not mean multiplication or provide numerical effects.

| Variable role | Simple structure | What should be considered before adjustment? |
| --- | --- | --- |
| Confounder | $$T\leftarrow C\to Y$$ | In this simple graph, adjusting for $$C$$ can close the backdoor path |
| Mediator | $$T\to M\to Y$$ | It transmits part of the treatment effect; when estimating a total effect, it is generally not adjusted for as an ordinary baseline covariate |
| Collider | $$T\to S\leftarrow Y$$ | Conditioning on $$S$$ may open a previously closed path and create a noncausal association |
| Pretreatment prognostic factor | Predicts $$Y$$, and adding it does not invalidate the adjustment set | Appropriate adjustment may improve precision |
| Instrumental variable | Affects $$T$$ and affects $$Y$$ only through $$T$$, with additional independence conditions required | Predicting treatment alone does not make it a confounder to adjust for; instrumental-variable methods have a separate identification logic |

“Conditioning” includes both putting a variable in a regression and selecting a sample based on a variable. For example, analyzing only members of one hospital cohort can introduce selection bias if inclusion is affected by treatment and by factors related to the outcome.

Treating an instrumental variable as an ordinary adjustment covariate may also amplify bias when unmeasured confounding exists; it does not automatically improve confounding control. [Pearl's analysis of bias-amplifying variables](https://ftp.cs.ucla.edu/pub/stat_ser/r356.pdf).

The backdoor criterion, d-separation (rules for blocking paths), and instrumental variables are later topics; separate notes are still to be added. For now, master the basic distinctions in the table.

For a concrete application, see [Confounding and Treatment Components: Kidney Transplantation]({{ "/causal-inference/confounding-treatment-components/" | relative_url }}): baseline recipient differences may cause confounding, while characteristics of the organ actually received may be part of treatment itself. “Imbalanced, predictive of the outcome, and present before surgery” alone cannot determine whether to adjust.

### 7.4 Can the result change with a different target population?
{: #section-35 }

Yes. The mean outcome if everyone receives a treatment depends on the target population's characteristic distribution:

$$
\mathbb{E}[Y(t)]
=
\sum_x \mathbb{E}[Y(t)\mid X=x]P(X=x)
$$

Here, $$t$$ specifies treatment and $$x$$ a baseline stratum; $$\mathbb E[Y(t)\mid X=x]$$ is the stratum's average outcome if everyone in it received $$t$$, $$P(X=x)$$ is its population proportion, and $$\sum_x$$ adds “within-stratum mean × stratum proportion.” Unlike the identification formula in §5, the right side still contains potential outcomes: it only decomposes the target-population mean and has not yet replaced it with observed data.

In this example, even if the treatment effects within mild and severe disease stay unchanged, average mortality risks under both treatments change at a hospital with a larger proportion of severe cases. Since the risk differences also differ between the two strata, the ATE changes too. If the risk differences were identical across strata, changing the stratum proportions alone would not change the ATE.

Extending findings to another population involves **transportability**. To reweight directly using the new hospital's $$P(X)$$, one must additionally justify that the stratum-specific outcomes or effects being used can be transported across populations and that there is sufficient overlap between populations. This requires separate consideration in multicenter RWE (real-world evidence).

## 8. What should you study next?
{: #section-36 }

### 8.1 From identification to estimation
{: #section-37 }

Companion hand-calculation notes: [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}) and [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) use the same teaching dataset to show how standardization and weighting estimate the same intervention risks.

All the methods below can estimate this note's ATE under appropriate conditions. For now, focus on what each method does.

| Method | Basic idea |
| --- | --- |
| [g-computation]({{ "/causal-inference/g-formula/" | relative_url }}) / outcome regression | Predict each person's outcome under A and under B, then average over the target population |
| [IPW]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}), inverse probability weighting | Weight people by the probability of their actual treatment so that the weighted treatment groups represent the target population |
| [G-estimation]({{ "/causal-inference/g-estimation/" | relative_url }}) | Model treatment effects and estimate parameters using conditional mean relationships after subtracting candidate effects |
| AIPW, augmented inverse probability weighting (note forthcoming) | Combine an outcome model and a treatment-assignment model to construct an estimator with a double-robustness property |

“Doubly robust” roughly means that, under the identification assumptions and appropriate statistical conditions, an estimator may remain consistent if either of the two model types is correct. It cannot replace identification assumptions such as no unmeasured confounding.

### 8.2 Connection to Target Trial Emulation
{: #section-38 }

[Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}) begins by asking: if we could conduct an ideal trial to answer this question, how should it be designed?

One key choice is whether to estimate the effect of “being assigned a treatment” or of “following a treatment strategy according to the protocol.” See [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}).

It requires specifying the study population, treatment strategies, assignment procedure, follow-up, outcomes, causal contrast, and analysis plan. This aligns the causal question with the observational-data analysis, covering intervention definition, comparability, and study timing. [Hernán and Robins on the target trial framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).

For example, eligibility determination, treatment assignment, and the start of follow-up must be coordinated to avoid design problems such as immortal time bias. [Hernán and colleagues on target trials and time alignment](https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/).

For diagrams and concrete examples, see [The three components of time zero]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-1) and [Immortal time bias]({{ "/causal-inference/target-trial-emulation/" | relative_url }}#section-7).

### 8.3 Next steps
{: #section-39 }

The next note for a first review is [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}): specify “which population, which two intervention scenarios, and which outcome” before studying particular estimation methods. The following is a list of later topics; completing all of them is not required before beginning TTE.

- [ ] Backdoor criterion (note forthcoming): How do we choose an appropriate adjustment set?
- [ ] d-separation (note forthcoming): How do we determine whether a path is blocked?
- [ ] Frontdoor criterion (note forthcoming): Are other identification approaches available when backdoor adjustment is unavailable?
- [ ] [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}), [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}), and [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}): understand the three estimation approaches through hand calculations, then read their longitudinal extensions.
- [ ] AIPW (note forthcoming): Develop a deeper understanding of doubly robust estimation.

## 9. Five questions to check your understanding
{: #section-40 }

1. Which populations do $$\mathbb{E}[Y\mid T=1]$$ and $$\mathbb{E}[Y(1)]$$ each describe?
2. Why can B have a lower death proportion in both mild and severe disease but a higher death proportion when pooled?
3. Why does the adjustment formula use the same $$P(X)$$ for both treatments?
4. Which assumption fails if patients with severe disease cannot receive A at all?
5. Does putting every variable into a regression guarantee elimination of bias?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. The first describes people who actually receive B; the second describes the entire target population if everyone received B.
2. Group B contains a higher proportion of severe cases, so the pooled comparison mixes in differences in severity composition.
3. We want to compare the average outcomes of the same target population under two treatments.
4. Positivity; outcomes under A among patients with severe disease lack direct support in that population.
5. No. Adjusting for a mediator may change the effect being estimated, and adjusting for a collider may introduce bias; omitted confounding does not disappear automatically either.

</details>
