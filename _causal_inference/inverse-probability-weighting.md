---
layout: "causal-note"
title: "Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights"
description: "Calculate propensity scores, treatment and censoring weights, balance diagnostics, ATE, and ATT with reproducible examples."
group: "Estimation"
order: 14
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-13"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Continue with the same 1,000-person table", "anchor": "section-1"}, {"title": "2. Step 1: Estimate the propensity score", "anchor": "section-2"}, {"title": "3. Step 2: Invert the probability of the action actually received", "anchor": "section-3"}, {"title": "4. Step 3: Weight both people and deaths", "anchor": "section-4"}, {"title": "5. Why does the weighted-risk formula have this form?", "anchor": "section-5"}, {"title": "6. Steps for baseline IPW in an actual study", "anchor": "section-6"}, {"title": "6.1 A complete multivariable logistic regression example: Initiating drug A versus drug B", "anchor": "section-15"}, {"title": "Step 6: Check weighted balance on the four baseline variables", "anchor": "section-22"}, {"title": "6.2 IPTW and PSM: One propensity score, two ways to construct comparable groups", "anchor": "section-48"}, {"title": "7. Why multiply weights across time for sustained strategies?", "anchor": "section-26"}, {"title": "8. IPTW and IPCW: Do not confuse the probabilities", "anchor": "section-29"}, {"title": "9. Are IPW and a marginal structural model the same thing?", "anchor": "section-31"}, {"title": "10. Large weights, stabilized weights, and positivity", "anchor": "section-32"}, {"title": "11. What assumptions does IPW require?", "anchor": "section-35"}, {"title": "12. Review alongside the g-formula", "anchor": "section-36"}, {"title": "13. Self-check", "anchor": "section-37"}, {"title": "References", "anchor": "section-38"}]
previous_note: "/causal-inference/g-formula/"
next_note: "/causal-inference/longitudinal-iptw/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). For notation, see [Reading Causal Formulas: From Symbols to Questions]({{ "/causal-inference/reading-causal-formulas/" | relative_url }}); every formula below is also explained where it appears.

Prerequisites: [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}) and the baseline example in [The G-Formula]({{ "/causal-inference/g-formula/" | relative_url }}). For the longitudinal sections, also use [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}) and [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}). For survival models after weighting, see [The Cox Proportional Hazards Model]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**The idea in one sentence**

**Given pretreatment health, the rarer a person’s actual treatment choice, the greater that record’s weight in an inverse-probability-weighted analysis.**

When exchangeability, positivity, consistency, and related conditions hold and the necessary probabilities are appropriately estimated, the groups’ weighted outcomes can estimate what would happen if the same target population received each intervention.

</aside>


IPW means inverse probability weighting. IPTW is inverse probability of treatment weighting; IPCW is inverse probability of censoring weighting, which uses the inverse probability of **remaining uncensored**. They address different selection processes.

**On a first reading, calculate the tables in §1–4, focusing on “weighting both people and deaths.”** Then read the multivariable drug A versus B logistic regression example in §6.1 to connect hand calculations with a research workflow, then use §7 to enter the separate longitudinal IPTW note and return here for censoring weights in §8. Leave the two estimators in §5 and extreme weights and longitudinal stabilization in §10 for a second reading. Stabilized weights are first defined before the table in §6.1.

## 1. Continue with the same 1,000-person table
{: #section-1 }

Target question: How much would one-year mortality risk differ if everyone in the original target population initiated treatment at baseline versus if nobody initiated? Only the baseline action is intervened on; later care follows its usual course in each intervention world. Assume complete outcome observation. All data below are for teaching.

| Baseline health $$L$$ | Treatment $$A$$ | Number | Deaths | Risk |
| --- | ---: | ---: | ---: | ---: |
| Low risk | 1 | 100 | 5 | 5% |
| Low risk | 0 | 400 | 40 | 10% |
| High risk | 1 | 400 | 80 | 20% |
| High risk | 0 | 100 | 40 | 40% |

The variables used throughout are: $$A$$, baseline treatment action, with $$A=1$$ for initiation and $$A=0$$ for no initiation; $$L$$, health measured before the treatment decision, here either “low risk” or “high risk”; and $$Y$$, one-year mortality, 1 for death and 0 otherwise. An individual’s $$Y$$ is 0 or 1, while a group’s mortality risk can be 5%, 20%, and so on.

The original target population contains 500 low-risk and 500 high-risk patients. Treated risk is $$85/500=17\%$$, and control risk is $$80/500=16\%$$.

At first glance, the treated mortality risk of 17% exceeds the controls’ 16%. But within the table, low-risk treated and control risks are 5% and 10%, while high-risk risks are 20% and 40%. Why is treatment associated with lower risk within both strata but higher risk after pooling?

When calculating 17%, high-risk people make up 80% of the treated group; when calculating 16%, they make up only 20% of controls. **Both treatment and the composition of the compared populations have changed.** Lower within-stratum risks alone do not establish causality, but the example shows that the original overall risks do not compare a common health composition.

The target population originally contained 500 of each risk category. Estimates for “everyone treated” and “everyone untreated” should both refer to that composition. The g-formula predicts and averages using it; IPW instead redefines how much each observed record contributes to the average.

This raises a concrete question: **With only 100 low-risk treated patients, how can their records represent the target population’s 500 low-risk patients?** Treatment probabilities provide the information needed to calculate that multiplier.

## 2. Step 1: Estimate the propensity score
{: #section-2 }

Among 500 low-risk patients, only 100 receive treatment. Thus only one fifth of this category’s treatment outcomes appear in the actual treated group. Among 500 high-risk patients, 400 receive treatment, so four fifths are observed. We need both proportions to determine how much each category’s records should contribute.

Expressing “what proportion of people with this health receive treatment?” as a probability defines the propensity score:

$$
e(L)=P(A=1\mid L).
$$

Read each symbol: $$e$$ names the propensity-score function, and $$L$$ in parentheses specifies the health information used. Here $$e(L)$$ is not the mathematical constant $$e\approx2.718$$. $$P(\cdot)$$ denotes probability; $$A=1$$ is the event “initiate treatment”; the bar $$\mid$$ means “given,” restricting calculation to people with the same $$L$$. The expression **defines** a propensity score; it is not a treatment-effect formula.

It means: **the probability of receiving treatment in the observed data among people with this pretreatment health.**

It is not the probability of death, treatment success, or a clinician’s subjective “degree of inclination.”

Here:

$$
e(\text{low risk})=100/(100+400)=0.2,
$$

$$
e(\text{high risk})=400/(400+100)=0.8.
$$

The low-risk numerator 100 is the number treated; denominator $$100+400=500$$ includes all low-risk people. Thus the probability is 0.2, or 20%. The high-risk calculation likewise stays within that category. Both probabilities are unitless and between 0 and 1.

With multiple health variables, models such as logistic regression can estimate $$P(A=1\mid L)$$. The prediction target is **treatment choice**, unlike the g-formula’s outcome model.

**Classical baseline IPTW usually does not require a train/test split.** Fit one logistic regression using everyone’s baseline features and treatment labels, then calculate probabilities for those same people. Everyone jointly contributes to one coefficient set; each person does not train an individual model. For a worked coefficient calculation and the distinction between fitting and prediction, see [Does classical IPTW require a train/test split, and how does logistic regression produce each propensity score?]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-28).

## 3. Step 2: Invert the probability of the action actually received
{: #section-3 }

Return to the representation problem. There are 100 actual low-risk treated patients and 500 low-risk people in the target population, requiring multiplier $$500/100=5$$. The preceding treatment probability was $$100/500=0.2$$, so its inverse is exactly $$1/0.2=5$$.

**This is why we invert a probability rather than arbitrarily assigning a large number to rare records: it restores “the observed subset” to “the original category’s size.”** High-risk treated patients require $$500/400=1.25$$. Controls require separate calculations based on how common no treatment is within each category.

For baseline IPTW targeting mean intervention outcomes in the entire population, the general unstabilized weight expresses this count logic as a piecewise formula. In practice replace $$e(L)$$ with estimate $$\widehat e(L)$$:

$$
w_i=\begin{cases}
1/e(L_i),&A_i=1,\\
1/[1-e(L_i)],&A_i=0.
\end{cases}
$$

The population formula now applies to individual $$i$$:

- $$i$$: person index, such as person 1, 2, or 3—not month.
- $$A_i,L_i$$: person $$i$$’s actual treatment and baseline health; $$e(L_i)$$ is treatment probability for people with that health.
- $$w_i$$: person $$i$$’s unitless weight. The two rows mean “use the first if actually treated, otherwise the second,” not two simultaneous weights for one person.
- $$1-e(L_i)$$: probability of no treatment given the same health. If treatment probability is 0.2, no-treatment probability is $$1-0.2=0.8$$.
- $$\widehat e(L_i)$$: the propensity score estimated from the sample and model, marked with a hat. True $$e(L_i)$$ is usually unknown, so computed weights depend on estimation.

The formula says: **find how common this person’s actual action is given their health, then invert that probability.**

Equivalently, $$w_i=A_i/e(L_i)+(1-A_i)/[1-e(L_i)]$$. This merely abbreviates the same piecewise definition: when $$A_i=1$$, the second term is 0; when $$A_i=0$$, the first is 0.

The key is: **treated people use the probability of treatment, and untreated people use the probability of no treatment. Do not give everyone $$1/e(L)$$.**

| Health and actual action | Action probability | Weight | Intuition |
| --- | ---: | ---: | --- |
| Low risk, treated | 0.2 | 5 | Few comparable people are actually treated, so each represents more similar patients |
| Low risk, untreated | 0.8 | 1.25 | Most comparable people are already observed in this group |
| High risk, treated | 0.8 | 1.25 | Most comparable people are already observed in this group |
| High risk, untreated | 0.2 | 5 | Few comparable people are actually untreated, so each represents more similar patients |

Restoring counts does not ensure that outcomes represent everyone. We must also assume that, after controlling relevant health, treated patients represent comparable target patients’ average outcomes **under the treatment intervention**. Low-risk treated patients may, for example, have unrecorded differences in health awareness; perfect weighted balance of low/high-risk counts would not remove that unmeasured confounding.

A weight of 5 also does not assert that “this person’s outcome equals four other people’s counterfactual outcomes.” Representation concerns average outcomes in comparable populations, not identification of any individual’s other potential outcome.

## 4. Step 3: Weight both people and deaths
{: #section-4 }

Once we know each person’s contribution, apply the same weight to the whole record. Among low-risk treated patients, 5 die and 95 survive, all with weight 5. Weighted deaths are 25, weighted survivors 475, and weighted total 500.

Why multiply deaths by 5 as well? Weighting changes **the whole record’s contribution to the average**. Increasing the denominator to 500 while retaining only 5 deaths would incorrectly change 5% to 1%, effectively inventing 400 survivors. Correct weighting preserves the observed stratum risk $$25/500=5\%$$ and changes that stratum’s share of the overall result.

| Health | $$A$$ | Original number | Weight | Weighted number | Original deaths | Weighted deaths |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Low risk | 1 | 100 | 5 | 500 | 5 | 25 |
| Low risk | 0 | 400 | 1.25 | 500 | 40 | 50 |
| High risk | 1 | 400 | 1.25 | 500 | 80 | 100 |
| High risk | 0 | 100 | 5 | 500 | 40 | 200 |

Each weighted treatment group now contains 500 low-risk and 500 high-risk people. Stratum-specific observed risks remain unchanged, while previously different group compositions share a common standard. Now calculate each risk as “weighted deaths ÷ weighted people”:

$$
\widehat R_1=\frac{25+100}{500+500}=12.5\%,
$$

$$
\widehat R_0=\frac{50+200}{500+500}=25\%.
$$

$$\widehat R_1$$ means estimated treatment-intervention risk; $$\widehat R_0$$ means estimated no-treatment-intervention risk. $$R$$ denotes risk and subscripts 1 and 0 identify actions, **not year 1 and year 0**. Both follow-up horizons are one year. Hats remind us that these are finite-sample estimates, targeting the original population’s mortality risk under each action given the relevant identification assumptions.

In the treatment formula, $$25+100$$ is weighted deaths, and $$500+500$$ is the total weighted treated population, including deaths and survivors; the control calculation is analogous.

The risk difference $$RD$$ is treated minus control risk: $$12.5\%-25\%=-12.5$$ percentage points. The unitless risk ratio $$RR$$ divides them: $$12.5\%/25\%=0.5$$, meaning half the control risk. A negative difference’s interpretation depends on the outcome; here $$Y=1$$ means death, so it indicates lower mortality.

This agrees with [The G-Formula]({{ "/causal-inference/g-formula/" | relative_url }}). Both methods give low- and high-risk populations equal shares and compare the two actions.

Exact equality here comes from directly estimating probabilities using the same stratified table. With real data and different models, the two estimators need not match exactly in finite samples.

<aside class="study-callout study-callout--important" markdown="1">

**Weighted counts are not new independent patients**

Each group’s weighted count of 1,000 means it represents the original 1,000-person target distribution. There are still only the original 1,000 individual records.

Do not calculate standard errors as though there were now 2,000 independent patients. Extreme weights can actually reduce effective information.

</aside>


## 5. Why does the weighted-risk formula have this form?
{: #section-5 }

The previous section divided 125 weighted deaths by 1,000 weighted people. Real studies may have thousands of health combinations and different weights for everyone, making a four-row manual table impractical. The formula below simply expresses **the death proportion after weighting individuals** as record-by-record computer operations. It introduces no new effect definition.

A common normalized weighted mean is:

$$
\widehat R_a=
\frac{\sum_i I(A_i=a)w_iY_i}{\sum_i I(A_i=a)w_i}.
$$

- $$a$$: the fixed action being evaluated, either 1 or 0; uppercase $$A_i$$ is the individual’s actual action. Use $$a=1$$ for treatment risk and $$a=0$$ for no-treatment risk.
- $$\widehat R_a$$: under the relevant assumptions, an estimate of one-year mortality if the entire target population received $$a$$. The hat denotes estimation and the subscript the strategy value.
- $$\sum_i$$: add over everyone in the sample, with $$i$$ running from the first person to the last—not across times.
- $$I(A_i=a)$$: an indicator, 1 if the person actually received that action and 0 otherwise, retaining the relevant group’s records.
- $$Y_i$$: person $$i$$’s one-year outcome, 1 for death and 0 otherwise. Adjacent $$I(A_i=a)w_iY_i$$ terms are multiplied.
- Numerator: that group’s weighted event count; a death contributes its weight and a survivor contributes 0.
- Denominator: the sum of all weights in the group, or weighted population count. Survivors remain in the denominator.

Read: **multiply each selected group member’s death indicator by their weight, sum, then divide by all weights in that group**. The earlier treatment numerator is 125 and denominator 1,000, giving 12.5%.

This is a Hájek-type estimator: dividing by the weighted count normalizes the weights. You can stop here on a first reading; you have the core baseline IPW calculation. Another denominator form is retained below for comparing estimators.

<details class="study-callout" markdown="1">
<summary>Second reading: Why does another estimator divide by the original total sample size?</summary>

A Horvitz–Thompson form divides directly by original sample size $$n$$:

$$
\widehat R_a^{HT}=\frac1n\sum_i\frac{I(A_i=a)Y_i}{\widehat P(A_i=a\mid L_i)}.
$$

Here $$n$$ is the original total, 1,000—not the original 500 treated people or the 2,000 obtained by adding weighted groups. Superscript $$HT$$ labels the Horvitz–Thompson method; **it is not a power**. $$\widehat P(A_i=a\mid L_i)$$ estimates action $$a$$’s probability for people with person $$i$$’s health: $$\widehat e(L_i)$$ if $$a=1$$, and $$1-\widehat e(L_i)$$ if $$a=0$$. The indicator zeros records outside the selected group, so retained records use their actual-action probability as denominator.

Read: **divide the outcomes of actual action-$$a$$ recipients by their treatment-choice probabilities, sum over everyone, then divide by the original total sample size**. Weighted treated deaths are 125, so HT also gives $$125/1000=12.5\%$$.

The estimators agree here but generally differ in finite samples.

</details>


With censoring in survival data, weighting observed deaths and dividing by people does not automatically estimate five-year risk; appropriate survival estimation and censoring adjustment are required.

## 6. Steps for baseline IPW in an actual study
{: #section-6 }

For the connection to the paper being studied, see [What is an IPTW framework?]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-3), linking this 1,000-person example to ML propensity scores, stabilized IPTW, balance checks, and weighted survival analysis.

1. **Define target population and strategies first.** These weights target the average treatment effect (ATE) in the full original population. A target effect among actual treated patients requires different weights.
2. **Select pretreatment confounding information.** Use causal knowledge and measurement order, rather than including every available variable or only statistically significant ones.
3. **Fit the treatment-choice model.** For example, predict baseline initiation using age, kidney function, and medical history.
4. **Calculate individual weights.** Also assess missingness, probabilities near 0 or 1, and data support.
5. **Check weighted balance.** Compare covariate distributions and standardized differences, not only propensity-model predictive accuracy. The aim is comparability of required baseline features, not maximum ability to classify who was treated.
6. **Estimate target outcomes.** Calculate appropriate weighted risks or survival curves, or fit a target marginal model.
7. **Assess uncertainty.** Use estimator-appropriate variance methods or resampling. Bootstrap generally should re-estimate weight models; repeated records or clones require correlation handling at the original-person level.

Balanced measured variables after weighting are a useful diagnostic, not proof that unmeasured confounding is absent.

### ATT: Decide whose question to answer before calculating control weights
{: #section-7 }

**The average treatment effect on the treated (ATT) concerns actual recipients of the treatment of interest: how would their average outcomes differ if they received that treatment versus the control strategy?** Defining the target population by actual treatment does not require them to receive treatment in both hypothetical scenarios.

We continue with §1’s 1,000-person teaching table and one-year mortality to explain the original 500-person discussion. The multivariable A/B drug example appears at this subsection’s end and in §6.1; do not mix the datasets.

#### 1. Start with the same table and identify the target population
{: #section-8 }

| Baseline health | Actually treated | Deaths among treated | Actually untreated | Deaths among untreated |
| --- | ---: | ---: | ---: | ---: |
| Low risk | 100 | 5 | 400 | 40 |
| High risk | 400 | 80 | 100 | 40 |
| Total | 500 | 85 | 500 | 80 |

ATE targets all 1,000 people, half low risk and half high risk. ATT targets the 500 actually treated: 100 low risk (20%) and 400 high risk (80%).

Both ATT scenarios concern the latter population:

- All 500 treated at baseline: already observed, with 85 deaths and risk 85/500=17%.
- The same 500 untreated at baseline: unobserved directly and estimated from comparable controls.

This does not mean stopping after some period of treatment or directly comparing two different populations. It posits two baseline strategies for the same people. Their actual-treated label determines whose outcomes interest us; it does not prohibit considering their untreated counterfactuals.

#### 2. Why do treated people receive weight 1?
{: #section-9 }

The target population is these 500 people themselves. Its composition—100 low risk and 400 high risk—is already the one to retain, so each treated person keeps one original contribution. This is not because their treatment probability was 100% or because ATT needs no confounding control.

What is missing is this population’s untreated outcome. Although actual controls also happen to number 500, their low/high-risk counts are 400/100; their crude 16% risk cannot directly represent the target.

#### 3. Before formulas, ask how much each control category should contribute
{: #section-10 }

The target has 100 low-risk and 400 high-risk people; controls contain 400 low risk and 100 high risk.

- Low-risk controls: reduce their total contribution from 400 to 100, giving individual weight 100/400=0.25.
- High-risk controls: increase their contribution from 100 to 400, giving weight 400/100=4.

A weight of 0.25 is not a 25% probability or a judgment that someone is unimportant. That control category is overrepresented relative to the ATT target and needs a smaller record contribution. Weight 4 increases the contribution of underrepresented high-risk controls.

#### 4. Weight people and deaths together
{: #section-11 }

| Data estimating untreated outcomes | Original number | Original deaths | Weight | Weighted number | Weighted deaths |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low-risk controls | 400 | 40 | 0.25 | 100 | 10 |
| High-risk controls | 100 | 40 | 4 | 400 | 160 |
| Total | 500 | 80 | — | 500 | 170 |

Low-risk mortality remains 40/400=10% before weighting and 10/100=10% afterward; high-risk mortality remains 40/100=40% and 160/400=40%. What changes is the categories’ overall contributions, not their death proportions.

Estimated untreated risk in the target population is therefore (10+160)/(100+400)=34%. The ATT risk difference, “treated minus untreated,” is 17%−34%=−17 percentage points. The 170 is a weighted event contribution, not 170 deaths actually observed in another world for these 500 treated patients.

#### 5. Why does e/(1−e) equal this count ratio?
{: #section-12 }

Within a health stratum, let actual treated count be n₁ and untreated count n₀. Estimated treatment probability is e=n₁/(n₁+n₀), and no-treatment probability 1−e=n₀/(n₁+n₀). Therefore:

$$
\frac{e}{1-e}=\frac{n_1/(n_1+n_0)}{n_0/(n_1+n_0)}=\frac{n_1}{n_0}.
$$

n₁ and n₀ are group counts within the same health stratum, not times; e is treatment probability. The common total cancels. Read this as “treated count relative to untreated count in that stratum.” This is an odds, not a probability, and can exceed 1. Probability e=0.8 gives odds=0.8/0.2=4, meaning treated to untreated 4:1—not 400% treatment probability.

Low-risk stratum: e=0.2, e/(1−e)=0.2/0.8=0.25.
High-risk stratum: e=0.8, e/(1−e)=0.8/0.2=4.

Common ATT weights are therefore 1 for treated people and ê(L)/[1−ê(L)] for controls. They shift the control distribution toward the treated target distribution. With multiple continuous features, ê(L) comes from a jointly fitted logistic or other model rather than exact person-by-person stratification. Finite-sample weighted counts and balance then generally are not exact and require diagnostics. [Austin and Stuart (2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4626409/)

#### 6. Why does this differ from the ATE of −12.5 percentage points?
{: #section-13 }

The low-risk stratum’s risk difference is 5%−10%=−5 percentage points, while the high-risk difference is 20%−40%=−20. Absolute differences vary across categories.

| Target | Low-risk share | High-risk share | Treated risk | Untreated risk | Risk difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| ATE: all 1,000 people | 50% | 50% | 12.5% | 25% | −12.5 percentage points |
| ATT: 500 actually treated people | 20% | 80% | 17% | 34% | −17 percentage points |

ATE averages 0.5×(−5)+0.5×(−20)=−12.5 percentage points; ATT averages 0.2×(−5)+0.8×(−20)=−17. High-risk people have larger absolute benefits and make up more of the ATT target, so this example’s ATT is larger in magnitude. ATT is not generally always greater than ATE; identical effects on the chosen scale or identical relevant population compositions can make them agree.

In g-computation terms, estimate untreated stratum risks of 10% and 40% from controls, then average using the treated group’s 20%/80% composition: 0.2×10%+0.8×40%=34%. ATT standardizes to the treated population’s baseline distribution.

#### 7. Why can these controls represent treated patients? And how does this map to drugs A/B?
{: #section-14 }

Matching counts alone does not justify causality. Given the same measured health, controls’ untreated outcomes must represent treated patients’ average untreated counterfactuals, and control data must support the relevant health combinations present among treated people. Consistency, reliable measurement, appropriate models, and related conditions are also required. Unmeasured severity or health behaviors may invalidate representation.

For §6.1’s multivariable A/B example, ATT means: **Among the 1,119 actual drug A initiators, how would one-year hospitalization risk differ if all initiated A versus if those same people initiated B?** It does not include everyone who took any medication; B users also receive treatment but serve as the specified comparison group.

Let Z=1 denote A, Z=0 denote B, and e(L)=P(Z=1|L). A receives weight 1 and B ê/(1−ê). Simulated patient 4 actually initiates B and has ê≈0.542066, giving ATT weight approximately 0.542066/0.457934=1.183719, versus unstabilized ATE weight 1/0.457934=2.183719. The probability model can stay the same while weights change with the target population.

The same A/B simulation gives ATT risks of 14.03% for A and 19.58% for B, difference −5.55 percentage points. Full-population ATE risks are 10.88% and 15.03%, difference −4.15. This is a different simulated dataset with hospitalization as the outcome; do not mix it with this subsection’s 500-person mortality risks of 17%/34%.


### 6.1 A complete multivariable logistic regression example: Initiating drug A versus drug B
{: #section-15 }

<aside class="study-callout study-callout--important" markdown="1">

**A shared comparative-effectiveness example**

The following reproducible **3,000-person simulated teaching dataset** represents no actual drugs and supplies no clinical effectiveness evidence. Drugs A and B are reasonable alternatives for the same disease at a similar treatment stage. **Both groups receive treatment: Z=1 means initiating A and Z=0 initiating B; 0 does not mean untreated.** We use Z to avoid confusing the drug name A with treatment variable A.

The earlier 1,000-person single-variable “treatment versus no treatment” example remains a hand-calculation introduction. This is a separate research-workflow example; do not mix their counts or results.

</aside>


#### Step 1: Specify the target trial and analysis cohort
{: #section-16 }

Question: Among eligible patients suitable for either drug, how much does one-year disease-related hospitalization risk differ between initiating A and initiating B at baseline?

- Eligibility: the same disease and treatment stage, meeting both drugs’ common suitability criteria; specify a 12-month window with no A/B use and available medical history for washout and observation.
- Time zero: the day of the first qualifying initiation of A or B, aligning eligibility, grouping, and follow-up start. Simultaneous initiation of both drugs is outside these two single-drug initiation strategies.
- Intervention: specify only which drug starts at baseline, allowing usual care afterward in each strategy world. One-year sustained use is not required, and future discontinuation or switching does not retrospectively remove baseline entrants.
- Outcome Y: 1 for the defined hospitalization within one year and 0 otherwise. To focus on baseline IPTW, the simulation assumes complete one-year outcomes with no loss to follow-up or competing events requiring adjustment.
- Target: the average risk difference if the whole eligible population initiated A versus B—a population contrast of baseline initiation strategies. It cannot directly be called a genuinely randomized ITT effect or a PP effect of one-year sustained adherence.

These are teaching target-trial specifications. The script directly generates an already eligible analysis cohort; it does not simulate real chart screening or washout verification. For new-user design operations, see [Active-Comparator New-User Design]({{ "/causal-inference/active-comparator-new-user/" | relative_url }}).

#### Step 2: Assemble baseline features and actual drug labels
{: #section-17 }

Of 3,000 people, **1,119 initiate A and 1,881 initiate B**. Overall proportions are 0.373 for A and 0.627 for B.

| Variable | Definition and coding | Model role |
| --- | --- | --- |
| age10 | (age−70)/10; age 70=0, 80=1, 60=−1 | Continuous age scale; one-unit increase means ten years |
| D | Recorded baseline diabetes: 1=yes, 0=no | Comorbidity |
| S | Simulated baseline severity score; higher means more severe | Continuous health indicator that may be negative; not a real clinical scale |
| H | Prior use of background treatment C before baseline: 1=yes, 0=no | Prior treatment information, not previous A/B use |
| Z | Baseline A initiation=1, B initiation=0 | Logistic regression label, not an input covariate |
| Y | One-year hospitalization: 1=yes, 0=no | Outcome-analysis variable, excluded from PS fitting |

All L=(age10,D,S,H) are determined before the baseline treatment decision. Real research must assess adjustment-set sufficiency using causal knowledge; listing four features does not establish that four suffice to remove confounding.

#### Step 3: Fit one logistic-regression coefficient set using all patients
{: #section-18 }

The model is:

$$
e(L_i)=P(Z_i=1\mid L_i),\quad
\widehat e(L_i)=\frac{1}{1+\exp(-\widehat\eta_i)},
$$

$$
\widehat\eta_i=\widehat\beta_0+\widehat\beta_1age10_i+\widehat\beta_2D_i+\widehat\beta_3S_i+\widehat\beta_4H_i.
$$

$$i$$ indexes patients; e is the propensity-score function and exp the exponential function. η is the additive linear predictor—the log-odds of predicted treatment probability. β_0 is the intercept and the remaining β values shared coefficients; hats mark sample estimates. Adjacent symbols multiply, and the logistic transformation maps η to a 0–1 probability.

Fitting uses all 3,000 patients’ L and Z, **without Y, without requiring a train/test split, and without a separate model for each patient**. Starting from zero coefficients, the script uses Newton iterations to obtain the unregularized logistic maximum-likelihood solution:

| Coefficient | Fitted value | Interpretation |
| --- | ---: | --- |
| Intercept | −0.686970 | Log-odds at age 70, D=0, S=0, H=0 |
| age10 | +0.480725 | Holding other variables fixed, ten additional years increase the log-odds of choosing A rather than B by this amount |
| D | +0.781641 | Recorded diabetes is associated with greater tendency to choose A |
| S | +0.617510 | Greater severity is associated with greater tendency to choose A |
| H | −0.498737 | Prior background treatment C use is associated with greater tendency to choose B |

These coefficients were **actually fitted** to the simulated sample, not copied from the data-generating coefficients. They describe treatment choice, not causal effects of the characteristics or drugs on hospitalization. Logistic regression adds terms on the log-odds scale; +0.48 does not mean a 48-percentage-point probability increase.

#### Step 4: Enter each person’s own L into the common formula
{: #section-19 }

Consider actual simulated patient 2: age 80.299, D=1, S=0.402844, H=0, and actual initiation of A.

First transform age: age10=(80.299−70)/10≈1.029912. Then substitute:

$$
\widehat\eta_2=-0.686970+0.480725\times1.029912+0.781641\times1+0.617510\times0.402844-0.498737\times0\approx0.838536.
$$

$$
\widehat e(L_2)=\frac{1}{1+\exp(-0.838536)}\approx0.698157.
$$

This means “among people with these pretreatment features, an estimated 69.8% initiate A and 30.2% B.” It is neither hospitalization risk nor the probability that A is effective.

Before the table, define its weight columns: **w_i is patient i’s ordinary unstabilized IPTW; SW_i is their stabilized weight.** SW is an abbreviation, not S times W; i indexes patients, not time. Both are unitless record contributions, not probabilities or treatment effects.

Ordinary weights invert the conditional probability of the drug actually received. Stabilized weights additionally multiply by “that actual drug’s proportion in the whole cohort”: 0.373 for every A patient and 0.627 for every B patient. The table shows the results; Step 5 explains numerator, denominator, and this rescaling.

These are actual outputs for different patients from the same model. Displayed values are rounded; the script calculates at full precision:

| Patient | Age | D | S | H | Actual drug | η | ê(L): A probability | Unstabilized weight | Stabilized weight |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| 1 | 85.361 | 0 | 0.735696 | 1 | B | 0.007028 | 0.501757 | 2.007053 | 1.258422 |
| 2 | 80.299 | 1 | 0.402844 | 0 | A | 0.838536 | 0.698157 | 1.432343 | 0.534264 |
| 3 | 58.048 | 0 | −0.626155 | 0 | A | −1.648187 | 0.161354 | 6.197547 | 2.311685 |
| 4 | 68.214 | 1 | 1.066546 | 1 | B | 0.168661 | 0.542066 | 2.183719 | 1.369192 |

#### Step 5: Use A’s probability for A and B’s probability for B
{: #section-20 }

Unstabilized IPTW targeting the entire population is:

$$
w_i=\begin{cases}1/\widehat e(L_i),&Z_i=1\ (\text{drug A}),\\1/[1-\widehat e(L_i)],&Z_i=0\ (\text{drug B}).\end{cases}
$$

**Stabilization multiplies ordinary weights by a common within-group proportion, changing their overall scale.** A constitutes 1,119/3,000=0.373 and B 1,881/3,000=0.627 of the full cohort. These numbers come directly from the analysis cohort; no additional multivariable logistic regression is needed.

Corresponding stabilized IPTW is:

$$
SW_i=\begin{cases}0.373/\widehat e(L_i),&Z_i=1,\\0.627/[1-\widehat e(L_i)],&Z_i=0.\end{cases}
$$

Read: **how common this person’s actual drug is in the whole cohort, divided by how common it is among people with their baseline characteristics**. The numerator is a marginal proportion without conditioning on individual health; the denominator is a health-conditional probability. They operate at different probability levels. SW_i can be below or above 1.

**First use a separate 100-person A/B teaching table to see what “rescaling” does.** It has only low- and high-risk categories for hand calculation; it is not the preceding 3,000-person simulation.

| Baseline health | Actually taking A | Actually taking B | Total | Proportion choosing A in this category |
| --- | ---: | ---: | ---: | ---: |
| Low risk | 10 | 40 | 50 | 10/50=0.2 |
| High risk | 30 | 20 | 50 | 30/50=0.6 |
| Total | 40 | 60 | 100 | Overall A=40%, B=60% |

The target is all 100 people, half low risk and half high risk. Ordinary ATE weights make each drug group represent this target composition:

| Health and drug | Original count | Ordinary weight calculation | Ordinary weighted count | Stabilizing multiplier | Stabilized weighted count |
| --- | ---: | --- | ---: | --- | ---: |
| Low risk, A | 10 | 1/0.2=5 | 50 | Overall A proportion, 0.4 | 20 |
| High risk, A | 30 | 1/0.6=5/3 | 50 | Overall A proportion, 0.4 | 20 |
| Low risk, B | 40 | 1/0.8=1.25 | 50 | Overall B proportion, 0.6 | 30 |
| High risk, B | 20 | 1/0.4=2.5 | 50 | Overall B proportion, 0.6 | 30 |

After ordinary weighting, A has 50+50=100 and B also has 100, totaling 200. **These are the contributions through which each group represents all 100 target patients—not 100 additional patients or an error that must be corrected.**

After stabilization, every A weight is multiplied by 0.4, producing a total of 20+20=40. Every B weight is multiplied by 0.6, producing 30+30=60. The combined total returns to 100. The 100 actual records have weights summing to 100, so the mean weight per record is 100/100=1; this does not mean every weight equals 1.

Look at the health proportions *within* each group. Ordinary weighting gives both A and B 50% low-risk and 50% high-risk patients. After stabilization, the low-risk proportion is 20/40=50% in A and 30/60=50% in B. Both still match the whole target population. **Rescaling totals from 100/100 to 40/60 does not restore the original, imbalanced health compositions: 25%/75% in A and approximately 66.7%/33.3% in B.**

Rescaling therefore brings the overall weight scale closer to the original sample while retaining the within-group relative contributions needed here. For a risk normalized by its own group's weight sum, the multiplier cancels between numerator and denominator; either ordinary or stabilized weights can be used. “200 became 100” is not by itself a reason to claim better precision.

<details class="study-callout" markdown="1">
<summary>Second reading: What does “in expectation” mean?</summary>

This small table uses each stratum's actual count proportions, so the totals 100/100 and 40/60 hold exactly. Multivariable models generally do not produce exact equality in a single sample.

The theoretical expectation means imagining many samples, each of size N, drawn from the same population through the same mechanism; weighting with true propensity scores; and averaging the weight sums across samples. Ordinary A and B weight sums each average N, totaling 2N. After multiplication by the true marginal treatment proportions, they average N×P(Z=1) and N×P(Z=0), totaling N. N is original sample size, and P(Z=1) and P(Z=0) are the population probabilities of choosing A and B, which sum to 1. These are theoretical averages, not promises that every actual sample meets the equalities exactly.

Actual analysis also estimates propensity scores and uses sample group proportions. The mean stabilized weight is therefore often near 1, but exact equality to 1 does not determine whether the method is correct.

</details>

An A patient with ordinary weight 5 receives stabilized weight 5×0.373=1.865; another A patient with weight 2 receives 0.746. Their relative contributions remain 5/2=2.5, so within-group relative weights are unchanged.

**The name “stabilized” does not guarantee more stable estimation.** This baseline within-group constant rescaling cancels exactly from normalized group risks. The two risk-difference estimators agree in every sample, so rescaling alone cannot be claimed to reduce sampling variance. Within-group effective sample sizes also remain unchanged. Other estimators and longitudinal stabilization have different properties requiring method-specific assessment.

An A patient with conditional treatment probability 0.001 has ordinary weight 1,000 and stabilized weight 373. Stabilization does not fix a near-zero denominator. It is also different from “truncation,” which caps weights at a limit, and does not automatically fix inadequate overlap.

Distinguish ATT: scaling all A and B weights by their respective constants still targets the full-population ATE risk contrast. ATT instead retains A as the target, with A weights 1 and B weights ê/(1−ê). The numerator changes serve different purposes and targets.

- Patient 2 actually initiates A: w=1/0.698157≈1.432343; SW=0.373/0.698157≈0.534264.
- Patient 4 actually initiates B: w=1/(1−0.542066)≈2.183719; SW=0.627/(1−0.542066)≈1.369192.
- Patient 3 actually chooses A despite its relative rarity for that history, receiving larger weight 6.197547.

**B is an active comparator drug, not no treatment.** B’s probability equals 1−e(L) only in this A/B-only cohort. With three drugs A, B, and C, “not A” cannot simply mean “B.”

#### Must the two group sizes be equal?
{: #section-21 }

**Neither TTE nor IPTW requires equal A/B group sizes.** The 1,119 A and 1,881 B patients can be analyzed directly with a clear target, sufficient overlap, and the other identification assumptions. There is no need to delete B patients just to equalize counts.

- **Original counts** are actual observed patients. Ratios of 1:1, 1:2, and others are possible; real randomized trials may also use unequal allocation.
- **Baseline balance** means similar distributions of age, history, and other features, not equal totals. Two groups of 500 can differ greatly in severity, while unequal groups can have identical feature proportions.
- **Weighted counts** are weight sums, not actual or independent patients. With true unstabilized ATE weights, each group’s expected sum equals the total population, but estimated probabilities and finite samples need not produce exact equality. Stabilized weights change each group’s overall scale and likewise do not require equal group sums.

Each group’s risk divides weighted events by its own weight sum. The two denominators may differ; each group must represent the same target population’s corresponding intervention outcome, not mechanically contain the same count.

The earlier single-variable example produced exactly 1,000 weighted people per group through stratified proportions, not a TTE entry requirement. Sample size and allocation affect precision; a very small group, few events, or poor overlap may destabilize estimation without violating a rule requiring equal counts.

#### Step 6: Check weighted balance on the four baseline variables
{: #section-22 }

This section asks whether weighting has done what we need it to do, before Step 7 compares hospitalization outcomes. It uses the same 3,000-person simulation: 1,119 drug A and 1,881 drug B patients. Every number is simulated for teaching. **We are examining pretreatment characteristics, not testing whether drug A works.**

##### 6.1 Why check? Calculating weights does not make the groups comparable by itself
{: #section-39 }

A and B were not randomly assigned. The original A group is older, more frequently diabetic, and sicker; these differences may affect both drug choice and hospitalization.

Logistic regression estimates treatment probabilities from the features and model form supplied. It may omit important relationships, use an inappropriate form, or encounter data without comparable patients. Obtaining a numerical weight does not establish that these problems are solved.

Before looking at effectiveness, therefore, check three different things:

| Diagnostic purpose | What does it ask? | Main methods |
| --- | --- | --- |
| Baseline balance | After weighting, are age, health, and history distributions more similar between groups? | Weighted means/proportions, SMDs, and distribution checks |
| Data overlap | Do both A and B contain observations for patients with similar treatment propensities? | Group-specific PS distributions, sparse intervals, and individual histories |
| Weight concentration | Does the result depend on a few patients with extremely large weights? | Weight distributions, tail contributions, and ESS |

These checks cannot replace one another. Means may appear balanced because one or two patients carry much of a group's representation. Equal means can also conceal different age distributions.

##### 6.2 First method: Understand weighted means and proportions
{: #section-40 }

A **mean** is an average level, such as average age in group A. Everyone contributes equally to an ordinary mean; in a weighted mean, each person contributes according to the previously calculated weight.

Take a separate three-person example with ages 60, 70, and 80 and weights 1, 1, and 2. The ordinary mean is 70 years; the weighted mean is:

$$
(60\times1+70\times1+80\times2)/(1+1+2)=72.5\text{ years}.
$$

Nobody's age changes; the 80-year-old contributes twice as much. Likewise, a change in this study's weighted mean age reflects statistical contributions, not patients becoming younger.

The general formula is:

$$
\mu_w=\frac{\sum_i w_i x_i}{\sum_i w_i}.
$$

$$\mu_w$$ is the weighted mean; $$i$$ indexes patients; $$x_i$$ is one baseline characteristic for that patient; and $$w_i$$ is the diagnostic weight, which can be the stabilized $$SW_i$$ defined earlier. $$\sum$$ means addition across people. Calculate A's mean using only A patients, and B's using only B patients; do not pool both into one mean.

**The mean of a binary variable is a proportion.** Code recorded diabetes as 1 and its absence as 0. Averaging these indicators gives the diabetes proportion. If the three patients' diabetes indicators are 0, 1, and 1, with the same weights 1, 1, and 2, the weighted proportion is (0×1+1×1+1×2)/4=75%. It is not a direct count ratio, but “sum of weights among patients with diabetes ÷ sum of weights in the whole group.”

Thus “27.31% diabetes after weighting in A” means patients with diabetes contribute approximately 27.31% of A's total weight. It does not mean that diagnoses or original patient counts were changed.

##### 6.3 Why not just inspect the raw difference? SMD provides a common scale
{: #section-41 }

Age differences are measured in years, diabetes-proportion differences in percentage points, and severity in another score. Their raw magnitudes are not directly comparable. Even a three-year age difference means something different when ages are tightly clustered versus widely spread.

The **standardized mean difference, SMD, divides the between-group mean difference by a scale describing within-group variation in that variable.** Here we take the absolute value to focus on magnitude:

$$
\mathrm{SMD}=\frac{|\mu_A-\mu_B|}{\sqrt{(s_A^2+s_B^2)/2}}.
$$

- $$\mu_A,\mu_B$$: the A/B means of one variable; for a binary variable these are proportions.
- $$|\mu_A-\mu_B|$$: the absolute difference, regardless of which group is higher.
- $$s_A^2,s_B^2$$: within-group variances, describing how individual values vary around their group mean. These are not standard errors of the means.
- $$(s_A^2+s_B^2)/2$$: the average variance. Taking its square root returns to the variable's original units, giving the pooled standard-deviation scale used here.
- Numerator and denominator units cancel, leaving SMD unitless. SMD=0.1 means a mean difference of about one tenth of this standard-deviation scale, not “10% of patients are imbalanced.”

First understand variance and standard deviation. Ages 60, 70, and 80 have ordinary mean 70 and deviations −10, 0, and 10. Squared deviations are 100, 0, and 100. Sample variance=(100+0+100)/(3−1)=100 years², and standard deviation=√100=10 years. Squaring prevents positive and negative deviations from canceling; the square root restores years as the unit.

Use ordinary means and variances before weighting and their weighted counterparts afterward. **The comparison concerns differences in the same baseline variable among the same patients before and after statistical weighting—not patients' changes during follow-up.**

<details class="study-callout" markdown="1">
<summary>For reproduction: How is this example's weighted variance calculated?</summary>

To match the formula in the paper's extension note, the script uses:

$$
s_w^2=\frac{\sum_i w_i}{(\sum_i w_i)^2-\sum_i w_i^2}\sum_iw_i(x_i-\mu_w)^2.
$$

$$\mu_w,x_i,w_i$$ have the same meanings as above; $$s_w^2$$ is weighted variance. Square each person's deviation from the weighted mean, multiply by their weight, and sum. The leading fraction is a sample correction factor. $$(\sum w_i)^2$$ squares the sum, whereas $$\sum w_i^2$$ sums individually squared weights; they differ. When all weights equal 1, the factor becomes 1/(number of people−1), recovering ordinary sample variance.

In the three-person example, $$\mu_w=72.5$$. The weighted sum of squared deviations is 1×(60−72.5)²+1×(70−72.5)²+2×(80−72.5)²=275. Weights sum to 4 and squared weights to 6, so variance=4/(16−6)×275=110 years² and standard deviation≈10.488 years.

Software implementations of SMD differ; some retain the preweighting standard deviation in the denominator. This note's table recalculates weighted variances using the definition above. Align definitions when comparing software and inspect variances themselves, so an inflated denominator is not mistaken for better adjustment of means.

</details>

##### 6.4 Calculate the table's age and diabetes SMDs step by step
{: #section-42 }

**Age before weighting:**

1. A's mean is 72.016418 years and B's 69.078417, differing by about 2.938 years.
2. Their variances are approximately 44.617816 and 45.035372 years².
3. The pooled standard-deviation scale is √[(44.617816+45.035372)/2]≈6.695267 years.
4. SMD≈2.938/6.695267≈0.439.

**Age after weighting:**

1. A's weighted mean is 70.296075 and B's 70.158071, differing by about 0.138 years.
2. Weighted variances are approximately 45.643801 and 45.969204 years².
3. The pooled standard-deviation scale is approximately 6.768050 years.
4. SMD≈0.138/6.768050≈0.020.

We therefore see more than “0.439 got smaller”: the mean age difference fell from about 2.94 to 0.14 years and also became much smaller relative to the spread of age.

**Diabetes before weighting:** A=0.396783 and B=0.202552, giving a difference of 0.194231, or about 19.42 percentage points. Using binary-variable variances produces a pooled standard deviation of about 0.447868, so SMD≈0.194231/0.447868≈0.434.

**Diabetes after weighting:** A=0.273104 and B=0.274195. Their absolute difference is about 0.001090, or 0.109 percentage points. The pooled standard deviation is about 0.446036, giving SMD≈0.00244, displayed as 0.002 to three decimal places. Calculations use full precision, so working backward from rounded table entries may give slightly different values.

##### 6.5 How should you read the table? Inspect each row, then the overall pattern
{: #section-43 }

| Baseline variable | A before weighting | B before weighting | Before SMD | A after weighting | B after weighting | After SMD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Age (years) | 72.016 | 69.078 | 0.439 | 70.296 | 70.158 | 0.020 |
| Diabetes proportion | 39.68% | 20.26% | 0.434 | 27.31% | 27.42% | 0.002 |
| Mean severity score | 0.509 | −0.122 | 0.653 | 0.101 | 0.114 | 0.012 |
| Background treatment C use | 38.96% | 44.87% | 0.120 | 41.92% | 42.57% | 0.013 |

A common rough diagnostic reference is **absolute SMD below 0.1**; to follow the paper's definition, this example counts ≤0.1 as meeting its criterion. This is a rule of thumb, not a mathematical boundary proving successful causal identification. Research quality does not fundamentally change between 0.099 and 0.101.

- Age: 0.439→0.020, substantially reducing the original difference and meeting this criterion.
- Diabetes: 0.434→0.002, substantially reducing the proportion difference and meeting the criterion.
- Severity: 0.653→0.012, the largest original difference, with closer weighted means.
- Background treatment C: 0.120→0.013, originally just above the reference threshold and closer after weighting.

An appropriate statement is: **The four measured baseline variables have similar weighted means or proportions, and all four absolute SMDs are below 0.1.** Do not claim that all confounding is eliminated, that randomization has been achieved, or that this table shows drug effectiveness.

Group sizes were not equalized, nor were all means forced to match exactly. Equal means can conceal different distributions: one group could all be age 70, while the other is half 50 and half 90. Both means are 70, but their age distributions differ greatly. Real studies should examine weighted distribution plots, quantiles, variances, and important nonlinear terms and interactions—for example, the proportion both elderly and severely ill. A common Love plot displays each variable's pre- and postweighting SMD alongside a 0.1 reference line, making remaining imbalances easier to locate. It does not replace distribution checks.

Do not use “baseline comparison p>0.05” as a balance criterion. P values also depend on sample size, and nonsignificance does not imply similarity. A high treatment-model AUC is not a pass criterion either: AUC measures discrimination of treatment choice. For principles of mean/proportion, distribution, and overlap diagnostics, see [Austin and Stuart (2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4626409/).

##### 6.6 Second check: Do the groups' propensity scores overlap?
{: #section-44 }

**Purpose: check that the comparison is not being forced between entirely different patients.** The logistic regression's ê(L) predicts A's probability. If a category has high ê but almost nobody actually receives B, little evidence describes its outcomes under B. The analogous problem occurs when low-ê regions contain few A patients.

**Method: separate patients by actual A/B receipt and inspect PS histograms or densities, together with counts in each interval.** With unequal group sizes, within-group proportions or densities help compare shapes, but retain actual counts to avoid concealing sparse data.

The updated script exports these unweighted counts:

| Predicted probability of A | Actual A count | Actual B count |
| --- | ---: | ---: |
| 0≤ê<0.2 | 88 | 507 |
| 0.2≤ê<0.4 | 359 | 839 |
| 0.4≤ê<0.6 | 368 | 413 |
| 0.6≤ê<0.8 | 273 | 114 |
| 0.8≤ê≤1 | 31 | 8 |

**Interpretation:** Both drugs appear in every broad interval, suggesting some overlap. However, only eight B patients are in the highest-probability interval. Examine whether a small number of tail observations carry its representation and whether their baseline histories are comparable with A patients. Counts in five broad bins do not establish positivity within finer regions or joint multivariable histories.

The overall range of 0.0323–0.9087 reports only minimum and maximum estimated values, not where the groups overlap. Logistic outputs generally lie between 0 and 1 by construction, so “all probabilities are positive” does not prove positivity. Group-specific ranges are approximately A=0.0624–0.9037 and B=0.0323–0.9087; overlapping ranges likewise cannot replace interval counts and characteristic checks.

##### 6.7 Third check: Are weights concentrated in a few patients?
{: #section-45 }

**Purpose: identify heavy dependence on a small number of patients.** For example, an actual B patient with ê=0.99 has characteristics strongly associated with A. Their stabilized B weight is 0.627/(1−0.99)=62.7, so changes to that record could matter greatly.

**Method:** Within A and B, inspect minima, medians, 95th/99th percentiles, maxima, and the share of total group weight held by a small number of the largest weights. The median means about half the weights fall below it; the 95th percentile means about 95% do not exceed it—not a 95% confidence interval. Software quantile interpolation may differ slightly.

| Stabilized weight SW | A group | B group |
| --- | ---: | ---: |
| Minimum | 0.413 | 0.648 |
| Median | 0.809 | 0.884 |
| 95th percentile | 2.136 | 1.693 |
| 99th percentile | 3.294 | 2.441 |
| Maximum | 5.976 | 6.870 |
| Share of total weight in the largest approximately 1% of records | 4.61% | 3.36% |

The last row rounds 1% of each group's count upward: 12 A and 19 B patients. Those 12 A patients carry about 4.61% of A's total contribution. This describes concentration, not their exact influence on the final effect estimate, which also depends on their outcomes and other factors.

**Interpretation:** Weights are unequal, but “the maximum is below 10” does not establish safety. No fixed acceptable upper limit applies to all studies. Assess tail counts, relative contributions, overlap, ESS, influential patients' characteristics, and sensitivity analyses together. Weights were not truncated here.

##### 6.8 What is ESS, and why is it below the actual count?
{: #section-46 }

Here, **effective sample size, ESS, is a diagnostic based on weight inequality.** It asks approximately how many records with similar contributions this group resembles in terms of concentration. It neither removes patients nor precisely measures all independent information in the treatment-effect estimator.

Take a separate four-person example. If all weights equal 1, contributions are equal and ESS=4. If weights are 1, 1, 1, and 7, the last patient carries 70% of the total. There are still four people, but information is no longer evenly distributed.

A common formula is:

$$
\mathrm{ESS}=\frac{(\sum_iw_i)^2}{\sum_iw_i^2}.
$$

Here $$i$$ ranges only over the drug group, and $$w_i$$ is that patient's weight, possibly $$SW_i$$. The numerator squares the sum of weights; the denominator sums squared individual weights. Squaring makes large weights more prominent in the denominator. Equal weights give ESS equal to the actual group size; for nonnegative weights, greater concentration reduces ESS.

For the unequal four-person example, ESS=(1+1+1+7)²/(1²+1²+1²+7²)=100/52≈1.92. This does not mean only 1.92 people remain; a few records dominate the contributions.

Actual calculations for this simulation are:

- A: stabilized weights sum to about 1,119.987 and squared weights to 1,534.034. ESS≈1,119.987²/1,534.034≈817.7, versus 1,119 actual patients—about 73.1% of the original count.
- B: stabilized weights sum to about 1,879.687 and squared weights to 2,164.577. ESS≈1,632.3, versus 1,881 actual patients—about 86.8%.

**Interpretation:** A's weights are less even, with a larger relative ESS reduction. These two numbers alone cannot establish adequate precision. Rare outcomes may still provide few events, and repeated records introduce correlation. Formal analysis needs standard errors and confidence intervals appropriate to the estimator.

Multiplying every weight in a group by the same constant multiplies both ESS's numerator and denominator by its square, which cancels. Moving from ordinary to stabilized weights therefore does not recover ESS here. Smaller-looking stabilized weights do not create information.

##### 6.9 What if diagnostics are poor? What can you conclude afterward?
{: #section-47 }

| Finding | What to examine or do first |
| --- | --- |
| An important variable retains a large SMD | Check units, coding, missing-data handling, and baseline measurement timing; assess justified nonlinearities or interactions omitted from the treatment model, revise, and repeat diagnostics |
| Similar means but different distributions | Examine quantiles, variances, plots, and relevant variable combinations; do not focus solely on passing a mean-SMD threshold |
| A patient category receives almost exclusively one drug | Assess common eligibility and data support; explicitly revise the target or population if necessary, rather than dropping patients while claiming the original full-population ATE |
| Extreme weights and sharply reduced ESS | Investigate model/data problems and tail patients; conduct prespecified or transparently reported sensitivity analyses. Truncation changes estimation, requiring new balance and result checks—not merely smaller numbers |

Revise models with attention to design, baseline balance, and data support, not “which model makes the effect significant.” Diagnostics interact: a more complex model is not necessarily better, and reducing extreme weights may sacrifice balance.

**What this step supports in this example:** The four measured variables have much closer means/proportions; broad PS bins show overlap, but few B records occur in the high-probability region; unequal weights reduce A/B ESS to about 818/1,632. We can proceed to report teaching outcome estimates while retaining these limitations. We cannot yet claim complete joint-distribution balance, absence of unmeasured confounding, or that an actual clinical study meets an acceptable evidence standard.

For reproduction, the accompanying script now exports each variance, SMD denominator, group-specific weight quantiles, weight sums and squared sums, PS-bin counts, and tail contributions. There is no need to reconstruct intermediate values from rounded display tables. Step 7 now uses the weights to compare one-year hospitalization outcomes.

#### Step 7: Use these weights to compare one-year risks for A and B
{: #section-23 }

With complete outcomes, calculate separately within each drug group:

$$
\widehat R_A=\frac{\sum_{i:Z_i=1}w_iY_i}{\sum_{i:Z_i=1}w_i},\qquad
\widehat R_B=\frac{\sum_{i:Z_i=0}w_iY_i}{\sum_{i:Z_i=0}w_i}.
$$

R denotes one-year hospitalization risk; subscripts A/B identify drug strategies; the colon restricts each sum to the relevant group. Event records such as death or hospitalization contribute their weights to the numerator, and everyone in the group contributes to the denominator. Here Y is hospitalization, not death.

| Analysis | A risk | B risk | A−B risk difference | A/B risk ratio |
| --- | ---: | ---: | ---: | ---: |
| Crude comparison | 14.03% | 12.33% | +1.70 percentage points | 1.138 |
| Full-population IPTW | 10.88% | 15.03% | −4.15 percentage points | 0.724 |
| Full-population stabilized IPTW | 10.88% | 15.03% | −4.15 percentage points | 0.724 |

Here stabilization multiplies weights by a constant within each group, scaling the normalized risk’s numerator and denominator equally and producing the same result. This does not imply that every weighted model’s point estimates and variances are unaffected by between-group rescaling.

A appears worse crudely partly because its recipients were initially sicker. The weighted comparison more closely represents initiation strategies in a common population. **A direction reversal is neither proof of successful IPTW nor an inevitable real-data result.** This is a deliberately constructed simulation with no confidence intervals or significance conclusions yet.

The generating model’s expected risks in these baseline patients are approximately A=10.44% and B=14.44%, differing from finite-sample IPTW because treatment and outcome sampling are random. Real studies do not know such generating-model “truth” and cannot use it to verify unbiasedness. The script illustrates point estimates, not a complete clinical-analysis package; formal analysis must address missingness/censoring, complex sampling or repeated records, and suitable inference.

#### Step 8: How does this same A/B example connect to other weights?
{: #section-24 }

- **ATT**: If the target becomes “the 1,119 actual A initiators, all initiating A versus all initiating B,” A weights are 1 and B weights ê/(1−ê). The same data yield A=14.03%, B=19.58%, difference −5.55 percentage points. This targets a different population and cannot validate the full ATE as if it answered the same question. “Treated” in ATT specifically means A here; B users also receive treatment.
- **Longitudinal IPTW**: Sustained A versus sustained B requires predicting each next action from past treatment and current history, then constructing cumulative weights matched to strategies and analysis. Baseline ê(L) is only the first component, not a value to repeat for all later probabilities; see §7.
- **IPCW/CCW**: If sustained-strategy effects are estimated by artificially censoring protocol deviations, model remaining compatible and uncensored. The baseline A/B PS is not an uncensoring probability, and the same adherence process must not be adjusted twice; see §8.
- **Survival analysis**: With unequal observed follow-up, the complete one-year binary-outcome formula is insufficient; appropriate weighted survival curves or models are needed. No HR was estimated here, so 0.724 is not an HR; see [The Cox Proportional Hazards Model]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}).

#### Reproduction and reading order
{: #section-25 }

Read through Step 5 and manually calculate patients 2 and 4’s weights, then examine balance and outcome tables. Return to §7 to understand why later treatment choices need new probability models.

- [Runnable Python script]({{ "/assets/causal-inference/iptw-lr-example/multivariable_iptw.py" | relative_url }}): NumPy only, fixed random seed 20260909; generates data, fits logistic regression using actual Z, and outputs JSON.
- [Complete results]({{ "/assets/causal-inference/iptw-lr-example/results.json" | relative_url }}): generating and fitted coefficients, full-precision calculations for eight patients, SMDs, risks, and weight diagnostics.

In the script, a=1 means drug A and a=0 drug B, corresponding to Z here. y1prob/y0prob are simulated hospitalization probabilities under A/B initiation; their names must not be mistaken for treatment/no treatment.


### 6.2 IPTW and PSM: One propensity score, two ways to construct comparable groups
{: #section-48 }

**Inverse probability of treatment weighting (IPTW) assigns different statistical weights to patients. Propensity score matching (PSM) uses propensity scores to find suitable comparators. Neither is the propensity score itself, and neither is the final outcome model.**

#### A common starting point: Multivariable logistic regression predicts A/B choice
{: #section-49 }

Let Z=1 mean initiating drug A and Z=0 initiating B. L includes age, diabetes, pretreatment severity, and background treatment C use. The propensity score e(L)=P(Z=1 | L) is the probability of receiving A among people with these features, not mortality risk.

Both methods can use the preceding multivariable logistic regression: fit coefficients with Z as the dependent variable and L as predictors, then obtain each person's ê(L). A logistic model does not inherently belong to IPTW or PSM; the distinction is how its scores are subsequently used.

For a separate illustration with hypothetical coefficients, set η=−0.5+0.4×(age−70)/10+0.8×diabetes+0.6×severity−0.3×background treatment C, and ê(L)=1/[1+exp(−η)]. A 75-year-old with diabetes, severity 2, and no C use has η=1.7 and ê(L)≈0.846. The following sections explain how to use this multivariable score. These coefficients are teaching choices, not the preceding simulation's fitted estimates.

#### PSM: Find drug B patients with nearby propensity scores
{: #section-50 }

Suppose the A patient's score is 0.846 and candidate B patients score 0.840, 0.600, and 0.200. Nearest-neighbor matching first considers 0.840 because it is closest to 0.846.

That does not mean the two patients have identical age, diabetes, or severity. Different feature combinations can produce similar scores. The propensity score's balancing property concerns population distributions, not “two people with the same score are the same person.” After matching estimated scores in a finite sample, examine balance for each baseline variable.

Specify common matching rules in the analysis:

- **1:1 matching:** match each A patient with one B patient; 1:2 and other ratios are possible.
- **Nearest neighbor:** choose the closest candidate on a specified distance scale, such as the score or its logit. State the scale.
- **Caliper:** impose a maximum allowable distance. Even the nearest patient may be too far away; do not force the match. For a purely illustrative caliper of 0.02 on the raw score scale, 0.846 can match 0.840 but not 0.600. A value of 0.02 is not a universal recommendation.
- **With or without replacement:** decide whether the same B patient may be reused for other A patients. Reuse creates no additional patients; analysis must account for contributions and dependence.

Simple 1:1 matching without replacement retains matched patients; unmatched patients do not enter that matched sample's effect estimate. With complete one-year mortality follow-up, compare death proportions in matched A and B groups. With censoring, use survival analysis compatible with the matching design and censoring mechanism. Standard errors should appropriately account for matched-set structure, rather than treating every matched record as independent by default.

#### IPTW: Let the probability of the actual action determine its contribution
{: #section-51 }

For ordinary baseline IPTW targeting all eligible patients' ATE, A patients receive 1/ê(L) and B patients 1/[1−ê(L)].

With the same score of 0.846, actual A receipt produces weight about 1.18; actual B receipt produces about 6.47. B is rarer among people with these features, so its records receive greater representation.

Baseline IPTW without truncation or restriction to common support usually retains positive weights for all analysis patients. Retaining records does not guarantee precision: a few large weights can substantially reduce ESS. Use the weights to estimate risks, risk differences, or weighted survival quantities, rather than comparing only unweighted outcome proportions.

#### The distinction most often misread: Whose average effect is estimated?
{: #section-52 }

**ATE** asks how average outcomes differ if all eligible patients initiate A versus all initiate B. The ordinary ATE IPTW weights above target this population.

**ATT** asks how average outcomes differ among actual A initiators if all initiate A versus if those same people initiate B. Common matching designs that use A as the anchor and find B controls for each A patient usually target ATT. If some A patients cannot be matched and are excluded, the supported population may become successfully matched A patients rather than the entire original A group.

IPTW can also target ATT, with A weights 1 and B weights ê(L)/[1−ê(L)]. Matching is likewise not limited to one target or algorithm. Do not memorize “IPTW always means ATE and PSM always means ATT.”

If IPTW's ATE differs from PSM's matched-population effect, the populations and their effects may differ; neither computation is necessarily wrong. Before treating them as cross-validation, align target populations, A/B strategies, outcomes, follow-up, effect scales, and analysis rules.

#### Comparison table
{: #section-53 }

| Feature | IPTW | Common PSM: A-anchored nearest-neighbor matching |
| --- | --- | --- |
| Use of PS | Convert it into each patient's weight | Measure distance between candidate matches |
| Patient contribution | Determined by the specified weights | Determined by matching inclusion, ratio, and reuse |
| Must original group sizes be equal? | No | No; 1:1 matching without replacement produces equal matched counts afterward |
| Target population | Determined by weights, such as ATE or ATT | Usually A patients; clarify the target if A patients are lost |
| Signs of poor overlap | Extreme weights and reduced ESS | No suitable matches, or residual differences from forced matches |
| Key diagnostics | Weighted variable-specific SMDs/distributions, PS overlap, weights, and ESS | Matched variable-specific SMDs/distributions, distances, retained counts, and excluded patients' characteristics |
| Subsequent analysis | Weighted outcome estimation with suitable inference | Outcome estimation and inference compatible with matching structure |

#### A connection: Matching also allocates statistical contributions
{: #section-54 }

In the simplest 1:1 matching without replacement, selected records can be viewed as contributing 1 and unselected records 0. More complex matching can generate noninteger or reuse weights. These are not automatically the IPTW weights 1/e or 1/(1−e).

Both methods aim to create treatment and comparison populations comparable on baseline features, but assign contributions differently. Do not mechanically apply original IPTW after matching on the assumption that more adjustment is better; combined estimators need a clear target and methodological justification.

#### Shared limitations and choosing between methods
{: #section-55 }

Both require appropriately defined treatment strategies, no unmeasured confounding, sufficient treatment-choice support in the target population, and suitable model and analysis conditions. Neither repairs an incorrect time zero, immortal time bias, or unmeasured variables. Small SMDs provide evidence of measured balance, not proof of achieved randomization.

In TTE, both belong to confounding adjustment after protocol and cohort definition and before outcome-effect estimation. Define the ATE/ATT question first, then assess available data. With a full-population ATE target and good overlap, ATE IPTW directly corresponds to the target. If A users are the focus and B provides enough comparable patients, matching or ATT weighting may be considered. With severe lack of overlap, neither creates nonexistent comparisons.

Do not choose based on which method gives a significant p value. First assess whether they answer the same question, balance baseline features, have data support, and permit appropriate inference. Neither baseline PSM nor baseline IPTW automatically handles time-varying confounding for sustained strategies.

References: [Austin's propensity-score methods review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3144483/); [Austin on paired and unpaired inference after matching](https://pubmed.ncbi.nlm.nih.gov/21337595/); [Li and colleagues on target populations and balancing weights](https://arxiv.org/abs/1404.1785).


## 7. Why multiply weights across time for sustained strategies?
{: #section-26 }

This section is expanded in [Longitudinal IPTW: Sustained Drug A versus Drug B]({{ "/causal-inference/longitudinal-iptw/" | relative_url }}). After the baseline example here, beginners should read that note's §1–§6, then return for censoring weights in §8.

The central idea is that the first weight addresses baseline treatment choice. Later health affects the second choice, requiring another adjustment to the contribution already carried forward: cumulative weight=first factor×second factor. Time passing does not automatically require more weights; the need depends on the target strategy and treatment/censoring selection processes.

### A numerical example with two decisions
{: #section-27 }

Of 100 people with the same baseline health, 50 choose A and receive first weight 2. Suppose their relevant histories remain alike before the second decision and 10 continue A; the second factor is 5. These 10 people receive cumulative weight 2×5=10, totaling 100. Adding to obtain 7, or using either factor alone, does not address both selections.

For the complete count explanation, health branches, and weighted AA/BB outcomes, see the new note's §3–§5. Its §7 calculates probabilities and weights for four treatment histories using two actually fitted multivariable logistic regressions. Symbols are defined before use, and the longer formula appears in §8.

### Why include time-varying health in the weight model?
{: #section-28 }

It may affect both the current drug choice and subsequent outcomes. However, previous treatment may have changed this health state, so adjustment should not force later health distributions to be identical under sustained AA and BB. The new note's §6 uses the severely ill branch, 5×8=40, to explain why we do not also invert the probability of the health state. Its §9–§11 cover event timing, sequential diagnostics, stabilization, and connections to CCW.

## 8. IPTW and IPCW: Do not confuse the probabilities
{: #section-29 }

So far we handled “who receives which treatment.” Continued outcome observation is a separate selection process. Even with randomized baseline treatment, preferential loss of sicker patients can make observed outcomes disproportionately represent healthier people. We must also ask: **given the same known history, whose later outcomes remain visible?**

| Weight | What does the denominator estimate? | What does it address? |
| --- | --- | --- |
| IPTW | Probability of the actual treatment action given current history | Confounding related to treatment choice |
| IPCW | Probability of remaining uncensored given current history | Selection from loss to follow-up or artificial censoring |

If sicker patients are more likely both to leave follow-up and to die, the remaining sick patients may inadequately represent the original sick population.

If the probability of remaining observable at a step is 20% given the relevant history, those retained can receive censoring factor $$1/0.2=5$$, provided enough history is known for them to represent comparable leavers’ target outcomes.

This shares the “rare records represent more people” logic, but the rare records are **those still observed**. If only 20 of 100 similar patients remain observable, weighting each by 5 can, under the assumptions, let their subsequent outcomes represent the original category. We have neither classified the 80 lost patients as alive nor guessed each person’s death time.

This is the distinction between censoring and death: **loss to follow-up makes future outcomes unknown; death, as the outcome here, means the target event has occurred**. An observed death contributes an event and needs no subsequent survival observation. The fact that the patient no longer attends does not turn known death into loss. The next formula handles remaining observable; it does not “weight deaths away.”

As with treatment weights, new opportunities for loss at each visit require multiplying inverse retention probabilities. One stepwise schematic form is:

$$
W_i^C(K)=\prod_{k=0}^K
\frac1{P(C_{k+1}=0\mid C_k=0,H_{ik},A_{ik})}.
$$

The censoring notation is:

- $$C_k$$: censoring indicator through time $$k$$, 0 for uncensored and 1 for already censored. **It is not the censoring time $$C$$ in months or years used in the Cox note**; these formulas use different encodings.
- $$C_{k+1}=0$$: “still uncensored at the next time”; $$k+1$$ is a subscript, not a power. Conditioning on $$C_k=0$$ asks the probability of remaining next step among currently uncensored people.
- $$H_{ik}$$: person $$i$$’s relevant information at this step, potentially including past health and treatment. Here $$H$$ means history, **not Cox cumulative hazard $$H_0(t)$$**.
- $$A_{ik}$$: person $$i$$’s current treatment action, included as a predictor of subsequent censoring.
- $$W_i^C(K)$$: cumulative censoring weight across intervals 0 through $$K$$. Superscript $$C$$ labels censoring, not a power; $$\prod$$ multiplies the inverse probabilities.

Read: **among currently uncensored people, estimate each probability of remaining under the existing history and treatment, then multiply its inverse across steps**. Two successive conditional retention probabilities of 0.8 give retained people cumulative weight $$(1/0.8)\times(1/0.8)=1.5625$$. This is neither mortality risk nor a probability of certain adherence.

Apply this schematic only within the relevant risk set, updating among those alive, observed, and eligible for that step. Retain observed death outcomes; do not code death as loss. If an outcome occurs during step $$k$$, use weights needed through the event according to actual event/censoring order, without requiring survival to the next scheduled measurement. Prespecify measurement, treatment, event, and censoring ordering in the data. These conditional probabilities generally also require estimation.

With several selection mechanisms, properly defined treatment and censoring weights may be multiplied. However, **the same treatment-adherence process** must not be adjusted once through IPTW and again through protocol-deviation IPCW.

### Connection to clone–censor–weight
{: #section-30 }

[Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}) artificially censors copies that deviate from a strategy. Weighting chiefly addresses the resulting strategy-compatibility selection by estimating the probability of remaining compatible and uncensored.

- Death while following the strategy: record the death; do not exclude it because the person “did not persist for five years.”
- A strategy specifying baseline initiation only: later discontinuation need not violate the protocol, so do not automatically censor then.
- A sustained-treatment strategy: discontinuation outside protocol exceptions may trigger artificial censoring, whose selection must then be addressed.

First distinguish [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}).

Nonfatal outcomes also require handling competing events such as death. See [Competing events and adaptations of classical methods]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}#section-47). Treatment weights do not automatically remove competing events; weighted Aalen–Johansen estimation can estimate real-world cumulative risk.

## 9. Are IPW and a marginal structural model the same thing?
{: #section-31 }

For how weights actually enter time-to-event analysis, see [Weighted Survival Analysis in TTE: From Risk Sets to Survival Curves and Cox]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}). First calculate weighted events, risk sets, and KM products using its eight-person table, then connect the same baseline multivariable logistic regression to death and loss-to-follow-up times. Do not apply complete one-year outcome proportions directly to incompletely followed data.

Calculating weights does not finish effect estimation. Weights specify each record’s contribution; those records must still yield strategy risks or fit a strategy–outcome relationship. This explains why IPW and MSM are distinct.

- **IPW is a weighted estimation method.**
- **A marginal structural model (MSM) models population outcome relationships under interventions.** IPW can estimate it.

For example, specify a marginal mortality-risk model under strategy $$g$$. Here $$g$$ names a complete prespecified action rule, such as “always treat,” not a patient index. Under corresponding assumptions, a marginal Cox proportional hazards model can also be specified and fitted with weights.

“Marginal” emphasizes the target population’s overall outcomes under each strategy, not a conditional coefficient holding all health variables fixed. Post-treatment health may develop different distributions under different strategies. The model must still specify how treatment history enters, its temporal structure, and functional form; effects in particular baseline subgroups may also be prespecified.

If weighted Cox is the final model:

- Outcome-model assumptions such as PH still matter.
- HR is still not a fixed-horizon risk ratio.
- A risk difference still requires obtaining and comparing the relevant risk curves.
- Appropriate standard errors address uncertainty, not confounding or incorrect time zero.

## 10. Large weights, stabilized weights, and positivity
{: #section-32 }

For stabilized weights, extremes, and effective sample sizes in the same multivariable A/B example, see Steps 5 and 6 of [the complete multivariable A/B logistic-regression IPTW example]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15). Step 7 explains invariance of normalized group risks to scaling.

### What do large weights mean?
{: #section-33 }

Giving rare records larger weights makes the method work, but also makes estimates depend more heavily on a few records. An action probability of 0.01 gives inverse weight 100; changing that one person’s outcome can noticeably alter the weighted result.

Possible causes include sparse samples, model problems, near-deterministic treatment choices, or inadequate support for the target strategy. Large weights do not automatically prove model misspecification but require investigation.

If an action needed under a history that can arise under the target strategy has true probability 0, there is no compatible record to use. Inverting a probability cannot create information. This is a structural positivity problem.

### Stabilization and truncation are different operations
{: #section-34 }

A baseline stabilized weight often replaces numerator 1 with the marginal probability of the actual treatment:

$$
SW_i=\frac{P(A=A_i)}{P(A=A_i\mid L_i)}.
$$

$$SW_i$$ is person $$i$$’s stabilized weight; $$SW$$ is an abbreviation, not multiplication. $$A$$ is the treatment variable and $$A_i$$ this person’s actual action, so $$P(A=A_i)$$ is “the whole population’s proportion taking this action,” without conditioning on health. Denominator $$P(A=A_i\mid L_i)$$ is the probability for people with that person’s health. Treated people use numerator $$P(A=1)$$ and untreated people $$P(A=0)$$. Both are estimated from data in practice.

Read: **divide how common this action is overall by how common it is given this person’s health**.

In the original example, each actual group contains half the sample, so both numerators are 0.5. Weights 5 and 1.25 become 2.5 and 0.625. Multiplying everyone within a group by the same constant does not alter that group’s normalized weighted risk.

Stabilization aims to improve weight scale and estimation precision while retaining the structure required for the target estimand. It does not eliminate near-zero denominators; simple within-group constant scaling here does not create effective information.

Longitudinal stabilization is more complex. Numerators often retain past treatment; if some baseline covariates are also retained, the target marginal model and subsequent standardization must match. Copying a numerator does not justify claiming all variables are balanced.

Truncation instead restricts unusually large or small weights to a prespecified range. It may improve precision but introduce bias, and cannot repair structurally unsupported treatment paths.

Report distributions, extreme values, weighted balance, and sensitivity analyses, rather than saying “IPW makes this equivalent to a randomized trial.” [Cole and Hernán: Weight construction and diagnostics](https://pmc.ncbi.nlm.nih.gov/articles/PMC2732954/)

## 11. What assumptions does IPW require?
{: #section-35 }

1. Well-defined interventions, consistency, and related conditions.
2. Measurement and appropriate use of sufficient confounding information; longitudinally, sufficient history before each decision.
3. In relevant histories possible under the target strategy, a chance of observing required actions—positivity. Censoring adjustment also requires a chance of remaining uncensored.
4. Reliable treatment- and censoring-probability estimation. Correct formulas with incorrect probability models can still produce incorrect weights.
5. Reliable treatment, outcome, health, and temporal information, with appropriate handling of follow-up selection.

If more frequent testing records more disease, IPW does not automatically recover true incidence. If future-use grouping creates immortal time, a baseline propensity score does not automatically correct it. Design appropriately first, then choose an estimator.

## 12. Review alongside the g-formula
{: #section-36 }

For the actual comparison on the same 3,000-person multivariable A/B dataset, see [G-formula and IPTW answer the same multivariable A/B question]({{ "/causal-inference/g-formula/" | relative_url }}#section-9). IPTW estimates one-year A/B risks of 10.88%/15.03%, while outcome logistic regression plus standardization gives 10.56%/15.08%. The former predicts treatment choice and the latter hospitalization. These simulated point estimates need not agree exactly in finite samples.

| Question | G-formula | IPW |
| --- | --- | --- |
| Main baseline model | Conditional outcome model | Treatment-probability model |
| How are data used? | Predict under different interventions for the target population, then average | Weight observed outcomes under actual actions |
| Longitudinal extension | Simulate/integrate health and outcome development | Weight across decisions and censoring histories |
| Health affected by past treatment | Allow development under each strategy, then aggregate | Use it to predict later selection and construct suitable weights |
| Main risks | Model misspecification, unsupported extrapolation, unmeasured confounding | Probability-model misspecification, extreme weights, unmeasured confounding |

Both can address the same causal question, and neither computational procedure alone guarantees identification. They can also be combined with other methods; this note first establishes the basic versions.

For a third common approach, see [G-Estimation and Structural Nested Models]({{ "/causal-inference/g-estimation/" | relative_url }}). It may also estimate treatment probabilities but uses them in estimating equations for a structural-effect model. Using propensity scores does not necessarily mean inverse probability weighting.

## 13. Self-check
{: #section-37 }

1. Why do controls use $$1/[1-e(L)]$$? — $$e(L)$$ is treatment probability given the same health; invert the probability of the person’s actual “no treatment” action.
2. Does weight 5 mean four additional people were recruited? — No. It increases only the record’s representation in estimation.
3. Why multiply longitudinal weights? — Each action’s selection given prior history must be handled sequentially.
4. Is a loss-to-follow-up weight the inverse death probability? — No. It estimates the probability of remaining observable.
5. If no one with a history follows a strategy, can truncation supply the missing evidence? — No.

## References
{: #section-38 }

- [Hernán and Robins: Causal Inference: What If](https://miguelhernan.org/whatifbook): baseline IPW, longitudinal treatment, and identification.
- [Cole and Hernán (2008): Constructing Inverse Probability Weights for Marginal Structural Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC2732954/): weights, stabilization, positivity, and practical checks.
- [Naimi, Cole, and Kennedy: An introduction to g methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6074945/): conceptual distinctions between g-methods and MSMs.
