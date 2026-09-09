---
layout: "causal-note"
title: "The G-Formula: From Standardization to Longitudinal Strategies"
description: "Predict and average over the same population, from a 1,000-person standardization example to longitudinal treatment rules."
group: "Estimation"
order: 13
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Why not directly compare the two groups’ proportions of deaths?", "anchor": "section-1"}, {"title": "2. Calculating the baseline g-formula by hand", "anchor": "section-2"}, {"title": "3. Writing the calculation as a formula", "anchor": "section-7"}, {"title": "4. What if health status has more than two values, “high” and “low”?", "anchor": "section-8"}, {"title": "5. Why do sustained strategies require a “longitudinal” g-formula?", "anchor": "section-13"}, {"title": "6. Two treatment decisions: Putting numbers into the longitudinal formula", "anchor": "section-14"}, {"title": "7. The longitudinal formula and the actual computational workflow", "anchor": "section-19"}, {"title": "8. What if the outcome is death and some people die along the way?", "anchor": "section-20"}, {"title": "9. Why is “calculating two worlds” not enough?", "anchor": "section-21"}, {"title": "10. Differences from IPW and Cox", "anchor": "section-22"}, {"title": "11. Self-check", "anchor": "section-23"}, {"title": "References", "anchor": "section-24"}]
previous_note: "/causal-inference/cox-proportional-hazards/"
next_note: "/causal-inference/inverse-probability-weighting/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

If subscripts, superscripts, and probability notation are still unfamiliar, use [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}) alongside this note. The notation is also explained wherever formulas appear; you do not need to finish studying mathematical notation before reading the examples.

Prerequisite for the baseline section: [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}). Prerequisite for the longitudinal section: [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}). Companion calculations: [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}); survival outcome models: [The Cox Proportional Hazards Model: Risk Sets, Estimation, and Bias]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Begin with a question**

We want to know how much difference there would be between “everyone in the same population receives treatment” and “everyone in that population does not receive treatment.” Yet the data contain some treated and some untreated people, and their health differs. How can such data answer the original question?

**The g-formula first estimates outcome risks under treatment and no treatment among people with the same health status, then applies those risks to one common target population to predict its average outcome under each intervention.**

If treatment changes subsequent health and further treatment decisions follow, we also predict how health develops and calculate forward, step by step, under the strategy.

</aside>


All numbers in this note are teaching examples, not real drug effects. We initially ignore loss to follow-up, measurement error, and sampling uncertainty to make the algorithm easier to understand; §9 discusses the assumptions required for a causal interpretation.

**On a first reading, master the standardization example in §1–4, then use §5 to move into the two treatment decisions in §6.** Each passage resolves a problem left by the previous one: why a crude comparison is insufficient → where usable risks come from → how to reconstruct a common target population → how to continue when treatment changes health. The formulas in §3 and §7 simply record the operations already performed; you can understand the examples first and then match the symbols to them.

## 1. Why not directly compare the two groups’ proportions of deaths?
{: #section-1 }

In [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}), a causal effect is defined as a contrast between outcomes under different interventions for the same individual or target population. The g-formula addresses the next computational question: **We can observe only the situation each person actually experienced. How can those data estimate the two possible outcomes for the whole target population?**

The specific question here is: “Among these 1,000 eligible patients, how much would one-year mortality risk differ if everyone initiated treatment at baseline versus if everyone did not initiate treatment at baseline?”

- $$A=1$$: initiate treatment at baseline; $$A=0$$: do not initiate at baseline. This example intervenes only on the baseline action; subsequent treatment follows its usual course in each intervention world.
- $$L$$: pretreatment health status, classified as low risk or high risk.
- $$Y=1$$: death within one year; $$Y=0$$: no death within one year.
- The target population contains 500 low-risk and 500 high-risk patients, each accounting for 50%.

The observed data are:

| Pretreatment health status $$L$$ | Treatment $$A$$ | Number of patients | Deaths | One-year mortality risk |
| --- | ---: | ---: | ---: | ---: |
| Low risk | 1 | 100 | 5 | 5% |
| Low risk | 0 | 400 | 40 | 10% |
| High risk | 1 | 400 | 80 | 20% |
| High risk | 0 | 100 | 40 | 40% |

Without adjustment:

Each fraction below is “number of deaths ÷ total number in that group.” The plus signs in the numerator and denominator combine the low- and high-risk strata; they do not add the two strata’s mortality percentages directly.

$$
\text{Risk in the treated group}=\frac{5+80}{100+400}=17\%,
$$

$$
\text{Risk in the control group}=\frac{40+40}{400+100}=16\%.
$$

The treated group appears to have a risk 1 percentage point higher. However, 80% of treated patients are high risk, compared with only 20% of controls. The actual treated and untreated groups do not represent the “same population’s outcomes under two interventions” that we want to compare. They represent **outcomes in two populations that already differed**.

Returning to the table, among low-risk patients, treated patients have a 5% risk and untreated patients a 10% risk; among high-risk patients, the corresponding risks are 20% and 40%. Why is the treated risk lower within both strata but higher after combining them? Because the crude comparison gives the two health categories different weights: the treated group mainly consists of high-risk patients who were already more likely to die. It mixes treatment differences with pre-existing health differences.

We therefore need to do two things: first obtain stratum-specific risks, such as “what happens to treated low-risk patients” and “what happens to treated high-risk patients,” then combine them using the original population’s equal proportions of low- and high-risk patients. The g-formula asks: **What would happen if both intervention worlds began with these original 1,000 people?** What we hold common is the pretreatment health distribution; post-treatment health need not be the same.

## 2. Calculating the baseline g-formula by hand
{: #section-2 }

### Step 1: Estimate the risk for each health category under each treatment
{: #section-3 }

The table gives four conditional risks:

| Health status | Risk among those actually treated | Risk among those actually untreated |
| --- | ---: | ---: |
| Low risk | 5% | 10% |
| High risk | 20% | 40% |

These are initially still observed risks. For example, 5% is the proportion of deaths among “the 100 low-risk patients who actually received treatment.” We want to use it to predict what would happen **if all 500 low-risk patients received treatment**. That step requires a justification; we cannot simply skip over it.

The justification is baseline conditional exchangeability: provided that health status $$L$$ sufficiently controls confounding, treatment choice within a health stratum provides no additional prognostic information about potential outcomes. Outcomes among actual treated patients can then help estimate the average outcome if everyone in the same stratum were treated; actual untreated patients can similarly help estimate the outcome if everyone in that stratum were untreated. We borrow the **average risk within a stratum**, without claiming that any two patients necessarily have identical individual outcomes.

Treatment must also be well defined, actual treatment must correspond to the specified intervention, and every stratum must contain data supporting both treatment and no treatment. If unmeasured disease differences that affect treatment and death remain within the low-risk stratum, 5% may not represent the risk if all low-risk patients received treatment. **Simply observing a lower treated risk in every stratum does not establish these identification conditions.** See §9 for the full conditions.

### Step 2: Place the entire target population in the treatment world
{: #section-4 }

With stratum-specific risks that can support intervention predictions, apply them to the original 1,000 people: 500 low risk and 500 high risk. Imagine everyone receives treatment, assigning the “low risk and treated” risk of 5% to low-risk patients and the “high risk and treated” risk of 20% to high-risk patients.

Retain the original baseline composition of 50% low risk and 50% high risk, because we are changing the treatment action rather than replacing the baseline population:

$$
\text{Risk if everyone is treated}
=0.5\times5\%+0.5\times20\%
=12.5\%.
$$

Equivalently, calculate expected counts: 25 deaths among the 500 low-risk patients and 100 among the 500 high-risk patients, totaling 125/1,000.

### Step 3: Place the same target population in the no-treatment world
{: #section-5 }

Step 2 provides the risk under one intervention, which is not yet a treatment effect. We need another prediction for **exactly the same 500 low-risk and 500 high-risk patients**. This time treatment is set to 0, so we use the table’s 10% risk for untreated low-risk patients and 40% for untreated high-risk patients. The population proportions remain 0.5 and 0.5.

$$
\text{Risk if everyone is untreated}
=0.5\times10\%+0.5\times40\%
=25\%.
$$

The expected number of deaths is 50+200=250, or 250/1,000.

### Step 4: Compare the two worlds
{: #section-6 }

Both numbers now refer to the same target population, outcome, and follow-up period, differing only in the assigned baseline action. Under the identification assumptions, we can interpret their difference or ratio as an intervention effect:

$$
RD=0.125-0.25=-0.125=-12.5\text{ percentage points},
$$

$$
RR=12.5\%/25\%=0.50.
$$

Here $$RD$$ is the risk difference, defined as “risk if everyone initiates minus risk if everyone does not initiate”; $$RR$$ is the risk ratio, defined as the former divided by the latter. $$0.125$$ and $$12.5\%$$ express the same risk. A negative risk difference means lower mortality risk under initiation; $$-0.125$$ on the percentage scale is **−12.5 percentage points**, not “a relative reduction of 12.5%.” A risk ratio of 0.50 means that the initiation strategy has half the reference strategy’s risk. A risk ratio has no units.

Under these assumptions and risk estimates, the prediction is that if the same 1,000 people all initiated treatment at baseline, there would be, on average, 125 fewer deaths within one year than if none initiated. It does not identify which specific 125 people would avoid death.

The estimates here are a **one-year risk difference and risk ratio**, not a Cox HR. The people in the two predicted worlds belong to the same target population; we have not actually observed both outcomes for each person.

## 3. Writing the calculation as a formula
{: #section-7 }

We completed the calculation without a complicated formula: **multiply each stratum’s risk by its population proportion, then add the contributions.** In statistics, this is called standardization: using a common population composition to combine risks under each treatment condition. The g-formula below records that operation and states when it can correspond to an outcome under intervention:

$$
\boxed{E[Y^a]=\sum_l E[Y\mid A=a,L=l]P(L=l)}.
$$

To translate each component, first distinguish variables from the values we assign:

- $$A$$ is the actual treatment variable; lowercase $$a$$ is the intervention value being evaluated. Here, $$a=1$$ means everyone initiates at baseline, and $$a=0$$ means everyone does not initiate at baseline.
- $$L$$ is baseline health status; lowercase $$l$$ successively takes the values “low risk” and “high risk.” $$L=l$$ means “health status belongs to the stratum currently being evaluated.”
- $$Y$$ is the actual one-year death indicator, with 1 for death and 0 for no death; $$Y^a$$ is the potential death indicator under intervention $$a$$. **The superscript $$a$$ labels the intervention; it is not an exponent.**
- $$E[\cdot]$$ denotes an expectation: an average in the relevant population. The quantity inside the brackets is what we average. $$E[Y^a]$$ is the average outcome if the entire target population receives $$a$$. Because death is recorded as 0 or 1 here, the average equals the proportion dying, so we can also write $$P(Y^a=1)$$, the mortality risk under that intervention. If $$Y$$ were blood pressure, $$E[Y^a]$$ would be average blood pressure, not mortality risk.
- $$P(\cdot)$$ denotes the probability of the event in parentheses, between 0 and 1. $$P(L=l)$$ is the proportion with that health status in the **target baseline population**.
- The vertical bar $$\mid$$ means “given” or “conditional on”; the comma means that the conditions hold simultaneously. Thus $$E[Y\mid A=a,L=l]$$ is the mean outcome **in the observed data** among people whose actual treatment is $$a$$ and health status is $$l$$—the proportion dying in this example.
- $$\sum_l$$ means adding one term for every value of $$l$$. Each term is “the stratum’s outcome risk × its proportion of the target population”; writing the two factors next to each other means multiplication, not another addition. For a continuous health variable, the corresponding operation uses integration or averages individual predictions.

Substituting $$a=1$$, the formula becomes: 5%, the risk among actual low-risk initiators, times the target low-risk proportion 0.5, plus 20%, the risk among actual high-risk initiators, times the target high-risk proportion 0.5, giving 12.5%. Substituting $$a=0$$ gives 25%.

**The equality connects two different things: a potential-outcome mean under intervention on the left and conditional risks from observed data on the right.** Treating the right-hand side as the left-hand side requires the identification assumptions in this note. Writing the observed condition $$A=a$$ in a formula does not itself confer a causal interpretation.

We must not instead average using $$P(L\mid A=1)$$ for the treated group and $$P(L\mid A=0)$$ for the control group, which would return us to the crude 17% versus 16% comparison. These expressions describe the actual initiators’ and noninitiators’ health distributions: 80% high risk in the former and only 20% in the latter, rather than one common target population’s baseline composition.

<aside class="study-callout study-callout--note" markdown="1">

**G-formula and g-computation**

The g-formula is first an **identification formula**: under the required conditions, it expresses a counterfactual target quantity as a function of the observed-data distribution.

G-computation often refers to the computational procedure for estimating that formula. The parametric g-formula usually estimates the required conditional distributions using a sequence of parametric models, followed by integration or simulation. These terms are sometimes used more loosely and interchangeably in the literature.

</aside>


For single-time-point standardization and identification conditions, see the relevant standardization chapters in [Hernán and Robins: What If](https://miguelhernan.org/whatifbook).

## 4. What if health status has more than two values, “high” and “low”?
{: #section-8 }

The hand calculation relied on a convenient condition: health had only two strata, high and low, each with enough observations. Real studies often need to consider age, kidney function, blood pressure, previous hospitalizations, and other variables simultaneously. Creating a separate cell for every combination produces many cells with very few or no people.

We need not abandon “predict within strata, then average over the same population.” We can replace the small table with an outcome model that estimates the mean outcome for different combinations of treatment and health:

$$
m(a,l)=E[Y\mid A=a,L=l].
$$

$$m$$ is the name we give the “conditional outcome mean function.” $$m(a,l)$$ means entering treatment value $$a$$ and health value $$l$$ into the function and obtaining the corresponding mean outcome. Here the output is mortality risk, for example $$m(1,\text{low risk})=0.05$$. Parentheses indicate function inputs, **not $$m$$ multiplied by $$a,l$$**. It is the same quantity as the conditional mean in §3.

We then perform the same standardization, using model predictions instead of table lookups. **Fitting a model and using it for intervention predictions are different operations**: fitting uses actual treatments and outcomes; only at prediction time do we set each person’s treatment input to 1 and 0.

The procedure is:

1. Fit a mortality risk model to the observed data, using treatment and sufficient baseline confounding information.
2. Retain each original person’s $$L_i$$, temporarily set the treatment input to 1, and predict $$\widehat m(1,L_i)$$.
3. Average everyone’s predictions to estimate the risk “if everyone were treated.”
4. Set $$A=0$$ for the same people, predict again, and average.
5. Compare the two averages.

$$
\widehat E[Y^a]=\frac1n\sum_{i=1}^n\widehat m(a,L_i).
$$

Read this as: “Calculate each person’s predicted risk when treatment is set to $$a$$, add the predictions, and divide by the number of people.” Specifically:

- $$n$$ is the number of people in the target sample used for standardization; here $$n=1{,}000$$.
- $$i$$ indexes people from 1 through $$n$$; it is not follow-up time. $$L_i$$ is person $$i$$’s baseline health information, which may contain several variables, such as age and blood pressure.
- A hat $$\widehat{\phantom m}$$ means “estimated from a finite sample.” $$\widehat m$$ is the fitted prediction function; $$\widehat E[Y^a]$$ estimates the true intervention mean $$E[Y^a]$$, rather than implying that the true value is already known.
- $$\widehat m(a,L_i)$$ is the prediction obtained by retaining person $$i$$’s baseline information and changing the treatment input to $$a$$. We change the model input; we do not actually change the patient’s treatment or observe their individual counterfactual.
- $$\sum_{i=1}^n$$ adds predictions for people 1 through $$n$$; $$1/n$$ converts the sum to an average. The formula gives everyone in the target sample equal weight; sampling or transport weights, if needed, would alter the averaging accordingly.

In the simple table example, setting $$a=1$$ gives a prediction of 0.05 for each of the 500 low-risk people and 0.20 for each of the 500 high-risk people. The average is $$(500\times0.05+500\times0.20)/1{,}000=0.125$$, exactly matching the stratified calculation in §2.

This is not the prediction for an “average patient” obtained by entering mean age and mean blood pressure. **The average of predictions** generally differs from **the prediction at average covariates**, especially in nonlinear models such as logistic regression.

Usually, reading off a treatment coefficient alone does not provide the desired population risk. For example, in logistic regression without relevant interactions, the treatment coefficient is the log of a conditional odds ratio (OR), and exponentiation gives the OR. Obtaining the population risks in this note—and then their risk difference or risk ratio—still requires the “predict for each person, then average” steps.

For survival outcomes with censoring, an appropriate survival model can be used; Cox is one possibility. The requirements for the outcome model, censoring adjustment, and causal identification must all be satisfied.

We have now solved the calculation for an intervention specifying only the baseline action. That does not yet answer a question about “treating at baseline and continuing according to a rule.” The latter intervention must include later treatment decisions, introducing another process we must handle: post-treatment changes in health.

### 4.1 A multivariable drug A versus drug B example: G-formula and IPTW answer the same question
{: #section-9 }

Use the same simulated data for 3,000 people as in [the complete multivariable logistic regression example: initiating drug A versus drug B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15). There are 1,119 drug A users and 1,881 drug B users. The comparison concerns one-year hospitalization risk if all eligible patients initiate A versus initiate B at baseline. Assume complete outcome ascertainment and an intervention on baseline initiation only; both groups receive an actual drug treatment.

**The g-formula predicts outcomes using medical history and treatment, then predicts and averages both the A and B strategies for the same people; IPTW predicts actual treatment choice using medical history and compares outcomes after weighting the actual A/B groups.** Here we compare outcome-regression-based g-computation at baseline with conventional IPTW. Strictly, the g-formula is an identification expression, while g-computation is an implementation for estimating it.

| Component | Outcome regression + g-computation | IPTW |
| --- | --- | --- |
| Model inputs | Baseline L and actual drug Z | Baseline L |
| Fitting label | One-year hospitalization Y | Drug choice Z |
| Predicted probability | Hospitalization risk under the specified drug | Probability of choosing A rather than B |
| After fitting | Hold each person’s L fixed, set the drug input to A and B, predict, and average | Retain each person’s actual drug and outcome; weight by the corresponding treatment probability |
| Is a train/test split required? | Not in the classical parametric implementation | Not in the classical parametric implementation |
| Main model risks | Outcome-model misspecification and extrapolation into unsupported regions | Treatment-probability-model misspecification and extreme weights |

Here Z=1 denotes A and Z=0 denotes B, and L=(age10,D,S,H), as in the IPTW example. age10=(age−70)/10; D is diabetes, S is continuous disease severity, and H is a history of background treatment C. Y is hospitalization: 1 if it occurred, 0 otherwise.

#### Fitting an actual outcome logistic regression to the same patients
{: #section-10 }

Fitting everyone’s actual L, Z, and Y together gives:

$$
\widehat m(z,L)=\frac{1}{1+\exp(-\widehat\eta_Y)},
$$

$$
\widehat\eta_Y=-2.123981-0.438381z+0.515036age10+0.409046D+0.570397S+0.008819H.
$$

m denotes the conditional outcome mean, here the hospitalization probability; z is the drug value entered into the model; η_Y is the outcome log-odds. All coefficients were fitted to the same simulated data. Hats indicate estimation. This logistic regression and IPTW’s logistic regression use the same people but fit different labels and have different coefficients. The drug coefficient is not the population risk difference; even its exponential cannot be read directly as a population risk ratio.

Next, calculate twice for each person:

1. Retain baseline age, diabetes, severity, and medical history; set the drug input to z=1 to obtain the predicted hospitalization risk under initiation of A for those characteristics.
2. Keep those baseline characteristics unchanged and set the drug input to z=0 to obtain the predicted hospitalization risk under initiation of B.
3. Average each of these two columns of probabilities over all 3,000 people.

The change concerns the drug input used for prediction after fitting. It does not alter actual treatment records or outcomes used for training, nor does it mean both counterfactuals were observed for each person. The model provides an average risk for the corresponding characteristics, not a definite outcome for one individual in another world.

The estimation formulas are:

$$
\widehat R_A=\frac1N\sum_{i=1}^N\widehat m(1,L_i),\qquad
\widehat R_B=\frac1N\sum_{i=1}^N\widehat m(0,L_i).
$$

N=3,000 is the size of the entire target sample; i indexes patients, with both sums covering the same people. m̂(1,L_i) and m̂(0,L_i) are their predicted probabilities under the A/B strategies. Both groups use the full N as the denominator, not the actual number taking each drug, because standardization targets the same whole population. This N denominator belongs to this standardization estimator; conventional normalized IPTW uses the sum of weights in each actual group as its denominator.

#### Results from the same data need not be exactly equal
{: #section-11 }

| Method | Drug A risk | Drug B risk | A−B risk difference | A/B risk ratio |
| --- | ---: | ---: | ---: | ---: |
| Unadjusted | 14.03% | 12.33% | +1.70 percentage points | 1.138 |
| IPTW | 10.88% | 15.03% | −4.15 percentage points | 0.724 |
| Logistic regression + g-computation | 10.56% | 15.08% | −4.52 percentage points | 0.700 |

All are simulated point estimates, not clinical evidence or conclusions about statistical significance. Different estimators of the same target question can yield different finite-sample results. A difference alone does not show that one method is wrong, and agreement alone does not establish absence of bias. Exact equality in the earlier simple stratified example arose from a particular algebraic correspondence between probabilities and proportions calculated directly in each stratum.

#### Shared requirements and differences in longitudinal settings
{: #section-12 }

Both methods require appropriate intervention and time definitions, identification assumptions such as exchangeability, consistency, and positivity, suitable models, and appropriate follow-up handling. Without enough comparison data, IPTW may produce large weights, whereas g-computation may produce apparently smooth numbers through extrapolation. Smooth predictions do not mean the lack of data support has disappeared.

For sustained A versus sustained B, the longitudinal g-formula simulates how health and outcomes change under treatment along each strategy; longitudinal IPTW constructs cumulative weights from conditional probabilities of each actual treatment decision. Post-treatment health may be affected by earlier drugs, so it cannot arbitrarily be held at its observed value while the baseline formula is simply repeated. Each method requires separate specification of the strategies and censoring procedures.

Using both treatment and outcome models can produce doubly robust estimators such as AIPW. This is not a simple average of the two estimates, and it is not the algorithm implemented in this example.

Reproduction script: [multivariable_iptw.py]({{ "/assets/causal-inference/iptw-lr-example/multivariable_iptw.py" | relative_url }}). In the results, the `g_computation` field records the outcome model and risks, and `risks` records IPTW and other estimates. Both use the same random seed, patients, and outcome.


## 5. Why do sustained strategies require a “longitudinal” g-formula?
{: #section-13 }

§1–4 set only the baseline action to treatment or no treatment; subsequent care follows its usual course under each intervention. If the question changes to “treat at both decisions” versus “do not treat at either decision,” we must specify both the first and second actions.

Suppose the first treatment improves health, and the second treatment decision depends on current health. Baseline health alone cannot explain the second treatment choice: new health information before the second decision may affect both treatment choice and eventual death. Consider the following temporal order:

$$
L_0\quad\prec\quad A_0\quad\prec\quad L_1\quad\prec\quad A_1\quad\prec\quad Y.
$$

Here $$\prec$$ means only “precedes,” not a causal arrow. First distinguish the order of records, then determine which variables causally affect others.

- $$L_0$$: pretreatment health.
- $$A_0$$: first treatment decision.
- $$L_1$$: subsequent health, before the second decision.
- $$A_1$$: second treatment decision.
- $$Y$$: outcome at the end of follow-up.

The subscripts 0 and 1 are **decision-time indices**, not automatically year 0 and year 1. $$A_0=1$$ means “treat at the first time point”; $$A_1=0$$ means “do not treat at the second time point.” The subscript tells us when the decision occurs; the 0/1 after the equals sign tells us which action is taken.

If treatment changes later health, we have $$A_0\to L_1$$. If health then affects subsequent treatment and the outcome, we have $$L_1\to A_1$$ and $$L_1\to Y$$.

The symbol $$\to$$ differs from the earlier $$\prec$$: $$\to$$ denotes an assumed direct causal arrow: the variable at its beginning affects the variable at its end. It does not simply mean it was measured earlier.

Health before the second decision, $$L_1$$, may therefore be both:

- Part of a pathway through which earlier treatment acts—a mediator.
- A confounder of the relationship between subsequent treatment and the outcome.

This creates an apparent conflict. Comparing the effect of the second treatment requires current health information; otherwise, the greater tendency of sicker patients to receive treatment may confound the comparison. Yet comparing the **whole strategy** also requires allowing the first treatment to have changed later health. A reduction in mortality achieved by earlier treatment improving health is part of the total effect we want to retain.

Omitting $$L_1$$ may therefore leave confounding of subsequent treatment; directly holding $$L_1$$ fixed in an ordinary outcome regression and reading treatment coefficients may also fail to yield the whole strategy’s total effect.

The longitudinal g-formula separates the problem into two connected steps: **first estimate how health is distributed after the first action, then estimate outcomes under the second action within each health category.** Finally, combine the outcome predictions using the health distribution generated by that strategy itself.

This joins “we need health information” with “treatment is allowed to change health.” Health information estimates the effect of later treatment while retaining the pathway through which earlier treatment changes health and thereby affects the outcome. Parametric implementations can use regression in these steps, so “regression” and “g-methods” should not be treated as opposing categories of tools. [Naimi et al.: An introduction to g methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6074945/)

## 6. Two treatment decisions: Putting numbers into the longitudinal formula
{: #section-14 }

### 6.1 A new, separate teaching scenario
{: #section-15 }

This section is a different example from the 1,000-person table in §1. Temporarily assume everyone survives to the second treatment decision, no one is lost to follow-up, and $$Y$$ occurs only within a fixed subsequent period. Thus $$L_1$$ is defined for everyone.

For simplicity, assume no additional baseline confounding adjustment is needed and that $$L_1$$ before the second decision sufficiently controls confounding between that treatment and the outcome. Assume consistency, positivity, and the other conditions also hold. These are teaching assumptions; they cannot be tested from the table’s numbers.

First ask: “Given the first action, what will health look like before the second decision?” Suppose the following health-transition probabilities have been estimated from observed data and, under these assumptions, can be used for intervention predictions:

| First decision | Subsequently in good health | Subsequently in poor health |
| --- | ---: | ---: |
| $$A_0=1$$ | 80% | 20% |
| $$A_0=0$$ | 40% | 60% |

This first table does not yet provide mortality risk. It only divides the baseline population into two branches: later good health and later poor health. A second table must answer: “After reaching this health branch, what is the outcome risk if treatment is or is not given at the second decision?”

| $$L_1$$ | Risk with $$A_1=1$$ | Risk with $$A_1=0$$ |
| --- | ---: | ---: |
| Good health | 5% | 10% |
| Poor health | 20% | 40% |

This simplified example also assumes that, given $$L_1,A_1$$, outcome risk no longer varies with $$A_0$$, so the outcome model needs only $$L_1,A_1$$. This is an additional simplification for this example; a general g-formula outcome model may still require earlier treatment and other history.

The roles of the two tables are now clear: **the first determines how many people enter each health category; the second determines their risk under the second action.** Once a strategy is chosen, we know which row of the first table to use and which cells of the second table to select.

### 6.2 Strategy 1: Treat at both decisions $$(A_0,A_1)=(1,1)$$
{: #section-16 }

“Treat at both decisions” specifies $$A_0=1$$ first, so the first table gives 80% good health and 20% poor health. It then specifies $$A_1=1$$ regardless of health, so the second table gives risks of 5% for good health and 20% for poor health. Add the two branch contributions:

$$
P(Y^{1,1}=1)=0.8\times5\%+0.2\times20\%=8\%.
$$

Here $$Y$$ is the death indicator during this section’s fixed subsequent period, with $$Y=1$$ indicating death. The two superscripts in $$Y^{1,1}$$ specify $$A_0=1$$ and $$A_1=1$$ in temporal order: “the potential outcome if treated at both decisions.” They are not a first power of $$Y$$ or the product of two numbers. $$P(Y^{1,1}=1)$$ is therefore the entire target population’s mortality risk under this rule, **not the observed death proportion among people selected because they actually received treatment twice**.

For 1,000 people, the formula has two branches: after the first treatment, 800 are expected to be in good health and 200 in poor health. With everyone treated again, expected deaths are $$800\times5\%=40$$ and $$200\times20\%=40$$, respectively. That is 80/1,000, or 8%. These branch counts are model predictions under the strategy; actual patients have not been transformed into a different population.

### 6.3 Strategy 2: Treat at neither decision $$(0,0)$$
{: #section-17 }

To calculate the other strategy, return to **the same people’s baseline** and start again. We cannot reuse the 80% good-health and 20% poor-health distribution generated by the previous strategy. Setting $$A_0=0$$ gives 40% good health and 60% poor health from the first table. Setting $$A_1=0$$ then selects risks of 10% and 40% from the second table:

$$
P(Y^{0,0}=1)=0.4\times10\%+0.6\times40\%=28\%.
$$

Similarly, $$Y^{0,0}$$ is the potential outcome after setting both treatment actions to 0. A superscript 0 does not mean that death did not occur; death is indicated by the subsequent “$$=1$$.” Here 0.4 and 0.6 are the predicted proportions in good and poor health after the first no-treatment decision, while 10% and 40% are their outcome risks under subsequent no treatment.

In this other intervention world for the same 1,000 people, 400 are expected to have good health and 600 poor health. With no treatment at the second decision, expected deaths are 40 and 240, totaling 280/1,000.

The risk difference is therefore $$0.08-0.28=-0.20$$, a reduction of 20 percentage points.

This resolves a common confusion: §2 required both groups to be averaged using the same health proportions, so why use 80%/20% and 40%/60% here? In §2, health preceded treatment and belonged to the common starting point; here, health follows the first treatment and may already have been changed by it.

**The two worlds have the same baseline population but different later health compositions.** That difference is precisely one possible effect of early treatment. We cannot artificially “adjust it to equality” and still claim to estimate the full total effect.

### 6.4 Dynamic strategies can also be evaluated
{: #section-18 }

The previous strategies assign everyone the same second action. Clinical rules may instead use health to decide. The calculation principle remains the same: first let health develop, then let the rule assign actions within each health branch.

For example, another strategy says: “Treat at the first decision; at the second, treat if health is poor and do not treat if health is good.”

Write the rule as $$A_0=1$$ and $$A_1=I(L_1=\text{poor})$$.

$$I(\cdot)$$ is an indicator function: it equals 1 when the condition is true and 0 when false. Thus $$I(L_1=\text{poor})=1$$ for poor health, assigning treatment at the second decision; for good health it is 0, assigning no treatment. This **assigns an action by rule**; it does not claim that clinicians in the observed data necessarily followed that rule. Naming the whole rule $$g$$, $$Y^g$$ denotes the potential outcome if it were followed; $$g$$ is not a blood-pressure or dosage value.

$$
P(Y^g=1)=0.8\times10\%+0.2\times20\%=12\%.
$$

Why does the first term use 10%? The rule assigns **no treatment** at the second decision to the 80% in good health, so we select the “good health, $$A_1=0$$” cell. It assigns treatment to the 20% in poor health, selecting the 20% risk for “poor health, $$A_1=1$$.” For 1,000 people, this gives $$800\times10\%+200\times20\%=120$$ deaths.

The 12% is only a result of this artificial rule and data scenario, not clinical treatment advice. It shows that a strategy can specify **what action to take when a particular health state is encountered**, rather than assigning the same treatment value to everyone forever.

## 7. The longitudinal formula and the actual computational workflow
{: #section-19 }

The hand calculation in §6 involved only two subsequent health states. If baseline health must also be distinguished, add another layer: first determine the proportions in each baseline category, then where they branch after the first treatment, then predict each branch’s outcome. The following formula connects these three operations.

With two decisions, a fixed end-of-follow-up outcome, and no early deaths or loss to follow-up, a simplified identification formula under sequential exchangeability, consistency, positivity, and related conditions is:

$$
E[Y^{a_0,a_1}]
=\sum_{l_0,l_1}
\underbrace{E[Y\mid L_0=l_0,A_0=a_0,L_1=l_1,A_1=a_1]}_{\text{Outcome prediction for this history}}
\underbrace{P(L_1=l_1\mid L_0=l_0,A_0=a_0)}_{\text{Post-intervention health distribution}}
\underbrace{P(L_0=l_0)}_{\text{Common baseline population}}.
$$

You need not memorize it on a first reading. Read the product on the right **from right to left** in time order: begin with the baseline population, develop health under treatment, then produce the outcome under subsequent treatment. The outer summation combines all paths. Reordering multiplication does not change its value; reading from the right simply mirrors the temporal process.

Breaking down the longitudinal formula:

- $$a_0,a_1$$ are the two treatment values assigned by intervention; they remain fixed during this calculation, for example at $$(1,1)$$. $$Y^{a_0,a_1}$$ is the potential outcome under those actions, and $$E$$ averages over the target population.
- $$l_0,l_1$$ are specific health values at the two times. $$L_0=l_0$$ denotes a baseline health state and $$L_1=l_1$$ a subsequent state. Unlike the fixed treatment values, these are possible histories traversed by the summation.
- $$\sum_{l_0,l_1}$$ sums over every possible combination of “baseline health, subsequent health.” If both times have good and poor states, there are four combinations, not just two values to add. Continuous variables require integration instead.
- The rightmost $$P(L_0=l_0)$$ gives the starting proportion of that patient category.
- The middle $$P(L_1=l_1\mid L_0=l_0,A_0=a_0)$$ is the conditional probability of developing subsequent health state $$l_1$$ given baseline health and the first treatment. This term allows the first treatment to change later health composition.
- The leftmost conditional mean, $$E[Y\mid L_0=l_0,A_0=a_0,L_1=l_1,A_1=a_1]$$, predicts the outcome under the whole history and second action. All four conditions after the bar hold simultaneously; with a 0/1 outcome $$Y$$ here, the mean is a conditional mortality risk.
- The three adjacent factors are **multiplied**: a path’s frequency times its risk gives its contribution to overall risk; summation then combines contributions across all paths. The text underneath merely explains the terms and adds no operation.

§6 omitted additional $$L_0$$ strata and assumed the outcome no longer depended on $$A_0$$ given $$L_1,A_1$$, allowing the long formula to reduce to “$$0.8\times5\%+0.2\times20\%$$.” In general, history variables cannot be removed without justification.

The hand example supplied both tables. An actual analysis first estimates the relationships they represent from observational data, then connects them under the specified strategy. The first two steps below “learn how health and outcomes develop”; the final four “use those relationships to calculate outcomes under a strategy”:

1. Estimate a health-transition model from observed data, such as $$L_1\mid L_0,A_0$$.
2. Estimate an outcome model, such as $$Y\mid L_0,A_0,L_1,A_1$$.
3. Use the same target population’s baseline information and set $$A_0$$ according to the strategy.
4. Generate $$L_1$$ from its estimated conditional distribution given that person’s history and assigned treatment; with few possible values, sum directly over all possibilities instead.
5. Set $$A_1$$ according to the fixed strategy or dynamic rule.
6. Predict outcomes and average; repeat under another strategy.

The “$$L_1\mid L_0,A_0$$ model” is shorthand for a conditional distribution: predicting subsequent health from initial health and first treatment. The “$$Y\mid L_0,A_0,L_1,A_1$$ model” predicts the outcome using the entire history so far. These expressions are neither stand-alone probability values nor divisions.

For a deterministic rule that completely specifies every action, treatment in the simulation is assigned directly by the rule, so this implementation generally needs no separate model of treatment choice. Health development and outcomes are what must be predicted. This does not mean confounding can be ignored: health and outcome models still require sufficient treatment and confounder histories.

This section presents a common implementation using simulation or summation over health-transition models. The g-formula can also be estimated through other approaches, such as sequential conditional expectations; simulating a complete path for every person is not mandatory.

If $$L_1$$ is affected by previous treatment, its actual observed $$L_1$$ value cannot simply be copied unchanged into another treatment world. We need its distribution under the specified intervention, not equal post-treatment health in both worlds.

These calculations have also assumed that everyone reaches the second decision and therefore has an $$L_1$$. Mortality studies often violate that condition: some people die before the next measurement. The next section explains why interval-by-interval calculations are then needed and why blood pressure or treatment should not continue to be predicted for those who have died.

## 8. What if the outcome is death and some people die along the way?
{: #section-20 }

The simplified formula in §7 cannot be mechanically applied when “some people die before $$L_1$$ is measured.” Death ends their subsequent health and treatment processes; blood pressure and treatment after death may be undefined. We cannot assign a fictitious health value to a dead person and pretend they will reach the next treatment decision.

The solution includes “survival to the next step” in the sequential prediction. A survival parametric g-formula usually divides follow-up into intervals, such as monthly updates. An implementation that simulates deaths can proceed as follows:

1. Update health for people alive at the start of an interval.
2. Assign treatment for that interval according to the strategy.
3. Predict the interval’s conditional death probability $$q_k$$.
4. Stop subsequent health and treatment processes after death.
5. Accumulate mortality risk across intervals and average over the original target population.

Here $$k$$ indexes follow-up intervals, such as months 1, 2, and 3. $$q_k$$ is the probability of dying during interval $$k$$, conditional on prior history and being alive at its start. $$q_k$$ lies between 0 and 1 and has no time unit; $$1-q_k$$ is the probability of surviving that interval under the same conditions. This shorthand does not include the entire history in the subscript, but $$q_k$$ may differ across histories and strategies.

It is not the instantaneous event rate $$h(t)$$ in a continuous-time Cox model: $$t$$ is continuous time since follow-up began, and $$h(t)$$ is the instantaneous death rate among those still alive just before $$t$$. It has units of “per unit time” and cannot directly be treated as an interval death probability.

Given the corresponding histories, survival probabilities across successive intervals combine by multiplying $$(1-q_k)$$; overall risk must also average over the different history paths generated by that strategy. Some implementations accumulate conditional probabilities directly without simulating individual deaths. **Multiplying an average hazard by years of follow-up does not generally give cumulative mortality risk.**

For example, in a simplified scenario with no further history distinctions, the first-interval death probability is 10%, and the second-interval probability among survivors is 20%. Starting with 100 people, 10 are expected to die in the first interval, leaving 90; the second interval produces $$90\times20\%=18$$ expected deaths. Total risk is 28%, or $$1-(1-0.10)(1-0.20)$$, rather than 10% plus 20%. The second 20% applies only to the 90 people still alive.

The example also shows why denominators matter: **each interval’s death probability concerns people alive at its start, but the final cumulative risk concerns the original 100 people.** With 28 expected deaths across both intervals, divide 28 by the original 100, rather than calculating only among those still alive at the end.

For a nonfatal outcome, specify in advance how competing events such as death enter the target question; do not casually treat them as ordinary noninformative censoring.

For implementation details, including variable ordering, history length, model fitting, natural-course checks, and simulation uncertainty, see [McGrath et al.: gfoRmula](https://pmc.ncbi.nlm.nih.gov/articles/PMC7351102/).

A “natural-course check” uses the models to simulate usual treatment processes and checks whether the corresponding observed results can be reproduced. It can reveal obvious model problems but cannot prove absence of unmeasured confounding. With informative loss to follow-up, the compared results must also use compatible censoring procedures; simulated curves should not automatically be expected to equal unadjusted observed curves.

## 9. Why is “calculating two worlds” not enough?
{: #section-21 }

We can now calculate two predictions under specified rules. But “the calculation runs” only establishes that the algorithm operates, not that its predictions are correct causal results. Return to the earliest step: why can actual treated patients’ conditional risks predict what would happen if all comparable patients were treated? If that borrowing is unjustified, more elaborate downstream predictions only carry the error forward.

The following conditions therefore support the entire calculation; they are not afterthoughts added once it is complete:

| Condition | What does it mean for this method? |
| --- | --- |
| Consistency and well-defined interventions | “Treatment” must be sufficiently clear, and actual treatment must correspond to the defined intervention |
| Baseline conditional exchangeability | For a baseline intervention, given the required baseline health information, treatment choice is independent of the corresponding potential outcomes; commonly expressed as no remaining confounding |
| Longitudinal sequential exchangeability | For a sustained strategy, given sufficient history before each decision, that treatment choice is independent of potential outcomes under the target strategy |
| Positivity | Within relevant histories, the data allow a chance of observing the treatment actions the strategy requires |
| Appropriate estimation models | Health-transition, outcome, and other models must reliably estimate the required conditional distributions |
| Correct measurement and censoring adjustment | Treatment, health, events, and temporal ordering must be measured reliably, with appropriate handling of loss to follow-up |

If a patient category never receives a treatment, a model may still generate predictions, but these may be unsupported extrapolations. No number of simulations can replace missing information on a key time-varying confounder.

Sampling uncertainty for the parametric g-formula can be assessed with methods such as bootstrap, generally refitting all models after resampling. Increasing the number of simulated people reduces Monte Carlo error only; it does not remove uncertainty or bias in the original sample.

The g-formula does not automatically correct an incorrect $$T_0$$, selective inclusion of treated survivors, or differential outcome detection. Design and measurement must first be appropriate.

Here $$T_0$$ specifically denotes the start of follow-up; the subscript 0 marks the starting point, not a treatment value. It should align with the decision time for eligibility assessment and strategy assignment.

**The first four conditions chiefly concern causal identification: could ideal infinite data answer the target question? Model choice and sample size affect estimation: can finite data estimate the required distributions accurately?** Accurate prediction on the original data cannot replace causal identification conditions.

## 10. Differences from IPW and Cox
{: #section-22 }

Starting from “risks among people with the same health,” this note constructs **average predictions** under two interventions for the target population. IPW takes another route: it retains observed outcomes and weights the data to represent the required target comparison. Both serve the same causal question but use the data differently.

| Method | What does it chiefly estimate here? | What happens next? |
| --- | --- | --- |
| G-formula | Conditional outcome risks; also health development in longitudinal settings | Predict under the specified intervention and average over the target population |
| IPW | Each person’s probability of actually receiving the corresponding treatment given their health | Reweight observed outcomes |
| Cox | Conditional hazard given the included variables | Can serve as a survival outcome prediction model or, with appropriate weights, fit a marginal model |

The baseline risks of 12.5% and 25% here are calculated again by weighting observed outcomes in [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}). With real data, the estimators may differ because of model choices and finite samples.

Another g-method is [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}): it specifies a structural model for treatment effects, then estimates parameters using the treatment mechanism and conditional-mean restrictions on transformed outcomes. This differs from the basic approach here of “predicting outcomes under each intervention, then averaging.”

## 11. Self-check
{: #section-23 }

1. Why can we not simply subtract 16% from 17%? — Those risks come from actual populations with 20% and 80% high-risk patients, mixing treatment differences with differences in baseline health composition.
2. Why can the 5% risk among actually treated low-risk patients predict the average risk if all low-risk patients were treated? — We need no remaining confounding given the required baseline information, together with consistency, positivity, and other identification conditions—not merely a plausible-looking percentage.
3. Why use 50% high risk and 50% low risk in both worlds? — We target an intervention contrast in the same original population, changing only baseline treatment rather than who enters the target population at baseline.
4. Why need post-treatment health proportions not be equal in the longitudinal example? — Early treatment can change health. Predict health distributions under each strategy, then use each strategy’s distribution to combine outcomes.
5. Why not directly add a second-interval death probability of 20% to the first interval’s 10%? — The 20% applies only to first-interval survivors. First calculate how many remain at risk, then return to the baseline population for the final cumulative risk.
6. Does using Cox or logistic regression as an outcome model mean it is no longer the g-formula? — No. The model estimates the required relationships; intervention predictions, integration, and standardization still follow. Reading one regression coefficient usually does not complete those steps.
7. Does large-scale simulation provide a large amount of new clinical data? — No. It computes consequences of existing data and assumptions. Simulation cannot create missing confounder information or repair an incorrect design.

## References
{: #section-24 }

- [Hernán and Robins: Causal Inference: What If](https://miguelhernan.org/whatifbook): standardization, the g-formula, and identification assumptions.
- [Naimi, Cole, and Kennedy: An introduction to g methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6074945/): treatment–confounder feedback and g-methods.
- [McGrath et al. (2020): gfoRmula](https://pmc.ncbi.nlm.nih.gov/articles/PMC7351102/): parametric g-formula algorithms for sustained strategies and survival applications.
- [Chiu et al.: Evaluating Model Specification When Using the Parametric G-Formula in the Presence of Censoring](https://pmc.ncbi.nlm.nih.gov/articles/PMC11043789/): interpreting natural-course checks in the presence of censoring.
