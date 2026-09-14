---
layout: post
title: "TxAgent: Therapeutic Reasoning Across a Universe of Tools"
description: "A detailed methodology reading of TxAgent: biomedical tool construction, dynamic tool retrieval, synthetic trajectory generation, stepwise supervision, and evaluation."
permalink: /txagent-therapeutic-reasoning/
date: 2026-09-13 12:00:00 -0400
research_area: healthcare-ai
math: true
tags: [Method, Healthcare AI, LLM, AI Agents, Therapeutic Reasoning, Tool Use]
---

**Paper:** Shanghua Gao et al., *TxAgent: An AI Agent for Therapeutic Reasoning Across a Universe of Tools*, [arXiv:2503.10970v1](https://arxiv.org/abs/2503.10970v1), March 14, 2025. These notes explain the **v1 paper**, including its Online Methods and extended figures. Page references refer to that 74-page PDF. The main goal is to explain how the system is constructed, trained, and evaluated; explanatory equations and pseudocode added here are identified as such.

TxAgent learns to alternate between an intermediate textual rationale, a structured action, and feedback from biomedical tools. Its contribution combines **a usable biomedical tool collection, a learned tool retriever, a pipeline for generating supervised action trajectories, and an instruction-tuned language model**. Understanding all four is necessary to interpret its results.

<nav class="table-of-contents" aria-label="Contents" markdown="1">

**Contents**

1. [The problem and the scope of the model](#problem)
2. [Components and the separation of training from inference](#components)
3. [ToolUniverse: schemas, execution, and biomedical coverage](#tooluniverse)
4. [Inference: the complete action-and-feedback loop](#inference)
5. [ToolRAG: retrieving tools and training the retriever](#toolrag)
6. [ToolGen: turning API documentation into usable tools](#toolgen)
7. [QuestionGen: constructing questions and reference answers](#questiongen)
8. [TraceGen: generating supervised trajectories with a Helper](#tracegen)
9. [TxAgent-Instruct and language-model training](#training)
10. [Worked examples: what each action contributes](#examples)
11. [Benchmark construction and scoring](#evaluation)
12. [Baseline models and comparison conditions](#baselines)
13. [Results, with the correct interpretation of each metric](#results)
14. [Ablations: tools, thoughts, and trajectory length](#ablations)
15. [What the evidence establishes and what remains open](#limitations)
16. [Reproducibility details and inconsistencies in v1](#reproducibility)
17. [Source map and terminology](#sources)

</nav>

## 1. The problem and the scope of the model
{: #problem }

A therapeutic question often contains several constraints. A drug may match a disease indication while being unsuitable for a particular age group, concomitant medication, or comorbidity. Answering requires identifying the relevant entities, finding the appropriate evidence, and combining it with the patient's stated conditions. A single association between a disease and a drug does not resolve this sequence of decisions.

TxAgent approaches the problem as **sequential evidence acquisition and answer construction**. The user supplies a natural-language question. The model decides which information is missing, selects tools, generates their arguments, reads the returned information, and decides whether to continue. It ultimately returns an answer, an explanation, and an observable record of its tool interactions. [Methods §1, pp. 39–45.](https://arxiv.org/pdf/2503.10970v1#page=39)

Three scope distinctions matter:

- **The implemented input interface is textual.** Although the abstract motivates multimodal precision therapeutics, the Discussion explicitly says that this version does not directly support pathology images, EHR data, or web-based laboratory results. A patient history written into a question is different from a dedicated longitudinal EHR encoder or an image-processing model.
- **“Personalization” means conditioning the answer on the supplied patient characteristics.** There is no reported patient-specific pharmacokinetic simulator, estimated treatment-effect model, or explicit optimization of a clinical utility function. The language model combines retrieved facts and textual constraints.
- **A retrieved statement and a valid clinical inference are separate things.** An API can return a real drug-label passage while the model still misinterprets its scope, misses a condition, or overstates the conclusion. The recorded trace makes parts of this process inspectable; it does not certify every conclusion.

<figure>
  <a href="{{ '/assets/healthcare-ai/txagent/figure-1-overview.png' | relative_url }}"><img src="{{ '/assets/healthcare-ai/txagent/figure-1-overview.png' | relative_url }}" alt="Figure 1 from TxAgent: the agent, ToolRAG, 211 biomedical tools, performance comparisons, and four examples of evidence retrieval and reasoning." width="690" height="1026"></a>
  <figcaption>Figure 1 from Gao et al. (2025). Panel a shows the inference loop; b–c describe the tool collection; d–e report DrugPC accuracy; f–i illustrate four behaviors. Click the figure to inspect it at full size. Drug-specific statements in the original figure describe the paper's historical examples.</figcaption>
</figure>

## 2. Components and the separation of training from inference
{: #components }

The name “TxAgent” can refer to the complete system or its trained language-model component. The following separation avoids attributing the capabilities of one component to another.

| Component | What it receives | What it produces | Where it is used |
| --- | --- | --- | --- |
| TxAgent language model | Question, previous actions and results, currently available tool schemas | Intermediate text, tool calls, and a final answer | Inference; trained on synthetic trajectories |
| ToolUniverse | A tool name and typed arguments | Biomedical information from an external API | Inference and data generation |
| ToolRAG | A natural-language description of a needed capability | Candidate tool descriptions and schemas | Inference and later rounds of data generation |
| ToolGen | API documentation and example data | Validated tool specifications and API mappings | Tool construction |
| QuestionGen | Biomedical reference information | Question, reference answer, explanation, and sometimes answer choices | Training-question and benchmark construction |
| TraceGen | Question, reference answer, explanation, tools, and their outputs | A screened trajectory of intermediate text and actions | Training-data construction |
| Tool graph | Descriptions of pairs of tools | Directed connections used to sample tool chains | Training-question construction only |
| Finish | A completion action associated with the final answer | Termination of the current reasoning process | Inference and training traces |

**The deployed agent does not need the ground-truth-aware Helper used by TraceGen.** ToolGen, QuestionGen, and TraceGen prepare the environment and training data. The runtime system uses the fine-tuned model, tool retrieval, and tool execution. Presenting all of the training agents as a committee that answers each user question would give the wrong architecture.

The main experiments use **Llama-3.1-8B-Instruct** as the language-model backbone. **gte-Qwen2-1.5B-instruct** is the separate embedding-model backbone used by ToolRAG. Consequently, “TxAgent-8B” names the main language model, not the total size or computational cost of every component in the full system.

<figure>
  <a href="{{ '/assets/healthcare-ai/txagent/extended-data-2-training-pipeline.png' | relative_url }}"><img src="{{ '/assets/healthcare-ai/txagent/extended-data-2-training-pipeline.png' | relative_url }}" alt="Extended Data Figure 2: ToolGen constructs and verifies tools; QuestionGen generates and evaluates questions; TraceGen uses a Helper, Solver, and tool provider to generate and evaluate trajectories." width="800" height="616" loading="lazy"></a>
  <figcaption>Extended Data Figure 2 from Gao et al. (2025). These are data-construction workflows. Human verification is explicitly shown for tool construction; the figure does not establish human review of every generated training trajectory.</figcaption>
</figure>

## 3. ToolUniverse: schemas, execution, and biomedical coverage
{: #tooluniverse }

### 3.1 What counts as a tool?

A tool is a **model-facing interface plus executable mapping logic**. Its description tells the language model what it does and how to call it. The backend translates the call into the provider's query format and returns the relevant data. The model does not generate the entire biomedical database or recreate its records from memory.

The description includes the tool's name and purpose. Each argument has a name, explanation, data type, and required/optional status. These fields matter: selecting a correct capability is insufficient if the model supplies a drug name to an argument that expects an ontology identifier.

This simplified example illustrates the interface; it is not a verbatim executable specification from the paper:

```json
{
  "name": "get_associated_targets_by_disease_efoID",
  "description": "Retrieve targets associated with a disease identified by EFO ID.",
  "parameters": {
    "type": "object",
    "properties": {
      "efoId": {"type": "string", "description": "Disease EFO identifier"}
    },
    "required": ["efoId"]
  }
}
```

A corresponding illustrative call is:

```json
{
  "name": "get_associated_targets_by_disease_efoID",
  "arguments": {"efoId": "EFO_0000305"}
}
```

The identifier should first have been established by a preceding lookup or supplied context. The backend can then insert it into the correct query. A returned target association score is evidence about an association in that resource; it is not automatically a probability of therapeutic benefit.

### 3.2 Providers and mapping rules

| Provider in v1 | Biomedical tools | Information role | How the backend maps calls |
| --- | ---: | --- | --- |
| openFDA | 156 | Drug labeling: indications, contraindications, dosage, warnings, population-specific information, and other fields | Connect input arguments to search fields and select return fields using the API's Elasticsearch-style interface |
| Open Targets | 52 | Disease–target, drug–target, and related biomedical associations | Insert arguments into GraphQL query variables and retrieve the specified fields |
| Monarch Initiative | 3 | Phenotypes and disease–phenotype connections, including HPO identifiers | Map arguments to the REST API request |
| **Total** | **211** | Biomedical tools | Standardized model-facing interfaces over different providers |

**ToolRAG and Finish are specialized tools in addition to these 211 biomedical tools.** PrimeKG supplies information for question generation; it is not a fourth provider in the 156 + 52 + 3 breakdown. [Figure 1 and Methods §2, pp. 45–47.](https://arxiv.org/pdf/2503.10970v1#page=45)

The paper's data-source description also reports the following historical resource sizes: more than 67,000 drug entries in the openFDA labeling source; 63,121 targets, 28,327 diseases, 18,041 drugs, 17,853,184 evidence entries, and 8,155,988 target–disease associations in the September 2024 Open Targets release; more than 18,000 HPO terms and 156,000 hereditary-disease annotations; and 17,080 diseases with 4,050,249 relationships in PrimeKG. These are source-resource statistics, **not the number of unique entities used for TxAgent training**, and drug entries should not be read as a deduplicated count of molecular drugs. [Methods §3.1, p. 48.](https://arxiv.org/pdf/2503.10970v1#page=48)

### 3.3 Coverage and directionality

The listed categories are adverse events, risks and safety; addiction and abuse; drug use in patient populations; administration and handling; pharmacology; drug use, mechanisms and composition; IDs and labeling; general clinical annotations; laboratory information; patient and caregiver information; disease–phenotype–target–drug links; biological annotations; publications; search; and target characterization.

Many tools expose opposite directions of the same information relationship. For example, “retrieve pediatric-use information for this drug” and “retrieve drugs matching this pediatric-use description” are different functions. The first starts with an entity and asks for a field. The second searches entities by field content. Choosing the wrong direction can yield an empty result even when the database contains the necessary evidence.

<figure>
  <a href="{{ '/assets/healthcare-ai/txagent/extended-data-3-tool-categories.png' | relative_url }}"><img src="{{ '/assets/healthcare-ai/txagent/extended-data-3-tool-categories.png' | relative_url }}" alt="Extended Data Figure 3: radial taxonomy of 211 ToolUniverse biomedical tools, grouped into drug safety, populations, pharmacology, biological associations, and other categories." width="826" height="892" loading="lazy"></a>
  <figcaption>Extended Data Figure 3 from Gao et al. (2025). Read outward from broad categories to specific capabilities and individual tools. This is a taxonomy of tool coverage, not the directed Tool Graph used to generate training questions. Click to enlarge.</figcaption>
</figure>

## 4. Inference: the complete action-and-feedback loop
{: #inference }

### 4.1 State and notation

To make the paper's notation easier to follow, use $$R_i$$ for a single step and $$\mathcal{R}_{<i}$$ for the ordered history before that step:

$$
R_i=(T_i,C_i,E_i),\qquad
\mathcal{R}_{<i}=(R_1,\ldots,R_{i-1}).
$$

| Symbol | Meaning |
| --- | --- |
| $$Q$$ | User's natural-language therapeutic question |
| $$T_i$$ | Generated intermediate text at step $$i$$ |
| $$C_i$$ | One or more structured function calls at that step |
| $$E_i$$ | Responses returned by those calls |
| $$P_i$$ | Tool schemas currently available to the language model |
| $$\mathcal B$$ | Full biomedical tool collection |
| $$A$$ | Final answer and rationale |
| $$F_{\mathrm{Tx}}$$ | Fine-tuned language model under the TxAgent system prompt |

The history is an ordered sequence. Writing a mathematical union, as parts of the original paper do, should not imply that message order is irrelevant.

### 4.2 Generate an intermediate rationale, then calls

The model first produces text conditioned on the question, previous observations, and visible tool schemas:

$$
T_i=F_{\mathrm{Tx}}(Q,\mathcal R_{<i},P_i).
$$

It then generates calls conditioned on that text as well:

$$
C_i=F_{\mathrm{Tx}}(Q,\mathcal R_{<i},T_i,P_i).
$$

These equations describe two parts of the model's autoregressive output, not two separately trained reasoning and action networks. A call contains a tool name and argument/value pairs. The external executor performs the operation and returns its response. The response becomes part of the history used for the next decision. [Methods §1.2, Eqs. 1–4, pp. 40–42.](https://arxiv.org/pdf/2503.10970v1#page=40)

### 4.3 Tool discovery changes the available action set

The model sees only the tools in $$P_i$$, rather than every full schema in $$\mathcal B$$ at every step. If the required capability is absent, it calls ToolRAG with a natural-language requirement. The retrieved schemas expand the available set:

$$
P_{i+1}=P_i\cup\operatorname{RetrieveTools}(q_i,\mathcal B),
$$

where $$q_i$$ is the model-generated description of what the next tool should do. This equation is an explanatory restatement of the update. The agent then inspects the candidate descriptions and chooses the relevant tool. Retrieving a tool does not execute it, and a retrieved candidate need not be selected.

This two-stage decision is central: **ToolRAG narrows the candidate capabilities; the language model selects and parameterizes an action in the current problem context.**

### 4.4 Parallel calls and sequential dependencies

A step can contain multiple function calls. Independent evidence requests, such as a known drug's indication and contraindications, can run in parallel. A dependent request must wait: if the next tool requires an EFO ID that has not yet been retrieved, it cannot reliably run alongside the lookup that produces that ID.

Thus the number of reasoning steps and the number of function calls measure different things. One step may produce several calls; a tool-discovery round also consumes interaction effort. A long textual rationale without an external observation is different from a sequence that acquires new evidence.

### 4.5 Feedback, unsuccessful calls, and stopping

An empty response is fed back to the model. It can revise the query, choose a different tool, or retrieve a new capability. The DMD example later in these notes demonstrates changing the direction of the lookup after an unhelpful call. This behavior is learned from trajectories; the Methods do not specify a complete deterministic retry policy for every possible API error.

The paper uses the marker `[FinalAnswer]` in the generated text to indicate that the model is ready to finish. The model produces the answer and calls **Finish**, ending the loop. This is a model-controlled stopping decision, not an independent theorem checker or clinical-safety validator.

The following pseudocode expresses the intended workflow. It is explanatory, not a runnable copy of Algorithm 1:

```text
history = []
available_tools = initial_specialized_tools

repeat:
    generate intermediate text from question, history, available_tools

    if model signals final answer:
        produce answer and rationale
        call Finish
        return answer, history

    generate structured calls using currently available tool schemas

    if the next action is tool discovery:
        run ToolRAG on the requested capability
        make retrieved schemas available for subsequent actions
    else:
        execute selected biomedical tools

    incorporate the action and its feedback into subsequent context
```

The pseudocode abstracts over message serialization and mixed batches of tool calls. The v1 Algorithms are high-level sketches; they do not fully specify dispatch, malformed-call recovery, timeout handling, or retrieval-result logging.

### 4.6 Summarizing long tool results

Long label passages and database responses can consume the context window. The paper uses the same backend language model under a summarization prompt:

$$
\widehat E_i=F_S(T_i,C_i,E_i).
$$

The summary is conditioned on the intermediate text and the call, so it can focus on information relevant to that step. In training-data preprocessing, oversized samples are shortened by replacing earlier tool responses with summaries, beginning with the earliest step and continuing until the sample fits. [Methods §1.2 and §4.2, pp. 42–43 and 57.](https://arxiv.org/pdf/2503.10970v1#page=57)

This is a compression mechanism. It does not add new evidence. A key failure mode is losing a qualifier, such as an age threshold, formulation, or condition attached to a warning. The paper does not report a separate quantitative test of summary fidelity or an exact context-length threshold.

## 5. ToolRAG: retrieving tools and training the retriever
{: #toolrag }

### 5.1 What is embedded?

ToolRAG embeds **tool descriptions** and the requested capability. Let $$d_j$$ be the description of tool $$j$$, and let $$f_\phi$$ be the embedding model. A conceptual retrieval rule is:

$$
z_j=f_\phi(d_j),\quad z_q=f_\phi(q),\quad
\mathcal K(q)=\operatorname{TopK}_{j}\;s(z_q,z_j).
$$

The returned items are the descriptions/schemas of tools indexed by $$\mathcal K(q)$$. The paper says that the top-$$k$$ tools with the highest embedding similarity are retrieved, but does not give the numerical $$k$$ or a precise similarity function. Accordingly, $$s$$ is left unspecified here.

For example, a request for “tools to retrieve contraindications for a known drug” should bring relevant field-lookup tools into context. The language model must still choose between similar candidates and provide the actual drug name or identifier.

### 5.2 Contrastive training objective

The retriever is initialized from **gte-Qwen2-1.5B-instruct** and fine-tuned on pairs of tool requirements and corresponding tool descriptions using **multiple negatives ranking loss**. [Methods §3.4, pp. 54–55.](https://arxiv.org/pdf/2503.10970v1#page=54)

The following standard formulation explains the named loss; it is **not an equation or complete hyperparameter specification reported in the paper**. For a batch of matched pairs $$(q_a,d_a)$$, other descriptions in the batch can act as negatives:

$$
\mathcal L_{\mathrm{retrieval}}
=-\frac{1}{N}\sum_{a=1}^{N}
\log\frac{\exp\{s(f_\phi(q_a),f_\phi(d_a))/\tau\}}
{\sum_{b=1}^{N}\exp\{s(f_\phi(q_a),f_\phi(d_b))/\tau\}}.
$$

Here $$N$$ is the batch size and $$\tau$$ is a temperature in this illustrative formulation. Training raises the matched description's relative similarity to the requirement. Multiple tools may satisfy similar requirements, so the way negatives are formed can matter; v1 does not supply that detail or the temperature.

### 5.3 How the initial training pairs are obtained

There is a circular dependency: a useful retriever needs trajectory-derived requirement–tool pairs, while generating realistic trajectories benefits from a useful retriever. The authors bootstrap it:

1. Infer an initial set of tools from the reference material used to create a question.
2. Generate initial trajectories using those tools before a trained ToolRAG is available.
3. Extract requirement–description pairs from the generated retrieval actions.
4. Train ToolRAG on these pairs.
5. Use the trained retriever to obtain additional tools during subsequent trajectory generation.
6. Collect more pairs and repeat retriever training and data generation.

This iterative process trains the **retriever** and improves synthetic data collection. It should not be described as reinforcement learning of TxAgent or as updating the retriever after every deployed user request. The paper does not report the iteration count or a round-by-round dataset-size breakdown.

### 5.4 Relationship to passage retrieval

The biomedical evidence comes from executing API tools. The vector index used by ToolRAG contains tool descriptions. This distinction explains how the system can query changed database content without re-embedding every drug-label passage into its own biomedical text index.

It still depends on database freshness, tool availability, and correctly maintained tool descriptions. The paper's comparison with static passage retrieval does not demonstrate that all possible RAG systems are unable to update their sources or perform multiple retrieval steps.

## 6. ToolGen: turning API documentation into usable tools
{: #toolgen }

ToolGen constructs the tool collection using three GPT-4o agents with specialized prompts, followed by human review. A shared model can serve several named roles through different instructions; these roles do not imply separately trained models. [Methods §2.2 and prompt sketches §7.2, pp. 46–47 and 64–65.](https://arxiv.org/pdf/2503.10970v1#page=46)

### 6.1 Summarizer: enumerate capabilities

The Summarizer reads a provider's API documentation and produces a list of concrete capabilities, such as finding active ingredients for a drug or retrieving disease-related phenotypes. The aim is to convert a large API schema into a useful list of operations that can later receive individual model-facing descriptions.

### 6.2 Tool Generator: construct specifications and mappings

For each capability, the Tool Generator produces the tool name, description, argument definitions, and the mapping needed to construct a valid API request. For openFDA, it connects input arguments to search fields and chooses return fields. For Open Targets and Monarch, it connects arguments to variables or fields in the provider's query interface.

The openFDA prompt specifically asks for both lookup directions: find drug names from information in a field, and retrieve field information from a drug name. The generator is also instructed to make new functions distinct from existing examples. A generated schema alone is insufficient; its fields must agree with the executable mapping.

### 6.3 Tool Checker: exercise the mapping against data

The validation procedure has several stages:

1. Check whether the mapping itself is valid.
2. Randomly sample relevant real entity names or IDs, such as drugs, diseases, or targets.
3. Test whether the API can retrieve useful information for these inputs.
4. Supply the information and tool specification to the Tool Checker, which creates natural-language test questions and corresponding calls.
5. Execute those calls and check whether they produce valid outputs.

A tool is removed if any stage fails. This evaluates more than JSON syntax, because it exercises the link between the advertised function and a real API response. It remains a finite set of checks, and the paper does not report per-tool test counts or exhaustive coverage of exceptional inputs.

### 6.4 Human verification

Human experts assess whether each generated tool has a meaningful application, behaves according to its description, and remains stable with unexpected inputs. They refine the tools before inclusion in ToolUniverse. The paper does not quantify reviewer agreement, rejection rates, or the number of experts per tool.

### 6.5 The separate Tool Graph

The Tool Graph is a directed graph with tools as nodes. An edge from tool $$u$$ to tool $$v$$ means that an output of $$u$$ can serve as an input of $$v$$. An LLM receives pairs of tool descriptions and decides whether the connection should exist.

For example, a name-to-disease-ID tool can precede a disease-ID-to-targets tool. Sampling such chains encourages generation of questions that require connected actions rather than isolated lookups.

**The graph is explicitly restricted to training-data construction.** Runtime tool selection is not a graph traversal. The authors avoid that constraint because graph construction is imperfect and a fixed graph would make new tool integration less flexible. [Methods §2.3, p. 47.](https://arxiv.org/pdf/2503.10970v1#page=47)

## 7. QuestionGen: constructing questions and reference answers
{: #questiongen }

QuestionGen turns biomedical reference material into a question $$Q$$, a reference answer $$G$$, and an explanation $$X$$. Multiple-choice instances also include options. The explanation is retained because it will guide the Helper in the next stage. The system uses GPT-4o with question-type-specific prompts. [Methods §3.1–3.2, pp. 47–50; prompt sketches, pp. 66–69.](https://arxiv.org/pdf/2503.10970v1#page=48)

### 7.1 Drug-centered questions

First, sample a drug from the FDA source and retrieve its label. Randomly choose a label field as the reference for question construction. Possible topics include an indication, population-specific use, dosage, warnings, and drug interactions.

The process also extracts descriptors such as mechanism of action, indications, and contraindications. These allow questions to refer to a drug through its properties rather than always naming it. The question, answer, and explanation must be supported by the supplied field information. The prompt requests varied formulations and discourages overlapping questions.

### 7.2 Disease-centered questions

This branch creates questions about treatment selection under patient constraints:

1. Sample a disease and gather its description, phenotypes, targets, and potential drugs.
2. Retrieve FDA documents for the candidate drugs.
3. Extract indications, population restrictions, contraindications, warnings, and interactions.
4. Organize the information by field.
5. Ask the Information Extractor to compare the drugs and identify differences supported by the reference material.
6. Ask the Question Generator to create a patient profile and question for which these differences make one option the intended answer.

Suppose two drugs share an indication, but their label restrictions differ for a specified patient characteristic. That difference can become a condition in the synthetic patient profile. The resulting question trains comparison and filtering rather than only recall of the indication.

The construction direction matters: **drug differences help determine the patient scenario**. These are generated vignettes, not a cohort of observed patients sampled from clinical records. They may be useful for testing whether a model applies an explicit restriction, but their distribution need not match clinical ambiguity or case frequency.

### 7.3 Tool-chain-centered questions

Sample a chain from the Tool Graph, often starting with an entity-resolution tool that converts a drug or disease name into an identifier. Gather information accessible through the chain, then give the relevant outputs and tool descriptions to the Question Generator.

The goal is to create questions requiring several connected capabilities, including dependencies between intermediate results. The prompt also uses relevant PrimeKG information and avoids placing obscure ontology IDs directly into the question. That prevents the question from giving away an internal identifier that the agent should learn to retrieve.

### 7.4 Three filters before trajectory generation

GPT-4o evaluates each generated question on:

| Check | Reference used | Failure it targets |
| --- | --- | --- |
| Knowledge grounding | Question and underlying reference material | Invented facts introduced during question generation |
| Answerability | Question and supplied evidence | Questions that cannot be solved from the intended source |
| Reasonableness | Generated explanation | Illogical or incoherent justification |

Any failed check discards the question. Passing these checks means that it satisfied the specified model-based screening process. It does not establish independent expert agreement on every training question. Human review is explicitly described for benchmark construction, discussed below.

## 8. TraceGen: generating supervised trajectories with a Helper
{: #tracegen }

Question–answer pairs do not by themselves teach the agent which tool to call next, how to respond to empty results, or when to search for another capability. TraceGen creates the missing sequence of actions and observations. Its three components are a **Helper**, a **Tool Provider**, and a **Solver**. Helper and Solver are implemented by prompting GPT-4o. [Methods §3.3, pp. 50–54.](https://arxiv.org/pdf/2503.10970v1#page=50)

### 8.1 Helper: guidance with access to the reference answer

The Helper sees $$Q$$, $$G$$, $$X$$, the previous trajectory, and a candidate answer if one exists. It produces a hint for the next step:

$$
H_{i+1}=\operatorname{Helper}(Q,G,X,\mathcal R_{\le i},A).
$$

Its prompt requests one-step guidance and instructs it not to reveal the final answer or directly answer-determining information. If the Solver's candidate answer disagrees with the reference, the Helper asks it to reflect and continue.

This is **answer-guided trajectory generation**. Even when the hint does not state the answer, access to $$G$$ and $$X$$ makes the teacher's task easier than the deployed agent's task. The final student training format does not include the Helper hint or a separate reference-answer field as input; the student learns from the resulting screened trajectories.

### 8.2 Tool Provider: privileged initial tools plus retrieval

The Tool Provider first infers an initial set $$\widehat P_0$$ from the reference information associated with the question. This gives the Solver access to tools likely to retrieve the required evidence.

Later, if the Solver needs a capability beyond that initial set, the Tool Provider uses ToolRAG to suggest additional tools. This is also where the iterative retriever training described in §5 becomes useful.

The initial set is a data-generation aid. At deployment, the user does not provide the reference material that was used to synthesize a training question.

### 8.3 Solver: intermediate text, calls, and real feedback

At each step, the Solver uses the question, history, available tools, and Helper hint to produce intermediate text and one or more calls. Real tool execution supplies the observations. The Solver then continues from the expanded history.

The prompt tells it to base answers on tool feedback, try another approach when earlier attempts fail, and avoid repeating unsuccessful thoughts and calls. When it believes the task is solved, it proposes a final answer. The Helper checks it against the reference. If it is incorrect, the final step is removed and generation continues. V1 uses both “END” and “Finish” in descriptions of this termination action.

### 8.4 Why virtual ToolRAG calls are inserted

If the Solver simply used all reference-derived tools immediately, the generated trajectories would omit the discovery behavior needed at deployment. To reduce that mismatch, the Solver first emits a **virtual ToolRAG call** before using a required tool from $$\widehat P_0$$. The virtual call names the tool and includes a rewritten description of its capability. These calls are later replaced with actual ToolRAG call arguments.

If the desired tool is outside the initial set, actual ToolRAG retrieval supplies candidates. This process both inserts tool-discovery actions into the demonstrations and produces requirement–description pairs for retriever training.

It should not be read as evidence that every early synthetic retrieval was a successful independent retrieval by the finished ToolRAG model. The initial demonstrations benefit from reference-derived tool choices; the later iterative stages move toward retrieval-driven selection.

### 8.5 Trajectory screening

TraceGen screens both correctness and behavior:

| Dimension | What is checked |
| --- | --- |
| Answer correctness | Compare the selected option with the reference for multiple-choice data; use GPT-4 to judge alignment for open-ended answers |
| Trajectory correctness | Use GPT-4 with the question and reference answer to assess the generated reasoning |
| Call correctness | Correct tool, argument names, argument types, and required arguments |
| Identifier grounding | Reject hallucinated entity names/IDs and IDs that appear without preceding contextual support |
| Evidence grounding | Reject answers derived from unsupported model knowledge instead of retrieved tool feedback |
| Repetition | Detect similar repeated thoughts and identical calls with identical arguments |

The Methods explicitly names **GPT-4** for trace judging, while generation and question checking name **GPT-4o**. The distinction is retained here. Failed trajectories are discarded. Thresholds for thought similarity, acceptance rates, and maximum correction attempts are not reported.

This pipeline supplies supervised examples of desired behavior. There is no reported reward optimization, policy-gradient step, or reinforcement-learning stage in the TxAgent language-model training procedure.

## 9. TxAgent-Instruct and language-model training
{: #training }

### 9.1 Dataset units and temporal exclusion

| Reported item | Count | Meaning |
| --- | ---: | --- |
| Biomedical tools | 211 | Base tool collection whose descriptions are augmented |
| Therapeutic questions | 85,340 | Questions and functional instructions |
| Reasoning trajectories | 85,340 | Demonstrations associated with those questions |
| Reasoning steps | 177,626 | Reported total intermediate steps |
| Function calls | 281,695 | Calls can outnumber steps because a step can contain several calls |
| Instruction-tuning samples | 378,027 | Final training examples after processing the component datasets |

The authors remove drugs approved **after 2023** from the training data; evaluation centers on drugs approved in **2024**. This separates the intended drug-approval periods. It does not imply that every sentence in an older drug's label was frozen before 2024, or that all biomedical information about a later-approved drug was absent from every model's pretraining. [Methods §4.1, pp. 55–56.](https://arxiv.org/pdf/2503.10970v1#page=55)

One accounting detail remains unresolved: the described decomposition makes one sample per trajectory step, yet the reported 177,626 steps and 378,027 samples do not directly match. The paper mentions augmentation and integration of component datasets but does not give a complete numerical reconciliation. These counts should be quoted as reported, not used to infer an exact number of unique examples per step.

### 9.2 Stepwise supervision: predict the next action from its history

For a trajectory with $$M$$ steps, each nonfinal training example contains:

$$
\text{Input}_i=[S,Q,\mathcal R_{<i},P_i],\qquad
\text{Target}_i=[T_i,C_i],\qquad i<M,
$$

where $$S$$ is the system prompt. The final example predicts the completion text, Finish call, and answer:

$$
\text{Input}_M=[S,Q,\mathcal R_{<M},P_M],\qquad
\text{Target}_M=[T_M,C_M,A].
$$

The earlier observations are in the **input**, while the next thought and action are the **target**. This trains a policy over interaction histories rather than a mapping from the original question directly to the final answer. The final answer appears as a target at completion, not as a reference-answer field available to every student input. [Methods §4.1, Eq. 7.](https://arxiv.org/pdf/2503.10970v1#page=56)

### 9.3 Matching parallel calls with responses

Each call and its corresponding response receive the same randomly generated identifier. The identifier associates results with the right call when a step contains multiple calls. Historical call/response pairs include this ID, but the random ID is removed from model output targets because it is unpredictable.

This is distinct from a biomedical identifier such as an EFO ID. A call ID is bookkeeping generated by the interaction system; an ontology ID identifies an entity and must be obtained from valid context or evidence.

### 9.4 Augmentation and the failure mode each strategy targets

| Strategy | Procedure | Intended effect |
| --- | --- | --- |
| Rewrite tool fields | Generate 20 alternatives for tool names, function descriptions, argument names, and argument descriptions; sample rewritten fields | Reduce dependence on memorized names and wording |
| Keep calls consistent with rewritten schemas | Replace tool and argument names in the corresponding calls | Teach schema-conditioned argument generation rather than mismatched names |
| Include unused retrieved candidates | Add all tools returned by ToolRAG, including those not used in the demonstration | Expose the model to imperfect retrieval |
| Add distractor tools | Randomly sample extra tools into the candidate set | Train selection among competing capabilities |
| Shuffle tool order | Randomize the tool list | Reduce positional shortcuts |
| Compress long histories | Replace earlier full tool results with summaries until the example fits | Preserve more steps within the context window |

The 20 rewrites do not mean there are 20 independent biomedical backends per tool. The executable capability is represented under alternative interface wording. Consistency between the rewritten schema and the target call is essential; otherwise augmentation would produce incorrect training examples. The paper does not specify how many distractors are added to each example or every field-sampling detail. [Methods §4.2, pp. 56–57.](https://arxiv.org/pdf/2503.10970v1#page=56)

### 9.5 Language model, LoRA, and the loss mask

The main model starts from **Llama-3.1-8B-Instruct** and is adapted with **Low-Rank Adaptation (LoRA)**. For intuition, a standard LoRA update can be written as $$W'=W+\Delta W$$, with $$\Delta W=BA$$ and a low inner rank. This explains the type of adaptation; v1 does not provide its rank, scaling, target modules, or dropout.

Inputs and targets are serialized using the model's instruction/chat format and tokenized. The paper's training loss is:

$$
\mathcal L_{\mathrm{Tx}}
=-\sum_{t\in I_{\mathrm{out}}}
\log p_\theta(x_t\mid x_{<t}),
$$

where $$I_{\mathrm{out}}$$ indexes tokens belonging to the target output. Earlier question text, schemas, and tool responses condition prediction but are not themselves supervised targets in that example.

For an input containing a long label response, the model therefore learns which next rationale and action follow from that response. It is not trained by this loss to reproduce the external tool's entire returned label. This design encourages action generation from observations, although masking alone cannot guarantee that the model never memorizes facts. [Methods §4.3, Eq. 8, pp. 57–58.](https://arxiv.org/pdf/2503.10970v1#page=58)

The ToolRAG contrastive objective and TxAgent's autoregressive objective train different components. They should not be combined into a claimed joint end-to-end objective: the paper describes iterative retriever training and subsequent supervised language-model adaptation, not a single differentiable loss through all API calls.

### 9.6 Compute and implementation information

Training TxAgent-8B uses **four NVIDIA H100 GPUs**, **320 GB aggregate GPU memory**, and **9.93 GPU-days**. GPU-days aggregate accelerator time; they are not the same as 9.93 elapsed calendar days. The paper lists TRL, Alignment Handbook, Transformers, DeepSpeed, and PyTorch, with parameter sharding for distributed training.

The authors describe PyTorch FSDP for multiple nodes and a single-node DeepSpeed Stage 3 arrangement. Their wording equates the latter with an FSDP implementation; these should be understood as related sharding approaches rather than identical software implementations. The v1 methods are insufficient to reproduce the exact training run without additional configuration files. The missing settings are listed in §16.

## 10. Worked examples: what each action contributes
{: #examples }

These examples explain the workflows illustrated in the March 2025 paper. They are historical case illustrations rather than updated prescribing instructions. The important objects are the information dependencies and decision points. [Figure 1 and Figure 4; main text pp. 5–6 and 15–17.](https://arxiv.org/pdf/2503.10970v1#page=15)

### 10.1 Disease name → identifier → associated targets

The breast-cancer example illustrates a dependency between calls:

| Stage | Information available | Action | What becomes available next |
| --- | --- | --- | --- |
| Resolve the disease | Natural-language disease name | Retrieve its disease identifier and description | The returned EFO ID, shown as `EFO_0000305` in Figure 1 |
| Discover an association tool | A disease identifier and a need for targets | Ask ToolRAG for disease-to-target capabilities | Schemas of candidate association tools |
| Retrieve associations | Identifier and a compatible tool schema | Call the disease-to-target tool | Target IDs, names, and scores |
| Construct the answer | Retrieved target records | Select and describe relevant returned associations | An answer whose named entities can be checked against tool output |

The learning problem includes knowing to resolve an entity before invoking an ID-based tool. The Tool Graph can encourage such chains during data generation, but runtime selection is still made from the context. The returned associations are not evidence that the system has experimentally validated those targets for treatment.

### 10.2 Candidate treatment → failed lookup → corrected lookup direction

The DMD example begins with a pediatric patient whose stated constraints exclude steroid and exon-skipping treatments. TxAgent retrieves candidate drugs by indication, identifies a candidate that meets the stated mechanism constraints, and then seeks pediatric-use information.

One attempted tool searches **drug names by pediatric-use information** and returns no useful result for the query. The agent then retrieves a tool that returns **pediatric-use information by drug name** and uses it to verify the remaining condition. The figure's final candidate is Duvyzat.

The transferable behavior is not merely “retry a call.” It is recognizing that the chosen interface has the wrong input–output direction, finding a different schema, and applying it. Empty output does not necessarily mean that no suitable drug or supporting information exists.

### 10.3 A known drug → two parallel evidence requests

In the Cobenfy geriatric-use example, the question asks both for a dosage limit and its explanation. The agent retrieves dosage information and geriatric-use information in parallel because the drug is already identified and neither lookup depends on the other's output. It combines the returned limit with the population-specific explanation.

This separates **what the label recommends** from **why the retrieved label gives a different recommendation for this population**. Correct synthesis requires preserving population qualifiers and units, not simply returning a numeric string from the first tool.

### 10.4 Drug interactions and comorbidity filtering

The Xolremdi/Prozac example combines indication and contraindication retrieval for one drug with interaction-related information about the concurrent medication. The methodological task is to connect a retrieved restriction to properties of another drug. The paper's descriptions of the CYP2D6 mechanism are not fully consistent between the case narrative and Discussion, so these notes do not adopt that narrative as a current clinical rule.

The hypertension/AV-block example first generates a candidate list by indication, then searches contraindications to exclude candidates matching the comorbidity. It illustrates **candidate generation followed by constraint checking**. However, “not returned by this contraindication search” does not establish comprehensive safety or superiority over all alternatives. Search completeness, spelling, synonyms, label scope, and additional patient variables remain relevant.

## 11. Benchmark construction and scoring
{: #evaluation }

### 11.1 Five benchmark names represent related tests

| Benchmark | Questions | Construction | Primary capability tested |
| --- | ---: | --- | --- |
| DrugPC | 3,168 | QuestionGen builds questions from selected FDA-label fields, focusing on 2024 approvals | Drug-related question answering across 11 categories |
| BrandPC | 3,168 | Transform drug references in DrugPC to brand names | Robustness to naming variation |
| GenericPC | 3,168 | Transform drug references in DrugPC to generic names | Robustness to naming variation |
| DescriptionPC | 626 | Replace names with descriptions; manually remove cases no longer answerable | Entity identification from properties plus question answering |
| TreatmentPC | 456 | Construct patient scenarios from differences among treatment options | Applying patient-specific restrictions and comparing therapies |

BrandPC and GenericPC are transformations of DrugPC, not independent samples of an unrelated clinical problem distribution. DescriptionPC is a filtered derivative. Adding all rows would overstate the number of independent underlying cases. [Table 1 and Methods §5.1, pp. 36 and 59–61.](https://arxiv.org/pdf/2503.10970v1#page=59)

For BrandPC/GenericPC, Methods §5.1 says questions without relevant drug names remain unchanged and questions specifically asking for brand–generic conversion are also kept unchanged. The main text uses different wording for conversion questions; the Methods description is used here, with that discrepancy recorded in §16.

### 11.2 DrugPC categories and source fields

| Category | Questions | Examples of FDA-label fields used |
| --- | ---: | --- |
| Drug overview | 242 | Description; principal display panel |
| Ingredients | 83 | Product data elements |
| Warnings and safety | 515 | Boxed warning; contraindications; adverse reactions; drug interactions |
| Dependence and abuse | 53 | Abuse; controlled substance; overdosage |
| Dosage and administration | 507 | Indications and usage; dosage and administration; dosage forms; instructions |
| Use in specific populations | 333 | Pregnancy; pediatric use; geriatric use; nursing mothers |
| Pharmacology | 565 | Mechanism; pharmacodynamics; pharmacokinetics |
| Clinical information | 146 | Clinical studies |
| Nonclinical toxicology | 172 | Nonclinical toxicology; carcinogenesis, mutagenesis, fertility; animal toxicology |
| Patient-focused information | 349 | Patient information; medication guides and package inserts |
| Storage and supply | 203 | How supplied; storage and handling |
| **Total** | **3,168** | |

QuestionGen creates questions, options, and reference answers from the relevant fields, and checks answerability and correctness against that context. Humans review and refine the benchmark, including removing non-biomedical questions such as manufacturer information. Methods §5.1 says most questions have four options, with some having two or five; the main text's “4–5” statement is not exhaustive.

### 11.3 TreatmentPC construction

TreatmentPC starts from drugs approved in 2024 and their indications, then gathers other treatments for the same diseases. Label information is compared across candidate drugs. Patient-specific details are chosen so that one option is the intended suitable answer, including scenarios involving pregnancy, comorbidities, and concurrent medication restrictions.

The 2024 criterion therefore anchors construction of the benchmark; it should not be read as saying every comparator drug appearing in a vignette was first approved in 2024. The benchmark measures performance on deliberately constructed distinctions among treatments. It does not report treatment outcomes in 456 prospectively observed patients.

### 11.4 Multiple-choice accuracy

For question $$n$$, the model receives the options and chooses one. With reference label $$y_n$$ and selected label $$\widehat y_n$$:

$$
\operatorname{Accuracy}_{\mathrm{MC}}
=\frac{1}{N}\sum_{n=1}^{N}\mathbf 1[\widehat y_n=y_n].
$$

This metric evaluates the selected option. It does not separately grade every sentence in the intermediate text.

### 11.5 “Open-ended accuracy” is a two-stage protocol

The paper first removes the choices and asks the model to generate a free response. It then supplies that generated response as context and asks the model to choose among the original answer options. Accuracy is computed from this second-stage selection. [Methods §5.2, p. 61.](https://arxiv.org/pdf/2503.10970v1#page=61)

An explanatory notation is:

$$
a_n=\operatorname{Generate}(Q_n),\qquad
\widetilde y_n=\operatorname{MapToOption}(a_n,\mathcal O_n),
$$

$$
\operatorname{Accuracy}_{\mathrm{open}}
=\frac{1}{N}\sum_{n=1}^{N}\mathbf 1[\widetilde y_n=y_n].
$$

The first stage removes the answer-choice cue from answer generation, which makes it meaningfully different from ordinary MC evaluation. However, the final metric still depends on an option-mapping task. It can miss incorrect extra claims in a free response, and mapping can itself introduce errors or cues. It is **not the fraction of complete free-form treatment plans judged clinically correct by independent clinicians**.

This benchmark scoring should also be distinguished from the GPT-4 judge used to filter open-ended **training trajectories**. They are different procedures at different stages.

### 11.6 DescriptionPC requires correct entity grounding

Drug names are replaced with indications, mechanisms, contraindications, or interactions. Because several drugs can match a description, the authors include compatible alternatives in the accepted reference identities. The model first identifies the drug and then answers the question using that identity.

The strict two-step metric requires both components to be correct:

$$
\operatorname{Accuracy}_{\mathrm{joint}}
=\frac{1}{N}\sum_{n=1}^{N}
\mathbf 1[\widehat d_n\in D_n^{\mathrm{valid}}]
\mathbf 1[\widehat y_n=y_n].
$$

An incorrect identity makes the final result incorrect even if the option happens to be right. This exposes a failure hidden by answer-only scoring: a model can infer a plausible answer from descriptive cues without correctly grounding the drug.

### 11.7 What the temporal split controls

Excluding post-2023 approvals from supervised training and focusing evaluation on 2024 approvals reduces one obvious overlap route. It supports testing whether external tools can supply knowledge about later approvals.

It does not independently establish complete absence of contamination. Drugs may have preapproval publications, older names, related compounds, or updated labels. Model training cutoffs and synthetic teacher knowledge differ. The paper does not provide a full provenance-level overlap audit, a detailed label-snapshot policy, or a reproducible list of every exclusion decision.

## 12. Baseline models and comparison conditions
{: #baselines }

The comparisons involve several kinds of systems:

| Baseline family | Models | Evaluation arrangement described in the paper |
| --- | --- | --- |
| General LLMs | GPT-4o; Llama-3.1-8B-Instruct; Llama-3.1-70B-Instruct | Answer using internal model knowledge; shown without ToolUniverse access |
| Tool-use LLMs | ToolACE-8B; WattTool-8B | Access to ToolUniverse; adapted to repeated tool interactions and final-answer emission |
| Reasoning LLMs | DeepSeek-R1; distilled Llama-8B and Llama-70B versions | TreatmentPC comparisons using prompted reasoning, without the external tool access of TxAgent |
| TxAgent | Adapted Llama-3.1-8B-Instruct plus ToolRAG and ToolUniverse | Domain-trained multi-step tool use and retrieved biomedical evidence |

For the tool-use baselines, tool outputs are fed back as user messages to permit additional rounds. A **GiveAnswer** tool provides a structured way to emit the final answer. Both tool-use baselines start from the same Llama-3.1-8B-Instruct family as TxAgent. [Main text pp. 11–12 and 14–15.](https://arxiv.org/pdf/2503.10970v1#page=11)

The tool-use comparison is stronger than comparing only against models without tools, but it still combines domain-specific training, schema selection, context handling, stopping behavior, and wrapper compatibility. Poor baseline completion rates can reflect orchestration failures as well as biomedical reasoning failures. On DrugPC, invalid-answer rates are 58.9%/56.6% for WattTool and 63.1%/60.7% for ToolACE in MC/open-ended settings.

Comparisons with larger general or reasoning models demonstrate the effectiveness of the full configured system under these conditions. They do not isolate the causal effect of language-model parameter count or prove that an 8B model has superior intrinsic clinical reasoning when evidence access is held equal.

## 13. Results, with the correct interpretation of each metric
{: #results }

All entries below are accuracy percentages reported in v1. “Open-ended” retains the two-stage meaning in §11.5. Differences between percentages are expressed as **percentage points (pp)**.

### 13.1 DrugPC

| Model | Multiple choice | Open-ended |
| --- | ---: | ---: |
| Llama-3.1-8B-Instruct | 65.4 | 45.6 |
| Llama-3.1-70B-Instruct | 75.1 | 52.8 |
| GPT-4o | 76.4 | 66.3 |
| ToolACE-8B | 31.3 | 32.7 |
| WattTool-8B | 34.7 | 37.1 |
| **TxAgent-8B** | **93.8** | **92.1** |

TxAgent exceeds GPT-4o by 17.4 pp in MC and 25.8 pp in open-ended scoring. Its score decreases by only 1.7 pp when choices are removed from the first stage. Figure 2 also reports stronger performance across all 11 DrugPC categories. These results support effective source-backed drug question answering under the reported protocol. [Figures 1–2, pp. 23–26.](https://arxiv.org/pdf/2503.10970v1#page=23)

### 13.2 Brand names, generic names, and descriptions

The name-variant table reports multiple-choice accuracy.

| Model | DrugPC | BrandPC | GenericPC |
| --- | ---: | ---: | ---: |
| GPT-4o | 76.4 | 70.2 | 77.3 |
| Llama-3.1-70B-Instruct | 75.1 | 73.0 | 76.8 |
| TxAgent-8B | 93.8 | 93.6 | 93.7 |

The paper reports a variance of **0.00667** across TxAgent's DrugPC/BrandPC/GenericPC accuracy values. This describes small variation in aggregate scores across three naming conditions. It does not measure individual-case agreement or uncertainty over repeated runs. When accuracy values are expressed as 93.8, 93.6, and 93.7 percent, their population variance is approximately 0.00667 percentage-points squared.

**DescriptionPC is more difficult and is not part of that low-variance calculation:**

| Model | Answer correct, ignoring identity | Drug identity correct | Both correct |
| --- | ---: | ---: | ---: |
| GPT-4o | 85.9 | 55.8 | 48.2 |
| Llama-3.1-8B-Instruct | 78.3 | 6.4 | 5.3 |
| Llama-3.1-70B-Instruct | 85.3 | 23.6 | 20.1 |
| TxAgent-8B | 90.4 | 60.1 | 56.5 |

TxAgent still leads, but its 90.4% answer-only score falls to 56.5% when correct drug identification is required. This is a substantial unresolved grounding challenge. The abstract's wording about similarly low variance across name and description variants is broader than the detailed results support. [Figure 3a–b and main text pp. 12–13.](https://arxiv.org/pdf/2503.10970v1#page=27)

### 13.3 TreatmentPC

| Model | Multiple choice | Open-ended |
| --- | ---: | ---: |
| Llama-3.1-8B-Instruct | 56.1 | 33.1 |
| Llama-3.1-70B-Instruct | 70.4 | 49.6 |
| GPT-4o | 74.1 | 61.4 |
| ToolACE-8B | 14.7 | 13.4 |
| WattTool-8B | 18.2 | 5.9 |
| DeepSeek-R1-Distill-Llama-8B | 50.7 | 40.1 |
| DeepSeek-R1-Distill-Llama-70B | 64.5 | 56.4 |
| DeepSeek-R1, full 671B model | 76.5 | 67.5 |
| **TxAgent-8B** | **86.8** | **75.0** |

TxAgent exceeds the full DeepSeek-R1 model by 10.3 pp in MC and 7.5 pp in open-ended scoring. The advantage concerns this comparison of an evidence-retrieving, domain-trained agent with reasoning models using internal knowledge. It does not separate retrieval advantages from reasoning-policy advantages. [Figure 4a–c, pp. 29–30.](https://arxiv.org/pdf/2503.10970v1#page=29)

## 14. Ablations: tools, thoughts, and trajectory length
{: #ablations }

The ablations help explain which components matter, but each intervention must be read precisely. A test that changes training data answers a different question from a test that caps inference. The accuracy tables in §14.1–14.5 report multiple-choice results; §14.6 separately labels interaction counts for both settings. [Main text pp. 17–19; Figure 3c–g; Methods §6.](https://arxiv.org/pdf/2503.10970v1#page=17)

### 14.1 Replace biomedical APIs with LLM-generated tool responses

The agent still emits calls, but the selected tool's description and arguments are sent to an LLM instructed to act as that function. The LLM generates the supposed response instead of querying the biomedical source. This retains much of the action structure while replacing the evidence source.

| Tool response backend | DrugPC | TreatmentPC |
| --- | ---: | ---: |
| Real ToolUniverse tools | 93.8 | 86.8 |
| Llama-3.1-8B as tools | 68.7 | 67.1 |
| GPT-4o as tools | 72.7 | 74.8 |

These are the **Figure 3c labels**. The TreatmentPC model assignments in the p. 17 prose are reversed relative to the figure: it assigns 67.11 to GPT-4o and 74.78 to Llama-8B. Both presentations show real tools ahead of the simulated tool backends; the exact ordering of the two simulated backends is inconsistent in v1.

The defensible inference is that replacing external records with generated approximations hurts performance. This supports the importance of evidence access. It does not show that every response from an API is correct or sufficient.

### 14.2 Increase the available biomedical tool subset

The authors use nested subsets, so larger subsets include the smaller ones. Figure 3d reports:

| Fraction of ToolUniverse, as labeled in Figure 3d | DrugPC | TreatmentPC |
| --- | ---: | ---: |
| 10% | 78.4 | 71.7 |
| 25% | 84.9 | 73.2 |
| 50% | 88.9 | 83.8 |
| 75% | 92.7 | 86.0 |
| 100% | 93.8 | 86.8 |

The prose on p. 18 says **20%**, whereas the figure labels **25%**. The second row is therefore identified explicitly as the figure value. The improvement suggests that broader tool coverage helps on these benchmarks. It does not establish that arbitrary additional tools always help or that latency and retrieval quality remain constant as a toolbox grows. The paper does not give repeated subset-sampling uncertainty.

### 14.3 Remove intermediate thoughts

The authors remove thoughts from the training data and train a variant that directly generates calls. At inference, it alternates calls and observations, with textual output interpreted as the final answer. This changes both the demonstrations and the behavior learned from them; it is not merely hiding the display of the same trained agent's thoughts.

| Configuration | DrugPC | TreatmentPC |
| --- | ---: | ---: |
| With thoughts, Figure 3e control | 93.8 | 86.4 |
| Without thoughts | 71.5 | 64.9 |
| Difference | 22.3 pp | 21.5 pp |

The TreatmentPC control is 86.4% in this panel and its accompanying text, while most other full-model results are 86.8%. These numbers are preserved rather than silently substituted.

The experiment supports the usefulness of explicit intermediate-text supervision within this training setup. It does not prove that generated rationales faithfully reveal internal computation, or isolate verbalized reasoning from all changes in sequence length and supervision.

### 14.4 Limit trajectory depth in training

The paper filters the training data to retain samples with at most 1, 3, or 5 reasoning steps, or uses all available steps, then constructs the corresponding stepwise examples. Inference is left unrestricted. It does not report truncating longer trajectories into shorter ones; the detailed sample counts after filtering are not given.

| Maximum training steps, Figure 3f | DrugPC | TreatmentPC |
| --- | ---: | ---: |
| 1 | 71.6 | 66.9 |
| 3 | 92.8 | 80.9 |
| 5 | 93.0 | 86.4 |
| Full | 93.8 | 86.8 |

Longer demonstrations are associated with better performance, especially on treatment comparison. Training only on shallow interactions gives the student less exposure to dependent lookups, recovery from unhelpful results, and evidence integration. Because the procedure changes available training examples, the comparison may also change training-data quantity and composition; it is not an isolated intervention on an abstract “reasoning depth” variable.

### 14.5 Limit reasoning steps during inference

Here the model is trained on the full dataset. At a selected step cap, the system forces `[FinalAnswer]` and requires the model to answer from the evidence accumulated so far. Trajectories that finish before the cap are unchanged.

| Inference step limit, Figure 3g | TreatmentPC accuracy |
| --- | ---: |
| 1 | 73.5 |
| 3 | 74.1 |
| 4 | 80.3 |
| 5 | 81.6 |
| 6 | 82.0 |
| Full | 86.8 |

Additional opportunities to retrieve and process information improve performance. The main text describes diminishing returns beyond five steps, but the full setting remains **5.2 pp above the five-step result**. It would overstate the figure to say that five steps recover full performance. “One step” is also a protocol-specific cap; the paper does not provide enough timing detail to equate it universally with zero external evidence.

### 14.6 Observed steps and calls

Extended Data Figure 4 reports the following averages:

| Benchmark and setting | Reasoning steps | Tool calls |
| --- | ---: | ---: |
| DrugPC, multiple choice | 4.62 | 4.49 |
| DrugPC, open-ended | 4.60 | 4.64 |
| TreatmentPC, multiple choice | 4.97 | 7.30 |
| TreatmentPC, open-ended | 6.12 | 8.02 |

TreatmentPC requires more interaction effort, especially when generating without options. These are interaction counts, not measured latency or monetary cost. The figure does not fully specify whether specialized calls and finalization are counted identically across the two measures, so one should not derive an exact number of biomedical queries per thought from their ratio. [Extended Data Figure 4, p. 34.](https://arxiv.org/pdf/2503.10970v1#page=34)

## 15. What the evidence establishes and what remains open
{: #limitations }

### 15.1 What is supported

The study provides evidence that a compact, domain-adapted language model can be an effective controller of biomedical tools. The model learns entity resolution, schema-conditioned calls, tool discovery, use of returned evidence, and continuation after unsuccessful attempts. The ablations support the importance of actual external data, adequate tool coverage, and training on multi-step interactions.

The synthetic-data pipeline is a major methodological contribution. It converts reference documents and APIs into demonstrations of actions that cannot be learned from final-answer pairs alone. Its separation into tool construction, question construction, and trajectory construction makes the dependencies understandable and offers distinct places to inspect errors.

### 15.2 What the reported accuracy does not establish

**Clinical effectiveness.** The evaluation does not measure patient outcomes, adverse-event reduction, clinician workload, prescribing error rates in practice, or prospective clinical benefit. Claims about improving therapeutic decision-making should be read as motivations and potential applications beyond the reported benchmark results.

**Independently grounded evaluation distributions.** Questions are deliberately generated from the same kinds of evidence available through the tools. This is appropriate for testing evidence use, but favors questions answerable from the selected labels and databases. Unanswerable, contradictory, incompletely specified, or out-of-scope clinical questions need separate evaluation.

**Independent validation of synthetic data.** GPT-family models generate and screen the questions and trajectories. Shared model errors can therefore survive model-based checks. Human benchmark review adds a separate review stage, but reviewer counts and inter-rater agreement are not reported, and the paper does not establish clinician adjudication of every training trajectory.

**Faithfulness of intermediate text.** The action log establishes which calls were emitted and what evidence was returned. A fluent intermediate rationale is still generated text. Tool provenance does not guarantee that every stated reason caused the eventual answer or that omitted evidence was considered.

**Complete safety checking.** A contraindication lookup can reveal a restriction; absence of a retrieved restriction does not prove safety. A candidate list may be incomplete, a label may apply to a specific formulation, or a summary may lose a qualifier. Selecting among deliberately constructed MC options is easier to define than finding the best treatment in an open clinical decision space.

**Causal treatment-effect estimation.** Applying label-based restrictions is different from estimating what would happen to this patient under alternative treatments. The paper does not introduce confounding adjustment, potential-outcome estimation, or a calibrated individualized benefit–risk model.

### 15.3 Open technical questions

The Discussion identifies limited tool coverage, uncertainty quantification, integration of internal knowledge with tool feedback, and multimodal inputs as open issues. Several additional questions follow from the method:

- How often does retrieval miss the necessary tool, independently of the language model's subsequent choice?
- How stable are answers when API records, schemas, synonyms, or label versions change?
- Can the agent recognize insufficient information and abstain or request clarification?
- What happens under malformed responses, timeouts, unavailable services, or contradictory sources?
- How reliably do summaries preserve numeric values, population qualifiers, and evidence limitations?
- How much of the improvement remains when a strong general agent receives the same tool retrieval, domain data, and inference budget?
- How do latency, token use, and the number of API calls vary across successful and failed cases?

These are methodological gaps or follow-up evaluations, not claims that the authors performed the corresponding experiments. A full safety assessment would also need to examine how untrusted tool-response content is handled; the paper does not specify that boundary in detail.

Local hosting of the language model can improve control over model execution, but calls to external biomedical APIs still transmit their arguments. “Locally deployed” alone does not establish that an entire deployment keeps all patient-related data on the same machine; data-flow design must be evaluated separately.

## 16. Reproducibility details and inconsistencies in v1
{: #reproducibility }

### 16.1 Reported versus unreported implementation details

| Component | Explicitly reported | Needed for an exact reproduction but not specified in the v1 Methods |
| --- | --- | --- |
| TxAgent model | Llama-3.1-8B-Instruct; LoRA; output-token autoregressive loss | Learning rate, optimizer, scheduler, batch size, gradient accumulation, epochs, seeds, validation split, checkpoint selection |
| LoRA configuration | Low-rank adaptation | Rank, scaling, dropout, target modules |
| Context processing | Summarize long tool outputs; replace earlier results first in training preprocessing | Exact context limit, summary prompt in full, thresholds, truncation and message-packing details |
| ToolRAG | gte-Qwen2-1.5B-instruct; top-k retrieval; multiple negatives ranking loss; iterative training | Numerical k, similarity function, pooling/normalization, temperature, negative handling, pair counts, training rounds, optimizer settings |
| Question/trace generation | Agent roles; data sources; filtering dimensions; prompt sketches | Full prompts, generation settings, rejection rates, retry bounds, judge agreement, complete dataset accounting |
| Tool validation | Mapping checks, sampled API tests, human verification | Per-tool test suites, reviewer counts, coverage and reliability statistics |
| Inference | Thought/call/feedback loop; multiple calls; Finish marker | Decoding settings, default execution limits, timeout/retry policy, invalid-call recovery, resource accounting |
| Benchmarks | Dataset sizes; source-field mapping; temporal approval criterion; scoring protocols | Full snapshot and overlap audit, detailed adjudication protocol, uncertainty over repeated runs |

Public code or later releases may supply additional settings. They should be version-pinned and distinguished from the v1 paper's specification; these notes do not silently fill gaps with settings from a newer release.

### 16.2 Source discrepancies that affect interpretation

| Location | Issue in v1 | How these notes handle it |
| --- | --- | --- |
| Abstract versus Figure 3a–b / p. 13 | Low variance is described broadly across name and description forms; the detailed variance concerns DrugPC/BrandPC/GenericPC | Restrict the variance claim to those three naming conditions; report DescriptionPC separately |
| p. 17 versus Figure 3c | TreatmentPC scores for GPT-4o-as-tools and Llama-as-tools are assigned in opposite orders | Use the figure's labeled values and explicitly state the conflict |
| p. 18 versus Figure 3d | Second toolbox subset is 20% in prose and 25% in the figure | Label the numeric table as Figure 3d values |
| Figure 3e / p. 18 versus overall TreatmentPC results | Thought-ablation control is 86.4%; most full-model results are 86.8% | Preserve the ablation-specific control |
| §4.1 dataset accounting | 177,626 reported steps and 378,027 instruction samples are not numerically reconciled | Report both without inventing a conversion factor |
| Main text p. 12 versus Methods §5.1 | Brand–generic conversion questions are described as modified versus kept unchanged | Follow Methods and note the discrepancy |
| Main text p. 10 versus Methods §5.1 | Options described as 4–5 versus mostly 4 with some 2 or 5 | Use the fuller Methods description |
| Extended Data Figure 1, p. 31 | Example active-ingredient tool is paired with return fields for dosage/administration and supply | Avoid copying that pair as a valid executable specification |
| §3.3 and Algorithms | END/Finish naming and schematic indexing/branching are not fully consistent | Explain the intended completion process; label pseudocode as explanatory |
| Interaction example pp. 15–16 versus Discussion p. 20 | The direction of the CYP2D6 interaction explanation changes | Discuss the evidence-combination method without adopting the inconsistent account as clinical guidance |

These discrepancies do not erase the reported overall performance pattern. They limit how precisely individual settings, comparisons, and clinical examples can be reconstructed from v1 alone.

## 17. Source map and terminology
{: #sources }

### 17.1 Where to find each part in the paper

| Topic | Primary location |
| --- | --- |
| Inference state, equations, summarization, and termination | Online Methods §1, pp. 39–45; Algorithm 1 |
| Tool specifications, ToolGen, and Tool Graph | Online Methods §2, pp. 45–47; Extended Data Figures 1–3 |
| Source databases and QuestionGen | Online Methods §3.1–3.2, pp. 47–50 |
| Helper, Tool Provider, Solver, virtual retrieval, and trace filtering | Online Methods §3.3, pp. 50–54; Algorithm 2 |
| ToolRAG bootstrapping | Online Methods §3.4, pp. 54–55 |
| Dataset decomposition, augmentation, LoRA, and training loss | Online Methods §4, pp. 55–58 |
| Benchmarks and evaluation | Table 1, p. 36; Online Methods §5, pp. 59–61 |
| Main results and ablations | Figures 1–4, pp. 23–30; main text pp. 9–19 |
| LLM-as-tools and no-thought implementation | Online Methods §6, pp. 61–63; Algorithm 3 |
| Prompt outlines | Online Methods §7, pp. 63–71 |
| Interaction counts and limitations | Extended Data Figure 4, p. 34; Discussion, pp. 20–21 |

### 17.2 Terms that are easy to confuse

| Term | Meaning in this paper |
| --- | --- |
| Tool schema | Description and argument contract shown to the language model |
| Tool backend | Executable mapping from arguments to a provider's API |
| Tool retrieval | Finding candidate capabilities from their descriptions |
| Evidence retrieval | Executing biomedical tools to obtain source information |
| Tool Graph | Training-only graph of potential output-to-input connections |
| Trajectory | Ordered intermediate text, actions, observations, and completion |
| Stepwise sample | One history-conditioned prediction target from a trajectory |
| Helper hint | Answer-aware guidance used during synthetic trajectory generation |
| Virtual ToolRAG call | Inserted discovery action for a reference-derived training tool |
| Open-ended accuracy | Accuracy after free generation followed by option mapping |
| Grounded answer | An answer intended to use returned evidence; still subject to inference and completeness errors |

**Primary source:** Gao, S., Zhu, R., Kong, Z., Noori, A., Su, X., Ginder, C., Tsiligkaridis, T., and Zitnik, M. (2025). *TxAgent: An AI Agent for Therapeutic Reasoning Across a Universe of Tools*. [Version 1](https://arxiv.org/abs/2503.10970v1) · [PDF](https://arxiv.org/pdf/2503.10970v1) · [Project](https://zitniklab.hms.harvard.edu/TxAgent/) · [TxAgent code](https://github.com/mims-harvard/TxAgent) · [ToolUniverse code](https://github.com/mims-harvard/ToolUniverse).

Figures reproduced above are excerpts from Figure 1 and Extended Data Figures 2–3, attributed to Gao et al. Numerical results and methodological details are taken from the v1 paper; critical interpretations are identified in the surrounding text.
