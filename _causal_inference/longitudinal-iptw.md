---
layout: "causal-note"
title: "Longitudinal IPTW: Sustained Drug A versus Drug B"
description: "Understand why treatment weights multiply across decisions, using complete count examples, two fitted logistic regressions, event timing, and longitudinal diagnostics."
group: "Estimation"
reading_label: "Companion to step 14"
order: 14.1
math: true
causal_notes: true
mermaid: true
date: "2026-09-13"
last_modified_at: "2026-09-13"
tags: ["causal-inference", "inverse-probability-weighting", "longitudinal", "sustained-treatment"]
toc: [{"title": "1. First express “sustained use” as two concrete decisions", "anchor": "section-1"}, {"title": "2. Why is baseline weighting alone insufficient?", "anchor": "section-2"}, {"title": "3. Temporarily hold health alike: Why does 100→50→10 require multiplication?", "anchor": "section-3"}, {"title": "4. When health branches: A complete 200-person A/B example", "anchor": "section-6"}, {"title": "5. Weights alone do not give outcomes: Weight people and events together", "anchor": "section-9"}, {"title": "6. A common misunderstanding: Why can subsequent health differ under AA and BB?", "anchor": "section-10"}, {"title": "7. Where do the probabilities come from in research? Fit two multivariable logistic regressions", "anchor": "section-11"}, {"title": "8. After the examples, write the multitime formula", "anchor": "section-16"}, {"title": "9. When is a weight used? Do not apply later factors to earlier records", "anchor": "section-19"}, {"title": "10. What should you check, and what conditions are required?", "anchor": "section-20"}, {"title": "11. Second-reading supplement: Stabilization and CCW", "anchor": "section-21"}, {"title": "12. Self-check and references", "anchor": "section-24"}]
previous_note: "/causal-inference/inverse-probability-weighting/"
next_note: "/causal-inference/weighted-survival-analysis/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). This note expands [Why multiply weights across time for sustained strategies?]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-26)

Only two prerequisites are needed: ordinary baseline IPTW inverts the probability of the actual action, and [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}) distinguishes “specify initiation only” from “require continued use.” For the inputs, fitting, and weights of a multivariable baseline logistic regression, see [The complete multivariable drug A versus B example]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15).

<aside class="study-callout study-callout--abstract" markdown="1">

**The one idea this note explains**

Baseline weights address the first treatment choice. A later treatment choice related to health introduces another selection process that must also be addressed. The second adjustment acts on contributions already established by the first: multiply “previous cumulative weight × current weight factor,” rather than adding the factors.

</aside>

<aside class="study-callout study-callout--tip" markdown="1">

**A reading order for beginners**

First read §1–§6: establish the timeline, calculate counts and outcomes, then understand why subsequent health need not be identical. On a second reading, use §7–§10 to replace count proportions with multivariable logistic regression and then examine multitime formulas and diagnostics. Stabilization and CCW connections are in §11; they are not prerequisites for understanding multiplication. All data are teaching simulations. The 100-, 200-, and 6,000-person examples are separate, not published research or clinical findings.

</aside>

## 1. First express “sustained use” as two concrete decisions
{: #section-1 }

Imagine comparing two alternative drugs for the same disease at the same treatment stage:

- Strategy AA: choose A at baseline and use it through the first interval; choose A again at month 3 and use it through the second interval.
- Strategy BB: choose B at baseline and use it through the first interval; choose B again at month 3 and use it through the second interval.

We divide six months into two intervals, with one drug decision at each interval's start and no switching or discontinuation within it. These are the only two drug options, and treatment versions such as dose are fixed by the teaching protocol. If real practice allows no treatment, multiple drugs, combinations, or within-interval changes, encode and define those strategies separately rather than copying this binary setup.

The target population is defined at baseline: everyone meeting common eligibility criteria and suitable for either A/B strategy. Compare their outcomes under AA versus BB, without quietly changing the target to “patients who happened to persist in practice.”

<pre class="mermaid">
flowchart LR
    L0["Before baseline:<br/>record age, history,<br/>and health"] --> Z0["Decision 0:<br/>choose A or B"]
    Z0 --> L1["Before month 3<br/>drug decision:<br/>record new health"]
    L1 --> Z1["Decision 1:<br/>choose A or B<br/>for the next interval"]
    Z1 --> Y["End of second interval:<br/>record outcome"]
</pre>

To make multiplication clear first, both hand calculations and code assume everyone reaches the second decision, nobody is lost, outcomes are observed only after that decision, and no competing events occur. **These are simplifying data assumptions, not instructions to exclude real patients with early events.** Section 9 addresses real survival data.

We use Z for the drug label: Z=1 means A and Z=0 means B. Subscripts 0 and 1 index decisions, not drug names. For example, Z₀=1 and Z₁=0 means A followed by B: AB.

## 2. Why is baseline weighting alone insufficient?
{: #section-2 }

At baseline, some patients are more likely to choose A; the first weight handles that selection. Three months later, health may have improved or worsened, and this new health state may affect continuation or switching.

For example, among initial A users, those who improve may tend to continue A while those still severely ill switch to B. Retaining only actual persistent A users may select a healthier group than all initial A users. Baseline weights cannot preemptively address this later selection.

Distinguish two questions:

| Question | What does subsequent switching mean? |
| --- | --- |
| Initiate A versus B at baseline, with usual care afterward | Switching is part of the later natural course; longer follow-up alone does not automatically require additional treatment weights |
| Sustain AA versus BB | Switching is incompatible with these two fixed strategies; adherers' crude outcomes do not directly represent everyone following each strategy |

What is needed is adjustment for selection at each relevant treatment decision, not mechanical multiplication every calendar month. Analysis intervals must match the protocol, records, and treatment process.

## 3. Temporarily hold health alike: Why does 100→50→10 require multiplication?
{: #section-3 }

Consider only AA in a minimal count example. All 100 people have the same relevant baseline health; 50 actually choose A. Further suppose those 50 also have the same relevant histories before the second decision. Ten continue A, and the others switch to B.

### First choice: Only 50 of 100 people receive A
{: #section-4 }

The A proportion is 50/100=0.5. Give each actual A patient weight 1/0.5=2. Now 50×2=100: the first selection is addressed.

### Second choice: Only 10 of those 50 continue A
{: #section-5 }

The continuation proportion is 10/50=0.2. At the second step, multiply these 10 records by another factor of 1/0.2=5.

Each of the 10 already contributes 2 units; each unit is now expanded fivefold. Each person's final contribution is 2×5=10. Ten people×10=100, again representing the original target size.

| How are these ten AA records handled? | Total contribution | What is missing? |
| --- | ---: | --- |
| First weight 2 only | 10×2=20 | Does not address selection when only one fifth remain compatible at the second decision |
| Second factor 5 only | 10×5=50 | Does not address baseline selection when only half chose A |
| Add 2 and 5 | 10×7=70 | Not two successive representation adjustments |
| Multiply 2 and 5 | 10×10=100 | Includes both selections |

**Multiplication arises because the second adjustment expands an existing contribution—not because the two time points are independent.** The second probability is explicitly conditional on previous treatment and current history, allowing dependence between choices.

Exact count restoration comes from these deliberately simple proportions. Whether the records also represent outcomes depends on conditions such as exchangeability given history. This does not find nine individual counterfactual copies for each patient.

## 4. When health branches: A complete 200-person A/B example
{: #section-6 }

The previous example held second-decision histories alike to clarify multiplication. Now allow health to change.

All 200 people have the same relevant baseline features; 100 start A and 100 start B. Both baseline actions have probability 0.5 and first weight 2. At month 3, before the second drug decision:

| First drug | Improved/milder health | Still severely ill | Total |
| --- | ---: | ---: | ---: |
| A | 80 | 20 | 100 |
| B | 40 | 60 | 100 |

This allows the first treatment to change later health—for example, more patients have milder health after A. The second drug choice then occurs:

| Previous drug and current health | Branch count | A next interval | B next interval | Proportion continuing the same drug |
| --- | ---: | ---: | ---: | ---: |
| A first, milder | 80 | 64 | 16 | 64/80=0.8 |
| A first, severe | 20 | 5 | 15 | 5/20=0.25 |
| B first, milder | 40 | 10 | 30 | 30/40=0.75 |
| B first, severe | 60 | 30 | 30 | 30/60=0.5 |

Actual AA histories number 64+5=69; BB histories number 30+30=60. AB and BA patients also genuinely exist. Failure to continue their initial drug does not retrospectively make them ineligible at baseline.

### Why has restricting to adherers already changed health composition?
{: #section-7 }

Severe illness originally affected 20% of initial A users but only 5/69≈7.25% of AA adherers. Restricting to AA selects milder patients. Among initial B users, severe illness originally affected 60%, versus 30/60=50% of BB adherers.

Everyone's baseline weight is 2. Giving the 69 AA patients only this weight leaves their severe proportion at 7.25%; the second selection remains uncorrected.

### Calculate the second factor and cumulative weight within each branch
{: #section-8 }

| Strategy and health | Actual compatible count | Baseline weight | Probability of second actual action | Second factor | Cumulative weight | Final weighted count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AA, milder | 64 | 2 | 0.8 | 1/0.8=1.25 | 2×1.25=2.5 | 160 |
| AA, severe | 5 | 2 | 0.25 | 1/0.25=4 | 2×4=8 | 40 |
| BB, milder | 30 | 2 | 0.75 | 1/0.75=4/3 | 2×4/3=8/3 | 80 |
| BB, severe | 30 | 2 | 0.5 | 1/0.5=2 | 2×2=4 | 120 |

In the first row, 160=64×2.5; in the second, 40=5×8. AA's total contribution is 200 and BB's is also 200, each representing the same baseline 200-person target population under its respective strategy.

**“Five severe AA patients×weight 8=40,” not 200.** These five represent only AA's severe branch. Add the milder branch's 160 to represent the whole target population.

## 5. Weights alone do not give outcomes: Weight people and events together
{: #section-9 }

Suppose the following hospitalizations occur after the second decision and by month 6:

| Strategy and health | Actual count | Actual hospitalizations | Cumulative weight | Weighted count | Weighted hospitalizations |
| --- | ---: | ---: | ---: | ---: | ---: |
| AA, milder | 64 | 8 | 2.5 | 160 | 20 |
| AA, severe | 5 | 2 | 8 | 40 | 16 |
| BB, milder | 30 | 6 | 8/3 | 80 | 16 |
| BB, severe | 30 | 15 | 4 | 120 | 60 |

Therefore:

- AA risk=(20+16)/(160+40)=36/200=18%.
- BB risk=(16+60)/(80+120)=76/200=38%.
- Risk difference=18%−38%=−20 percentage points.

A crude comparison restricted to actual persistent users gives AA=(8+2)/69≈14.49% and BB=(6+15)/60=35%. These differences result from weighting. Their direction does not establish methodological success; these are constructed teaching numbers, not real drug effects.

Outcomes are complete and occur after the second decision, so this example can directly compare weighted risks among compatible histories. AB/BA outcomes do not enter AA/BB's direct risk numerators here, but their treatment records help estimate actual choice probabilities. Other approaches may fit marginal structural models including all treatment histories; those require explicit model forms, not unexplained mixing of history groups.

A causal interpretation for the whole target population additionally requires §10's conditions. Unlike simply discarding switchers and comparing crude outcomes, this calculation explicitly constructs weights for both treatment decisions.

## 6. A common misunderstanding: Why can subsequent health differ under AA and BB?
{: #section-10 }

After weighting, severe patients represent 40/200=20% under AA and 120/200=60% under BB. This does not automatically mean weighting failed.

**The first drug may actually change month-3 health.** In the same target population, sustained A and sustained B may produce different health distributions. The task is to address confounding because health affects the second treatment choice, while retaining the pathway through which first-interval treatment affects outcomes via health.

<pre class="mermaid">
flowchart LR
    Z0[First drug] --> L1["Health before<br/>second decision"]
    L1 --> Z1[Second drug]
    L1 --> Y["Final hospitalization<br/>outcome"]
    Z0 --> Y
    Z1 --> Y
</pre>

The diagram illustrates relevant paths only; actual analysis also needs baseline confounding and other considerations. L₁ can be a confounder for the second treatment and a mediator of the first treatment's effect. This is treatment–confounder feedback.

**Do not additionally invert the probability of the health state merely to make AA and BB have identical month-3 health.** These weights address treatment selection; they do not force all health paths into the same proportions.

For example, consider “A first→severe→continue A”:

- Probability of initially choosing A=0.5.
- Proportion with severe health after initial A=0.2.
- Probability of again choosing A among initially A-treated, severe patients=0.25.

The complete treatment–health–treatment path proportion is 0.5×0.2×0.25=0.025, and 2.5% of 200 is five people. But the treatment weight is 1/(0.5×0.25)=8, **without division by 0.2**, preserving the severe branch's composition under that strategy.

This also explains why a product of treatment probabilities is generally not the joint probability of the entire health history and need not equal the full cohort's proportion with AA histories.

## 7. Where do the probabilities come from in research? Fit two multivariable logistic regressions
{: #section-11 }

Real data cannot usually be reduced to mild/severe strata. We generate a separate 6,000-person dataset with the same teaching timeline: two decisions, followed by outcomes only after the second. Two logistic regressions learn the probability of choosing A. This dataset is separate from both the 200-person hand calculation and the baseline note's 3,000-person example.

### 7.1 Define every input first, avoiding future information in the baseline model
{: #section-12 }

| Symbol | Meaning |
| --- | --- |
| age10 | (age−70)/10; increases by 1 for each additional ten years |
| D | Baseline diabetes: 1=yes, 0=no |
| S₀ | Continuous severity score before the first treatment decision; higher means more severe |
| H | Prebaseline background treatment C history: 1=yes, 0=no; not previous A/B use |
| Z₀ | Actual baseline drug: 1=A, 0=B |
| S₁ | New severity score at month 3, before the second drug decision |
| Z₁ | Actual second drug: 1=A, 0=B |
| Y | Hospitalization after the second decision: 1=yes, 0=no |

In the simulation, Z₀ affects S₁, which then affects Z₁ and Y. Neither S₁ nor future Y belongs in the baseline treatment-probability model.

### 7.2 First logistic regression: Predict Z₀
{: #section-13 }

Inputs are age10, D, S₀, and H; the label is Z₀. Fit one shared coefficient set using all 6,000 people, obtaining:

$$
\widehat\eta_0=-0.488285+0.340301age10+0.519202D+0.534670S_0-0.253146H.
$$

η₀ is the linear predictor for the first drug choice—the predicted log-odds. A hat denotes an actually fitted value. Multiply features by coefficients and add; the first term is the intercept. The logistic transformation ê₀=1/[1+exp(−η̂₀)] gives the probability of choosing A, where exp denotes the exponential function. B's probability is 1−ê₀.

### 7.3 Second logistic regression: Predict Z₁
{: #section-14 }

Inputs include baseline features, Z₀, and new health S₁; the label is Z₁. The model knows “which drug has already been used and how the patient is doing now,” rather than baseline health alone. The actual fitted model is:

$$
\widehat\eta_1=-0.299058+0.238421age10+0.392496D+0.200912S_0-0.086679H+0.662451Z_0+0.674771S_1.
$$

Again set ê₁=1/[1+exp(−η̂₁)]. **ê₁ always predicts choosing A at the second decision**, not everyone's probability of continuing their initial drug. Continuation probability is ê₁ for initial A users and 1−ê₁ for initial B users.

Both models are fitted jointly across the cohort and then predict for those people. This classical parametric analysis does not require a separate test set, and each patient does not fit an individual model. The second model uses records eligible at the second decision; here everyone happens to reach it. With many real-world decision points, a pooled logistic model including time and history may also be used. Pooling does not justify ignoring temporal or historical relationships.

### 7.4 Four actual histories: Use each action's corresponding probability
{: #section-15 }

| Patient ID | History | ê₀: first A probability | ê₁: second A probability | First weight | Second factor | Cumulative weight |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 9 | AA | 0.476900 | 0.568636 | 1/ê₀=2.096875 | 1/ê₁=1.758594 | 3.687551 |
| 1 | BB | 0.403522 | 0.246796 | 1/(1−ê₀)=1.676509 | 1/(1−ê₁)=1.327661 | 2.225836 |
| 2 | AB | 0.394100 | 0.554970 | 1/ê₀=2.537424 | 1/(1−ê₁)=2.247038 | 5.701689 |
| 3 | BA | 0.544881 | 0.692548 | 1/(1−ê₀)=2.197228 | 1/ê₁=1.443944 | 3.172673 |

Each row multiplies the inverse probabilities corresponding to that person's actual action at each decision. AB and BA also have defined treatment-history weights, but this does not make them compatible AA or BB histories.

Patient 9 has age10≈0.062907, D=0, S₀≈0.700270, H=0, Z₀=1, and S₁≈−0.359818. The first logistic regression gives η̂₀≈−0.092465 and ê₀≈0.476900; the second gives η̂₁≈0.276289 and ê₁≈0.568636. The final weight is therefore 1/(0.476900×0.568636)≈3.687551.

The code generates random data and then estimates coefficients from observed treatment labels. These are not generating parameters presented as fitted coefficients. See the [calculation script]({{ "/assets/causal-inference/longitudinal-iptw-example/two_decision_lr.py" | relative_url }}) and [full-precision results]({{ "/assets/causal-inference/longitudinal-iptw-example/results.json" | relative_url }}). The script requires only NumPy and calls the existing baseline example's logistic-fitting function.

There are 1,443 actual AA and 2,019 BB histories. Weighted risks for their compatible histories with complete outcomes are approximately 8.01% and 18.04%, a difference of −10.03 percentage points. These illustrate calculation only, with no clinical-effectiveness or statistical-significance conclusion. The script does not complete the comprehensive diagnostics or confidence intervals required for a formal study.

## 8. After the examples, write the multitime formula
{: #section-16 }

### First define the current factor and the cumulative weight so far
{: #section-17 }

- i: patient index.
- k: treatment-decision index, starting at 0.
- êᵢₖ: predicted probability that patient i chooses A at this decision, given history available beforehand.
- qᵢₖ: conditional probability of patient i's actual action now. For actual A, q=ê; for actual B, q=1−ê.
- uᵢₖ=1/qᵢₖ: the current unitless weight factor.
- Wᵢ(k): cumulative, unitless treatment weight through decision k. Capital W reminds us that multiple factors have accumulated.

Write the sequence recursively:

$$
W_i(0)=u_{i0},\qquad W_i(1)=u_{i0}u_{i1},\qquad W_i(2)=u_{i0}u_{i1}u_{i2}.
$$

Read: “one factor at baseline; multiply the existing contribution by another at the second decision; multiply by another at the third.” More compactly:

$$
W_i(K)=\prod_{k=0}^{K}u_{ik}=\prod_{k=0}^{K}\frac1{q_{ik}}.
$$

Π is the product symbol, and K indexes the last decision. If K=1, there are two decisions, 0 and 1—not one. qᵢₖ is estimated along that person's contemporaneous history, not one proportion shared by everyone throughout the study.

### What exactly is included in “given history”?
{: #section-18 }

Use historyᵢₖ for the relevant available history before person i's kth decision, avoiding confusion with the single background-treatment variable H in §7. At baseline it includes age, D, S₀, and background treatment. At the second decision, add Z₀ and S₁. At the third, add further prior actions and new measurements.

qᵢₖ is the estimated P(current drug choice matches the patient's actual Zᵢₖ | historyᵢₖ). The bar means “given.” This definition accommodates dependence between treatments, health changes, and feedback from previous treatment. The history bars and treatment-weight superscript used in the original main note's longer notation encode these ideas; superscript A labels treatment weights, not drug A or exponentiation.

## 9. When is a weight used? Do not apply later factors to earlier records
{: #section-19 }

For using time-varying weights at each event time, see §9 of [Weighted Survival Analysis in TTE]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}). Its §3–§5 first explain risk sets and survival curves with fixed weights.

Suppose a patient's baseline weight is 2 and the cumulative weight after the second decision is 10:

| Interval | Decisions already made | Cumulative weight for the relevant records |
| --- | --- | ---: |
| Baseline until the second decision | Decision 0 only | 2 |
| After the second decision | Decisions 0 and 1 | 10 |

Do not assign weight 10 from baseline, which would use choices and health information that only occur later.

If a real patient experiences the study outcome at month 2, retain the event and use the relevant pre-event weights. Do not delete the event, label the patient nonadherent, or require survival to the second decision for inclusion merely because no new prescription occurs at month 3.

For mortality, do not create treatment records after death. For loss to follow-up, consider censoring adjustment according to its mechanism. The simplified end-of-study proportion formula here applies only to the complete-outcome setting stated above. General survival outcomes require updated risk sets and appropriate weighted survival estimation, not each person's final weight copied backward across all follow-up.

## 10. What should you check, and what conditions are required?
{: #section-20 }

**First, check baseline comparability.** Use baseline IPTW's SMD, distribution, and overlap diagnostics to assess appropriate baseline data support for the two Z₀ groups.

**Second, examine conditional overlap and adjustment at each decision.** Among comparable previous treatment and relevant health histories, are both current choices represented, and is the model appropriate? Final AA/BB counts are insufficient. In the 200-person table, only five of 20 severe patients after A continue A, already indicating reliance on relatively few records in that branch.

**Third, align the diagnostic with its time point.** When later health is affected by previous treatment, the final AA and BB groups need not have equal S₁ means. Check balance in current Z₁ choices within the relevant prior-treatment-history strata, or use conditional diagnostics appropriate to the longitudinal model. Do not impose a study-wide rule that every time-varying variable must have identical SMDs across final strategy groups. For baseline principles, see [Checking weighted balance on the four baseline variables]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-22), then relate them to §6 here.

**Fourth, track cumulative weights and information concentration over time.** Products of inverses for several uncommon choices may become large. Examine each period's weight distribution, tail patients, ESS, and sensitivity. Multiplication cannot create data on zero-probability paths, and truncation cannot supply nonexistent controls.

A causal interpretation requires at least sufficient treatment–outcome confounding information before each action (sequential exchangeability); a chance of the required action under relevant histories possible under the target strategies (sequential positivity); reliable strategies and measurements with consistency; and appropriate probability and outcome/censoring analysis models. Restoring the count table to 200 does not prove these conditions.

## 11. Second-reading supplement: Stabilization and CCW
{: #section-21 }

### Stabilized weights still multiply over time, with a numerator in each factor
{: #section-22 }

SWᵢ(K) denotes patient i's stabilized cumulative weight through decision K; SW is an abbreviation. A common form uses the probability of the actual action given only prior treatment history as each numerator, and its probability given prior treatment plus relevant health history as the denominator, then multiplies across decisions.

In the 200-person table, both baseline A/B numerators are 0.5. At the second decision, 69 of the 100 initial A users continue A, giving AA's second numerator 0.69. Sixty of the 100 initial B users continue B, giving BB's numerator 0.60.

- AA, severe: SW=(0.5/0.5)×(0.69/0.25)=2.76, versus ordinary cumulative weight 8.
- AA, milder: SW=(0.5/0.5)×(0.69/0.8)=0.8625, versus ordinary weight 2.5.
- Both AA categories multiply ordinary weights by 0.5×0.69=0.345, so the normalized risk for this fixed strategy remains 18%. BB likewise multiplies by 0.5×0.60=0.30, retaining risk 38%.

Cancellation is possible because the numerator product is constant within each fixed history here. Longitudinal numerators do not simply repeat the overall baseline A proportion at every period. If they retain certain baseline variables, subsequent marginal models and standardization must match. The label “stabilized” does not establish improved precision in this example.

### Artificial censoring does not mean adjusting the same process twice
{: #section-23 }

AA/BB effects can also be estimated by artificially censoring follow-up at deviation from fixed strategies and weighting for remaining compatible. Distinguish stages: baseline treatment selection and later compatibility selection may address different points in time. For the same continuation/switching decision, do not apply the second treatment factor here and then multiply by that same probability's inverse again as IPCW.

When baseline A/B initiation is already clear, cloning is not automatically needed. Consider an appropriate CCW design when features such as grace periods make baseline records compatible with several strategies; see [Clone–Censor–Weight]({{ "/causal-inference/clone-censor-weight/" | relative_url }}). This note explains why successive selection requires successive adjustment, not that every sustained-strategy analysis must organize data identically.

## 12. Self-check and references
{: #section-24 }

1. Why not add 2 and 5? — The second adjustment acts on records already carrying weight 2, multiplying their contribution by 5.
2. Must the two treatments be independent to multiply? — No; the second probability explicitly conditions on history.
3. For a BB patient whose second model predicts A probability 0.25, what is that step's factor? — 1/(1−0.25)=4/3.
4. Why not also invert the probability of severe health? — The target here requires adjusting treatment choice while retaining the health distribution generated under previous treatment.
5. Does different later health under AA/BB prove adjustment failed? — No; it may reflect early treatment effects. Diagnostics must address the current choice and relevant history.
6. Do switchers become ineligible from baseline? — No. Future behavior does not revoke baseline eligibility; later records' contributions depend on the target strategy and analysis plan.
7. Can prehospitalization records use a treatment factor calculated only afterward? — No; real survival analysis updates weights in chronological order.

Methodological references—the numerical tables and simulation code are independent teaching constructions:

- [Cole and Hernán (2008): Constructing Inverse Probability Weights for Marginal Structural Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC2732954/): longitudinal treatment probabilities, stabilized weights, and model checks.
- [Naimi, Cole, and Kennedy: An introduction to g methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6074945/): treatment–confounder feedback and g-methods.

Return to [IPTW and IPCW: Do not confuse the probabilities]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-29), then enter [Three Target Trial Emulation Designs]({{ "/causal-inference/target-trial-designs/" | relative_url }}). Understand the estimand and why weighting is needed before choosing a suitable way to organize data.
