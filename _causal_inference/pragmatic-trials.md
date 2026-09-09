---
layout: "causal-note"
title: "Pragmatic Trials in Routine Care"
description: "Connect routine-care trial conditions with randomization, treatment strategies, and ITT or PP questions."
group: "Trial design"
order: 7
math: true
causal_notes: true
date: "2026-09-09"
last_modified_at: "2026-09-09"
tags: ["causal-inference", "target-trial-emulation"]
toc: [{"title": "1. How does it differ from an explanatory trial?", "anchor": "section-1"}, {"title": "2. An invented example: How might two antihypertensive drugs be compared?", "anchor": "section-2"}, {"title": "3. Pragmatic and randomized describe different dimensions", "anchor": "section-3"}, {"title": "4. More than a binary division into “pragmatic” and “nonpragmatic”", "anchor": "section-4"}, {"title": "5. Why do pragmatic trials often report ITT but also study PP?", "anchor": "section-5"}, {"title": "6. How does this relate to TTE and the earlier hormone-therapy protocol?", "anchor": "section-6"}, {"title": "7. Self-check", "anchor": "section-9"}]
previous_note: "/causal-inference/biomarkers-well-defined-interventions/"
next_note: "/causal-inference/target-trial-emulation/"
---

Study guide: [Causal Inference Study Guide]({{ "/causal-inference/" | relative_url }}).

<aside class="study-callout study-callout--abstract" markdown="1">

**Understand the purpose first**

A **pragmatic trial** aims to inform practical healthcare decisions by comparing intervention strategies as closely as possible to the routine-care conditions in which its findings will be applied.

It asks: What happens when a strategy is introduced into ordinary hospitals, clinics, and patients' lives? This note mainly concerns pragmatic randomized trials; closeness to routine care and random assignment can coexist.

</aside>


On a first reading, use §1–§4 to understand pragmatism as a study purpose and design orientation, then connect it to [Intention-to-Treat and Per-Protocol Effects]({{ "/causal-inference/intention-to-treat-per-protocol/" | relative_url }}) and [Target Trial Emulation]({{ "/causal-inference/target-trial-emulation/" | relative_url }}) through §5–§6. PRECIS-2 details can wait until you design a study yourself.

## 1. How does it differ from an explanatory trial?
{: #section-1 }

An **explanatory trial** tends to test whether an intervention produces its intended effect under more controlled research conditions. A **pragmatic trial** tends to provide evidence for choosing and implementing treatments under usual conditions of use.

A common introductory distinction is:

- **Efficacy**: Can the intervention produce its intended effect under relatively ideal research conditions?
- **Effectiveness**: What effect does adopting the intervention have under routine conditions?

This distinguishes purposes and design orientations. Both study intervention effects under their respective conditions. An explanatory trial does not necessarily yield a “pure pharmacological effect,” and a pragmatic trial does not imply identical effects in every real-world setting.

The following are common tendencies, not classification rules that every trial must meet:

| Design aspect | More explanatory | More pragmatic |
| --- | --- | --- |
| Participants | May select a more restricted population to reduce complexity | Aims to represent people who would actually receive the intervention, including relevant comorbidities and co-medications |
| Setting and personnel | May rely on specialist research centers, additional training, and resources | Aims to match the hospitals, clinics, and usual treatment providers where findings will be applied |
| Treatment delivery | More strictly standardizes implementation details | Retains reasonable routine-care adjustments within prespecified strategy boundaries |
| Adherence support | May add research-specific reminders, supervision, or other measures | Aims to reflect adherence support available in routine practice |
| Follow-up and outcomes | May add research-specific visits and measurements | Aims to resemble routine follow-up and use outcomes meaningful to patients or healthcare decisions |

For these design orientations and their continuum, see [Loudon and colleagues (2015): PRECIS-2](https://www.bmj.com/content/350/bmj.h2147).

## 2. An invented example: How might two antihypertensive drugs be compared?
{: #section-2 }

Suppose a healthcare system wants to know whether drug A or B is the more suitable initial choice for eligible patients with hypertension.

A more pragmatic randomized trial might:

1. Recruit through community clinics that usually see these patients.
2. Randomize to strategy A or B.
3. Have usual treating physicians adjust doses within prespecified limits and address safety issues.
4. Integrate follow-up with routine visits where possible, supplementing data when needed to ensure reliable outcomes.
5. Observe prespecified hospitalizations, adverse events, or other patient-relevant outcomes.

Patients may have comorbidities, face everyday medication difficulties, or need treatment adjustments. These require explicit handling in the protocol and analysis.

If the study instead enrolls only a very narrow population, adds daily medication supervision, and frequently performs tests absent from usual care, it becomes more explanatory in those dimensions. Pragmatism cannot be determined from “which drug is used” alone.

This example illustrates design structure without assuming either drug is actually better.

Consider one patient: Ms. Wang is eligible for both drugs and has co-medications commonly encountered in routine outpatient care. A more pragmatic design might let her usual physician adjust doses within protocol options at her regular clinic, with locally available refill support. A more explanatory design might add weekly research calls, extra tests, and dedicated medication supervision.

Both designs can randomize groups and carefully verify outcomes. The added resources in the latter may themselves change adherence and treatment effects. If ordinary clinics cannot supply those resources, researchers must consider how the results apply there. **Pragmatism means placing the comparison in conditions suited to its intended use, not reducing quality control.** The call and visit frequencies here are teaching assumptions, not disease-specific care recommendations.

## 3. Pragmatic and randomized describe different dimensions
{: #section-3 }

| Term | What does it describe? |
| --- | --- |
| Randomized | How are treatment strategies assigned? |
| Pragmatic | How closely do the population, setting, treatment delivery, follow-up, and other arrangements match the routine care in which results will be applied? |

Thus, **pragmatic trials can use random assignment; a pragmatic randomized trial combines both features**. Patients can receive care in ordinary clinics while a study protocol randomly determines their treatment groups.

Randomization helps establish comparability between assignment groups; resemblance to routine care helps answer practical application questions. The former does not automatically guarantee applicability everywhere, and the latter does not automatically eliminate bias.

Pragmatism does not mean having no clear protocol, ignoring safety rules, or accepting unreliable outcomes. Study procedures should match the intended use. [The pragmatic clinical trials textbook](https://rethinkingclinicaltrials.org/chapters/design/what-is-a-pragmatic-clinical-trial/)

## 4. More than a binary division into “pragmatic” and “nonpragmatic”
{: #section-4 }

These designs are usually understood along an **explanatory–pragmatic continuum**. A trial may enroll patients who closely resemble routine patients while using more rigorous research procedures for outcome measurement.

Open-label treatment, broad eligibility, active comparators, and follow-up using routine data are possible features, not a checklist that must be satisfied in full. For example:

- Patients may know their assignment while outcome assessors remain blinded.
- If a treatment is ordinarily appropriate only for a specific population, reasonable narrow eligibility criteria can still fit a pragmatic purpose.
- Important outcomes can be additionally verified; using routine data does not require accepting unvalidated records.

“Close to routine practice” requires asking: **routine for which population and which healthcare system?** Care resources ordinarily available in one region may be unavailable elsewhere. The pragmatic label alone does not establish universal applicability.

<details class="study-callout" markdown="1">
<summary>Advanced: PRECIS-2 supports design across nine domains</summary>

It considers eligibility criteria, recruitment, setting, organization and resources, flexibility of delivery, flexibility of adherence, follow-up, primary outcome, and primary analysis. Each domain is usually rated from 1 (more explanatory) to 5 (more pragmatic).

Its purpose is to assess alignment between design and intended trial use, not to treat higher scores as higher scientific quality or require every domain to reach 5. [The original PRECIS-2 paper](https://www.bmj.com/content/350/bmj.h2147)

</details>


## 5. Why do pragmatic trials often report ITT but also study PP?
{: #section-5 }

ITT asks what results from assignment to a strategy in the trial's adherence and care environment. This is relevant to many practical decisions, so pragmatic randomized trials often emphasize it.

The same trial can also ask what would happen if the same target population followed each specified strategy. That is the PP question.

The two distinctions answer different questions, while design conditions influence the meaning of the corresponding effects:

| Distinction | What does it describe? |
| --- | --- |
| Pragmatic / explanatory | How do the study purpose and design conditions correspond to routine application? |
| ITT / PP | Is the causal effect of interest assignment to a strategy or adherence to its protocol? |

**Pragmatic does not equal ITT, and explanatory does not equal PP.** For example, additional adherence support may alter a trial's assignment effect, so ITT interpretation still requires describing the trial setting. Pragmatic trials can target both effects. Rigorous PP analysis must address adherence-related confounding and selection, rather than simply delete nonadherers. [Murray, Swanson, and Hernán: Guidelines for estimating causal effects in pragmatic randomized trials](https://arxiv.org/abs/1911.06030)

Likewise, estimating PP does not require forcing every participant to adhere perfectly in reality. A trial can retain routine treatment processes and estimate “what would happen under adherence to specified strategies” when the necessary assumptions and data conditions hold.

## 6. How does this relate to TTE and the earlier hormone-therapy protocol?
{: #section-6 }

### Routine-care data usually make trials with pragmatic features easier to emulate
{: #section-7 }

Routine medical records and claims capture usual treatment, testing, and healthcare use. If a target trial requires blinding, research-specific tests, or intensive adherence support absent from the database, faithful emulation from those records may be difficult.

For the routine-data setting they discuss, Hernán and Robins therefore describe target trials as generally closer to pragmatic trials. **This concerns the trial conditions the data can support; it does not mean TTE creates real random assignment.** Emulation still requires addressing confounding from observational treatment choice and assessing the sufficiency of data and identification conditions. [Hernán and Robins (2016): Treatment strategies](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/)

### Which relevant features appear in the hormone-therapy protocol?
{: #section-8 }

In [Hormone Therapy and Breast Cancer: A Target Trial Protocol]({{ "/causal-inference/hormone-therapy-target-trial/" | relative_url }}), participants know their assigned group, treatment strategies include safety exceptions, the outcome is five-year breast-cancer diagnosis, and follow-up through contact with the healthcare system is discussed. These arrangements relate to practical medical decisions.

However, **these features alone do not establish the trial's overall level of pragmatism**. One must also know how participants differ from routine eligible patients, the implementation resources, extra visits, and adherence support. Safety-related stopping rules are not unique to pragmatic trials either.

The protocol's inclusion of both ITT and PP is compatible with a pragmatic purpose. It can address both actual outcomes after strategy assignment and outcomes under adherence to strategies that include safety exceptions.

## 7. Self-check
{: #section-9 }

1. Can randomizing patients in community clinics constitute a pragmatic trial?
2. Does use of electronic medical records establish that a study is a pragmatic randomized trial?
3. Is estimating PP in a pragmatic trial contradictory?
4. Do pragmatic-trial findings automatically generalize to every hospital?

<details class="study-callout" markdown="1">
<summary>Suggested answers</summary>

1. Yes; random assignment is compatible with routine-care settings.
2. No. Electronic medical records are a data source; they establish neither randomization nor the study's design and intended use.
3. No; design conditions and the target causal effect are different dimensions, but PP must be estimated appropriately.
4. No; target populations, resources, treatment, and care processes still need comparison.

</details>
