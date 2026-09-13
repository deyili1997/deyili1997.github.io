---
layout: "causal-note"
title: "Weighted Survival Analysis in Target Trial Emulation"
description: "Learn survival records, risk sets, weighted Kaplan–Meier and Cox, then connect longitudinal weights, federated estimation, and competing events."
group: "Estimation"
reading_label: "Companion to step 14"
order: 14.2
math: true
causal_notes: true
date: "2026-09-13"
last_modified_at: "2026-09-13"
tags: ["causal-inference", "target-trial-emulation", "survival-analysis", "inverse-probability-weighting"]
toc: [{"title": "0. Start from zero: Understand follow-up records before survival curves", "anchor": "section-1"}, {"title": "0.11 A beginner's path: Ordinary Cox → weighted Cox in TTE → federated Cox in the paper", "anchor": "section-12"}, {"title": "1. Where does survival analysis fit within TTE?", "anchor": "section-27"}, {"title": "2. Why not simply divide deaths by the baseline population?", "anchor": "section-28"}, {"title": "3. Risk sets: Who still contributes when a death occurs?", "anchor": "section-29"}, {"title": "4. An eight-person table: Fix the weights first to understand the time calculations", "anchor": "section-30"}, {"title": "5. Weighted Kaplan–Meier: Calculate each step, then multiply survival across steps", "anchor": "section-31"}, {"title": "6. What about loss to follow-up? Survival analysis handles timing without guaranteeing removal of censoring bias", "anchor": "section-38"}, {"title": "7. Weighted Cox: How do weights enter risk-set comparisons?", "anchor": "section-39"}, {"title": "8. How does multivariable LR connect to actual time-to-event data?", "anchor": "section-42"}, {"title": "9. How are baseline and longitudinal weights used in survival analysis?", "anchor": "section-43"}, {"title": "10. Stabilization, confidence intervals, and reporting", "anchor": "section-46"}, {"title": "10.1 Competing events: How do standard methods change when patients die before dementia?", "anchor": "section-47"}, {"title": "11. Return to the two TTE extension papers", "anchor": "section-58"}, {"title": "12. Self-check and sources", "anchor": "section-59"}]
previous_note: "/causal-inference/longitudinal-iptw/"
next_note: "/causal-inference/target-trial-designs/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}). Prerequisites: time zero in [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}), events and risk sets in [The Cox Proportional Hazards Model]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}), and baseline logistic regression (LR) and weights in [Inverse Probability Weighting]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}). For longitudinal weights, see [Longitudinal IPTW: Why Weights Multiply Across Treatment Decisions]({{ "/causal-inference/longitudinal-iptw/" | relative_url }}).

**Read according to your current learning goal:** Start with events and risk sets in §0, then follow [the beginner's path from ordinary Cox to weighted Cox in TTE and federated Cox]({{ "/causal-inference/weighted-survival-analysis/" | relative_url }}#section-12) through its three stages. You do not need to finish every prerequisite note first.

## 0. Start from zero: Understand follow-up records before survival curves
{: #section-1 }

This section requires no knowledge of Cox, HRs, propensity scores, or weights. First ask: **What exactly did we record, and which outcomes do we actually know or not know?** You can stop after understanding this section and approach weighting gradually afterward.

### 0.1 Survival analysis studies time from a starting point to an event
{: #section-2 }

When comparing drugs A and B, for example, we may want to know not only whether someone dies within a year but also in which month death occurs. Survival analysis uses information about “when the event happens” and “how long observation continues.”

An event is something the study defines in advance and plans to record: death, first hospitalization, first disease diagnosis, and so on. “Survival” names the method; if the event is first hospitalization, the curve describes the probability of not yet having a first hospitalization, not literally of remaining alive. To avoid adding competing-event issues immediately, we initially use all-cause death as the event.

Every study must first clarify three things:

1. **Where does the clock start?** For example, the day each patient initiates A or B.
2. **Which event are we waiting for?** For example, all-cause death.
3. **How long can observation continue?** For example, six months from each person's starting point.

Patients may enter on different calendar dates; “month 2” means two months after each patient's own baseline. TTE also requires aligning eligibility, strategy classification, and the start of follow-up, but we do not need a statistical model yet.

### 0.2 First examine one group of five patients, without comparing drugs
{: #section-3 }

Five people are followed from their own study starting points for up to six months, producing these records. All numbers are invented for teaching.

| Patient | What do we know? | Observation time (months) | Was death observed at that time? |
| --- | --- | ---: | ---: |
| Person 1 | Died at month 2 | 2 | 1 |
| Person 2 | Last confirmed alive at month 3, then lost to follow-up | 3 | 0 |
| Person 3 | Died at month 4 | 4 | 1 |
| Person 4 | Alive when the study ended at month 6 | 6 | 0 |
| Person 5 | Alive when the study ended at month 6 | 6 | 0 |

We need at least two columns: **how long the person was observed, and whether observation ended with death or without an observed death**. Event indicator 1 means an observed death; 0 means no death was observed and the record ends here. Zero does not mean the person will never die.

Although Persons 2 and 4 both have indicator 0, the information differs: Person 2 is known to survive only to month 3, whereas Person 4 is known to survive to month 6. We cannot classify both as “six-month survivors.”

### 0.3 Censoring: The record stops here; what happens later is unknown
{: #section-4 }

Right censoring in this example means that a patient is known not to have died up to a certain time, but their later death time is unobserved.

- Person 2 is lost at month 3: we know survival to month 3, but not whether death occurs at month 4 or 5.
- Persons 4 and 5 reach administrative end at month 6: we know they survive to the study's required six-month horizon. They may die later, but this follow-up does not continue.

**Censoring does not mean deleting the whole person, declaring them dead, or declaring them alive throughout the remaining period.** The known earlier portion of their record remains useful.

Stopping medication does not necessarily mean loss to follow-up. If survival status remains observable, outcome information remains available. Whether to censor artificially for a protocol deviation is a separate design choice in sustained-strategy analyses, outside this introductory section.

### 0.4 Why do two deaths not establish a six-month mortality risk of 2/5?
{: #section-5 }

Two deaths were observed: Persons 1 and 3. The fraction 2/5 = 40% is the “proportion with a death actually recorded in this dataset,” but Person 2's status after month 3 is unknown. Calling 40% the complete six-month risk effectively treats Person 2 as a confirmed six-month survivor.

If all five six-month outcomes were complete, we could directly calculate the death proportion. With incomplete follow-up such as Person 2's, the person should contribute only during the known period. Survival analysis permits this use of partial follow-up, but it still requires appropriate censoring assumptions; computation cannot recover the actual unknown outcomes of lost patients.

### 0.5 Risk sets: Who is still observed and alive just before a death?
{: #section-6 }

At each death time, identify patients who are still alive and under observation immediately before that moment. These people form the risk set. Here “at risk” means that the target event could still be observed, not that everyone is severely ill.

- Before Person 1 dies at month 2, all five people are in the risk set, including Person 1.
- After Person 2 is lost at month 3, that person no longer enters later risk sets, but contributed earlier.
- Before Person 3 dies at month 4, Person 1 has died and Person 2 has been lost. Only Persons 3, 4, and 5 remain: three people.

First identify the set just before the event, then count this event. Do not remove the person dying from the denominator before calculating their event contribution.

### 0.6 Survival probability and mortality risk: Learn these two quantities first
{: #section-7 }

Six-month survival probability asks, “Starting from baseline, what is the probability of surviving beyond six months?” Six-month all-cause mortality risk asks, “What is the probability of dying within six months?” For the same starting point, horizon, and all-cause death outcome, these sum to 1.

Write $$S(t)$$ for the probability of surviving beyond time $$t$$; $$S$$ stands for survival. The symbol $$t$$ is elapsed time from baseline, such as $$t=6$$ months, not a patient identifier. Risk is $$1-S(t)$$. No understanding of hazard or HR is needed yet.

### 0.7 Kaplan–Meier: Join the surviving fractions across event times
{: #section-8 }

Kaplan–Meier (KM) estimates a survival curve step by step from risk sets. Begin at 100% survival at baseline. At each death, calculate the fraction of the risk set that does not die in that event, then multiply the preceding survival estimate by that fraction.

**Month 2:** Five people are at risk and one dies. The surviving fraction for this step is $$(5-1)/5=4/5$$. Starting from 100%, estimated survival becomes $$100\%\times4/5=80\%$$.

**Month 3:** Person 2 is lost, with no new death, so the curve does not fall because of this loss. What changes is that the next risk set no longer includes Person 2.

**Month 4:** Three people are at risk and one dies. This step's surviving fraction is $$(3-1)/3=2/3$$. We previously estimated that 80% survive the first step; multiply by the current $$2/3$$:

$$
\widehat S(4)=\frac45\times\frac23=\frac8{15}\approx53.33\%.
$$

The hat marks an estimate from these data. Multiplying the fractions joins “surviving the earlier stage” with “surviving this step among those who reached it”; it does not assume the stages are independent. The month-4 fraction $$1/3$$ is the conditional event fraction at that event time, not cumulative mortality risk in the entire baseline population, and not directly the continuous-time hazard.

**Month 6:** Persons 4 and 5 are alive at administrative end, with no new deaths. Estimated six-month survival remains 53.33%, so estimated six-month mortality risk is $$1-53.33\%=46.67\%$$.

| Time | What happens? | Risk set before the event or censoring | New deaths | KM survival estimate |
| --- | --- | ---: | ---: | ---: |
| Baseline | Observation begins | 5 | 0 | 100% |
| Month 2 | Person 1 dies | 5 | 1 | 80% |
| Month 3 | Person 2 is lost | 4 | 0 | 80%; no drop |
| Month 4 | Person 3 dies | 3 | 1 | 53.33% |
| Month 6 | Persons 4 and 5 are alive at study end | 2 | 0 | 53.33%; no drop |

The 46.67% does not claim that exactly 2.3335 of five people died. It is a probability estimated using incomplete follow-up. Such a small sample is extremely imprecise; this section illustrates the algorithm only.

### 0.8 How should you read the curve?
{: #section-9 }

The horizontal axis is elapsed time from baseline; the vertical axis is estimated probability of remaining alive. A KM curve begins at 100%, drops at death times, and stays horizontal between deaths. Short ticks or other symbols often mark censoring, which does not itself create a downward step.

Here survival is 100% from baseline until just before month 2; 80% from month 2 until just before month 4; and about 53.33% from month 4 to month 6. A horizontal segment does not mean there is absolutely no risk of dying afterward. Nor does a long curve imply that many people support its tail. These data cannot directly answer risk beyond month 6.

### 0.9 KM still requires an important condition
{: #section-10 }

After Person 2 is lost, we use events among people still observed to estimate subsequent survival. If Person 2 leaves precisely because of severe deterioration while the remaining people are healthier, this borrowing may be unreliable.

Correct use of risk sets therefore does not automatically remove loss-to-follow-up bias. To explain the calculation, we temporarily assume this group's censoring mechanism permits the KM estimate above. Real studies must examine noninformative censoring or make appropriate adjustments. Section 6 provides more detail.

### 0.10 Return to drugs A and B: Comparison and weighting come next
{: #section-11 }

So far we have calculated one group only. To compare drugs, calculate a curve for A and a curve for B. At the same six-month or one-year horizon, read each risk and compare their difference.

For example, one-year survival probabilities of 90% and 85% correspond to mortality risks of 10% and 15%, hence an A-minus-B risk difference of −5 percentage points. These are teaching numbers for reading curves, not evidence that A causally protects patients: baseline health may differ between the groups.

The next learning sequence is therefore: **how ordinary survival curves are calculated → why the groups may be incomparable → how IPTW changes risk-set and event contributions → whether Cox is needed to summarize an HR.** Survival analysis is not synonymous with Cox. Learn to read curves and risks before other models.

A complete beginner can stop here. Once you can distinguish “death,” “loss to follow-up,” and “alive at study end,” continue to weighting below; there is no need to master every formula in one sitting.

<aside class="study-callout study-callout--abstract" markdown="1">

**First remember where the weight goes**

Survival analysis updates the people being compared according to event times. IPTW brings each patient into the current risk set with their own weight; when an event occurs, it also contributes according to that patient's weight.

**Weight the record's contribution; do not multiply survival time by the weight or multiply the final HR by a number.**

</aside>

<aside class="study-callout study-callout--tip" markdown="1">

**Two passes for beginners**

If starting from zero, read §0 first. On the first subsequent pass, read §1–§6: research question, time and censoring, risk sets, and hand-calculated weighted survival curves. On the second pass, read §7–§10: Cox, actual multivariable calculations, longitudinal weights, and uncertainty. The long formula in §7 can remain collapsed.

The eight-person table is a hand-calculation exercise. The 3,000-person example reuses baseline features and drug assignments but **generates new death times and loss-to-follow-up times**. These differ from the earlier completely observed one-year binary hospitalization outcome, so their numbers must not be mixed. All are simulated data, not evidence of clinical drug effects.

</aside>

## 0.11 A beginner's path: Ordinary Cox → weighted Cox in TTE → federated Cox in the paper
{: #section-12 }

**This is a continuous explanation; you need not finish all the other notes first.** If events, censoring, or risk sets remain unclear, read §0 above. Then follow the three stages below, adding one layer at a time: compare events, adjust for treatment selection, and finally distribute the computation across hospitals.

| Stage | First question to answer | What is added? |
| --- | --- | --- |
| Ordinary Cox | How does the model compare patients when an event occurs? | Follow-up records, risk sets, hazard, partial likelihood |
| Weighted Cox in TTE | How can we adjust the comparison when A/B groups differ at baseline? | Explicit causal question, LR propensity scores, patient IPTW |
| Federated Cox | How can hospitals estimate together while holding separate patient data? | Hospital identifiers, local objectives, parameter exchange and aggregation |

### Stage 1: Ordinary Cox, before weights or hospitals
{: #section-13 }

#### 1. Fix the research setting and one patient table
{: #section-14 }

Teaching question: Follow patients from first initiation of drug A or B and compare time to all-cause death. Using all-cause death lets us first learn the core calculation; dementia and its competing events are deferred to §10.1.

| Patient | Actual drug | Follow-up result |
| --- | --- | --- |
| Person 1 | A | Dies at month 2 |
| Person 2 | A | Alive when study ends at month 6 |
| Person 3 | B | Dies at month 4 |
| Person 4 | B | Last confirmed alive at month 3, then lost |

Before the month-2 death, all four form the risk set. Before the month-4 death, only Persons 2 and 3 remain: Person 1 has died and Person 4 has been lost. Although Person 4 has no recorded death, that person contributes through the month-2 risk set. This four-person example explains an algorithm; it is not a sample sufficient for research conclusions.

#### 2. Explain hazard and HR next
{: #section-15 }

Hazard is the instantaneous event rate among those who have not yet experienced the event, not the proportion dead by that time. The simplest treatment model codes drug A as $$A=1$$ and drug B as $$A=0$$:

$$
h(t\mid A)=h_0(t)\exp(\beta_A A).
$$

Here $$h_0(t)$$ is the B group's baseline hazard and can change over time; $$\beta_A$$ is the treatment coefficient the model estimates. The A-to-B multiplier is $$\exp(\beta_A)$$, the HR. Let $$r=\exp(\beta_A)$$ to simplify the hand calculation.

Trying $$r=0.5$$ means the model assumes A's current hazard is half B's, not that one-year mortality probability is halved. “Proportional hazards” means the model treats this multiplier as constant over time.

#### 3. How does the model evaluate a candidate HR?
{: #section-16 }

At the same event time, the common $$h_0(t)$$ cancels from numerator and denominator, leaving relative multipliers: $$r$$ for A patients and 1 for B patients.

Person 1 dies at month 2: the event case's multiplier is $$r$$ and the risk-set total is $$2r+2$$, giving contribution $$r/(2r+2)$$. Person 3 dies at month 4: the event case's multiplier is 1 and the total is $$r+1$$, giving $$1/(r+1)$$.

Multiply the two event contributions:

$$
L(r)=\frac{r}{2r+2}\times\frac1{r+1}.
$$

Here $$L$$ is partial likelihood, a function for evaluating candidate parameters. It is not the population's survival probability or “the probability this HR is correct.”

| Candidate HR $$r$$ | Month-2 contribution | Month-4 contribution | Product |
| --- | --- | --- | --- |
| 0.5 | 1/6 | 2/3 | 1/9 ≈ 0.1111 |
| 1 | 1/4 | 1/2 | 1/8 = 0.125 |
| 2 | 1/3 | 1/3 | 1/9 ≈ 0.1111 |

Software seeks the coefficient maximizing partial likelihood; here the maximum occurs at $$r=1$$. Each drug group has a death at a different event time, so the model must account for both events rather than consider only the first death.

**What you should now be able to explain:** At each event, Cox compares people currently in the risk set. People who do not die or are lost later still contribute through the denominator. Ordinary Cox computation alone does not establish a causal interpretation.

For slower definitions and derivations, read [The Cox Proportional Hazards Model]({{ "/causal-inference/cox-proportional-hazards/" | relative_url }}), §1–4.

### Stage 2: Place the comparison in TTE and add IPTW to the same table
{: #section-17 }

#### 4. Why is the ordinary comparison insufficient?
{: #section-18 }

In practice, A may be prescribed more often to older patients, patients with diabetes, or those with greater severity. Even if Cox uses event times correctly, the raw treatment comparison may mix treatment differences with baseline differences.

TTE first defines eligibility, A/B strategies, common time zero, outcome, follow-up, and target effect. Here the question is “initiate A versus initiate B,” not sustained use. Confounding adjustment and outcome estimation follow those definitions. Cox can directly include baseline covariates; this path studies another approach—IPTW followed by a weighted Cox working model containing a treatment indicator. The HR targets and interpretations of these approaches cannot simply be equated.

#### 5. Generate weights with multivariable LR first; distinguish it from Cox
{: #section-19 }

Let $$L$$ denote pretreatment age, diabetes, severity, and background treatment C. LR uses actual A/B assignment as the label and estimates $$e(L)=P(A=1\mid L)$$, producing $$\widehat e(L)$$; denote its coefficients by $$\pi$$. The Cox coefficient $$\beta_A$$ is a different parameter, estimated later using event times.

The corresponding ordinary ATE treatment weights are $$1/\widehat e(L)$$ for A and $$1/[1-\widehat e(L)]$$ for B. See [the complete multivariable LR example comparing initiation of A and B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) for the full fitting calculation.

Add hypothetical LR outputs to the four people above. These scores illustrate the method; they were not fitted using these four people alone.

| Patient | Drug | Probability of A, $$\widehat e(L)$$ | Probability of actual drug | IPTW $$w$$ |
| --- | --- | --- | --- | --- |
| Person 1 | A | 0.5 | 0.5 | 2 |
| Person 2 | A | 0.5 | 0.5 | 2 |
| Person 3 | B | 0.8 | 0.2 | 5 |
| Person 4 | B | 0.5 | 0.5 | 2 |

Baseline weights require diagnostics such as covariate-by-covariate balance, overlap, and extreme values. Being able to calculate numbers does not establish successful adjustment, and this four-person table cannot assess those research requirements.

#### 6. Weights enter the same Cox calculation in two places
{: #section-20 }

At month 2, the risk set still contains four people; times and events have not changed. The weighted denominator is $$2r+2r+5+2=4r+7$$. Person 1's event contribution is multiplied by weight 2, expressed as exponent 2 in product form.

At month 4, the risk set still contains Persons 2 and 3. The weighted denominator is $$2r+5$$; Person 3's event contribution uses weight 5.

Thus:

$$
L_w(r)=\left(\frac{r}{4r+7}\right)^2\left(\frac1{2r+5}\right)^5.
$$

**Compare this with ordinary Cox above:** Everyone at risk contributes according to their weight in the denominator, and each event contributes according to the event case's weight. Nobody's death time changes and no patients are added.

Taking logs makes the exponents easier to see:

$$
\ell_w(r)=2[\log r-\log(4r+7)]-5\log(2r+5).
$$

Software maximizes this objective, giving $$r\approx0.8982$$ here. Its difference from the unweighted 1 arises from changing patient contributions, not multiplying the original HR by an “average weight.” Omitted event-case weights in the numerators correspond only to constants independent of $$r$$ and do not affect the optimum. The weighted fractions should no longer be interpreted simply as probabilities of individual identity.

**What you should now be able to explain:** Propensity scores predict treatment; Cox analyzes event times. IPTW enters both risk sets and event contributions. ATE weights do not turn an HR into an average risk difference; fixed-horizon risks require appropriate curves. Baseline IPTW also does not automatically handle informative loss to follow-up or nonproportional hazards.

See §7–10 for weighting details, and weighted KM for fixed-horizon risk. First understand these two locations for weights, then read the longer formula.

### Stage 3: Move computation across hospitals and enter the paper's federated Cox model
{: #section-21 }

#### 7. Add hospital identifiers before adding every symbol
{: #section-22 }

Now treat the same four-person table as hospital 1's data; hospital 2 has its own patients. Hospitals are not the A/B groups: treatment-comparison support should be examined within each hospital.

Hospital 1 calculates local $$\ell_1(\beta)$$ and hospital 2 calculates $$\ell_2(\beta)$$. Each uses its own follow-up records, events, and risk sets; they seek a common $$\beta$$.

The paper's notation corresponds to: $$k$$ = hospital index; $$i$$ = event-time index; $$j$$ = patient index within a risk set; $$D_i^{(k)}$$ = the set of event cases at that time in that hospital; and $$q$$ = an index within that set of event cases. The symbol $$\prod$$ means multiply and $$\sum$$ means add. Start with no tied death times, then introduce $$D$$ and $$q$$.

#### 8. Where do the paper's equations (5)–(9) fit in this sequence?
{: #section-23 }

| Paper equation | Meaning already learned | New element |
| --- | --- | --- |
| (5) | Hazard = baseline × relative multiplier | General covariate vector $$z$$ and coefficient vector $$\beta$$ |
| (6) | Unweighted risk-set contributions multiplied across events | Hospital $$k$$'s local risk sets |
| (7) | Weight both risk sets and event contributions | $$D$$ and $$q$$ indices for multiple events at the same time |
| (8) | Multiply hospitals' partial likelihoods | Aggregate across hospitals, while risk sets remain local |
| (9) | Combine local log objectives | Additional hospital fractions $$p_k$$ and regularization |

Now proceed to [the equation-by-equation explanation of federated Cox]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-77). It continues with the exact same four-person table, so no new example is required.

#### 9. How do parameters move between hospitals?
{: #section-24 }

The server sends this round's common $$\beta$$ → hospitals update from that starting point using local objectives → they return local parameters or updates → the server aggregates them → the next round begins. Federated PS training uses a separate parameter vector $$\pi$$; see [the detailed federated LR explanation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}#section-63).

For example, two hospitals have aggregation fractions $$1/4$$ and $$3/4$$ and updated local treatment coefficients −0.2 and −0.4. An illustrative FedAvg coefficient is $$(1/4)(-0.2)+(3/4)(-0.4)=-0.35$$. Exponentiating gives $$\exp(-0.35)\approx0.705$$, the HR corresponding to that parameter. This is not direct averaging of the hospitals' HRs, and one averaging round does not necessarily produce the global optimum.

Distinguish three quantities: patient $$w$$ is IPTW; hospital $$p_k=N_k/N$$ is an aggregation fraction, with $$N_k$$ the hospital's sample size and $$N$$ the total; regularization parameter $$\mu$$ controls the strength of the restriction on local parameter deviation.

#### 10. Once the calculation is clear, check three boundaries in the paper
{: #section-25 }

1. **Local risk sets are not global risk sets.** Equation (8) uses $$R_i^{(k)}$$, comparing an event case with patients at risk in the same hospital. This structure is closer to a hospital-stratified Cox objective with shared coefficients than to the common risk set in an unstratified pooled-data model.
2. **Equation (9) is not merely the logarithm of equation (8).** It additionally multiplies by $$p_k$$ and adds regularization. Whether local objectives are sums or averages must be explicit; do not assume equivalence to analyzing all patients centrally.
3. **The penalty's sign depends on optimization direction.** Maximizing log likelihood requires subtracting a nonnegative penalty; minimizing negative log likelihood requires adding it. Ambiguity in the printed expression and an error in code are separate questions.

Detailed checks and sources appear in the extension's §5.16–5.17. You need not memorize those algorithmic details on the first pass. Once the calculation is clear, retain these boundaries so that “federated” is not automatically read as “identical to centralized analysis.”

### After this path, check whether you can answer
{: #section-26 }

- Why does Person 4 no longer enter the Cox denominator at month 4?
- Why does Person 3's weight appear in both the risk set and that person's own event contribution?
- Which data relationships determine LR's $$\pi$$ and Cox's $$\beta$$?
- Why is hospital fraction $$p_k$$ different from patient IPTW?
- Does the paper actually combine all hospitals' risk sets when combining their contributions?

After following this section into the extension, read §10.1 here when returning to AD outcomes. First master the all-cause mortality sequence, then add death before dementia as an extra pathway.

## 1. Where does survival analysis fit within TTE?
{: #section-27 }

First specify the target trial: Among eligible patients with the same disease, how does initiating A versus B at baseline affect all-cause mortality risk over the next year? This baseline example intervenes only on initiation, with usual care afterward; it does not require a full year of continuous use. A and B are both reasonable active treatments.

<pre class="mermaid">
flowchart TD
    A[Target trial: population, strategies, time zero, outcome, follow-up, target effect] --> B[Construct the observational cohort: actual A or B initiators]
    B --> C[Fit LR using pretreatment features; calculate IPTW and assess baseline balance and overlap]
    B --> D[Organize each person's event or censoring time from the common study starting point]
    C --> E[Weighted survival analysis: event and risk-set contributions at each event time]
    D --> E
    E --> F[Survival curves, fixed-horizon risk differences or ratios, or appropriate HRs and intervals]
</pre>

TTE defines the question and timing; IPTW addresses confounding related to treatment selection; survival analysis uses event timing and incomplete follow-up. None substitutes for the others: a correctly fitted Cox model cannot repair an incorrect time zero, and IPTW does not automatically repair loss-to-follow-up bias.

Survival analysis can examine time to first AD diagnosis or hospitalization as well as death. We use all-cause mortality for the hand calculation to avoid competing-risk complexity initially. If the outcome becomes AD, death prevents future AD occurrence. Treating all deaths as ordinary censoring and interpreting $$1-\mathrm{KM}$$ as real-world cumulative AD risk is therefore inappropriate. Specify the competing-event target and method, such as an appropriate weighted cumulative incidence function.

## 2. Why not simply divide deaths by the baseline population?
{: #section-28 }

Person 1 is observed for a full year without dying; Person 2 is observed only to month 3 and then lost. Neither has a recorded death, but the meanings differ: Person 1's one-year outcome is known, whereas Person 2's status after month 3 is unknown.

Treating Person 2 as alive at one year invents information. Deleting the entire record wastes the three months already known. We therefore record “how long observation lasted and why it ended.”

| Column | Meaning | Example |
| --- | --- | --- |
| id | Patient identifier | A1 |
| Z | Baseline drug label: 1 = A, 0 = B | 1 |
| time | Duration from the person's own time zero to the event or observation end | 2 months |
| event or $$\delta$$ | 1 = death observed at `time`; 0 = right-censored at `time` | 1 |
| $$w$$ or $$SW$$ | Estimated treatment weight: the patient's contribution to analysis here | 2 |

Right censoring means only that the person had not experienced the event by observation end; subsequent status is unknown. It includes both loss to follow-up and scheduled study end. The value $$\delta=0$$ does not mean the patient will never die or has zero probability of death.

Let $$T$$ denote the underlying event time and $$C$$ the end of observable follow-up. Record $$\mathrm{time}=\min(T,C)$$; `event` indicates whether the event was observed before or at that endpoint. The symbols $$T$$ and $$C$$ are durations, not drug labels. Actual analyses must also specify the ordering of same-day events and censoring. This note's event times have no ties; each event case belongs to the risk set immediately before their event.

## 3. Risk sets: Who still contributes when a death occurs?
{: #section-29 }

The risk set at $$t$$ contains **people who are alive and still under observation immediately before $$t$$**. The person dying is included just before that death; do not remove them from the denominator first.

- Someone who died earlier no longer enters subsequent risk sets.
- Someone lost earlier has unknown subsequent status and no longer enters subsequent risk sets.
- Someone still observed and alive enters the risk set, even if they will be lost later.

Each group's Kaplan–Meier curve uses its own risk sets. Cox comparisons of A versus B usually use risk sets containing both groups. Both update over time, but they serve different calculations.

## 4. An eight-person table: Fix the weights first to understand the time calculations
{: #section-30 }

The propensity scores $$\widehat e$$ below are supplied for hand calculation, not fitted by LR in these eight people. We do not claim that they establish causal balance. Section 8 provides an actual multivariable fit. Analysis ends at month 6.

| Patient | Actual drug | $$\widehat e$$: probability of A | Ordinary IPTW $$w$$ | Observation time (months) | event | Reason |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| A1 | A | 0.5 | 2 | 2 | 1 | Dies at month 2 |
| A2 | A | 0.5 | 2 | 3 | 0 | Lost at month 3 |
| A3 | A | 0.25 | 4 | 5 | 1 | Dies at month 5 |
| A4 | A | 0.5 | 2 | 6 | 0 | Alive at month-6 study end |
| B1 | B | 0.5 | 2 | 1 | 1 | Dies at month 1 |
| B2 | B | 0.75 | 4 | 4 | 1 | Dies at month 4 |
| B3 | B | 0.5 | 2 | 4.5 | 0 | Lost at month 4.5 |
| B4 | B | 0.5 | 2 | 6 | 0 | Alive at month-6 study end |

For A, $$w=1/\widehat e$$; for B, $$w=1/(1-\widehat e)$$. Both baseline weight totals are 10, while each actual group contains four people. Ten is the total contribution of records, not ten actual patients. These weights stay fixed over time, but deaths and censoring change the risk sets.

## 5. Weighted Kaplan–Meier: Calculate each step, then multiply survival across steps
{: #section-31 }

### 5.1 What happens without weighting?
{: #section-32 }

Ordinary Kaplan–Meier (KM) calculates, at each death time, deaths at that time divided by the number currently at risk. Subtracting this fraction from 1 gives the conditional surviving fraction for the step. Multiplying the steps up to the current time estimates survival from baseline.

This event-time fraction is not the continuous-time hazard itself; it is the conditional event fraction used by KM at that time.

### 5.2 Which two components change with weighting?
{: #section-33 }

Replace “number of deaths now” with **the sum of weights of people dying now**, and “number in the current risk set” with **the sum of weights of current risk-set members**. Both must use a consistent weighting scheme appropriate to that time.

For one group, define $$d_w(t)$$ as the sum of weights of deaths at $$t$$ and $$n_w(t)$$ as the sum of risk-set weights immediately before $$t$$. The letter $$d$$ denotes event contribution, $$n$$ the contribution at risk, and subscript $$w$$ weighting, not a drug name.

The surviving fraction for this step is $$1-d_w(t)/n_w(t)$$. Multiply it by the previous survival estimate. Do not simply add the event-time fractions $$d_w/n_w$$ and call the result cumulative mortality risk.

### 5.3 Calculate group A by hand
{: #section-34 }

**A1 dies at month 2.** A1, A2, A3, and A4 are all still observed, totaling weight $$2+2+4+2=10$$. The death weight is 2.

This step's surviving fraction is $$1-2/10=0.8$$, so survival changes from 1 to 0.8.

**A2 is lost at month 3.** There is no death, so the curve does not drop now. A2 no longer enters later risk sets, and weight 2 no longer contributes to later denominators. A2 is neither declared dead nor treated as if continued survival were known.

**A3 dies at month 5.** Only A3 and A4 remain at risk, totaling weight $$4+2=6$$. The death weight is 4.

This step's surviving fraction is $$1-4/6=1/3$$. Estimated survival from baseline to month 5 is:

$$
\widehat S_A(5)=0.8\times\frac13\approx0.2667.
$$

Here $$S$$ means survival probability, subscript $$A$$ identifies the drug, the argument 5 means follow-up month 5, and the hat marks an estimate. This is not A3's own survival probability; it is the population curve estimated from this group's weighted data.

A4 is alive at month-6 administrative end. With no new death, the curve remains about 26.67%. Six-month all-cause mortality risk is $$1-26.67\%=73.33\%$$.

| A-group event time | Current death weight | Risk-set weight before event | This step's surviving fraction | Cumulative survival |
| --- | ---: | ---: | ---: | ---: |
| Month 2 | 2 | 10 | 0.8 | 0.8 |
| Month 5 | 4 | 6 | 1/3 | 0.2667 |

### 5.4 Calculate group B by hand
{: #section-35 }

B1 dies at month 1: risk-set weight = 10 and death weight = 2, giving $$S_B(1)=0.8$$.

B2 dies at month 4: B1 has left; weights of B2, B3, and B4 total $$4+2+2=8$$. Death weight is 4, so $$S_B(4)=0.8\times(1-4/8)=0.4$$.

B3 is lost at month 4.5 and B4 reaches administrative end at month 6. No new deaths occur, leaving six-month survival of 40% and mortality risk of 60%.

The weighted six-month risk difference A minus B is therefore $$73.33\%-60\%=+13.33$$ percentage points. This is a teaching calculation; an eight-person curve does not establish causal drug effects.

### 5.5 Why not divide weighted deaths by the baseline weight total?
{: #section-36 }

Group A's weighted deaths total $$2+4=6$$, and its baseline weight total is 10. Dividing gives 60%, whereas KM gave 73.33%. The difference arises because A2 cannot keep contributing to later at-risk denominators after being lost at month 3.

With no early censoring and complete outcomes at a common horizon, fixed-weight KM reduces to the corresponding weighted event proportion. With censoring, this simplification generally fails. Unweighted KM in this table gives mortality risks of 62.5% for A and 50% for B—another calculation distinct from weighted KM.

### 5.6 Write the general formula last
{: #section-37 }

Let $$t_j$$ be a group's $$j$$th distinct death time and $$\tau$$ the horizon at which risk is to be reported. Weighted KM is:

$$
\widehat S(\tau)=\prod_{t_j\leq\tau}\left(1-\frac{d_w(t_j)}{n_w(t_j)}\right).
$$

The symbol $$\prod$$ means multiplication across terms. Update only at death times through $$\tau$$; censoring itself creates no downward step. Calculate the formula separately for each drug group. Risk is $$1-\widehat S(\tau)$$; then form a risk difference or risk ratio.

This product connects survival across successive event times. The product in [Longitudinal IPTW]({{ "/causal-inference/longitudinal-iptw/" | relative_url }}) constructs weights for successive treatment choices. **Both multiply, but they multiply different things.**

## 6. What about loss to follow-up? Survival analysis handles timing without guaranteeing removal of censoring bias
{: #section-38 }

KM retains known follow-up before loss and removes the person from subsequent risk sets. That is a way to use records, not proof that loss-to-follow-up bias has been resolved.

If more severely ill people are more likely both to be lost and to die, people remaining at risk may not represent the subsequent risks of those lost. Baseline treatment IPTW alone does not automatically handle this selection.

Interpreting the KM estimates above as target survival curves requires noninformative censoring conditions appropriate to the analysis population and weight construction. If censoring depends on measured history, additional inverse probability of censoring weights (IPCW), an appropriate outcome model, or other methods may be considered. Censoring being independent conditional on some variables does not automatically mean that a within-group KM curve using only treatment IPTW has handled censoring adequately.

For example, patients of a certain type with estimated retention probability 0.8 at a time point may receive retention-weight factor $$1/0.8=1.25$$. With treatment weight 2, an appropriate combined weight may be $$2\times1.25=2.5$$. Retention probability is not death probability; observed deaths must not be treated as lost patients needing compensation.

For the missingness or loss mechanism actually modeled, examine available history, timing, positivity, and model specification. When artificially censoring strategy deviations, do not adjust twice for the same adherence process through both treatment and censoring weights.

## 7. Weighted Cox: How do weights enter risk-set comparisons?
{: #section-39 }

### 7.1 What do Cox and KM each answer?
{: #section-40 }

KM directly estimates survival curves over time, from which six-month or one-year risk differences can be obtained. It does not require proportional hazards between groups.

A marginal Cox model containing only a drug label can be written $$h_A(t)=h_B(t)\times\exp(\beta)$$. Here $$h$$ is instantaneous mortality rate among current survivors, $$\beta$$ the unknown drug coefficient, and $$\exp(\beta)=\mathrm{HR}$$. Under an assumption or working model, one relative multiplier summarizes the groups' time-to-event relationship.

**An HR is not a one-year mortality risk ratio.** Even HR = 0.7 does not directly mean that one-year death probability falls by 30%. A single HR requires particular caution with crossing survival curves or nonproportional hazards. Marginal hazards also compare those surviving to that time under each respective strategy, rather than always comparing exactly the same survivors.

### 7.2 See both weighted Cox contributions in the same eight-person table
{: #section-41 }

At a death time, Cox examines the current A/B risk set together. Let $$r=\exp(\beta)$$ be a candidate HR: each A patient has relative score $$r$$ and each B patient score 1. This score differs from IPTW: it depends on the HR currently being fitted, whereas IPTW comes from the treatment-probability model.

B1 dies at month 1, with everyone in the risk set. A-group weights total 10 and B-group weights total 10, so the weighted total score is $$10r+10$$. Trying $$r=2$$ gives weighted scores 20 for A and 10 for B; trying $$r=0.5$$ gives 5 and 10.

Weighted Cox changes both:

1. **Every risk-set member:** contributes “IPTW × Cox relative score” to the total denominator score.
2. **The actual event case's event term:** the observation's contribution to the fitting objective is enlarged or reduced by that person's IPTW. B1's weight is 2, giving that event term two units of contribution.

When A3 dies at month 5, A's risk-set weights total 6 and only B4 remains from B, with weight 2. The weighted total score becomes $$6r+2$$, while A3's event term receives weight 4. Software combines all time points to choose $$\beta$$.

Thus “weighted Cox” does not mean multiplying the HR by an average weight or simply including a predictor column named `weight` in the regression formula.

<details class="study-callout" markdown="1">
<summary>Second pass: Weighted log partial likelihood without tied death times</summary>

Let $$i$$ index a person who dies, $$t_i$$ their death time, $$R(t_i)$$ the combined risk set immediately beforehand, $$Z_i$$ their A/B label, and $$w_i$$ their fixed baseline treatment weight. A common weighted estimation objective, ignoring constants independent of $$\beta$$, is:

$$
\ell_w(\beta)=\sum_{i:\delta_i=1}w_i\left[\beta Z_i-\log\left\{\sum_{j\in R(t_i)}w_j\exp(\beta Z_j)\right\}\right].
$$

The outer sum runs over deaths; $$w_i$$ weights the current event contribution. The inner sum runs over the risk set at that time; $$w_j$$ weights each at-risk record. The function $$\log$$ is the natural logarithm. The event case's log relative score, $$\beta Z_i$$, is reduced by the log total risk-set score. The model seeks the $$\beta$$ maximizing this objective. This is a weighted estimation objective, not a claim that fractional-weight patients are new independent patients.

For this example's four events, A/B risk-set weight totals are 10/10 at month 1, 10/8 at month 2, 6/8 at month 4, and 6/2 at month 5. Event weights are respectively 2, 2, 4, and 4. Therefore:

$$
\ell_w(\beta)=2[-\log(10r+10)]+2[\beta-\log(10r+8)]+4[-\log(6r+8)]+4[\beta-\log(6r+2)],\quad r=\exp(\beta).
$$

Solving this objective in code gives HR ≈ 0.741. However, these curves cross later in follow-up, so the number should not be read as lower six-month risk or a reliable constant causal effect. It demonstrates how Cox summarizes time information. Group A actually has higher six-month risk here, highlighting that HR and fixed-horizon risk are different quantities.

Real data often contain tied event times, requiring explicit handling such as Breslow or Efron. Software may differ in conventions for case weights, ties, and variance. This hand-written example covers only a point estimate without ties and does not replace a complete software implementation.

</details>

## 8. How does multivariable LR connect to actual time-to-event data?
{: #section-42 }

Reuse the baseline features and A/B assignments of the same 3,000 people: 1,119 receive A and 1,881 receive B. The propensity score for A is still fitted using age, diabetes, severity, and background treatment C history:

$$
\widehat\eta=-0.686970+0.480725\times\mathrm{age10}+0.781641\times D+0.617510\times S-0.498737\times H,
\qquad
\widehat e=\frac1{1+\exp(-\widehat\eta)}.
$$

Here $$\mathrm{age10}=(\mathrm{age}-70)/10$$; $$D$$ is diabetes, coded 0/1; $$S$$ is a continuous severity score; $$H$$ is baseline background treatment C, coded 0/1; and $$\widehat\eta$$ is predicted log-odds of treatment. They are all pretreatment variables. Neither death time nor censoring time enters the PS model. Stabilized weights remain $$0.373/\widehat e$$ for A and $$0.627/(1-\widehat e)$$ for B. See [the full multivariable LR fit]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15).

This note separately simulates death times and independent random loss-to-follow-up times, applies administrative end at month 12, and constructs each person's `time` and `event`. Independent loss is ensured by the simulation design, not a claim about real data.

| Quantity | Drug A | Drug B |
| --- | ---: | ---: |
| Original number of patients | 1,119 | 1,881 |
| Observed deaths | 222 | 375 |
| Lost before death within 12 months | 311 | 452 |
| Direct deaths / baseline population | 19.84% | 19.94% |
| Unweighted KM 12-month mortality risk | 23.81% | 23.20% |
| Stabilized-IPTW KM 12-month mortality risk | 18.96% | 26.63% |

The weighted 12-month risk difference is −7.67 percentage points, with risk ratio ≈ 0.712. Stabilized-weight Cox gives HR ≈ 0.673, **which differs from risk ratio 0.712**. Unweighted KM handles follow-up timing and censoring but does not remove treatment-selection confounding; weighted KM additionally uses treatment weights.

All are simulated point estimates. No significance is claimed, and the drug coefficient in the data-generating conditional hazard is not treated as a verified constant marginal HR. A research report should assess conditions such as PH and specify the chosen HR's interpretation and limitations.

[Python reproduction script]({{ "/assets/causal-inference/weighted-survival-example/weighted_survival.py" | relative_url }}) / [Computed results]({{ "/assets/causal-inference/weighted-survival-example/results.json" | relative_url }}). The script includes the eight-person hand calculation and the 3,000-person simulation, reuses the verified LR fitting function, and calculates weighted KM and Cox point estimates without tied events. It does not provide standard errors or complete survival-model diagnostics.

## 9. How are baseline and longitudinal weights used in survival analysis?
{: #section-43 }

### Baseline initiation of A versus B
{: #section-44 }

If the intervention specifies only baseline initiation, a person's treatment weight can remain fixed throughout follow-up. What changes is when the person enters or leaves risk sets and whether additional censoring weights are needed. Later discontinuation or switching does not automatically revoke baseline group membership or trigger artificial censoring.

### Sustained AA versus BB strategies
{: #section-45 }

For sustained treatment, weights may update at each decision. Suppose a person's treatment weight is 2 in the first interval and accumulates to 8 after the second decision. First-interval risk-set and event contributions can use only the contemporaneous 2; weight 8 applies to the second interval. Do not backfill the final weight 8 into earlier records. If the person dies in the first interval, record the death rather than inventing a second treatment decision.

Under a “censor upon strategy deviation” approach, post-deviation records no longer represent that strategy. Retain preceding event and at-risk time and adjust appropriately for the selection. Early deaths cannot be removed because patients “did not complete the course.” A common implementation uses start/stop intervals with the cumulative weight available then.

| id | Interval start | Interval end | Event at interval end? | Weight available in this interval |
| --- | ---: | ---: | ---: | ---: |
| Person 1 | 0 | Month 3 | 0 | 2 |
| Person 1 | Month 3 | Month 5 | 1 | 8 |

This is an illustration, not a directly runnable sustained-strategy dataset. Both rows belong to one person, so dependence must be handled. Nor does putting a single “current A/B” variable in Cox automatically estimate a sustained strategy's total effect. Target strategies, treatment-history model, compatibility, and censoring rules must match.

With time-varying weights, a product-limit form can still calculate risk-set and event fractions using the appropriate contemporaneous weights at each event. But constructing records and weights that represent the strategy is a prerequisite. Supplying everyone's final weight to a static KM calculation does not complete the task.

## 10. Stabilization, confidence intervals, and reporting
{: #section-46 }

**Baseline stabilization and group-specific KM:** Multiplying every weight in one group by the same constant multiplies both the death-weight sum and risk-set-weight sum at each event. The constant cancels in $$d_w/n_w$$. Thus ordinary and stabilized baseline IPTW give the same within-group KM curves in this note.

**This result does not directly extend to Cox.** A Cox risk set contains A and B together. Different constants for the two groups change their relative contributions within the same risk set, so finite-sample HRs need not be exactly equal. This simulation gives HR ≈ 0.672359 with ordinary weights and ≈ 0.672528 with stabilized weights—very close but different. Multiplying everyone's weights by one common constant leaves the point estimate unchanged.

**Uncertainty:** Weighted counts are not actual independent sample sizes, so ordinary variance formulas must not be applied as though replicated records were independent people. Weighted Cox usually calls for appropriate sandwich/robust variance, but robust variance treating estimated weights as fixed does not necessarily capture the PS-estimation step fully. Estimator-specific joint inference or resampling may be used. Resampling generally should refit the PS, recalculate weights, and handle repeated records or clones at the original-patient level. A `robust=True` option cannot repair confounding, an incorrect starting point, or incorrect strategies.

R's `coxph` documentation distinguishes case weights, robust variance, and ties. Check software arguments; do not add the weight column merely as an ordinary covariate. [Official coxph documentation](https://www.stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html)

Reports should specify target strategies and population, common time zero, outcome and competing events, group-specific deaths/censoring and numbers at risk, weight construction and diagnostics, censoring assumptions, risk curves and prespecified risk contrasts, HR model conditions, and corresponding confidence intervals. When few patients remain at risk in the tail, do not present that curve segment as a precise estimate of long-term risk.

## 10.1 Competing events: How do standard methods change when patients die before dementia?
{: #section-47 }

### Specify the target first: First dementia, not all-cause death
{: #section-48 }

Consider comparing first dementia within five years after initiating A or B. A patient who dies without dementia can no longer develop first dementia afterward. An event that prevents the target event is a **competing event**. “Competing risks” names the corresponding time-to-event framework; it does not mean that two statistical risk numbers compete.

| Target event | Possible competing event | Explanation |
| --- | --- | --- |
| First dementia | Death before dementia | First dementia cannot develop after death |
| Cardiovascular death | Noncardiovascular death | A person cannot first die of another cause and then die of a cardiovascular cause |
| First hospitalization | Death before first hospitalization | Death ends the opportunity for first hospitalization |
| All-cause death | Generally no other type of death acts as a competing event | Deaths from every cause belong to the target outcome |

Discontinuation and switching are not automatically competing events, because dementia can still occur afterward. Dementia followed by death does not erase the dementia already observed; a first-event analysis classifies the first event as dementia. Studying subsequent death as well requires a multistate model such as “no dementia → dementia → death.” [Competing risks and multistate-model tutorial](https://stat.ethz.ch/CRAN/web/packages/survivalVignettes/vignettes/tutorial.html)

### Loss and death: One makes later status unknown; the other makes the target event impossible
{: #section-49 }

Loss at year 2 means dementia or death might occur afterward, but the data do not tell us. Death without dementia at year 2 means we know that first dementia can no longer occur.

For cumulative risk in a real world where death before dementia remains possible, retain death as an observed event type rather than treating it as ordinary loss or deleting the entire record. Basic data contain follow-up time and status: 0 = genuine right censoring, 1 = first dementia, 2 = death before dementia.

### Five people show why 1 − KM answers the wrong risk question
{: #section-50 }

There is no loss to follow-up in this table; every record determines the first-event status through month 5. Months simplify hand calculation, not imply that dementia usually develops at this speed.

| Patient | First event or follow-up end |
| --- | --- |
| Person 1 | Month 1: dies without dementia |
| Person 2 | Month 2: first dementia |
| Person 3 | Month 3: dies without dementia |
| Person 4 | Month 4: first dementia |
| Person 5 | Month 5: alive without dementia |

The observable first-dementia proportion by month 5 is $$2/5=40\%$$. If deaths are mistakenly treated as KM censoring:

- At month 1, Person 1's death is “censored”; KM does not fall and four people remain.
- At month 2, Person 2 develops dementia; KM is multiplied by $$3/4$$.
- At month 3, Person 3's death is “censored”; KM does not fall and two people remain.
- At month 4, Person 4 develops dementia; KM is multiplied by $$1/2$$.

The result is $$1-\mathrm{KM}=1-(3/4)(1/2)=62.5\%$$, rather than 40%. Death reduces later denominators without consuming probability mass as an event that prevents dementia.

The 62.5% can be viewed as a net-risk quantity derived from the dementia cause-specific hazard. Without additional assumptions, however, it cannot be called “the causal dementia risk if everyone were prevented from dying.” Even if some latent event times for competing causes are independent, censoring deaths in $$1-\mathrm{KM}$$ does not yield real-world cumulative incidence of the target event.

### CIF and Aalen–Johansen: Include both event types in the calculation
{: #section-51 }

The **cumulative incidence function (CIF)** is the probability, starting from baseline, of experiencing the target event by time $$t$$ before a competing event. Denote the dementia CIF by $$F_{AD}(t)$$ here.

Define $$S(t)$$ as the probability of remaining free of either first event through $$t$$: alive and without dementia. It is not survival alone. Define $$F_D(t)$$ as the probability of death before dementia by $$t$$. Then:

$$
S(t)+F_{AD}(t)+F_D(t)=1.
$$

The quantity $$F_D$$ is not all-cause mortality risk including deaths after dementia.

At each event time, identify $$R$$ = the number still event-free and observed immediately beforehand; $$d_{AD}$$ = the number developing dementia now; $$d_D$$ = the number dying before dementia now; and $$S_{\mathrm{before}}$$ = estimated event-free probability just before this time.

$$
\text{New dementia probability at this time}=S_{\mathrm{before}}\frac{d_{AD}}{R},
\qquad
S_{\mathrm{after}}=S_{\mathrm{before}}\left(1-\frac{d_{AD}+d_D}{R}\right).
$$

Add the new dementia probabilities over time to obtain $$F_{AD}$$. This is the Aalen–Johansen (AJ) estimator in a simple competing-risks setting. Initially, $$S=1$$ and both CIFs are 0.

| Month and event | $$R$$ before event | $$S$$ before event | New dementia probability | $$S$$ after event | Cumulative dementia probability |
| --- | --- | --- | --- | --- | --- |
| Month 1: Person 1 dies | 5 | 1 | 0 | 4/5 | 0 |
| Month 2: Person 2 develops dementia | 4 | 4/5 | (4/5) × (1/4) = 1/5 | 3/5 | 1/5 |
| Month 3: Person 3 dies | 3 | 3/5 | 0 | 2/5 | 1/5 |
| Month 4: Person 4 develops dementia | 2 | 2/5 | (2/5) × (1/2) = 1/5 | 1/5 | 2/5 |

Death does not increase the dementia CIF, but it reduces the population fraction that can contribute future dementia probability. At the end, dementia accounts for 40%, death before dementia 40%, and remaining event-free 20%. With genuine right censoring, AJ still calculates using risk sets, but appropriate censoring assumptions remain necessary.

### Cox still works, but distinguish cause-specific hazards from cumulative risks
{: #section-52 }

**Cause-specific Cox** can study how drugs A and B relate to the instantaneous dementia rate among people currently alive and without dementia.

When fitting dementia cause-specific Cox, remove people who die from risk sets at death and code them as non-dementia events in that model's event indicator, commonly 0 in software. Computationally this resembles censoring, **but it does not require imagining that dead people remain capable of developing dementia**. Estimating cause-specific hazards does not require independent latent times for the competing causes. Genuine loss to follow-up still requires appropriate ignorable-censoring conditions.

To obtain a five-year dementia CIF, dementia Cox alone is insufficient. Also estimate the cause-specific hazard of death before dementia, then combine both to calculate event-free probability and cumulative dementia probability. Two Cox models or other jointly coherent models can be used.

A cause-specific HR is not a five-year risk ratio or automatically a direct causal effect excluding pathways through death. Treatments may change the composition of survivors, so A/B risk-set populations no longer maintain their initial composition over time. [A causal framework for competing-event targets](https://pmc.ncbi.nlm.nih.gov/articles/PMC7811594/)

### Fine–Gray: Another model, not a “corrected ordinary HR”
{: #section-53 }

The Fine–Gray model targets the subdistribution hazard corresponding to a CIF. Its denominator differs from cause-specific Cox: people who have experienced a competing event are retained in a special way in an extended computational set, with appropriate weights also involved when censoring occurs. This is a mathematical construction, not a claim that dead people can develop dementia.

Its result is a subdistribution hazard ratio (sHR). An sHR of 0.7 does not mean five-year dementia risk falls by 30%, and it cannot be interpreted like a cause-specific HR as “the instantaneous-rate ratio among people still alive without dementia.” It can model CIFs, but is neither the only competing-event method nor mandatory for every causal TTE. [Guidance on interpreting Fine–Gray models](https://pmc.ncbi.nlm.nih.gov/articles/PMC5698744/)

If the target is the five-year absolute risk difference between A and B, adjusted CIFs and their risk difference often answer more directly than an sHR alone. AJ and standardization after cause-specific modeling can also estimate CIFs.

### How does IPTW adapt? Estimate treatment probability as before; estimate weighted CIFs afterward
{: #section-54 }

Continue with the multivariable LR above: A/B assignment is the label, and pretreatment age, diabetes, severity, background treatment C, and other features are predictors. For the target population ATE, use $$1/\widehat e(L)$$ in A and $$1/[1-\widehat e(L)]$$ in B. Select confounders considering treatment relationships with both the target and competing events, not solely which variables predict dementia.

Competing events do not automatically change the treatment-weight formula. The crucial change is to avoid censoring deaths as ordinary losses and using weighted $$1-\mathrm{KM}$$ as real-world dementia risk.

**Weighted AJ makes three replacements:** Replace $$R$$ with the total weight $$W$$ of people still event-free; replace $$d_{AD}$$ with the weight sum $$D_{AD}$$ of current dementia cases; replace $$d_D$$ with the weight sum $$D_D$$ of current deaths before dementia. Thus:

$$
\Delta\widehat F_{AD,w}=\widehat S_{w,\mathrm{before}}\frac{D_{AD}}{W},
\qquad
\widehat S_{w,\mathrm{after}}=\widehat S_{w,\mathrm{before}}\left(1-\frac{D_{AD}+D_D}{W}\right).
$$

Here $$\Delta$$ marks this step's increment in estimated dementia probability, hats mark estimates, and subscript $$w$$ indicates weighting. For teaching, suppose the five patients above all belong to group A. Multivariable LR supplies $$\widehat e=(0.5,0.8,0.5,0.4,0.8)$$, giving ordinary IPTW $$(2,1.25,2,2.5,1.25)$$ and baseline weight total 9. These scores are illustrative outputs, not a model trained on five patients alone.

- Month 1, death weight 2: $$S$$ falls from 1 to $$7/9$$.
- Month 2, dementia weight 1.25: add $$(7/9)\times(1.25/7)=1.25/9$$; $$S$$ falls to $$5.75/9$$.
- Month 3, death weight 2: $$S$$ falls to $$3.75/9$$.
- Month 4, dementia weight 2.5: add $$(3.75/9)\times(2.5/3.75)=2.5/9$$.

The final weighted dementia CIF is $$(1.25+2.5)/9\approx41.67\%$$. With no loss, this example simplifies to weighted event count divided by baseline weight total; with loss, that fraction cannot be applied mechanically. Apply the same procedure in group B, compare CIF differences or ratios at the prespecified time, and use appropriate uncertainty estimation. [IPTW and competing risks](https://pmc.ncbi.nlm.nih.gov/articles/PMC11803134/)

Genuine loss may require extra IPCW. For the total effect on real-world competing risk, do not automatically inverse-weight death away; that changes the research target. When baseline stabilization multiplies all weights in a group by a constant, that constant cancels from these AJ ratios.

### How do PSM, the g-formula, and longitudinal strategies adapt?
{: #section-55 }

**PSM:** Use baseline propensity scores to find comparable A/B patients, then estimate competing-risk CIFs in the matched sample with inference compatible with matching. Matching does not remove death's competing nature; the target may remain the matched A-treated patients. [Matching and competing risks](https://pubmed.ncbi.nlm.nih.gov/30347461/)

**G-formula:** In each short interval, among people alive without dementia, model three mutually exclusive destinations: dementia this interval, death before dementia this interval, or remaining event-free. A multinomial LR can use treatment, time, age, diabetes, and other inputs. Alternatively, use two conditional binary models with an explicitly defined ordering; do not fit two unrestricted probabilities that can sum to more than 1.

For example, under A for everyone, suppose mutually exclusive per-interval transition probabilities are 0.10 for dementia, 0.20 for death, and 0.70 for remaining event-free. Two-interval dementia risk is $$0.10+0.70\times0.10=0.17$$. Ignoring death and calculating $$0.10+0.90\times0.10=0.19$$ changes the target. If illustrative B-for-everyone probabilities are 0.15 for dementia, 0.05 for death, and 0.80 for no event, two-interval dementia risk is $$0.15+0.80\times0.15=0.27$$, giving risk difference −0.10. Actual multivariable analysis predicts using each person's baseline features in the same target population and then averages. With time-varying health, simulate its history as well and stop updating the initial state after either first event.

**Sustained strategies and CCW:** Construct longitudinal weights for strategy adherence and genuine loss, then combine them with appropriate competing-event estimation. Death itself is not medication nonadherence and must not automatically be removed through ordinary artificial censoring. Weight timing and target effect still require explicit definitions.

**Composite endpoint:** If the target becomes “first dementia or death,” both are target events and appropriate KM/Cox methods can be used. But this is a different outcome from dementia risk alone. Tracking death after dementia or repeated hospitalizations may require multistate or recurrent-event frameworks.

### TTE must first decide: Allow competing events or hypothesize eliminating them?
{: #section-56 }

The real-world total-effect question is: If the same target population all initiated A versus all initiated B, how would five-year probability of dementia occurring first differ while death remains possible? Under appropriate causal identification conditions, adjusted CIF contrasts can answer without assuming death has been eliminated.

A lower dementia CIF does not necessarily indicate better overall health. For example, with 100 people per group and no loss: A has 10 dementia-first cases, 40 death-first cases, and 50 remaining event-free; B has 20 dementia-first cases, 10 death-first cases, and 70 remaining event-free. A has less dementia but more death before dementia. Therefore also show the competing-event CIF. If overall mortality matters, separately analyze all-cause death including death after dementia; “death before dementia” is not a substitute.

A different question asks, “If some intervention prevented death, how would A/B affect dementia?” It requires defining an additional intervention and stronger identification conditions. A dementia trajectory that does not exist after death cannot be invented by an ordinary censoring convention. Do not automatically label cause-specific HR, Fine–Gray sHR, or death-censored $$1-\mathrm{KM}$$ as this direct effect.

### How standard methods adapt to competing events
{: #section-57 }

| Original method | Common misuse | Adaptation matching the target |
| --- | --- | --- |
| $$1-\mathrm{KM}$$ | Censor deaths as ordinary losses and call the result real-world dementia risk | Use the dementia CIF from AJ; KM remains suitable for a genuine single-event or composite endpoint |
| Ordinary Cox | Read HR directly as a five-year risk ratio | Specify a cause-specific HR; combine models for all causes to obtain CIFs, or use an appropriate CIF model |
| Fine–Gray | Treat sHR as a risk ratio or a direct effect “eliminating death” | Interpret within the subdistribution model and report predicted CIFs and prespecified-time risks |
| IPTW | Assume balance eliminates competing events | Treatment weights plus weighted AJ or suitable competing-risk estimation |
| PSM | Ignore deaths after matching | Estimate CIFs in the matched sample and use inference reflecting matching |
| G-formula | Simulate only dementia and allow dead patients to develop it | Jointly simulate target and competing events; stop generating subsequent dementia after death |
| IPCW | Automatically inverse-weight death away as loss | Model genuine censoring; eliminating competing events requires a separate target and assumptions |

For the two papers under study, AD-incidence outcomes require checking how deaths before dementia are recorded and handled. All-cause mortality has no competing “death from another cause” event. Seeing “Cox/IPTW” alone does not tell us whether authors estimated real-world CIFs. A cause-specific HR can be a legitimate target; death removing a person from the risk set does not by itself make the entire analysis wrong.

## 11. Return to the two TTE extension papers
{: #section-58 }

Table 1 and Methods of the 2023 high-throughput paper connect ML propensity scores, IPTW, and Cox/KM: construct drug emulations and baseline weights, then analyze time to AD. The statistical analysis states a noninformative-censoring assumption. “Used IPTW” must not be read as “censoring was separately modeled and adjusted.” Its AD-risk interpretation also requires considering how death and other competing events were handled.

The 2025 federated TTE framework includes federated IPTW and federated Cox. Federation changes where computation occurs and how model information is aggregated, while treatment weights, event times, risk sets, and target effects still need distinction. Distributed implementation details appear in the subsequent paper discussion; this note's hand calculation does not replace algorithm verification.

For the papers and detailed reading, see [TTE Extensions: High-Throughput Drug Screening and Federated Target Trial Emulation]({{ "/causal-inference/high-throughput-federated-tte/" | relative_url }}).

## 12. Self-check and sources
{: #section-59 }

1. Does the curve drop immediately when A2 is lost at month 3? — No, but A2 no longer enters later risk sets.
2. Does weight 4 with death at month 5 mean “20 months survived”? — No. Time remains five months; only the record's contribution changes.
3. Can events be weighted while risk sets retain actual headcounts? — No. Both components must use a consistent weighting scheme.
4. Does baseline IPTW automatically handle informative loss? — No. Examine censoring conditions and appropriate adjustment.
5. If weight 2 later becomes 8, can earlier records be changed to 8? — No. Future choices cannot be used to backfill earlier contributions.
6. Does HR = 0.7 imply a one-year risk ratio of 0.7? — No. They are different target quantities.

Sources:

- [Austin: The use of propensity score methods with survival or time-to-event outcomes](https://pmc.ncbi.nlm.nih.gov/articles/PMC4285179/): connecting propensity scores with marginal survival curves and HRs.
- [Adjusted restricted mean survival times in observational studies](https://pmc.ncbi.nlm.nih.gov/articles/PMC7534830/): expressing weights in event and at-risk counts.
- [Official R survival coxph documentation](https://www.stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html): implementation details for weights and variance.
