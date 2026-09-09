---
layout: "causal-note"
title: "The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias"
description: "Calculate risk-set comparisons and partial likelihood, then distinguish hazard ratios from causal risk contrasts."
group: "Estimation"
order: 12
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Risk, survival, and hazard are different quantities", "anchor": "section-1"}, {"title": "2. What assumption does the Cox model make?", "anchor": "section-2"}, {"title": "3. Why do the data need “time + event indicator”?", "anchor": "section-3"}, {"title": "4. A hand calculation: Risk sets and partial likelihood", "anchor": "section-4"}, {"title": "5. How does a real study get from data to results?", "anchor": "section-8"}, {"title": "6. Why do the biases discussed earlier affect Cox?", "anchor": "section-9"}, {"title": "7. Can time-dependent Cox solve every longitudinal problem?", "anchor": "section-12"}, {"title": "8. A correctly estimated Cox model can still be misinterpreted", "anchor": "section-13"}, {"title": "9. How do Cox, the g-formula, and IPW work together?", "anchor": "section-14"}, {"title": "10. Self-check", "anchor": "section-15"}, {"title": "References", "anchor": "section-16"}]
previous_note: "/causal-inference/time-related-biases/"
next_note: "/causal-inference/g-formula/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). For notation, see [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}); this note also explains formulas alongside their use.

Prerequisite: time zero, follow-up, and censoring in [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}). Continue with [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}) and [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}).

Suppose we compare deaths in two patient groups. Knowing only “20 people died in group A and 10 in group B” is insufficient: how many people did each group originally contain? Did deaths happen early or late? Some people were observed for six months and others for five years—can these be treated as equally complete five-year records?

Survival analysis uses information about **when events occur and how long each person remains under observation**. Cox regression is one such model. It breaks follow-up into comparisons at successive event times: identify people whose deaths could still be observed then, and examine the characteristics of the person who actually died. We first explain the quantity being compared, then work through the process with four people.

<aside class="study-callout study-callout--abstract" markdown="1">

**First understand what Cox compares at each event**

Whenever someone experiences an event, Cox asks: **Immediately before this time, who was still under observation and event-free? How did the event case’s treatment and health differ from those of people who could still have experienced the event?**

These successive comparisons estimate relationships between treatment, age, and other variables and the instantaneous event rate. The calculation itself does not establish causality; biases in design, treatment classification, or measurement can still affect results.

</aside>


The outcome here is all-cause mortality; all numerical examples are invented for teaching. **On a first reading, start with §1–4 and the four-person risk-set example, then read §6 to connect bias to the data the model receives.** You may initially skip the calculus derivation of partial likelihood.


Multivariable worked example: [A complete multivariable logistic-regression IPTW example comparing drug A and drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15). It shows how baseline features of 3,000 people enter one common logistic regression to produce propensity scores, weights for both groups, balance diagnostics, and one-year risks. Z=0 means drug B, not no treatment.

## 1. Risk, survival, and hazard are different quantities
{: #section-1 }

“How many people die within five years?” and “Among people who have survived to year three, how quickly do deaths occur next?” are different questions. The first retains the baseline population as its reference; the second concerns only those alive at the current time. Cox directly models the latter, so distinguish them before writing formulas.

First distinguish three time symbols: $$T_0$$ is the start of follow-up; $$T$$ is a person’s elapsed time from baseline to death; $$t$$ is a time horizon the researcher asks about, such as $$t=5$$ years. $$T$$ can vary across people, whereas $$t=5$$ asks about the same five-year period. We use continuous time and do not consider competing causes of death because the outcome is all-cause mortality.

$$P(\cdot)$$ is the probability of the event in parentheses. $$\leq$$ means “less than or equal to,” and $$>$$ means “greater than.” Thus $$P(T\leq5)$$ is “the probability of dying within five years after entry.”

| Concept | Question | Example |
| --- | --- | --- |
| Cumulative risk $$P(T\leq t)$$ | What proportion will die between baseline and $$t$$? | Five-year mortality risk of 20% |
| Survival probability $$S(t)=P(T>t)$$ | What is the probability of still being alive at $$t$$? | Five-year survival probability of 80% |
| Hazard $$h(t)$$ | Among people alive at $$t$$, how quickly do deaths occur over the next very short interval? | Instantaneous death rate at a time point |

Hazard is a **rate conditional on still being alive**, not the probability of death over a fixed period. To understand it, begin with a short interval: among people who have survived to year three, examine the probability of death over the next short period and divide by its length. This describes the rate over that interval. Shrinking the interval indefinitely yields the hazard at year three.

The limit formula rigorously expresses “restrict to survivors, then convert a short-term death probability into a rate”:

$$
h(t)=\lim_{\Delta t\to0}\frac{P(t\leq T<t+\Delta t\mid T\geq t)}{\Delta t}.
$$

Read the definition in layers:

- $$h(t)$$: the hazard, or instantaneous event rate, at $$t$$; $$h$$ names the function and the $$t$$ in parentheses tells us where to evaluate it.
- $$\Delta t$$: a very short interval; $$\Delta$$ means an increment, not an effect difference here. With years as the unit, $$\Delta t=0.01$$ years is about 3.65 days.
- $$t\leq T<t+\Delta t$$: death occurs in the short interval from $$t$$ to $$t+\Delta t$$.
- $$\mid$$ means “given” or “conditional on”; $$T\geq t$$ means survival to the interval’s beginning. The numerator therefore concerns only people still alive.
- Division by $$\Delta t$$: converts the short-interval death probability into a rate per unit time.
- $$\lim_{\Delta t\to0}$$: shrink the interval and take the value this ratio approaches. Here $$\to$$ means “approaches,” not a causal arrow.

The full expression says: **among people alive at $$t$$, divide the probability of dying over the next very short interval by its duration, then let that duration approach zero.**

You need not memorize limits yet. When the interval is sufficiently short and hazard changes little within it, the death probability is approximately $$h(t)\Delta t$$, where adjacency denotes multiplication. For example, $$h(t)=0.2$$/year and $$\Delta t=0.01$$ years give approximately $$0.2\times0.01=0.002$$, or 0.2%. Hazard has units of inverse time and is not restricted to the 0–1 range of a probability.

Thus **HR = 0.70 does not mean “five-year mortality risk is reduced by 30%”**, nor that life expectancy increases by 30%. It describes a ratio of instantaneous event rates under the model’s specified conditions.

## 2. What assumption does the Cox model make?
{: #section-2 }

Now that hazard means the instantaneous event rate among current survivors, how do we describe its relationship between treated and control groups?

One simplification allows mortality rates to rise or fall over follow-up while assuming that, at any given time, the treated group’s rate is a fixed multiple of the control group’s. For example, we might try a model in which “the treated rate is always twice the control rate,” then use data to estimate the most appropriate multiple. This multiple is the hazard ratio, or HR.

Start with treatment alone: $$A=1$$ for treatment and $$A=0$$ for control. Write “common time pattern × between-group multiple” as:

$$
h(t\mid A)=h_0(t)\exp(\beta A).
$$

- $$h(t\mid A)$$: the instantaneous event rate at time $$t$$ given treatment status $$A$$; the bar denotes conditioning, not division.
- $$h_0(t)$$: the control group’s baseline hazard. Subscript 0 identifies the reference group; this rate can rise, fall, or fluctuate over time. It does not mean “the hazard on day 0.” It has the same units as $$h$$ on the left.
- $$\beta$$ (beta): the treatment regression coefficient, representing the model’s log hazard ratio. It is an unknown parameter, not a death probability.
- $$\exp(x)=e^x$$: $$x$$ is any input, such as $$\beta A$$; this is the exponential function with base $$e\approx2.718$$. $$\beta A$$ is multiplication; when $$A=0$$, $$\exp(\beta A)=1$$, and when $$A=1$$, it equals $$\exp(\beta)$$.
- $$\exp(\beta)$$: the treatment-to-control hazard ratio, HR. Dividing rates with the same units produces a unitless ratio. An ordinary proportional hazards model assumes it does not change over time.

The formula says: **this group’s current instantaneous event rate equals the baseline rate at the same time multiplied by a treatment-dependent factor.** This is a model assumption, not an identity that all survival data automatically satisfy.

For HR = 2, the control hazard may vary over time while the treated hazard is twice it at each corresponding time. **A constant ratio does not mean constant rates in both groups.**

Real patients also differ in age and health. To describe those relationships while comparing treatment, give each characteristic a coefficient. This is not a new estimation method; it extends the same Cox model from one variable to several.

Adding age and health $$L$$ gives:

$$
h(t\mid A,L)=h_0(t)\exp(\beta A+\gamma^\mathsf{T}L).
$$

The new $$L$$ denotes baseline covariates, possibly a vector such as age and a severity score; $$\gamma$$ (gamma) contains their coefficients. Superscript $$\mathsf{T}$$ denotes transpose, neither time $$T$$ nor a power. $$\gamma^\mathsf{T}L$$ multiplies corresponding coefficients and variables and adds them: if $$L=(L_1,L_2)$$, it means $$\gamma_1L_1+\gamma_2L_2$$. Here subscripts 1 and 2 identify variables, not follow-up visits. A continuous-variable coefficient corresponds to a one-unit change—for age recorded in years, one year. The same coefficient cannot be retained if age is rescaled into decades.

The full formula says: **given treatment and baseline health, the current instantaneous rate equals the baseline rate multiplied by a factor determined jointly by treatment, age, health, and other included features.**

Now $$\exp(\beta)$$ is a **conditional HR at the same $$L$$**. With interactions, the treatment HR may vary with $$L$$ and cannot always be read as a single fixed number.

After adding $$L$$, $$h_0(t)$$ refers to $$A=0,L=0$$, not the average rate among all controls; software may also center covariates. The specific baseline reference depends on parameterization, without changing between-group predictions.

## 3. Why do the data need “time + event indicator”?
{: #section-3 }

The model relationship is specified, but the HR still needs estimating. To learn from data, we must know exactly what each record tells us. In particular, “observation ended at month 3” can mean death or loss to follow-up; those do not convey the same information.

Suppose four people enter at a common $$T_0=0$$:

| Person | Treatment $$A$$ | End of observation (months) | Reason | Event indicator $$\delta$$ |
| --- | ---: | ---: | --- | ---: |
| A | 1 | 1 | Death | 1 |
| B | 0 | 2 | Death | 1 |
| C | 1 | 3 | Censoring | 0 |
| D | 0 | 4 | Death | 1 |

C’s record says: **we know they survived to month 3; after that, we do not know**. It cannot be treated as death at month 3 or survival to month 4. Yet the first three months are useful: when deaths occurred at months 1 and 2, C was still alive, helping the model evaluate who experienced those events first.

If death time is $$T$$ and censoring time is $$C$$, we observe:

$$
\widetilde T=\min(T,C),\qquad \delta=I(T\leq C).
$$

$$C$$ is elapsed time to censoring; $$\widetilde T$$, “T with a tilde,” is the observed end time, not necessarily the actual death time. $$\min(T,C)$$ takes whichever time is earlier. $$\delta$$ (delta) is the event indicator, and $$I(\cdot)$$ is an indicator function: 1 when the condition holds and 0 otherwise. Here $$\delta=1$$ means death was observed before or at censoring, and $$\delta=0$$ means censoring came first. Same-day events require prespecified data rules.

For example, C is lost at month 3, so $$C=3$$. The later death month may be unknown, but death was not observed before month 3, giving $$\widetilde T=3,\delta=0$$. This does not impute the unknown $$T$$ as 3.

The formula says: **record the earlier of death and censoring, then indicate whether an observed death caused observation to end**. The event indicator tells the model what the end time means.

<aside class="study-callout study-callout--important" markdown="1">

**Correctly labeling censoring does not make censoring harmless**

In this simple fixed-baseline-covariate setting, a common sufficient condition is that, given treatment and modeled covariates, censoring time provides no additional information about death time: $$T\perp C\mid A,L$$. This is conditional independent censoring. $$\perp$$ denotes statistical independence and $$\mid A,L$$ means “given the same treatment and covariates.” It does not require death and censoring to be completely unrelated in the pooled population.

If worsening health makes loss to follow-up more likely and the model does not appropriately handle that health information, ordinary Cox estimates may be biased. Equal censoring proportions in both groups do not establish the condition either.

This matters when estimating the original population’s hazard from those still observed, not only when interpreting causal effects. It is a common sufficient condition, not the only possible formulation for every Cox setting. [Jackson et al.: Independent censoring assumptions in Cox models](https://pmc.ncbi.nlm.nih.gov/articles/PMC4282781/)

</aside>


## 4. A hand calculation: Risk sets and partial likelihood
{: #section-4 }

### Step 1: Form the risk set at each death time
{: #section-5 }

Follow the four people’s timeline. At month 1, A dies. To ask “why was A the event case this time?” compare A with **people who could still experience an observed event immediately before this moment**. A person already dead cannot experience a first death again; after loss to follow-up, survival and death status are unknown, so the person cannot be treated as still observed.

The **risk set $$R(t)$$** contains people still under observation and free of the event immediately before it occurs. Uppercase $$R$$ is a set of people, not a risk value; $$t$$ is the current event time. The partial-likelihood denominator includes the current death case’s score because that person was in the risk set just before the event.

| Death time | Person who dies | Risk set | Why? |
| --- | --- | --- | --- |
| Month 1 | A | A, B, C, D | None had died or been censored |
| Month 2 | B | B, C, D | A has died |
| Month 4 | D | D | A and B have died; C was censored at month 3 |

Why specify “immediately before the event”? A was still a candidate just before dying. Removing A first would exclude the very person whose event we want to explain from the denominator.

Although C has no observed death, C contributes to the first two comparisons. Therefore, censored people must not simply be deleted. After leaving at month 3, C cannot re-enter the month-4 risk set because their survival status is unknown. This use still requires the appropriate censoring conditions in §3; merely “excluding lost patients” does not ensure the remaining people are representative.

### Step 2: Give each person in the risk set a relative score
{: #section-6 }

The risk set identifies candidates, but their event rates need not be equal. The Cox model in §2 supplies a comparison rule: controls receive a relative score of 1 and treated people the HR to be estimated. A candidate HR of 2 temporarily gives every treated person 2 points and every control 1 point—a model specification to be assessed against data.

Let $$r=\exp(\beta)$$, using lowercase $$r$$ for the unknown HR. It is positive and unitless, unlike the risk set $$R(t)$$. Treated people have score $$r$$ and controls score 1. These scores are relative instantaneous-rate multipliers, not individual death probabilities.

**Why does dividing a person’s score by the total yield the conditional probability below?** Within the same very short interval, each person’s death probability is approximately their hazard times the common interval length. Conditional on asking “who experienced the single event this time?”, the common duration cancels. The Cox model’s common baseline hazard also cancels, leaving each relative score’s share of the total. Continuous-time partial likelihood uses this limiting conditional comparison.

In this example without tied event times, given that exactly one risk-set member experiences an event at that time, the model’s conditional probability for “who experiences it” is:

$$
\frac{\text{Event case's score}}{\text{Sum of scores in the risk set}}.
$$

Temporarily use HR = 2: at month 1, scores are 2 for A, 1 for B, 2 for C, and 1 for D, totaling 6. The conditional probability that “this death is A’s” is $$2/6=1/3$$. This $$1/3$$ is neither A’s one-month mortality risk nor their risk over all follow-up; it conditions on an event occurring now and asks only whose event it is.

Replacing 2 with unknown $$r$$ gives the three observed-event contributions for any candidate HR:

- A’s death at month 1: $$r/(r+1+r+1)=r/(2r+2)$$.
- B’s death at month 2: $$1/(1+r+1)=1/(r+2)$$.
- D’s death at month 4: $$1/1=1$$.

At each time, $$h_0(t)$$ appears in numerator and denominator and cancels. Thus estimating $$\beta$$ does not first require a specific shape for the baseline hazard. This is the calculation’s value: use “who experienced each event” to estimate relative multipliers first, then estimate the baseline rate when absolute-risk predictions are needed.

### Step 3: Find the HR most consistent with the observed event sequence
{: #section-7 }

One comparison cannot determine the HR. A treated person’s death at month 1 supports a larger treatment score, whereas control B’s death at month 2 argues against making it too large. A candidate must account for all observed events, not only one death.

Multiply successive conditional contributions to obtain the **partial likelihood**. This does not assume disjoint risk sets: C indeed participates in the first two comparisons. Each contribution conditions on its updated risk set; their combination forms an objective function for the parameter.

The information concerns who experienced each event given its time and risk set:

$$
PL(r)=\frac{r}{2r+2}\times\frac{1}{r+2}\times1.
$$

$$PL$$ abbreviates partial likelihood; $$(r)$$ indicates the value obtained for a candidate HR; $$\times$$ multiplies the three event contributions. The denominator $$2r+2$$ comes from two treated people scoring $$r$$ each and two controls scoring 1 each.

Evaluate different candidate $$r$$ values to find which gives the strongest support to the observed events under these conditional comparisons. The program seeks the $$r$$ maximizing $$PL(r)$$. Here the maximum occurs at:

$$
\widehat r=\sqrt2\approx1.41,\qquad
\widehat\beta=\log(\sqrt2)\approx0.347.
$$

Hats indicate estimates from the sample: $$\widehat r$$ is the estimated HR and $$\widehat\beta$$ the estimated log HR. $$\sqrt2$$ is the positive number whose square equals 2, approximately 1.414. $$\log$$ throughout this note is the natural logarithm, inverse to $$\exp$$; $$\approx$$ means approximately equal. Thus $$\exp(0.347)\approx1.41$$: two scales expressing the same estimate.

Without calculus, compare a few candidates:

| Candidate HR $$r$$ | Resulting $$PL(r)$$ |
| ---: | ---: |
| 0.5 | 0.06667 |
| 1 | 0.08333 |
| About 1.414 | 0.08579 |
| 2 | 0.08333 |

The program searches a continuous range rather than only these four numbers. $$PL$$ compares how much candidate parameters support the observed event sequence; **0.08579 is neither mortality risk nor “the probability the HR is correct.”**

<details class="study-callout" markdown="1">
<summary>Expand this step when you want to see the calculus</summary>

Ignoring constants independent of $$r$$, log partial likelihood is $$\log r-\log(r+1)-\log(r+2)$$.

Its derivative is $$1/r-1/(r+1)-1/(r+2)$$. This is the slope of log partial likelihood as candidate $$r$$ changes. Setting the slope to zero finds an interior maximum and gives $$r^2=2$$, where superscript 2 denotes squaring. Since $$r>0$$, take the positive root. The omitted constant only shifts the curve vertically and does not change the maximizing $$r$$.

</details>


This four-person example illustrates only the algorithm; its estimate is extremely imprecise and cannot support clinical conclusions. Remember three points:

1. **One death in the treated group and two in controls do not imply HR = 1/2.** Event order and risk sets matter.
2. C enters the first two denominators but no death numerator; that is why a censored record remains informative.
3. When D alone remains, there is no between-group comparison. That event contributes 1 to the partial likelihood for $$\beta$$.

With multiple covariates, replace scores by $$\exp(\beta A+\gamma^\mathsf{T}L)$$ and estimate coefficients jointly. Real data with multiple events on the same day require ties handling, not an arbitrary invented order. [Official R survival documentation](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html)

## 5. How does a real study get from data to results?
{: #section-8 }

The four-person example completed “form risk sets → assign relative scores → calculate event contributions → choose parameters.” Real studies cannot begin with fitting, however. They first need appropriate eligibility, treatment, and follow-up definitions; otherwise, software will faithfully analyze data that do not answer the target question.

1. **Specify the target question first.** For example: “Among eligible patients, what is the effect of initiating drug A versus drug B today on five-year mortality risk?” Define population, strategies, $$T_0$$, endpoint, and effect scale. A common starting point means comparable clinical entry rules, not that everyone enters on the same calendar date.
2. **Construct follow-up correctly.** Retain deaths that should count after baseline; record loss to follow-up, administrative end, and changes over time. Do not use future information to backfill baseline treatment labels.
3. **Choose variables for the question.** Use causal knowledge to select required confounders, rather than including mediators, colliders, and every treatment component simply because data exist.
4. **Fit the partial likelihood.** Estimate coefficients, HRs, and uncertainty. Clustering or repeated records require appropriate variance estimation.
5. **Assess model suitability.** Examine proportional hazards, continuous-variable functional forms, interactions, and data support. Schoenfeld residuals can help assess PH but cannot verify absence of confounding.
6. **Report results matching the question.** A question about five-year death probability needs survival curves or risks, not only an HR.

If proportional hazards (PH) is clearly unsuitable, one constant HR may conceal early–late differences. Depending on the question, consider treatment–time interactions or other survival models; do not merely select a model yielding significance.

To answer “how many will die within five years?”, relative hazard multipliers alone are insufficient. With HR 0.70, treated absolute risk cannot be identical when control five-year risk is 2% versus 40%. **Partial likelihood dispenses with baseline-hazard information; absolute-risk prediction requires adding that information back.**

After estimating baseline cumulative hazard $$H_0(t)=\int_0^t h_0(u)du$$, the Cox model with these fixed baseline variables predicts:

$$
S(t\mid A,L)=\exp\{-H_0(t)\exp(\beta A+\gamma^\mathsf{T}L)\}.
$$

Distinguish lowercase $$h$$, uppercase $$H$$, and $$S$$:

- $$h_0(u)$$: the reference level’s instantaneous event rate at $$u$$.
- $$H_0(t)=\int_0^t h_0(u)du$$: accumulate baseline instantaneous rates over time from 0 to $$t$$. $$\int$$ denotes integration, with 0 and $$t$$ setting its limits; $$u$$ is a temporary time variable traversing the interval, and $$du$$ an infinitesimal duration. Rate multiplied by time makes $$H_0(t)$$ unitless.
- $$S(t\mid A,L)$$: the probability of surviving beyond $$t$$ given treatment and baseline covariates. For $$t=5$$ with time in years, it is conditional five-year survival.
- Outer $$\exp\{-\cdots\}$$: negate the grouped quantity and exponentiate it. The inner $$\exp(\beta A+\gamma^\mathsf{T}L)$$ remains the relative-rate multiplier defined in §2.

The formula says: **multiply baseline cumulative hazard by this person’s relative-rate multiplier, negate, and exponentiate to obtain their model-predicted survival probability.** Fitted predictions substitute estimates of the parameters and $$H_0$$; hats are omitted here to display the model relationship.

$$H_0(t)$$ is **not cumulative mortality probability** and is not restricted to 0–1. All-cause mortality probability is $$1-S(t)$$. For example, when $$H_0(5)\approx0.2231$$ and the relative multiplier is 1, survival is $$\exp(-0.2231)\approx0.8$$, and mortality probability is $$1-0.8=0.2$$.

<aside class="study-callout study-callout--example" markdown="1">

**Why does HR = 0.70 not allow simply multiplying five-year risk by 0.70?**

Consider another separate teaching scenario: at one fixed $$L$$, control five-year survival is 80%, and both groups satisfy proportional hazards with HR = 0.70 throughout. The formula gives treated five-year survival $$0.8^{0.70}\approx85.54\%$$, hence mortality risk about 14.46%.

The superscript in $$0.8^{0.70}$$ denotes a power: raise control survival 0.8 to power 0.70, rather than multiplying $$0.8\times0.70$$.

Control risk is 20%, so the five-year risk ratio is approximately $$14.46\%/20\%=0.723$$ and risk difference about −5.54 percentage points. **HR, risk ratio, and risk difference are 0.70, 0.723, and −5.54 percentage points, respectively; they are not interchangeable.** This conversion depends on the specified survival probability and PH model. An HR alone generally cannot determine risk. For a population with multiple $$L$$ values, predict separately and then average.

</aside>


Setting treatment and control in turn for **the same baseline target population**, predicting, and averaging yields standardized survival curves. Interpreting their difference causally also requires well-defined interventions, consistency, sufficient confounding control, positivity, appropriate outcome models, and censoring adjustment. This is one implementation of [The G-Formula]({{ "/causal-inference/g-formula/" | relative_url }}), not a guarantee supplied by Cox fitting alone.

## 6. Why do the biases discussed earlier affect Cox?
{: #section-9 }

Cox does not check why a patient was included or know about a death that went unrecorded. It receives **who entered, when observation began, when recorded events occurred, and treatment and covariates at event times**. These inputs determine every numerator and denominator in §4.

Understanding bias therefore need not involve memorizing another list of “Cox weaknesses.” Follow the calculation and ask: Are patients missing who should be in a risk set? Was future treatment labeled as current treatment? Were actual deaths unrecorded? Even with accurate records, the two groups within a risk set may have different underlying prognoses that the model inadequately handles.

| Problem | What changes in a Cox comparison? | Why does Cox fitting not automatically repair it? |
| --- | --- | --- |
| Baseline confounding | Treatment and control differ in prior prognosis within the same risk set | Omitted or mismeasured health may cause health-related event differences to be attributed to treatment |
| Immortal time bias | Future users are classified as already treated; early deaths are assigned elsewhere or excluded | The treated denominator includes people required to survive until future treatment, without corresponding early-death numerators |
| Lead time bias | Time origins correspond to different disease stages | Post-treatment survival may be calculated correctly without representing life extension from a common decision point |
| Depletion of susceptibles / survivor selection | High-risk people died or were excluded before analysis; remaining people no longer represent the original population | The model sees selected risk sets and cannot automatically recover omitted patients and deaths |
| Informative loss to follow-up or artificial censoring | People with better or worse future prognoses preferentially leave risk sets | A censoring indicator does not establish that those remaining represent those leaving |
| Surveillance bias / differential measurement error | Event detection or recording probabilities and timing differ by treatment | The model estimates the recorded-event process and cannot identify undiagnosed events itself |
| Time-varying confounding and treatment–confounder feedback | Health affects later treatment and outcomes and may be affected by past treatment | Omitting health may leave confounding; directly controlling it may block earlier treatment’s effect pathways |
| Adjusting for mediators, colliders, or treatment components | Alters the conditioned-on population or blocks the target total effect | The model estimates relationships under the specified conditions; “more adjustment” does not ensure the correct causal question |

### How does immortal time enter partial likelihood directly?
{: #section-10 }

Suppose A starts medication on day 7, but the researcher labels A as $$A=1$$ from day 0 because A “eventually used it.” When someone dies on day 3:

- A enters the Cox “treated” risk-set denominator.
- Everyone meeting that future-use definition had to survive to their own treatment-start date.
- People who might have used treatment but died first cannot enter the same future-user group.

The model sees fewer deaths during a period in which the group’s survival was artificially guaranteed. A larger sample only estimates the association created by this incorrect classification more precisely. See [Immortal Time, Lead Time, and Depletion of Susceptibles]({{ "/causal-inference/time-related-biases/" | relative_url }}).

Here “denominator” means **the sum of risk scores at each event time**, not simply total person-years across follow-up. Person-time intuition helps understand the direction, but Cox actually performs the successive risk-set comparisons in §4.

### Separate lead time from additional survival selection
{: #section-11 }

Suppose the same person dies at year 5 in either scenario, with early initiation at year 0 and late initiation at year 2. Survival measured from actual treatment is 5 versus 3 years; measured from a common decision point, both are 5 years.

Separately, including only “people who actually survived to late initiation” while deleting deaths during the late strategy’s waiting period adds **survival selection**. Cox cannot reconstruct the original strategies’ complete risks from the retained post-treatment records alone.

## 7. Can time-dependent Cox solve every longitudinal problem?
{: #section-12 }

No, although it can address specific recording problems. For example, treatment status can change over time:

| Person | Interval start | Interval end | Interval treatment $$A(t)$$ | Event at end |
| --- | ---: | ---: | ---: | ---: |
| A | Day 0 | Day 7 | 0 | 0 |
| A | Day 7 | Day 20 | 1 | 1 |

$$A(t)$$ is treatment status at $$t$$: 0 for currently untreated, 1 for currently treated. Parentheses indicate variation over time, not $$A$$ multiplied by $$t$$. An endpoint event of 1 means death at that interval’s end; 0 means no recorded death. A’s first interval ends only because treatment begins and the record must change; A should not be removed from the study.

A is therefore untreated in the day-3 comparison and treated by day 10. Data rules must clarify the order of treatment and events at interval boundaries.

This fixes one kind of “ever-treated” person-time misclassification. It **does not automatically resolve** why treatment started on day 7, how earlier health affected treatment and death, or which sustained or dynamic strategies are being compared. [Therneau et al.: Official guidance on time-dependent covariates](https://therneau.r-universe.dev/survival/doc/timedep.pdf)

If $$A_0\to L_1\to A_1$$ and $$L_1\to Y$$, treatment–confounder feedback requires careful handling. Here $$A_0$$ is baseline treatment, $$L_1$$ health before the next decision, $$A_1$$ that next treatment, and $$Y$$ the final outcome, such as death within five years. Subscripts 0 and 1 index temporal order. These $$\to$$ arrows denote assumed direct causal effects: earlier treatment changes later health, which then affects the next treatment and outcome. Appropriate longitudinal g-formula or IPW methods can address this. Conversely, merely seeing that $$L$$ changes over time does not establish that ordinary regression is unusable; examine the actual causal arrows and target effect. See [Reading the diagrams: Time-varying confounding need not imply treatment–confounder feedback]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}#section-9).

## 8. A correctly estimated Cox model can still be misinterpreted
{: #section-13 }

Hazards compare **the survivors remaining in each group**. If treatment changes early survival, the groups’ later survivors may differ. Changes in later HRs therefore cannot simply be interpreted as a weakening or reversal of drug effects in the same people. [Hernán: The Hazards of Hazard Ratios](https://pmc.ncbi.nlm.nih.gov/articles/PMC3653612/)

Distinguish:

- **Statistically describing each group’s survivor hazard correctly.**
- **Interpreting that survivor-conditional comparison as the average individual treatment effect in the same set of survivors.**

Risk sets shrinking as events occur is normal survival analysis; it does not establish that the Cox algorithm is inherently biased. Under full randomization and no treatment effect on survival, ordinary survival over time does not necessarily create systematic between-group differences.

The earlier dialysis example’s investigator 2 can still be biased under the null because entry additionally requires surviving to **different actual dialysis times corresponding to different strategies**. [Dialysis example and supplementary materials](https://pmc.ncbi.nlm.nih.gov/articles/PMC10400102/)

<details class="study-callout" markdown="1">
<summary>Advanced: Does this mean an HR can never be a causal target quantity?</summary>

No. One can transform the same baseline target population’s survival distributions under two interventions into hazards and define their ratio as a population-level causal target. It still does not mean “everyone’s hazard is multiplied by this amount,” nor is it the effect among people who would survive to that time under both interventions. Specify the target and interpretation explicitly; see [Fay and Li: Causal Interpretation of the Hazard Ratio in Randomized Clinical Trials](https://pmc.ncbi.nlm.nih.gov/articles/PMC11502288/).

</details>


Another advanced issue is noncollapsibility: even without confounding, a conditional HR at fixed covariates may differ from the population’s marginal HR. Thus not all change after adjustment represents “confounding removed.” On a first reading, remember: **a change in the adjusted HR alone does not prove that confounding was present**.

## 9. How do Cox, the g-formula, and IPW work together?
{: #section-14 }

| Level | Responsibility |
| --- | --- |
| Target trial design | Specifies interventions, population, starting time, and outcome ascertainment |
| Cox model | Describes how instantaneous event rates vary given treatment and covariates |
| G-formula | Averages conditional outcome predictions over the target population and histories under intervention |
| IPW | Reweights by treatment or censoring mechanisms to estimate target intervention outcomes from observed data |

Cox can be an outcome model within the g-formula, or a marginal Cox model can be fitted after appropriate IPW. A risk-difference target still requires risk curves. **Weighted Cox does not automatically turn an HR into a risk ratio or remove modeling and identification assumptions.**

## 10. Self-check
{: #section-15 }

1. Why should censored people not simply be deleted? — They contribute information to risk sets before censoring.
2. Does passing a PH test establish absence of confounding? — No. Model shape and causal identification are separate issues.
3. Does longer survival after earlier diagnosis prove death was delayed? — No. The time origin may have moved earlier.
4. Does including all time-varying variables in ordinary Cox necessarily estimate a sustained strategy’s total effect? — No. Confounders affected by previous treatment require appropriate handling.
5. Can a five-year mortality risk difference be read directly from the treatment coefficient? — No. Estimate and compare the corresponding risks.

## References
{: #section-16 }

- [R survival: Official coxph documentation](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html): models, event times, and implementation.
- [Therneau, Crowson, and Atkinson: Using Time Dependent Covariates and Time Dependent Coefficients in the Cox Model](https://therneau.r-universe.dev/survival/doc/timedep.pdf): risk sets, time-dependent covariates, and using future information.
- [Hernán (2010): The Hazards of Hazard Ratios](https://pmc.ncbi.nlm.nih.gov/articles/PMC3653612/): limitations of causal HR interpretation.
- [Fay and Li (2024): Causal Interpretation of the Hazard Ratio in Randomized Clinical Trials](https://pmc.ncbi.nlm.nih.gov/articles/PMC11502288/): population-level and individual-level HR interpretations.
- [Hernán and Robins: Causal Inference: What If](https://miguelhernan.org/whatifbook): survival analysis, standardization, and longitudinal causal estimation.
