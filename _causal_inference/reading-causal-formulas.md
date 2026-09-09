---
layout: "causal-note"
title: "Reading Causal Formulas: From Symbols to Questions"
description: "Read potential-outcome notation, interventions, probabilities, and risk differences one symbol at a time."
group: "Foundations"
order: 2
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. First write out the question in plain language", "anchor": "section-1"}, {"title": "2. Start with the innermost symbols", "anchor": "section-2"}, {"title": "3. The two expressions most easily confused", "anchor": "section-8"}, {"title": "4. When formulas get longer, check these symbols first", "anchor": "section-16"}, {"title": "5. Determine what the formula is doing", "anchor": "section-18"}, {"title": "6. Check each formula in this order", "anchor": "section-19"}, {"title": "Sources", "anchor": "section-20"}]
previous_note: "/causal-inference/potential-outcomes/"
next_note: "/causal-inference/causal-contrasts-estimands/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). No statistical prerequisite is required. Read §1–§3 first; consult §4–§6 when new notation appears later, without trying to memorize everything at once.

**A formula expresses a question in compact notation.** On a first reading, identify the population, strategy, outcome, and time horizon before reading the letters. All examples below are for teaching, not clinical research findings.

## 1. First write out the question in plain language
{: #section-1 }

Use the example in [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}) throughout: among a set of patients eligible today, how would five-year mortality risk differ if everyone followed A's complete protocol rather than B's complete protocol?

Let $$g_1$$ represent scenario A and $$g_0$$ scenario B. “Complete” means that initiation, continued treatment, permitted adjustments, and safety-related discontinuation rules have been specified, along with the assignment and care context retained. $$g$$ names a strategy; it is not a drug dose. Subscripts 1 and 0 distinguish the scenarios and cannot automatically be interpreted as treatment versus no treatment.

The question can be compressed to:

$$
\Delta_5=P(Y_5^{g_1}=1)-P(Y_5^{g_0}=1).
$$

Read this as: **five-year mortality risk under scenario A minus five-year mortality risk under scenario B is defined as the five-year risk difference.**

This defines only “what we want to know,” not yet “how to calculate it once data are available.” Writing an expression containing potential outcomes does not establish its identification.

## 2. Start with the innermost symbols
{: #section-2 }

### 2.1 First, Y: What exactly is measured?
{: #section-3 }

$$Y$$ usually denotes an outcome variable, but it does not mean death in every note. It might be blood pressure, measured in mmHg, or disease occurrence, coded 0 or 1. This example explicitly defines it as a death indicator.

Here, $$Y_5$$ concerns outcomes within five years from baseline. If someone is fully observed to survive beyond five years, their death indicator is 0; if they die within five years, it is 1. A person lost to follow-up within five years cannot be coded 0 merely because no death is recorded: their subsequent outcome may be unknown.

**The subscript 5 denotes the cumulative outcome through five years, not only outcomes occurring in the fifth year.** Death in year one also counts as “death within five years.”

### 2.2 Next, superscript g: Under which intervention scenario?
{: #section-4 }

$$Y_5^{g_1}$$ means “whether this person would die within five years if they were under scenario A.” The superscript identifies an intervention scenario and marks a potential outcome; **it does not raise Y to a power**.

By contrast, $$Y_5$$ alone usually denotes the outcome under the actual course of events. Appropriate actual outcomes can be linked to their corresponding potential outcomes only when the intervention definition and conditions such as consistency align. “What actually happened” and “what would happen under a specified rule” cannot be interchanged without explanation.

The same patient has potential outcomes under different scenarios, but actually follows only one path. Estimating population risks does not recover every person's unobserved potential outcomes.

### 2.3 Then, “equals 1”: What is the event inside the probability?
{: #section-5 }

$$Y_5^{g_1}=1$$ is the statement “if under scenario A, this person dies within five years.” Here, 1 means that the event occurs and 0 means it does not occur within the specified horizon; it is neither a patient identifier nor one year.

Thus, although they look identical, the 1 in $$g_1$$ and the 1 in “$$=1$$” have entirely different meanings: the former labels a strategy, while the latter codes an outcome.

### 2.4 The outer P: From one person's indicator to population risk
{: #section-6 }

$$P(\cdot)$$ means “the probability of the event inside the parentheses”; $$\Pr(\cdot)$$ is equivalent probability notation. Here, imagine randomly selecting someone from the defined target population and asking the probability that they would die within five years under scenario A.

Thus, $$P(Y_5^{g_1}=1)=0.08$$ means a five-year mortality risk of 8% under scenario A. It does not mean “strategy A has an 8% chance of working” or “we have 8% confidence.” Among 1,000 people of the same type under that scenario, 80 deaths are expected, although actual sample counts will fluctuate.

### 2.5 Finally, Delta: How are the risks compared?
{: #section-7 }

$$\Delta$$ is the Greek letter Delta, used here to name a difference; the 5 in $$\Delta_5$$ denotes the five-year horizon. A minus B sets the direction.

Using the teaching risks, 8% for A and 14% for B:

$$
\Delta_5=0.08-0.14=-0.06=-6\text{ percentage points}.
$$

Read this as “A has a five-year mortality risk 6 percentage points lower than B.” The minus sign says only that the first quantity is lower; whether this is beneficial depends on whether the outcome is death, recovery, or another measure.

For a risk ratio (RR), divide instead:

$$
RR_5=\frac{0.08}{0.14}\approx0.57.
$$

Here, $$RR_5$$ is A's five-year risk relative to B's. The numerator is A's risk and the denominator is B's risk, which must be nonzero. It has no physical unit and means that A's risk is approximately 0.57 times B's—a relative reduction of about 43%. **A reduction of 6 percentage points and a relative reduction of about 43% are not interchangeable.** The null value is 0 for a risk difference and 1 for a risk ratio; neither is the Cox hazard ratio.

## 3. The two expressions most easily confused
{: #section-8 }

Suppose $$A$$ denotes actual baseline treatment, with $$A=1$$ for treatment A and $$A=0$$ for treatment B, and $$Y=1$$ denotes death within the specified horizon. A and B are two treatments here; **0 does not mean no treatment**.

This section first simplifies the question to “receive A or B at baseline,” with subsequent care following the usual process under each intervention. It does not automatically include the full continued-treatment and safety-discontinuation rules from §1; complete strategies still require an explicitly defined $$g$$.

Read §3.1–§3.4 first to distinguish observation, intervention, and the two notational systems; §3.5 connects these to standardization through numbers. **The new do notation below does not introduce a third question; it expresses the intervention question in another notation.**

### 3.1 Without do: Examine outcomes among actual recipients of A
{: #section-9 }

$$
P(Y=1\mid A=1).
$$

Read from the inside out: $$A=1$$ means actually receiving treatment A; the bar $$\mid$$ specifies a condition; $$Y=1$$ denotes death; and the outer $$P$$ denotes probability. Together: **Among people who actually receive treatment A, what is the probability of death within the specified horizon?**

In a database, we first locate records of actual A recipients, then examine their deaths. People who originally received B are outside the population described by this conditional probability.

The problem is that the actual A group may not represent the whole target population. If people with more severe disease receive A more often, knowing that someone “received A” also gives information about their preexisting severity. More deaths in group A may reflect both treatment effects and greater initial severity, so they cannot be attributed solely to treatment.

### 3.2 With do: Set baseline treatment, then ask about outcomes
{: #section-10 }

If the question is “What would happen to the same target population if everyone received treatment A at baseline?”, write:

$$
P\bigl(Y=1\mid \operatorname{do}(A=1)\bigr).
$$

**Read do as “perform an intervention,” specifically here, “set baseline treatment A to 1, meaning treatment A.”** It is an intervention operator defining a hypothetical scenario, not a new patient variable, a probability, or d multiplied by o.

| Part of the formula | How should it be understood? |
| ------------------------ | ----------------------------- |
| $$A$$ | The treatment variable to be intervened on |
| $$1$$ | The specified treatment value, treatment A in this example; not “effective” or “death” |
| $$\operatorname{do}(A=1)$$ | Imagine setting the target population's baseline treatment to A, replacing the original treatment-choice mechanism |
| $$Y=1$$ | The event of interest under this intervention is death |
| The outer $$P$$ | The target population's probability of death under this intervention scenario |

The whole expression means: **If everyone in the target population received treatment A at baseline, what would be the probability of death within the specified horizon?** Both people who would originally receive A and people who would originally receive B belong to this population. Equal treatment does not mean equal ages, severity, or outcomes.

Why is there still a bar? This is the conventional form of do notation. Read $$\mid\operatorname{do}(A=1)$$ as a whole: “under an intervention setting A to 1.” **Seeing the bar does not mean we should continue interpreting this as selecting A=1 patients from the original database.**

For example, suppose a patient receives B in reality. In $$P(Y=1\mid A=1)$$, they are not part of the actual A group. In the target scenario described by $$P(Y=1\mid\operatorname{do}(A=1))$$, they remain a member of the target population, but we ask what would happen if they received A. Their actual outcome after B cannot simply be treated as their outcome after A.

For this distinction between observation and intervention, see [Pearl, Glymour, and Jewell, *Causal Inference in Statistics: A Primer*, §3.1–§3.2](https://bayes.cs.ucla.edu/PRIMER/pearl-etal-2016-primer-errata-pages-jan2021.pdf).

### 3.3 How does do relate to the potential outcome Y¹?
{: #section-11 }

You have already learned that $$Y^1$$ denotes a person's potential outcome if they received treatment A. Thus, for **the same target population, the same well-defined intervention, and the same outcome and horizon**:

$$
P\bigl(Y=1\mid\operatorname{do}(A=1)\bigr)=P(Y^1=1).
$$

The left side uses do to specify “the postintervention scenario in which Y is considered”; the right side places that same intervention in the outcome's superscript. On the right, superscript 1 denotes treatment A, while the later “=1” denotes death; the two 1s have different roles.

**This equality maps between two notations; it does not state that confounding has been eliminated or that the answer has been calculated from data.** Even with severe confounding in actual data, both sides can describe the same causal target awaiting identification. [Pearl (2009), §2.4 and footnote 4](https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf)

Place the three expressions side by side:

| Notation | Question | Which population? |
| --- | --- | --- |
| $$P(Y=1\mid A=1)$$ | What is mortality risk among actual recipients of treatment A? | The actual A group |
| $$P(Y=1\mid\operatorname{do}(A=1))$$ | What is mortality risk if everyone in the target population receives treatment A? | The entire originally defined target population |
| $$P(Y^1=1)$$ | What is mortality risk if everyone in the target population receives treatment A? | The same population as the row above |

The three expressions therefore represent **one observational question and one intervention question**. The first row generally cannot be directly equated with the last two. Appropriate exchangeability, consistency, and data-support conditions are needed to establish the corresponding identification relationship.

To replace treatment A with treatment B, change only the treatment value to 0: $$P(Y=1\mid\operatorname{do}(A=0))=P(Y^0=1)$$. The death event remains $$Y=1$$; it must not also change to $$Y=0$$.

### 3.4 What does do change in a causal diagram?
{: #section-12 }

Let $$L$$ denote pretreatment severity. Suppose severity affects both treatment choice and death, and treatment may also affect death. The left diagram shows the original mechanism; the right shows the mechanism after setting baseline treatment to A:

<pre class="mermaid">flowchart LR
    subgraph obs[&quot;Original treatment choice&quot;]
        direction TB
        L[&quot;L: Baseline severity&quot;] --&gt; A[&quot;A: Actual treatment&quot;]
        L --&gt; Y[&quot;Y: Outcome&quot;]
        A --&gt; Y
    end
    subgraph intervention[&quot;Intervention do(A=1)&quot;]
        direction TB
        Ld[&quot;L: Baseline severity&quot;] --&gt; Yd[&quot;Y: Postintervention outcome&quot;]
        Ad[&quot;A is set to 1: Treatment A&quot;] --&gt; Yd
    end</pre>

Arrows represent assumed direct causal effects, not just “occurs earlier in time.” L in both diagrams comes from the same target population's baseline severity; the right diagram does not substitute a healthier group of patients.

Originally, severity helps determine whether a person receives A or B. After this fixed-value intervention, treatment is set directly to A, and **the original mechanism determining treatment is replaced**. Graphically, this removes all arrows entering A; this simplified diagram shows only $$L\to A$$.

But $$L\to Y$$ remains: severe disease can still increase mortality risk. $$A\to Y$$ remains too: treatment's effect on outcome is exactly what we want to study. **What is severed is “how severity determines treatment,” not “how severity affects death,” and certainly not the treatment effect itself.**

This intervention holds other causal mechanisms fixed, without requiring all variable values to remain fixed. Later treatment does not rewrite baseline severity, but posttreatment severity and outcomes may change with treatment. This is an intervention scenario within the model; erasing an arrow does not automatically make actual observational data comparable. [Pearl (2009), §3.2.1](https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf)

### 3.5 A numerical example: Why can the two risks differ?
{: #section-13 }

Reuse the [1,000-person teaching table in the g-formula note]({{ "/causal-inference/g-formula/" | relative_url }}#section-1), naming its two actions A and B in this section, with **death within one year** as the outcome. This is a separate baseline-intervention example, not the complete-strategy example with five-year risks of 8% and 14% in §2.

Suppose all 1,000 people are eligible and their one-year outcomes are fully known:

| Baseline severity | Number in group A | Deaths / risk in group A | Number in group B | Deaths / risk in group B |
| --- | ---: | --- | ---: | --- |
| Less severe | 100 | 5 / 5% | 400 | 40 / 10% |
| More severe | 400 | 80 / 20% | 100 | 40 / 40% |

**First answer the observational question.** The actual A group has 500 people and 85 deaths, an observed risk of $$85/500=17\%$$; the actual B group has 500 people and 80 deaths, an observed risk of $$80/500=16\%$$. These sample proportions estimate $$P(Y=1\mid A=1)$$ and $$P(Y=1\mid A=0)$$, respectively.

Why does A appear worse? Severe cases make up 80% of group A but only 20% of group B. This is not a comparison in which the same target population receives A versus B.

**Next answer the intervention question.** Under $$\operatorname{do}(A=1)$$, all original 1,000 people receive A, while baseline composition remains 500 less-severe and 500 more-severe patients. We need their respective risks under A, then combine them with equal weights.

A bridge is required here: why can the table's 5% and 20% be borrowed? We must assume that, given sufficient baseline severity information, actual A recipients represent the average outcome that similar target patients would have under A. Treatment must also be well defined, consistency must hold, and each type of patient must have a chance of receiving the relevant treatment. This is the role of baseline exchangeability, consistency, positivity, and related conditions here. **The table's numbers themselves cannot prove that these conditions hold.**

Under these assumptions, standardize using sample stratum-specific risks:

- Estimated risk if everyone receives A: $$0.5\times5\%+0.5\times20\%=12.5\%$$.
- Estimated risk if the same population all receives B: $$0.5\times10\%+0.5\times40\%=25\%$$.

Here, 0.5 is the relevant baseline-severity stratum's proportion of the target population. Both predictions use a composition of 500 less-severe and 500 more-severe patients; only treatment changes. The observed A and B risks are therefore 17% and 16%, while the intervention risks estimated under the assumptions are 12.5% and 25%.

**do is not another way to write 17%; it clarifies which risk we want to estimate.** Answering this new question requires corresponding calculations that combine data and identification conditions.

The 12.5% alone is the risk under one intervention scenario; it must be compared with another scenario to obtain the treatment effect here. Taking A minus B, the estimated risk difference is $$12.5\%-25\%=-12.5$$ percentage points. This does not mean everyone's probability of death falls by the same amount.

<details class="study-callout" markdown="1">
<summary>Second reading: Write this standardization as an identification formula with do</summary>

Under the baseline-adjustment conditions above:

$$
P\bigl(Y=1\mid\operatorname{do}(A=a)\bigr)
=\sum_l P(Y=1\mid A=a,L=l)P(L=l).
$$

$$a$$ is the specified treatment value: 1 for treatment A and 0 for treatment B; it stays fixed during one calculation. $$L$$ is baseline severity, and $$l$$ is a particular value, “less severe” or “more severe.” $$\sum_l$$ adds contributions across severity strata. The first term, $$P(Y=1\mid A=a,L=l)$$, is the observed mortality risk conditional on both actual treatment and baseline severity; the comma means that both conditions hold. The second term, $$P(L=l)$$, is the stratum's proportion of the target population. Adjacent terms are multiplied.

The right side is therefore “risk in each stratum × that stratum's proportion of the target population, summed across strata.” For a=1, this gives $$0.5\times5\%+0.5\times20\%$$ above; actual estimation substitutes sample proportions or fitted models for population probabilities on the right.

The two equalities have different justifications: the equality between do and potential outcomes in §3.3 maps two notations for the same intervention; rewriting an intervention risk as a function of observed risks here is the step that depends on identification assumptions. See [Calculating the baseline g-formula by hand, step by step]({{ "/causal-inference/g-formula/" | relative_url }}#section-2) for the complete calculation.

</details>


### 3.6 Returning to TTE: do specifies a target but does not replace study design
{: #section-14 }

First, **writing do does not mean we have actually randomized patients.** It specifies an intervention scenario to study. Observational TTE still requires defining the target population, baseline, treatment strategies, and outcome, and assessing whether available data and assumptions support estimation. Changing every value in the database's A column to 1 while retaining the original Y does not produce everyone's outcome under treatment A.

Second, do alone does not determine ITT or PP. A in this section is **actual baseline treatment**, so $$\operatorname{do}(A=1)$$ concerns an actual treatment action, not a random-assignment effect. If $$Z$$ denotes “which strategy was assigned,” an intervention on Z and an intervention on actual action A have different targets. This distinction becomes especially important when some people do not follow their assigned treatment.

Third, A here denotes only baseline treatment. $$\operatorname{do}(A=1)$$ **does not automatically require continued treatment A in the future**. If the question is “initiate A and continue following the specified rules during follow-up,” later actions must also be included in the strategy—for example, by returning to $$g_1$$ and $$Y_5^{g_1}$$ in §1. One baseline do cannot replace the full protocol.

When you encounter do, ask three questions in order: **Which variable is intervened on? To which value or rule is it set? For which population and outcome horizon?** Only then move to “Can it be identified from the data?” and “Which estimation method should be used?”

<aside class="study-callout study-callout--check" markdown="1">

**Three quick checks**

1. Do original B recipients still count in the target scenario “everyone receives A”? — Yes, if they belong to the original target population; their actual B outcomes cannot simply be used as A outcomes.
2. Does the correspondence between do(A=1) and Y¹ mean confounding has been adjusted? — No; these are simply two notations for the same intervention.
3. After do, baseline severity no longer determines treatment. Does severity therefore stop affecting death? — No; its effect on death remains.

</aside>


### 3.7 What does it mean when the outcome is inside E?
{: #section-15 }

You will also see $$E[Y]$$ or $$\mathbb E[Y]$$, the population mean, called the expectation. For a 0/1 indicator $$Y$$, $$E[Y]=P(Y=1)$$. For example, among 100 fully observed people with eight 1s and ninety-two 0s, the sample mean is $$(8\times1+92\times0)/100=0.08$$, equal to the sample event proportion.

Similarly, $$E[Y\mid\operatorname{do}(A=a)]=E[Y^a]$$ is the average outcome under the same specified intervention. Here, $$a$$ can be 1 for A or 0 for B, and $$E$$ averages over the target population. If Y is a death indicator, this is also the intervention risk. If Y is blood pressure, it is mean blood pressure in mmHg and cannot be read as mortality risk.

## 4. When formulas get longer, check these symbols first
{: #section-16 }

The following are reading tools, not another model that needs estimating. The specific medical meaning of a letter is still determined by its paragraph.

| Notation | Meaning and a small example |
| --- | --- |
| Uppercase $$A,L,Y$$ and lowercase $$a,l$$ | Uppercase usually denotes variables; lowercase denotes particular values. $$A=a,L=l$$ focuses attention on people with that treatment and severity |
| $$L$$ or $$X$$ | Often denotes covariates, possibly a whole set of information such as age and severity; one letter need not represent only one number |
| $$i$$, $$n$$ | $$i$$ often identifies a patient and $$n$$ is sample size; $$Y_i$$ is patient i's outcome |
| $$k$$, $$K$$ | $$k$$ often identifies an assessment and $$K$$ the last one considered; check whether the note defines these as months, years, or visit numbers |
| $$A_0,A_1$$ | Often treatment at baseline and the next decision; these subscripts denote time, unlike the strategy labels in $$g_0,g_1$$ |
| $$\bar A_1=(A_0,A_1)$$ | In longitudinal treatment histories, the bar denotes the entire history through that time, not average treatment. In other statistical contexts a bar does denote a sample mean; follow the definition |
| $$\widehat R$$, $$\widehat\Delta$$ | A hat marks a sample estimate of risk R or effect Delta; the corresponding quantity without a hat usually denotes the true target value. A hat does not make an estimate unbiased |
| $$\sum_{i=1}^{n}Y_i$$ | Add outcomes from person 1 through person n; values 1, 0, 1 for three people sum to 2 |
| $$\frac1n\sum_{i=1}^{n}Y_i$$ | Sum first, then divide by the number of people to obtain the sample mean; the example above gives 2/3 |
| $$\prod_{k=0}^{K}q_k$$ | Multiply the terms from step 0 through step K; $$q_k$$ is the value at step k. If $$q_0=0.8,q_1=0.5$$, the product is 0.4. This only illustrates multiplication; q's probability interpretation in a particular study must be separately defined |
| $$I(A_i=1)$$ | Indicator function: 1 when the condition in parentheses is true, otherwise 0; makes eligible people's terms contribute to a sum and others' terms equal 0 |
| $$\operatorname{do}(A=a)$$ | The intervention operator setting treatment A to a; it does not select actual A=a recipients from the original data. See §3 for details |
| A comma after $$\mid$$ | Several conditions must hold simultaneously, as in $$A=1,L=l$$; it does not mean either condition alone |
| $$\perp$$ | Statistical independence; not a universal symbol for “no causal effect,” nor merely zero correlation |
| $$\min\{x,y\}$$ | The smaller of x and y; if two event times are 2 and 4 years, the earliest is 2 years |
| $$\exp(b)$$, $$\log(r)$$ | Natural exponential and natural logarithm, inverse operations; b and r are defined by the formula, and r must be positive. In Cox models, exponentiating a log HR commonly gives the HR |
| $$\gamma^{\mathsf T}L$$ | $$\gamma$$ is a coefficient vector and L a covariate vector; multiply each variable by its coefficient and sum, such as $$\gamma_1L_1+\gamma_2L_2$$. Here 1 and 2 identify covariates, not time; $$\gamma_1,\gamma_2$$ are their coefficients. Superscript T denotes vector transpose, not treatment or follow-up time |
| $$=$$, $$\approx$$, $$\neq$$ | Equal, approximately equal, and unequal. Approximation often indicates rounding, but check for other approximation assumptions in context |
| $$<$$, $$\leq$$, $$>$$, $$\geq$$ | Less than, less than or equal to, greater than, and greater than or equal to. Whether a boundary is included can affect time intervals and event definitions |

### The same letter may change meaning across notes
{: #section-17 }

| Easily confused symbol | How should it be distinguished? |
| --- | --- |
| $$T$$ | Treatment in the foundational-textbook note, event time in the Cox note, and $$T_0$$ as follow-up origin. These cannot automatically be treated as the same variable |
| $$E$$ | E in a diagram may mean eligibility; $$E[Y]$$ means expectation. Check whether it acts on a variable as an operator |
| $$H$$ | In g-estimation, $$H(\psi)$$ is a transformed outcome and $$\psi$$ a treatment-effect parameter to estimate; in Cox analysis, H may denote cumulative hazard; longitudinal medical histories may use yet another H notation |
| $$Y^*$$ versus $$Y^g$$ | The star marks a recorded outcome in the measurement-error note; superscript g marks a potential outcome under an intervention. These differ |
| $$P(\cdot)$$ versus a p-value | The former is an event probability. A significance-test p-value is the probability, under the specified testing hypothesis and model, of a statistic at least as extreme as observed; it is not the probability that a causal effect exists |
| $$g_0$$, $$A_0$$, $$Y_5$$ | These may denote a strategy label, baseline time, and a five-year horizon, respectively; not every subscript means time |

## 5. Determine what the formula is doing
{: #section-18 }

| Type | Purpose | Question to ask while reading |
| --- | --- | --- |
| Estimand definition | Specifies which counterfactual risks or means are to be compared | Are the population, strategies, outcome, horizon, and direction explicit? |
| Identification formula | Rewrites a target quantity as a function of the observed distribution under stated assumptions | Why does the equality hold, and which assumptions support it? |
| Statistical model | Specifies how a hazard, mean, or probability varies with variables | Which relationships does the model allow, and which does it rule out? |
| Estimation formula | Calculates an estimate using a finite sample, fitted models, and weights | Where does each number come from, and how is uncertainty quantified? |
| Algebra or bookkeeping rule | For example, decomposes postdiagnosis survival into two parts or selects the earliest end time | Is this only organizing numbers, without yet yielding a causal conclusion? |

For example, the five-year risk-difference definition merely writes “subtract two intervention risks”; [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}) then explains how, under relevant conditions, intervention risks can be obtained from observed stratum-specific risks. [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) handles population composition through another calculation. A method's name is not evidence that the identification assumptions hold.

## 6. Check each formula in this order
{: #section-19 }

1. **Read the plain-language question first.** If the population, action, or follow-up duration is unclear, complete the question first.
2. **Identify the outcome and its units.** Is Y a 0/1 indicator, mmHg, years, or something else?
3. **Distinguish superscripts, subscripts, conditions, and do.** Which marks an intervention and which marks time or an identifier? Does the bar introduce observed conditions or an intervention scenario specified by do?
4. **Read from the inside out.** Understand one event or mean first, then read probabilities, averages, sums, and contrasts.
5. **Substitute a few small numbers.** Check comparison direction and units, especially the distinctions among risk differences, risk ratios, and hazard ratios.
6. **Ask what justifies the equality.** Is it a definition, assumption, model, or a derivation already depending on identification conditions?

For detailed formulas, return as needed to [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}), [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}), [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}), and [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}). Those notes still need local definitions near their formulas; this note does not replace explanations of the specific medical context.

## Sources
{: #section-20 }

For foundations of potential outcomes, population risks, conditional probabilities, and causal identification, consult [Hernán and Robins, *Causal Inference: What If*, the authors' textbook](https://miguelhernan.org/whatifbook), especially Chapters 1–3 and the later chapters on standardization and weighting. The A-versus-B numbers and symbol-by-symbol explanations here are teaching illustrations.

For do notation and its correspondence to potential outcomes, see [Pearl (2009), *Causal Inference in Statistics: An Overview*, §2.4 and §3.2.1](https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf), and [Pearl, Glymour, and Jewell, *Causal Inference in Statistics: A Primer*, §3.1–§3.2](https://bayes.cs.ucla.edu/PRIMER/pearl-etal-2016-primer-errata-pages-jan2021.pdf). The numbers in §3 reuse this collection's g-formula teaching table.
