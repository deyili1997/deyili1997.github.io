---
layout: "causal-note"
title: "From Clinical Records to Adjustment Variables: NLP, Imaging, and Machine Learning"
description: "Turn pretreatment text and images into adjustment information, and understand what machine learning can and cannot solve."
group: "Extensions"
order: 21
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. Translation of the passage: From detecting problems to improving information", "anchor": "section-1"}, {"title": "2. What can “unmeasured” mean?", "anchor": "section-2"}, {"title": "3. NLP: Turning clinical text into analyzable information", "anchor": "section-3"}, {"title": "4. Image processing: Extracting needed baseline features from images", "anchor": "section-6"}, {"title": "5. How can machine learning help identify “combinations of variables”?", "anchor": "section-7"}, {"title": "6. Why do “more variables and better prediction” still not establish no confounding?", "anchor": "section-10"}, {"title": "7. Connecting the original passage's second and third paragraphs", "anchor": "section-11"}, {"title": "8. Self-check", "anchor": "section-12"}, {"title": "Sources", "anchor": "section-13"}]
previous_note: "/causal-inference/negative-control-outcomes/"
next_note: "/causal-inference/g-estimation/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

Prerequisite: conditional exchangeability in [Potential Outcomes and Identification Assumptions]({{ "/causal-inference/potential-outcomes/" | relative_url }}). Companion reading: [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}), [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}), and [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**What problem does this passage address?**

Some confounding information exists in clinical text, images, or numerous scattered records but never reaches the researcher's analysis table. Information extraction can make it usable, and appropriate statistical learning may use these variables more effectively.

**Improving confounding information and modeling does not prove that all confounding has been eliminated.**

</aside>


Read §1–§4 first to understand where the information comes from, then §5–§6 to connect machine learning, IPW, and causal identification.


Multivariable calculation example: [A complete multivariable LR-IPTW example comparing drugs A and B]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}#section-15) shows how baseline characteristics of 3,000 people enter one common logistic regression to produce propensity scores, both groups' weights, balance diagnostics, and one-year risks. Z=0 denotes drug B, not no treatment.

## 1. Translation of the passage: From detecting problems to improving information
{: #section-1 }

The following translates a passage on unmeasured confounding in Hernán and Robins (2016):

> Other approaches to ameliorating unmeasured confounding depend on extracting information from sources previously considered unsuitable for large-scale research. For example, new natural-language-processing and advanced-image-processing techniques may eliminate the need for labor-intensive, record-by-record chart review. Machine-learning tools and other computer-science methods may also help identify combinations of variables that improve confounding adjustment compared with traditional approaches.

Here, **ameliorating** means improving or reducing; **might** denotes possibility. The authors describe promising directions, not a guarantee that automated extraction or machine learning eliminates confounding, nor a claim that all manual validation becomes unnecessary. [Original text, page 760](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf)

The preceding passage, discussed in [Negative Control Outcomes and Residual Bias]({{ "/causal-inference/negative-control-outcomes/" | relative_url }}), asks “Does the analysis produce suspicious results for questions that should have known answers?” This passage goes further: “Which missing information can be added, and how can existing information be used more effectively for adjustment?”

## 2. What can “unmeasured” mean?
{: #section-2 }

First consider the term from the perspective of the **analysis table available to the researcher**. Distinguish three situations:

| Situation | Example | What might technology do? |
| --- | --- | --- |
| Recorded but not yet organized as a variable | Family history appears in clinical notes, but the billing table has no such field | Extract the variable from text and validate it |
| Not measured directly, but related clues exist | No complete frailty assessment is available, but pretreatment functional-status descriptions are recorded | Construct proxies to supplement relevant information |
| Neither directly recorded nor supported by sufficiently reliable clues | A factor affecting treatment and prognosis was not captured in available data | Running a more complex model on the same data cannot guarantee resolution of the omission |

Thus, “initially unmeasured, later available for adjustment” is not contradictory: researchers may expand information sources or convert previously unusable information into analytical variables. Extracting a label, however, is not the same as accurately measuring every relevant factor.

## 3. NLP: Turning clinical text into analyzable information
{: #section-3 }

**NLP means natural language processing.** One use here is identifying clinical information in medical-record text, rather than directly producing a causal effect.

### An example using hormone therapy
{: #section-4 }

Suppose subject-matter knowledge suggests that pretreatment knowledge of breast-cancer family history may affect both hormone-treatment choice and breast-cancer prognosis. The initial analysis table contains only age, diagnosis codes, and prescription records, with no family-history variable.

Under this hypothetical structure, omitting family history may leave:

$$
\text{Hormone-treatment choice}\leftarrow\text{Family history}\rightarrow\text{Breast-cancer outcome}.
$$

The record may already contain text such as:

| Pretreatment clinical text, all teaching examples | Candidate extraction |
| --- | --- |
| “Mother diagnosed with breast cancer at age 48” | Recorded first-degree-relative history of breast cancer; distinguish the relative from the patient |
| “Denies family history of breast cancer” | Explicitly recorded denial of family history |
| Family history not mentioned in this note | Unrecorded / unknown; do not automatically code as absent |

After validation, this information can enter an appropriate adjustment set. For example, use it in [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) to estimate treatment-choice probabilities, or in [The G-Formula: From Standardization to Longitudinal Strategies]({{ "/causal-inference/g-formula/" | relative_url }}) to fit a conditional outcome model.

<pre class="mermaid">flowchart LR
    TEXT[&quot;Pretreatment text&quot;] --&gt; EXTRACT[&quot;Extract candidate clinical information&quot;]
    EXTRACT --&gt; CHECK[&quot;Validate meaning, timing, and errors&quot;]
    CHECK --&gt; SET[&quot;Select adjustment variables using causal knowledge&quot;]
    SET --&gt; EST[&quot;Use in IPW / g-formula estimation&quot;]</pre>

Arrows denote workflow steps. The improvement comes from newly available information and its appropriate use; the label “used NLP” itself provides no causal identification.

### Why is validation still needed?
{: #section-5 }

Algorithms may confuse “the patient has the disease” with “the patient's mother has the disease,” “denied” with “present,” or “past status” with “current status.” Differences in record detail between treatment groups can also make extraction errors differential by group.

Also distinguish **when a clinical fact occurred** from **when its record was created**. A posttreatment note stating “mother previously had breast cancer” describes a historical fact, but does not establish that this information was equally fully recorded, known, or used at baseline in both groups. Reconstructing baseline from posttreatment text requires separate justification of extraction windows, recording mechanisms, and whether the information is affected by treatment or outcome. Keywords alone do not justify treating the entire future chart as baseline data.

Manual annotation or independent reference information is therefore usually still needed to evaluate extraction accuracy, missed information, and group differences. The original passage describes reducing the burden of record-by-record manual abstraction, not allowing unvalidated automated labels. For related principles, see [Surveillance Bias and Differential Measurement Error]({{ "/causal-inference/surveillance-measurement-bias/" | relative_url }}).

## 4. Image processing: Extracting needed baseline features from images
{: #section-6 }

The same idea applies to imaging. A database may store images while the analysis table records only “test performed”; clinical features in the image have not yet been quantified.

For example, if a study requires a feature that can be reliably measured in baseline images, image processing can attempt to extract it. Researchers must then assess measurement accuracy, whether it was obtained before treatment, and whether it belongs in the current confounding adjustment.

**Having actual images to process differs from having only billing records for a test.** If the database contains neither images nor test results, an image algorithm cannot recover actual findings merely from “test performed.” This also connects to [Having undergone mammography does not mean the result is known]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}#section-19).

Moreover, only people who undergo imaging have those features available. If testing is associated with severity or treatment choice, retaining only patients with images may introduce new selection problems. Data coverage and missingness processes need assessment.

## 5. How can machine learning help identify “combinations of variables”?
{: #section-7 }

This can be understood at two levels: **increasing available confounding-related information**, and **better fitting relationships of existing information with treatment and outcomes**. These should not be conflated.

### 5.1 Finding relevant information or proxies among many records
{: #section-8 }

Researchers may lack a complete health-status measure but have many pretreatment diagnoses, medications, procedures, and healthcare-use records. Their combination may indirectly reflect disease severity or other factors affecting treatment choice and prognosis.

A **proxy** supplies indirect information about a factor. Several relevant proxies may be more informative than ignoring the factor entirely, but do not mean that it has been accurately observed.

The original passage cites the **high-dimensional propensity score (hdPS)** as a concrete example. It constructs and screens many candidate variables from diagnoses, prescriptions, and similar data, supplements investigator-specified variables, and uses them for propensity-score adjustment. This is a semiautomated approach to variable processing and adjustment, not an algorithm that automatically discovers the true causal graph. [Schneeweiss and colleagues (2009)](https://pubmed.ncbi.nlm.nih.gov/19487948/)

Proxy adjustment does not guarantee smaller bias, much less absence of residual confounding. Assess what the proxies actually reflect and which causal paths their inclusion changes. [VanderWeele: Principles of Confounder Selection](https://pmc.ncbi.nlm.nih.gov/articles/PMC6447501/)

### 5.2 Fitting treatment or outcome models more flexibly
{: #section-9 }

Even when relevant confounders are measured, an overly simple model may fail to use them sufficiently. For example, age may relate nonlinearly to treatment choice, or a symptom may strongly influence that choice only under particular disease conditions.

Appropriate machine-learning methods can attempt to capture these nonlinearities and interactions. For example, IPW requires estimating:

$$
e(L)=P(A=1\mid L).
$$

Here, e names the propensity-score function and L in parentheses supplies pretreatment information as inputs; this is not e multiplied by L. P denotes probability and the bar means conditional on that information. A is a 0/1 indicator of actual treatment, with 1 denoting the treatment of interest and 0 the comparator strategy; L can contain several variables. $$e(L)$$ ranges from 0 to 1, has no physical unit, and must not be confused with the expectation operator $$E[\cdot]$$.

$$A=1$$ denotes receiving the treatment of interest, and $$L$$ contains information available for adjustment before this treatment decision. The model asks “How likely are people with these measured characteristics to choose this treatment?”, not “How likely is treatment to work for this person?” For example, if an actual treated person's estimated probability is 0.20, the simplest baseline ATE weight is $$1/0.20=5$$. Outcome data are still needed to estimate effects; neither 0.20 nor 5 is a treatment effect. See [Inverse Probability Weighting: From Propensity Scores to Longitudinal Weights]({{ "/causal-inference/inverse-probability-weighting/" | relative_url }}) for full conditions and calculations.

Here, the learning algorithm **estimates a conditional treatment probability**. After obtaining probabilities, researchers still construct weights, inspect balance and data support, and estimate the target effect. The Gruber study cited in the passage discusses ensemble learning to estimate inverse probability weights. [Gruber and colleagues (2015)](https://pubmed.ncbi.nlm.nih.gov/25316152/)

NLP, machine learning, and IPW therefore are not mutually exclusive choices. NLP can extract variables, machine learning can fit required models, and IPW can use estimated probabilities to construct a causal-effect estimate. Implementation also requires appropriate control of overfitting and statistical inference.

## 6. Why do “more variables and better prediction” still not establish no confounding?
{: #section-10 }

| Common misunderstanding | How should it be understood? |
| --- | --- |
| There are thousands of variables, so nothing is omitted | Many variables do not guarantee the required confounding information |
| Accurate treatment prediction makes causal analysis reliable | Accurate treatment prediction cannot verify exchangeability; assess the adjustment set, weighted balance, and positivity too |
| Include the patient's entire past and future chart | For a total effect of baseline initiation, posttreatment states and outcome information cannot be arbitrarily treated as baseline confounders |
| A strong proxy means the original factor is fully measured | Proxies may contain measurement error and leave residual confounding |
| Every pretreatment variable can be adjusted for | Even pretreatment variables may be inappropriate to condition on; selection still requires causal structure |

For example, posttreatment symptoms may transmit treatment effects, and follow-up testing may be jointly affected by treatment and latent disease. Automatically adjusting for them can change the target effect or introduce selection bias. Statistical association alone cannot distinguish confounders, mediators, and colliders. [Theoretical basis for confounder selection](https://pmc.ncbi.nlm.nih.gov/articles/PMC6447501/)

For sustained strategies, the requirement is not “always use baseline information only.” Organize information using the medical history before each treatment decision; treatment–confounder feedback requires corresponding longitudinal methods. See [Point Interventions and Sustained Strategies]({{ "/causal-inference/point-sustained-strategies/" | relative_url }}).

## 7. Connecting the original passage's second and third paragraphs
{: #section-11 }

| Approach | Main question | What can it provide? |
| --- | --- | --- |
| Negative controls / known-effect controls | Does the analysis produce results inconsistent with credible expectations? | Clues about residual bias or other problems |
| NLP / image extraction | Is important information present but absent from the analysis? | New analyzable variables or proxy information |
| Appropriate statistical learning | Are complex relationships among existing variables used adequately? | Potentially more suitable treatment or outcome models |

A reasonable workflow defines the target trial and needed confounding information first and checks data gaps; then extracts, validates, and appropriately uses additional information; finally evaluates results with negative controls and related approaches and reports bias that still cannot be ruled out.

Do not repeatedly try variables until a negative control reaches its null value. Agreement with the negative control supports only what it can examine; it does not certify every identification assumption.

## 8. Self-check
{: #section-12 }

1. Family history appears in clinical notes but not in the analysis table. What type of information gap is this?
2. If smoking is unmentioned in a note, can it be coded as nonsmoking?
3. Does extracting more variables with NLP prove the absence of unmeasured confounding?
4. Can machine learning help IPW, and which quantity does it estimate?
5. How do the control analyses in the second paragraph differ from information extraction in the third?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. Information is recorded but not yet organized as an analyzable variable.
2. No; absence of documentation differs from explicit denial.
3. No; extraction error, omissions, and inappropriate adjustment may remain.
4. Yes—for example, by estimating the probability of treatment choice conditional on pretreatment information. This does not replace causal identification conditions.
5. The former checks results against expectations; the latter attempts to supplement adjustment information. Appropriate modeling then makes further use of that information.

</details>


## Sources
{: #section-13 }

- [Hernán and Robins (2016): Using Big Data to Emulate a Target Trial](https://dlab.epfl.ch/teaching/spring2022/cs727/papers/hernan2016using.pdf): page 760 and references 19–21 in the original.
- [Schneeweiss and colleagues (2009): High-Dimensional Propensity Score Adjustment](https://pubmed.ncbi.nlm.nih.gov/19487948/): high-dimensional proxy information and propensity-score adjustment.
- [Gruber and colleagues (2015): Ensemble Learning of Inverse Probability Weights](https://pubmed.ncbi.nlm.nih.gov/25316152/): ensemble learning to estimate the probabilities needed for weighting.
- [VanderWeele (2019): Principles of Confounder Selection](https://pmc.ncbi.nlm.nih.gov/articles/PMC6447501/): limits of variable selection, temporal ordering, and proxy adjustment.

The clinical text, variable combinations, and clinical scenarios in this note are teaching assumptions, not validated extraction algorithms or actual treatment effects.
