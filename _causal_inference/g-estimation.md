---
layout: "causal-note"
title: "G-Estimation and Structural Nested Models"
description: "Use candidate-effect subtraction and treatment residuals to understand structural nested models and common treatment history."
group: "Estimation"
order: 22
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Start with the problem: Why is blood pressure higher in the treated group?", "anchor": "section-1"}, {"title": "2. What does g-estimation estimate?", "anchor": "section-2"}, {"title": "3. Why can we “subtract a candidate effect first”?", "anchor": "section-3"}, {"title": "4. Find the effect using the 200-person teaching example", "anchor": "section-10"}, {"title": "5. How are parameters estimated in an actual analysis?", "anchor": "section-14"}, {"title": "6. How do longitudinal treatments connect to “common treatment history”?", "anchor": "section-18"}, {"title": "7. Differences from the g-formula and IPW", "anchor": "section-19"}, {"title": "8. What conditions are needed?", "anchor": "section-20"}, {"title": "9. Self-check", "anchor": "section-21"}, {"title": "10. What does the source article mean by “common treatment history”?", "anchor": "section-22"}, {"title": "Sources and further reading", "anchor": "section-23"}]
previous_note: "/causal-inference/clinical-data-adjustment/"
next_note: "/causal-inference/high-throughput-federated-tte/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). Notation companion: [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}).

**This note answers a specific question: If treatment really lowers blood pressure, how can confounded observational data estimate how much it lowers blood pressure on average?** We begin with data, explain why we construct $$H(\psi)$$, and only then express the calculation as an equation.

<aside class="study-callout study-callout--tip" markdown="1">

**A route for your first reading**

Read §1–§4 first, following the same 200 people through “why a crude comparison fails → what to compare within the same health category → why subtract a candidate effect → how to find its value.” You do not need to master estimating equations yet.

§5 translates the manual comparison into an equation a computer can solve; §6 extends it to repeated treatment decisions; §7–§8 compare methods and review assumptions. §10 explains the source article’s phrase “common treatment history.” If treatment effects and before–after changes are still unclear, begin with [the two possible futures in the foundations note]({{ "/causal-inference/potential-outcomes/" | relative_url }}#section-1).

</aside>


This is an advanced stop in the study guide. You may first study the g-formula, IPW, and the three TTE designs, then return for a closer reading. All blood-pressure numbers below are **teaching examples, not a real drug study**.

## 1. Start with the problem: Why is blood pressure higher in the treated group?
{: #section-1 }

Suppose we study 200 people, comparing the effect of “initiating a treatment today” versus “not initiating today” on blood pressure one year later. Subsequent care follows its usual course, so “not initiating” concerns only today’s decision, not never receiving medication in the future. To focus on the algorithm, we temporarily ignore loss to follow-up.

We record three things: health before the treatment decision, initiation today, and blood pressure measured one year later. The data are:

| Baseline health | Number initiating | Initiators’ mean blood pressure at one year | Number not initiating | Noninitiators’ mean blood pressure at one year |
| --- | ---: | ---: | ---: | ---: |
| Milder disease | 20 | 110 | 80 | 120 |
| More severe disease | 80 | 150 | 20 | 160 |

Blood pressure is in mmHg. The values 110, 120, 150, and 160 are **within-group means at one year**, not baseline pressures or identical values for everyone in a group.

Directly comparing all initiators with all noninitiators gives:

$$
\text{Crude mean among initiators}=\frac{20\times110+80\times150}{100}=142,
$$

$$
\text{Crude mean among noninitiators}=\frac{80\times120+20\times160}{100}=128.
$$

Each term is “number in the stratum × its mean blood pressure.” Adding gives the group’s total blood pressure, then dividing by its 100 people gives the mean. The crude difference is $$142-128=+14$$ mmHg, apparently suggesting that initiation raises blood pressure by 14.

The counts reveal why: 80% of initiators have more severe disease, compared with only 20% of noninitiators. **The groups differ in both treatment and their original health composition.** In this teaching scenario, health affects both initiation and future blood pressure, making it a confounder.

We cannot therefore call +14 the treatment effect. The next question is what to compare to have a chance of separating health differences from treatment effects.

## 2. What does g-estimation estimate?
{: #section-2 }

The actual question is: **For the same target population, how much would average blood pressure at one year differ if everyone initiated today versus if nobody initiated today?**

Each person can experience only one scenario, so the other potential outcome is missing from observed data. Using other people’s records to supply comparison information requires conditions: after sufficient pretreatment information is given, the groups should be comparable. Here we temporarily assume the table’s “milder/more severe” categories contain all necessary confounding information. That is a teaching assumption, not something a real study could prove from this table alone.

Fix the notation we will use throughout:

| Symbol | Meaning in this example |
| --- | --- |
| $$A$$ | Initiation today: 1 for initiate, 0 for do not initiate; no units |
| $$L$$ | Health before the decision, here “milder” or “more severe”; in a real study it may be a set of confounding variables |
| $$Y$$ | Actual blood pressure measured at one year, in mmHg |
| $$Y^1$$ | This person’s potential blood pressure at one year if they initiated today |
| $$Y^0$$ | This person’s potential blood pressure at one year if they did not initiate today |
| $$\psi$$ | Pronounced psi: the effect parameter to estimate, in mmHg, defined as “initiate minus do not initiate” |

The superscripts in $$Y^1$$ and $$Y^0$$ label interventions; they are neither powers nor times. $$Y^1-Y^0$$ is the same person’s blood-pressure difference between two intervention scenarios, not “post-treatment minus pretreatment blood pressure.” For example, $$\psi=-10$$ means an average reduction of 10, not a post-treatment blood pressure of −10.

**The introductory idea of g-estimation is to specify an unknown parameter for the average treatment effect, then find a value compatible with the data and causal assumptions.** We begin with the simple model “the average effect is the same in each health stratum”; model terminology and longitudinal extensions come in §6. It does not require identical treatment responses for everyone.

You may already wonder: “If we can compare people with the same health, why not simply subtract the group means? Why subtract an effect?” In this small two-stratum table, direct comparison is indeed possible. The hand-calculable example shows how g-estimation recasts such comparisons as an extensible parameter-estimation method; it does not imply that simple problems require complicated algorithms.

## 3. Why can we “subtract a candidate effect first”?
{: #section-3 }

### 3.1 First distinguish what should be equal after handling confounding
{: #section-4 }

Focus on the milder-disease stratum. If confounding has been adequately handled, actual initiators and noninitiators should have the same average blood pressure at one year **if neither group initiated**. This statement compares both groups in the same no-initiation scenario.

In reality, however, one group initiated and the other did not. Even after confounding is handled, their **actual blood pressures can still differ because of treatment**. Here their means are 110 and 120; that difference does not automatically mean “confounding remains.”

In potential-outcome notation:

$$
E[Y^0\mid A=1,L]=E[Y^0\mid A=0,L].
$$

Read each component: $$E[\cdot]$$ means an average, $$\mid$$ means “given,” and the comma means conditioning on several things simultaneously. The left asks about average blood pressure “if not initiating” ($$Y^0$$) among actual initiators ($$A=1$$); the right asks the same question among actual noninitiators ($$A=0$$). The $$L$$ on both sides must describe the same health. **The superscript 0 specifies the hypothetical action; the A in the condition specifies the actual group.**

What permits this comparison? We assume conditional exchangeability:

$$
Y^a\perp A\mid L,\qquad a=0,1.
$$

Here $$a$$ is the intervention value, either 0 or 1; $$Y^a$$ is potential blood pressure in that scenario; $$\perp$$ denotes statistical independence. The statement means that, given sufficient $$L$$, actual treatment choice provides no additional information about the corresponding potential blood pressure. It is an assumption about potential outcomes; **it does not require observed blood pressure Y to be unrelated to treatment A**. Consistency is also required: when an action is actually taken, the observed outcome corresponds to the potential outcome under that action.

We now have a common reference: average blood pressure under “no initiation” within the same health stratum. But initiators have already received treatment, so their observed blood pressure cannot directly stand for blood pressure without initiation. This motivates the next transformation.

### 3.2 Use a candidate effect to put observed outcomes on a common reference
{: #section-5 }

Consider the milder stratum’s means: 110 for initiators and 120 for noninitiators. **If we tentatively suppose treatment lowers blood pressure by 10 on average, removing that reduction requires adding 10 back to the initiators’ 110, giving 120.** Noninitiators have no effect of today’s initiation to remove, so they remain at 120.

This is not “before–after arithmetic.” We are still working with one-year outcomes, using an effect model to try to transform initiators’ observed mean to the no-initiation reference.

The data must be able to contradict the candidate effect. Guessing a reduction of 5 changes 110 only to 115, leaving a difference of 5; guessing a reduction of 15 changes it to 125, overshooting the noninitiators’ 120. This suggests a parameter-estimation procedure: **try different effects and check whether transformed means within each health stratum satisfy the common-reference requirement.**

The simple effect model is:

$$
E[Y^1-Y^0\mid L]=\psi.
$$

$$Y^1-Y^0$$ is an individual’s blood-pressure difference between intervention scenarios; $$E[\cdot\mid L]$$ averages these differences among people with the same health. A single $$\psi$$ on the right assumes the same average effect in the milder and more severe strata. Square brackets identify what is averaged, not multiplication.

The model constrains **each stratum’s average effect**, not every person’s response. If average effects vary with health, the parameter or effect function must be allowed to vary with $$L$$; a constant model is not a universal fact.

### 3.3 Write the operation as H(ψ)
{: #section-6 }

Name the “outcome transformed using a candidate effect” $$H(\psi)$$:

$$
H(\psi)=Y-\psi A.
$$

#### Reading H symbol by symbol: How is an actual observation transformed?
{: #section-7 }

The formula says: **transformed outcome = observed outcome − candidate treatment contribution.**

- $$Y$$ is the recorded one-year blood pressure and $$A$$ the recorded initiation status; these records stay unchanged as candidate values are tried.
- $$\psi$$ is the effect being tried; $$\psi A$$ multiplies it by the initiation indicator. Its unit remains mmHg, so it can be subtracted from blood pressure.
- $$H$$ is a newly calculated variable, also in mmHg, not a newly measured blood pressure.
- Parentheses in $$H(\psi)$$ mean “H depends on the candidate parameter,” not H multiplied by $$\psi$$; $$\psi A$$ on the right is multiplication.

Since A takes only 0 or 1, this is:

$$
H(\psi)=
\begin{cases}
Y-\psi, & A=1,\\
Y, & A=0.
\end{cases}
$$

The brace means choose the row matching the condition: subtract the candidate effect for initiators and retain the original value for noninitiators. Do not add the two rows. A zero transformation term for a noninitiator **does not mean that person would have no treatment benefit if they initiated**; it means they did not actually take today’s initiation action.

#### Why does subtracting −10 add 10 back?
{: #section-8 }

For example, take an initiator’s record $$A=1,Y=110$$ and candidate effect $$\psi=-10$$:

$$
H(-10)=110-(-10)\times1=120.
$$

A reduction of 10 has the signed value −10. Removing that change means subtracting −10, which adds 10 back. For a noninitiator’s record $$A=0,Y=120$$:

$$
H(-10)=120-(-10)\times0=120.
$$

These individual records merely illustrate the calculation. The original table contains group means and does not require everyone’s value to be exactly 110 or 120. Since the same candidate value is subtracted from every initiator within a stratum, **the group’s mean H also equals its original mean minus that value**.

#### Why write H(ψ) rather than just H?
{: #section-9 }

For the same record $$A=1,Y=110$$, choosing $$\psi=0,-5,-10,-15$$ gives H values 110, 115, 120, and 125. The candidate parameter and computed result change; the original treatment record and measured blood pressure do not.

The formula itself therefore does not tell us the drug’s effect. It only tells us **how to transform outcomes if the effect had a particular value**. The next section uses all the data to check candidates. Removing treatment effects according to an effect model is often called *blipping down*.

<aside class="study-callout study-callout--warning" markdown="1">

**The transformed value is not a recovered individual counterfactual**

Even if the average-effect model is correct, an actual initiator’s H cannot be said to equal their true individual $$Y^0$$. Some may have reductions of 5 and others 15, averaging 10; adding 10 back to everyone does not recover each person’s other future. For actual noninitiators, consistency already gives $$H=Y=Y^0$$.

We use a **relationship between conditional means**. We have not learned everyone’s counterfactual, nor guaranteed equality of the groups’ entire distributions.

</aside>


<details class="study-callout" markdown="1">
<summary>Second reading: What is the full mean restriction at the correct parameter?</summary>

Denote the model’s true but unknown parameter by $$\psi_0$$. The subscript 0 simply marks “the true parameter,” not time or the untreated group. An arbitrary candidate is $$\psi$$, and the sample estimate below is $$\widehat\psi$$.

$$
E[H(\psi_0)\mid A,L]=E[Y^0\mid L]=E[H(\psi_0)\mid L].
$$

The left averages H within actual-treatment and health strata; the middle is the potential mean if everyone in the health stratum did not initiate; the right averages H by health alone. Equality means that, given L, additionally knowing actual A does not change H’s conditional mean.

The reasoning is that consistency and exchangeability let the initiators’ observed mean represent the initiation scenario and the noninitiators’ observed mean represent the no-initiation scenario within a stratum. The average-effect model specifies their difference as $$\psi_0$$. Subtracting that difference from initiators gives the no-initiation reference mean. No step requires identical individual effects.

</details>


For this interpretation of mean models, compare [Vansteelandt and Joffe (2014), §2–§3](https://arxiv.org/html/1503.01589v1).

## 4. Find the effect using the 200-person teaching example
{: #section-10 }

### 4.1 Return from the crude comparison to comparisons within health strata
{: #section-11 }

Return to the data in §1. The crude +14 difference mixes different health compositions, so examine the milder and more severe strata separately. For now, treat the table’s means as exact population relationships, without sampling error.

Initiator and noninitiator means are 110 and 120 in the milder stratum, and 150 and 160 in the more severe stratum. A shared effect parameter should satisfy the model restriction in both strata, not merely fit one.

### 4.2 Try candidate effects one by one
{: #section-12 }

| Candidate $$\psi$$ (mmHg) | Milder: initiators’ mean H | Milder: noninitiators’ mean H | More severe: initiators’ mean H | More severe: noninitiators’ mean H | Equal means within each stratum? |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 110 | 120 | 150 | 160 | No; 10 lower in both |
| −5 | 115 | 120 | 155 | 160 | No; 5 lower in both |
| **−10** | **120** | **120** | **160** | **160** | **Yes, equal in both** |
| −15 | 125 | 120 | 165 | 160 | No; 5 higher in both |

Each row does the same thing: subtract $$\psi$$ from initiators’ means and leave noninitiators unchanged. Thus −10 is compatible with both strata’s data and the common-effect model.

**The result means that, under this example’s identification assumptions and effect model, baseline initiation lowers mean blood pressure at one year by 10 mmHg compared with no initiation.** It does not say the two actual groups’ crude means differ by −10, much less that everyone’s blood pressure falls by 10.

This also answers “why subtract the effect of an effective treatment?” We do not assume treated and untreated people should have equal actual blood pressure. We use a **mean relationship that should hold after removing treatment’s effect**, working backward to estimate how much must be removed.

### 4.3 Why must we say “given L”?
{: #section-13 }

At $$\psi=-10$$, both H means equal 120 in the milder stratum and 160 in the more severe stratum. Yet recombining the strata gives $$142+10=152$$ for all initiators’ mean H, while all noninitiators remain at 128.

There is no contradiction: initiators still contain more people with severe disease. The H transformation does not change population composition. The method requires **equal means within the same health stratum**, not unconditionally equal group-wide means; it also does not require milder and more severe patients to have equal blood pressure.

Check this using standardization. Half of the 200-person target population has milder disease and half more severe disease:

- If everyone initiated, mean blood pressure would be $$0.5\times110+0.5\times150=130$$.
- If nobody initiated, it would be $$0.5\times120+0.5\times160=140$$.
- Comparing the same target population’s two scenarios gives $$130-140=-10$$ mmHg.

Here 0.5 is each health stratum’s share of the target population. The values 130 and 140 are standardized intervention means; 142 and 128 are the original groups’ crude means; 152 and 128 are crude H means. **These three calculations answer different questions and should not be conflated.**

<aside class="study-callout study-callout--check" markdown="1">

**Pause to confirm three statements**

Handling confounding justifies causal comparisons within health strata; subtracting a candidate effect constructs a new variable that should satisfy model restrictions; finding an appropriate candidate estimates the effect under those assumptions. The last two steps cannot prove that the first succeeded.

</aside>


## 5. How are parameters estimated in an actual analysis?
{: #section-14 }

In a two-stratum table, candidate values can be checked by eye. Real data may have many confounders, making manual stratification and trial values impractical. We therefore need a computational rule for “combining H mean differences within the same health categories.” That is the purpose of the estimating equation below.

### 5.1 Estimate treatment probabilities
{: #section-15 }

First ask what proportion initiates in each health category: $$20/100=0.2$$ in the milder stratum and $$80/100=0.8$$ in the more severe stratum. Denote this probability:

$$
e(L)=P(A=1\mid L).
$$

$$P$$ means probability; $$A=1$$ is actual initiation; $$\mid L$$ means given health. Lowercase $$e$$ names the probability function; it is neither uppercase $$E$$ for an average nor the mathematical constant. $$e(L)$$ lies between 0 and 1, has no units, and is usually called the **propensity score**.

Subtract each person’s stratum-specific initiation probability from their actual initiation indicator to obtain $$A-e(L)$$, the treatment-choice residual. Why subtract? Examine the four groups:

| Health and action | Number | Each person’s $$A-e(L)$$ | Number × residual |
| --- | ---: | ---: | ---: |
| Milder, initiate | 20 | $$1-0.2=0.8$$ | +16 |
| Milder, do not initiate | 80 | $$0-0.2=-0.2$$ | −16 |
| More severe, initiate | 80 | $$1-0.8=0.2$$ | +16 |
| More severe, do not initiate | 20 | $$0-0.8=-0.8$$ | −16 |

**Within each health stratum, initiators’ total positive contribution exactly balances noninitiators’ total negative contribution.** Although counts differ, this operation produces paired coefficients for comparing the two means. It is not IPW’s inverse probability; both methods use treatment probabilities differently.

### 5.2 Replace manual trial values with an estimating equation
{: #section-16 }

Now multiply each person’s residual by their H and sum within the stratum. From the previous table, the milder stratum contributes:

$$
16\times\text{Mean H among milder initiators}
-16\times\text{Mean H among milder noninitiators}.
$$

This combines “number × residual × mean H” and equals **16 times the within-stratum difference in mean H**. The more severe stratum also contributes 16 times its within-stratum difference. At candidate $$\psi=-5$$, both mean differences are −5, so the total is $$16\times(-5)+16\times(-5)=-160$$.

The manual candidate table therefore becomes:

| Candidate $$\psi$$ | Milder-stratum mean difference | More-severe-stratum mean difference | Total contribution |
| ---: | ---: | ---: | ---: |
| 0 | −10 | −10 | −320 |
| −5 | −5 | −5 | −160 |
| **−10** | **0** | **0** | **0** |
| −15 | +5 | +5 | +160 |

Set this sum to zero and solve for the candidate parameter. The formula simply compresses those operations into one line:

$$
\sum_i\{A_i-\widehat e(L_i)\}\{Y_i-\psi A_i\}=0.
$$

Read in computational order: **for each person, calculate the treatment residual and H, multiply them, then sum over everyone; find ψ that makes this sum zero.**

| Formula component | How to read it |
| --- | --- |
| $$i$$ | Patient index from 1 to sample size $$n$$; here $$n=200$$, not a time index |
| $$A_i,L_i,Y_i$$ | Person i’s actual initiation status, health, and one-year blood pressure |
| $$\widehat e(L_i)$$ | Their initiation probability estimated from the sample; the hat marks an estimate. A treatment-probability model can handle multiple variables |
| $$A_i-\widehat e(L_i)$$ | Actual initiation indicator minus predicted probability, without units |
| $$Y_i-\psi A_i$$ | Their transformed blood pressure, also written $$H_i(\psi)$$, in mmHg |
| The two adjacent braces | Calculate each expression, then multiply |
| $$\sum_i$$ | Sum the 200 products; shorthand for $$\sum_{i=1}^{200}$$ |
| $$=0$$ | The total is zero—not every individual product, and not necessarily the treatment effect |

We need not literally try every candidate. Expanding and rearranging gives a direct solution when the denominator is nonzero:

$$
\widehat\psi=
\frac{\sum_i\{A_i-\widehat e(L_i)\}Y_i}
{\sum_i\{A_i-\widehat e(L_i)\}A_i}.
$$

$$\widehat\psi$$ is the finite-sample effect estimate. The numerator sums “residual × observed blood pressure”; the denominator sums “residual × initiation indicator.” The symbols retain their meanings above. The numerator has units of mmHg and the denominator none, so the ratio is in mmHg.

Substituting the example:

| Health stratum | Numerator contribution | Denominator contribution |
| --- | ---: | ---: |
| Milder | $$20\times0.8\times110-80\times0.2\times120=-160$$ | $$20\times0.8\times1+80\times(-0.2)\times0=16$$ |
| More severe | $$80\times0.2\times150-20\times0.8\times160=-160$$ | $$80\times0.2\times1+20\times(-0.8)\times0=16$$ |
| Total | −320 | 32 |

Thus $$\widehat\psi=-320/32=-10$$ mmHg, matching the manual table. A zero denominator prevents this division: without sufficient variation in treatment actions, an equation cannot create comparison information. More complex effect models may require several equations and numerical solutions.

<details class="study-callout" markdown="1">
<summary>Second reading: From sample calculations back to population conditions</summary>

At the true parameter, H’s conditional mean does not vary with A, and $$E[A-e(L)\mid L]=0$$. The latter says that the average initiation indicator within a stratum equals its initiation probability, so subtracting that probability leaves a mean residual of zero. Hence $$E[\{A-e(L)\}H(\psi_0)\mid L]=0$$, and averaging over strata also gives zero.

This second expression averages “residual times H.” It holds because, within a stratum, H has the same conditional mean regardless of actual initiation. Factoring out that mean leaves the residual whose average is zero. These expressions use the true probability $$e(L)$$, true parameter $$\psi_0$$, and population expectation $$E$$. An actual analysis constructs their sample counterpart using estimated probabilities, sample sums, and the parameter to be solved for.

</details>


### 5.3 Obtaining zero association does not verify absence of confounding
{: #section-17 }

Distinguish two statements: **if every health stratum’s H mean difference is zero, the total is zero; a zero total does not guarantee zero differences in every stratum.** In this example both strata share the same average effect, so −10 satisfies both restrictions. If effects differ by health, a constant can yield a positive difference in one stratum and a negative difference in another that cancel. Then the effect model and target quantity need reconsideration; the solution is not automatically the target population’s average effect.

Unmeasured confounding is more fundamental. If the groups are not comparable within the same health category, the algorithm may still find a number that zeros the sample equation, but cannot establish exchangeability. **Finding a solution completes a calculation; obtaining the intended causal interpretation still depends on assumptions and design.**

The basic estimator here depends on the treatment-probability model, effect model, and corresponding identification assumptions. Auxiliary outcome models can yield more efficient or doubly robust versions, but those properties are not automatic for every form of g-estimation. A real analysis must also report standard errors or confidence intervals, using an appropriate estimating-equation variance or bootstrap that refits all models. This teaching table supplies no precision information for a real study.

For advanced methods, see [What If, Chapter 14 and companion code](https://miguelhernan.org/whatifbook) and [Vansteelandt and Joffe, §3.2](https://arxiv.org/html/1503.01589v1).

## 6. How do longitudinal treatments connect to “common treatment history”?
{: #section-18 }

So far we have considered a single initiation decision today. This is a simple special case of a structural mean model (SMM): the model describes average causal effects between potential outcomes, while g-estimation uses data to estimate its parameters.

Sustained-medication studies must also address repeated decisions, such as “initiate today, then continue or stop next month.” Later decisions depend on current health, which may itself depend on previous treatment. A one-time transformation using only baseline L cannot directly handle that whole process.

Consider two decision times:

```text
L₀ (initial health) → A₀ (first treatment decision) → L₁ (subsequent health) → A₁ (second decision) → Y
```

This depicts temporal ordering, not a complete DAG. In our scenario, $$A_0$$ can affect $$L_1$$, and $$L_1$$ affects $$A_1$$ and $$Y$$, creating treatment–confounder feedback.

At the second decision, incorporate the history already accumulated:

$$
\mathcal H_1=(L_0,A_0,L_1).
$$

$$\mathcal H$$ names the “set of historical information”; the calligraphic font distinguishes it from transformed outcome $$H$$. Subscript 1 marks history before the second treatment decision. Commas group variables together, rather than adding or multiplying them: $$L_0$$ is health before the first decision, $$A_0$$ the first action, and $$L_1$$ updated health before the second decision. $$A_1$$ is the action currently being decided, so it is not part of the **predecision** history; $$Y$$ occurs afterward.

Subscripts 0 and 1 here index decision times, unlike patient index $$i$$ or the true-parameter label $$\psi_0$$. For example, $$A_1=0$$ means “choose no treatment at the second decision”; 0 is the action value, and 1 the time index. Arrows in the temporal sketch indicate ordering; direct causal effects require separate judgment based on the research question.

Remember that $$\mathcal H_1$$ denotes medical history, whereas the earlier $$H(\psi)$$ is a transformed outcome.

- Among those not previously taking medication, one can study initiating versus not initiating now.
- Among those already taking medication, one can study continuing versus stopping now.
- Observational analysis must also handle health and other confounders before the current decision, not merely distinguish “previous use/no previous use.”

This setting uses a structural nested mean model (SNMM). **Structural** means the model targets causal effects; **mean** indicates average outcomes; **nested** organizes repeated strategy differences into history-specific effect contrasts at each decision. A longitudinal model describes **how changing treatment at one time changes the mean outcome, given the past and a clearly specified common reference strategy for subsequent treatment**. Without specifying later actions, the effect contrast at that decision is not defined.

Why often reason backward? The final observed Y is affected by both early and late treatment. To ask about an early decision’s effect when the model specifies a common later reference strategy, later treatment differences must first be handled according to the model. We can therefore consider the last treatment first, estimate its effect given history at that time, and construct an outcome with that effect removed; then use earlier history to address earlier treatment. Algorithms can also solve parameters jointly rather than literally fitting each stage by hand.

This is not simply repeating the single-treatment formula, nor gradually reconstructing each person’s “never-treated life.” Every step depends on the appropriate effect model, past history, subsequent reference strategy, and identification assumptions.

It differs from “putting $$A_0,A_1,L_1$$ into an ordinary outcome regression and calling the $$A_0$$ coefficient the total effect.” For later treatment, $$L_1$$ is prior information; for earlier treatment, it may be a post-treatment intermediate variable. G-estimation organizes these conditions using treatment-choice mechanisms and effect models at each time; all histories cannot be merged into one baseline adjustment set.

The theoretical link is **sequential exchangeability**: at each treatment decision, conditioning on sufficient prior treatment and covariate history supplies the corresponding no-unmeasured-confounding condition. Conditioning does not require finding two people with exactly identical histories; models can implement it.

See [Vansteelandt and Joffe, §5–§6](https://arxiv.org/html/1503.01589v1) for longitudinal definitions and restrictions, and [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}) for background.

## 7. Differences from the g-formula and IPW
{: #section-19 }

The table compares basic introductory implementations; it does not imply that the methods cannot be combined.

| Method | Main computational idea | How does it use this example’s data? |
| --- | --- | --- |
| G-formula / standardization | Estimate an outcome model, predict under specified interventions, and average; also handle covariate development longitudinally | Predict blood pressure under treatment and no treatment for the same target population |
| IPW | Estimate treatment-choice probabilities and reaggregate observed outcomes using appropriate inverse-probability weights | Change each record’s representation in the treated–untreated comparison |
| G-estimation | Specify a causal-effect model and construct estimating equations using the treatment mechanism and outcomes with effects removed | Find effect parameter $$\psi$$ satisfying conditional-mean restrictions |

All three methods can estimate the same −10 mmHg average effect here. In real studies, different target parameters, models, and samples may produce different results. In particular, when effects vary with history, an SNMM’s conditional-effect parameter is not automatically the population-average strategy effect; further aggregation over a specified target population may be necessary.

**A structural nested model is a model; g-estimation is an estimation method.** Likewise, a marginal structural model is a model, and IPW is one common way to estimate it. Distinguish model names, estimation methods, and target quantities; see [Causal Contrasts and Estimands]({{ "/causal-inference/causal-contrasts-estimands/" | relative_url }}).

## 8. What conditions are needed?
{: #section-20 }

| Condition | An introductory interpretation |
| --- | --- |
| Clear strategies and consistency | Specify initiation, continuation, discontinuation, and subsequent rules; observed records must correspond to the interventions |
| Conditional / sequential exchangeability | The basic no-unmeasured-confounding version needs sufficient predecision confounder information; identical treatment history alone is insufficient |
| Sufficient treatment variation and positivity support | Relevant histories must contain information for comparing different actions; if everyone in a category necessarily receives the same treatment, formulas cannot create evidence |
| An appropriate effect model | Assumptions such as constant mean effects or health-dependent effects must suit the question; misspecification may alter interpretation or introduce bias |
| Auxiliary-model conditions for the particular estimator | The basic version here needs reliable treatment probabilities; other versions have their own model-correctness requirements |
| Reliable measurement and censoring adjustment | Loss to follow-up, measurement error, and an incorrect follow-up origin cannot be ignored |

Some structural models use restrictions such as homogeneity to extrapolate from populations with treatment variation to others. That depends on additional modeling assumptions and does not mean “g-estimation needs no data support.” Instrumental-variable g-estimation also exists but uses different identification conditions; it is not an automatic solution to unmeasured confounding. This note describes the version relying on conditional/sequential exchangeability.

## 9. Self-check
{: #section-21 }

1. Why does the original crude difference of +14 not directly mean that treatment raises blood pressure by 14?
2. After controlling confounding, can actual blood pressure still differ because of treatment?
3. If the candidate average reduction is 10, why add 10 back to initiators? Does that establish their individual untreated blood pressures?
4. At the correct candidate, why is all initiators’ mean H of 152 still different from noninitiators’ 128?
5. What exactly does “residual × H” aggregate in the estimating equation?
6. Does a parameter yielding a zero sum prove that every stratum fits, or that there is no unmeasured confounding?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. Initiators include more people with severe disease, so the crude difference mixes treatment effects and health-composition differences.
2. Yes. Exchangeability requires comparable potential outcomes under the same intervention within health strata, not identical observed outcomes for two groups actually receiving different treatments.
3. A reduction of 10 means $$\psi=-10$$; removing it subtracts −10. A mean model does not guarantee that an actual initiator’s H equals their true individual $$Y^0$$.
4. The transformation does not change the groups’ health compositions. The restriction holds given L, rather than requiring equal crude population means.
5. Each stratum contributes 16 times its within-stratum H mean difference in this example, then contributions are summed across strata.
6. Neither. Stratum-specific differences can cancel, and an equation may still yield a number under incorrect causal or modeling assumptions.

</details>


## 10. What does the source article mean by “common treatment history”?
{: #section-22 }

When introducing target trials of initiating and discontinuing treatment, Hernán and Robins note that both compare people who share a common treatment history at baseline, connecting this to the basic idea of g-estimation. The passage can be rendered as:

> Incidentally, both target trials compare people with a common treatment history at baseline: nonusers in the original trial and users in the reversed trial. This reflects the basic idea of g-estimation.

Here **both target trials** refers to two separate trials, not a direct comparison of participants across them:

| Trial | Common starting point within the trial | Actions compared from that point |
| --- | --- | --- |
| Original trial | Everyone meets the protocol’s nonuse criterion | Initiate use or do not initiate |
| Reversed trial | Everyone is currently receiving treatment at baseline | Continue use or stop use |

In the original hormone-therapy protocol, nonuse means no use during the previous two years, not automatically lifetime never-use. Discontinuers in the reversed trial also have prior treatment histories and therefore are not never users.

**A common treatment history emphasizes asking, within the same prior-treatment context, “what happens if we take different treatment actions next?”** It does not require identical ages, diseases, doses, or complete life histories. If such differences confound the current action–outcome relationship, observational analysis must still handle them appropriately; “everyone is currently taking medication” alone does not ensure exchangeability.

For the current-user issue, see [Hormone therapy, depletion of susceptibles, and history that cannot be randomized]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}#section-18). Nor does this imply that “the effect of initiation” must be the negative of “the effect of stopping”: the trials differ in target population, previous exposure, and risk stage.

<aside class="study-callout study-callout--important" markdown="1">

**Design intuition does not complete estimation**

The authors use a brief aside to connect a methodological idea. Simply splitting nonusers into initiators/noninitiators, or current users into continuers/discontinuers, does not implement g-estimation. A causal-effect model must be specified and its parameters estimated using the treatment-choice mechanism and identification conditions.

</aside>


Source: [Hernán and Robins (2016), Assignment procedures, p. 760](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf). Reference 17 in the article points to Robins’s 1989 work on AIDS treatment trials and longitudinal causal inference.

## Sources and further reading
{: #section-23 }

- [Hernán MA, Robins JM. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available (2016)](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf): the original aside and the design context of treatment initiation and discontinuation.
- [Hernán MA, Robins JM. Causal Inference: What If, Chapter 14 and companion code](https://miguelhernan.org/whatifbook): an introduction to g-estimation through single treatments and structural mean models.
- [Vansteelandt S, Joffe M. Structural Nested Models and G-estimation: The Partially Realized Promise (2014)](https://arxiv.org/html/1503.01589v1): mean and distributional models, estimating equations, longitudinal extensions, and methodological conditions.
- Historical reference: Robins JM (1989). The analysis of randomized and non-randomized AIDS treatment trials using a new approach to causal inference in longitudinal studies. In: *Health Services Research Methodology: A Focus on AIDS*, pp. 113–159. Bibliographic details here follow reference 17 in Hernán and Robins (2016).

The blood-pressure data and calculations in this note are teaching examples and do not represent actual drug effects.
