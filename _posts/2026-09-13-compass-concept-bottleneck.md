---
layout: post
title: "(2026 Nature Medicine) COMPASS: A Concept Bottleneck Transformer for Immunotherapy Response"
description: "An architecture-focused reading of COMPASS: expression tokenization, Performer attention, hierarchical biological projection, contrastive pretraining, parameter-efficient adaptation, prototype inference, and interpretation of immune concepts."
permalink: /healthcare-ai/compass-concept-bottleneck/
date: 2026-09-13 21:00:00 -0400
research_area: healthcare-ai
math: true
tags: [Method, Healthcare AI, Transformer, Concept Bottleneck, Contrastive Learning, Immunotherapy, Transcriptomics]
---

**Paper:** Wanxiang Shen, Intae Moon, Thinh H. Nguyen, Michelle M. Li, Yepeng Huang, Nitya Nair, Daniel Marbach, and Marinka Zitnik. *Generalizable AI predicts immunotherapy outcomes across cancers and treatments*. **Nature Medicine 32, 3010–3022 (2026)**, published July 3, 2026. [Journal article](https://www.nature.com/articles/s41591-026-04502-7) · [Main PDF](https://www.nature.com/articles/s41591-026-04502-7.pdf) · [Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf) · [Official code](https://github.com/mims-harvard/COMPASS).

These English notes begin with the supplied **54-page Supplementary Information** and connect it to the main article and a pinned inspection of the public implementation. The priority is to explain the algorithm: what each tensor represents, where biological knowledge enters, which parameters learn in each stage, and how a new patient receives a prediction. Main-PDF page numbers count from the first PDF page; supplementary references give both the printed **S-page** and the PDF page when useful. Teaching examples, algebraic consequences, and implementation observations are identified explicitly.

**The central construction:** COMPASS first lets gene representations exchange information through a transformer, then compresses them through a predefined biological hierarchy into a small vector of named concepts. Contrastive pretraining shapes this concept space using unlabeled tumors; clinical labels subsequently train a response predictor or define class prototypes. The named bottleneck makes the model easier to inspect, but its scores remain learned representations whose biological meaning requires validation.

<nav class="table-of-contents" aria-label="Contents" markdown="1">

**Contents**

1. [The prediction problem and the role of the architecture](#problem)
2. [The complete forward pass and tensor dimensions](#architecture)
3. [Data preparation: what the encoder actually receives](#inputs)
4. [Gene tokenization and the cancer-type token](#tokenization)
5. [Contextual encoding with Performer attention](#encoder)
6. [Hierarchical projection: genes → signatures → concepts](#projector)
7. [What the concept bottleneck constrains](#bottleneck)
8. [Contrastive pretraining and negative sampling](#pretraining)
9. [The supervised response head](#classifier)
10. [NFT, LFT, PFT, and FFT: what changes and what stays frozen](#adaptation)
11. [Prototype inference and a worked patient example](#prototypes)
12. [Multi-stage adaptation to a drug or indication](#multistage)
13. [Validation designs and what generalization means](#evaluation)
14. [Ablations: which architectural choices matter](#ablations)
15. [Concept interpretation, SHAP, and patient response maps](#interpretation)
16. [Survival analysis and the separate Clinical Transformer extension](#survival)
17. [Paper–code differences and reproduction requirements](#implementation)
18. [A practical reconstruction of the pipeline](#recipe)
19. [Methodological assessment and source map](#assessment)

</nav>

## 1. The prediction problem and the role of the architecture
{: #problem }

The prediction unit is a **patient with a pretreatment bulk tumor transcriptome**. The downstream task is binary immune-checkpoint-inhibitor (ICI) response prediction. Most cohorts define response as complete or partial response, and non-response as stable or progressive disease. This target should be distinguished from treatment benefit relative to an alternative therapy, time to death, and an experimentally measured immune-cell state.

Three challenges motivate the model. First, the input has thousands of expression measurements while a clinical cohort may contain only a few dozen patients. Second, cohorts differ in cancer type, therapy, sample processing, and response prevalence. Third, a flexible gene-level predictor can be difficult to interpret. COMPASS addresses these challenges through three linked design choices:

| Design choice | Intended contribution | What it cannot establish by itself |
| --- | --- | --- |
| Pretrain on a much larger pan-cancer transcriptomic collection | Learn representations before using scarce ICI response labels | That the representation is already specific to treatment response |
| Route representations through curated biological concepts | Restrict the downstream feature space and expose named intermediate scores | That a score measures a biological quantity without error |
| Adapt only selected modules when clinical data are limited | Reduce the number of parameters fitted to response labels | That transfer will succeed on every unseen cohort |

The article's pretraining collection contains **10,184 TCGA tumors across 33 cancer types**. Its response benchmark contains **1,133 patients in 16 cohorts**, spanning seven cancer types. There are 346 responders and 787 non-responders. These are two different data resources with different roles: TCGA supplies representation-learning examples; ICI cohorts supply the clinical supervision and evaluation.

A “pan-cancer foundation model” here is a pretrained transcriptomic encoder with transfer mechanisms. It is not a general-purpose language model, an EHR sequence model, or a multimodal agent. Cancer type accompanies gene expression, but a drug identifier is not a separate input token in the main architecture equations. Drug-specific behavior is obtained through the choice of training cohorts and adaptation strategy. [Main article, Fig. 1 and Methods, PDF pp. 14–18](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=14).

## 2. The complete forward pass and tensor dimensions
{: #architecture }

Write the model as

$$
f_{\theta,\phi,\psi}(x,c)
= h_\psi\!\left(g_\phi\!\left(e_\theta(x,c)\right)\right),
$$

where $$e_\theta$$ is the gene encoder, $$g_\phi$$ is the hierarchical projector, and $$h_\psi$$ is a response head. The notation is a teaching decomposition of the paper's three modules. The same encoder–projector pair can also feed a non-parametric prototype rule or a separately trained survival model. Sections 2–12 first explain the architecture as reported in the paper; Section 17 documents material differences in the inspected software, including extra tokens, fine-tuning behavior, and the NFT decoder.

<pre class="mermaid">
flowchart TD
    X["Pretreatment expression: B × 15,672"] --> T["Gene-specific abundance embeddings and biases"]
    C["Cancer-type category"] --> CT["Learned cancer token"]
    T --> E["Contextual gene encoder: Performer"]
    CT --> E
    E --> G["Curated membership: weighted gene embeddings"]
    G --> S["132 biological signature scores"]
    S --> H["43 high-level biological concept scores"]
    E --> CC["Contextual cancer-token score"]
    H --> F["44-dimensional patient representation"]
    CC --> F
    F --> P["Supervised response head"]
    F --> N["Frozen representation + labeled class prototypes"]
</pre>

*Teaching schematic of the architecture described in the paper. It omits implementation-only tokens discussed in Section 17. The biological membership maps constrain the projector; attention in the encoder operates before those constraints.*

Let $$B$$ be batch size, $$L=15{,}672$$ the number of genes, and $$d$$ the token embedding dimension. The paper's forward-pass description has these stages:

| Stage | Tensor shape | Meaning |
| --- | --- | --- |
| Ordered expression matrix | $$B\times L$$ | One abundance value for each expected gene |
| Gene-token embeddings | $$B\times L\times d$$ | A vector per gene, carrying identity and abundance |
| Gene tokens plus cancer token | $$B\times(L+1)\times d$$ | Input sequence in the main Methods description |
| Contextual encoder output | $$B\times(L+1)\times d$$ | Each token can reflect other genes and cancer context |
| Biological gene-set vectors | $$B\times132\times d$$ | Weighted pooling within curated gene sets |
| Biological gene-set scores | $$B\times132$$ | One learned scalar per granular signature |
| Biological concept scores | $$B\times43$$ | Aggregation of signatures into broader named concepts |
| Final representation | $$B\times44$$ | 43 biological concepts plus a cancer-token-derived score |
| Supervised output | $$B\times2$$ | Two logits, then two class probabilities |

**132 versus 133, and 43 versus 44:** the biological hierarchy contains 132 granular signatures and 43 high-level concepts. Including the cancer channel gives 133 and 44. Supplementary Fig. S1 uses 133/44 in its NFT comparison; the signature-scoring comparisons use biological-only feature sets. These numbers are not interchangeable. A 44-dimensional representation also means **44 scalar features**, not 44 vectors of dimension $$d$$.

The main text does not provide every low-level encoder setting alongside these equations. Section 17 separately reports the inspected code configuration rather than silently assigning it to every published experiment. [Main Methods, PDF pp. 15–16](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=15); [Supplement, Fig. S1, S3/PDF p. 4](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=4).

## 3. Data preparation: what the encoder actually receives
{: #inputs }

Bulk RNA-seq measures a mixture of tumor, immune, stromal, and other cells in a biopsy. A high expression value may reflect more cells of a type, stronger expression within those cells, or both. COMPASS learns from this mixture; it does not directly observe individual cells or their spatial arrangement.

The article describes alignment to GRCh38/hg38 with STAR 2.7.5c and GENCODE v36 annotation. Counts are converted to transcripts per million (TPM), using gene lengths and the sample's total length-normalized counts. For cohorts with raw FASTQ data, sequencing reads are reprocessed; otherwise, available counts are converted using aligned gene lengths. The shared feature set consists of protein-coding genes available across the clinical expression data.

For clarity, a standard TPM calculation is

$$
r_{ig}=\frac{\operatorname{count}_{ig}}{\operatorname{length}_{g,\mathrm{kb}}},
\qquad
\operatorname{TPM}_{ig}=10^6\frac{r_{ig}}{\sum_{g'}r_{ig'}}.
$$

This equation explains the unit conversion. **TPM normalization does not itself remove batch effects or make two assays identical.** Library preparation, tissue composition, biopsy location, and technical processing can still influence expression.

Four details matter when reconstructing the inputs:

1. **Gene order is part of the model interface.** A column must correspond to the same gene as the associated embedding, bias, and signature memberships. A matrix with the right width but shuffled columns is invalid unless every associated index is also permuted.
2. **The shared gene panel is defined before deployment.** An incoming sample must be aligned to that panel. The published panel was selected using feature availability in the study's clinical datasets; that is not response-label supervision, but it does mean panel compatibility was checked against those data.
3. **Expression scale must match the checkpoint.** The manuscript describes TPM inputs, while its visualization section explicitly uses $$\log_2(\mathrm{TPM}+1)$$ and within-cohort z-scores for displayed gene values. Display normalization should not be assumed to be the neural network's preprocessing. The inspected implementation's preprocessing is recorded in Section 17.
4. **Labels are not completely homogeneous.** Van Allen includes an overall-survival-based stable-disease rule; Hugo uses immune-related RECIST; Zhao uses special pathology/radiographic response criteria. The common binary label therefore joins related but imperfectly identical endpoints.

A model can learn from these cohorts while still being sensitive to assay and labeling differences. Leave-one-cohort-out evaluation is useful partly because a random patient split would preserve many such cohort-specific characteristics in both training and testing. [Main Methods, PDF p. 14](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=14).

## 4. Gene tokenization and the cancer-type token
{: #tokenization }

### 4.1 A continuous value becomes a gene-specific vector

The paper uses one learned vector $$w_g\in\mathbb R^d$$ and one learned bias $$b_g\in\mathbb R^d$$ per gene. Its tokenization equation can be written

$$
t_{ig}=x_{ig}w_g+b_g.
$$

The same expression value produces different tokens for different genes because their $$w_g$$ and $$b_g$$ differ. Conversely, two patients with different abundance of the same gene move along that gene's learned direction $$w_g$$. The bias retains gene identity even when the expression value is zero.

This is a continuous feature tokenizer. There is no nucleotide sequence tokenization, word vocabulary, ranking of genes into a sentence, or discretization into expression bins in this equation. The article calls $$b_g$$ a learnable positional encoding, but its operational role is a **gene-specific identity bias**. It does not encode physical distance along a chromosome.

**Teaching example.** If $$w_g=(0.5,-0.2)$$, $$b_g=(0.1,0.3)$$, and $$x_{ig}=2$$, the pre-activation token is $$(1.1,-0.1)$$. Increasing abundance changes the vector along $$w_g$$; it does not replace the gene's identity. This numerical example is illustrative, not an observed COMPASS embedding. The inspected code adds a ReLU to this step, so code-level output would be $$(1.1,0)$$; that activation is absent from the main tokenization equation.

### 4.2 Cancer type is an embedding lookup

A categorical cancer label indexes a learned $$33\times d$$ matrix. For patient $$i$$,

$$
t_{i,\mathrm{cancer}}=W_{\mathrm{cancer}}[c_i,:].
$$

The integer code is an index, not an ordinal number with a meaningful magnitude. The cancer token enters attention together with the genes. After attention, its representation can reflect both cancer identity and the patient's expression pattern.

This distinction becomes important at the output: the additional scalar concept is a **projection of the contextualized cancer token**, not simply the original cancer label copied into the classifier. Removing that scalar after encoding is not necessarily equivalent to removing the cancer input before attention, because cancer information can already have spread into gene representations. Supplementary Method S5 describes the cancer-input ablation as excluding cancer information during both training and inference.

Leaving a cancer type out of ICI fine-tuning also does not necessarily mean the encoder has never encountered that cancer type in TCGA pretraining. “Unseen indication” must always specify which training stage it was absent from. [Main Methods, PDF p. 15](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=15).

## 5. Contextual encoding with Performer attention
{: #encoder }

Tokenization alone treats genes independently. The encoder then lets each token combine information from other tokens, producing patient-specific contextual vectors $$h_{ig}$$.

For one conventional attention head, the teaching equations are

$$
Q=HW_Q,\qquad K=HW_K,\qquad V=HW_V,
$$

$$
\operatorname{Attention}(H)
=\operatorname{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.
$$

An attention weight depends on the current patient's token representations. The value vector for a gene can therefore be modified by other genes and by cancer context. A cytotoxicity-associated gene token may be represented differently in two patients with the same expression of that gene but different surrounding transcriptional programs.

At more than 15,000 tokens, explicitly constructing all pairwise attention scores is expensive: one $$L\times L$$ matrix has about 246 million entries. The paper uses **Performer**, which approximates softmax attention with a feature-map formulation so that aggregation can be rearranged without materializing that full matrix.

The following equation explains the computational principle, not an additional objective introduced by COMPASS:

$$
\operatorname{Attn}(Q,K,V)
\approx D^{-1}\phi(Q)\bigl(\phi(K)^\top V\bigr),
$$

$$
D=\operatorname{diag}\!\left[\phi(Q)
\bigl(\phi(K)^\top\mathbf 1\bigr)\right].
$$

For a fixed feature-map width, the sequence-length dependence of these products is linear rather than quadratic. This is an approximation to attention, not a restriction to only physically adjacent genes or a curated gene-interaction graph. The biological membership restrictions enter later, in the projector.

The main Methods mention FlashAttention as an optional alternative. These should not be conflated: Performer changes the attention computation through an approximation; FlashAttention is an efficient implementation strategy for attention and is not automatically the same linear approximation. A reproducible report should identify which backend the checkpoint used.

**A key consequence for interpretation:** a signature may directly pool only its member genes, but those genes' encoder outputs can contain information from outside the signature. The hierarchy constrains the final routing of contextual vectors, not all upstream information exchange. [Main Methods, PDF p. 15](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=15).

## 6. Hierarchical projection: genes → signatures → concepts
{: #projector }

The projector supplies the model's biological structure. Its membership relations are curated in advance; its pooling weights and scalar projection are learned. The [Supplementary Data 1 link on the article page](https://www.nature.com/articles/s41591-026-04502-7#MOESM3) provides the gene sets underlying the hierarchy.

### 6.1 Pool contextual gene vectors inside each signature

Let $$G_k$$ be the member genes of signature $$k$$. A learnable vector $$a_k$$ has one entry for each member. Softmax converts it into weights:

$$
\alpha_{kg}=\frac{\exp(a_{kg})}
{\sum_{u\in G_k}\exp(a_{ku})},\qquad g\in G_k.
$$

The pooled signature vector is

$$
u_{ik}=\sum_{g\in G_k}\alpha_{kg}h_{ig}\in\mathbb R^d.
$$

There are three separate ideas here:

- **Membership:** genes outside $$G_k$$ are not directly pooled into signature $$k$$.
- **Learned weighting:** member genes need not contribute equally.
- **Patient specificity:** $$h_{ig}$$, and therefore $$u_{ik}$$, changes with the patient's expression and context.

The pooling weights $$\alpha_{kg}$$ are parameters shared across patients in the described equations and inspected implementation. They change during training, but they are not recomputed from each patient's expression as query–key attention weights. Calling this “attention pooling” is reasonable; describing it as a second patient-conditioned transformer would be inaccurate.

### 6.2 Reduce each signature vector to one scalar

A linear projection maps the $$d$$-dimensional signature vector into a score:

$$
s_{ik}=v^\top u_{ik}+b.
$$

The article's response-map Methods and the inspected implementation use a **shared scalar projection** across pooled vectors. The model therefore does not need a large independent MLP for every signature. It learns a common readout direction while gene-specific embeddings, context, membership, and pooling weights distinguish signatures.

The scalar is not a probability. It may be negative, and its orientation is learned. A positive value does not automatically mean that a cell type is abundant or a pathway is activated in an experimentally calibrated sense.

### 6.3 Aggregate granular signatures into broader concepts

Let $$\mathcal G_m$$ be the signatures assigned to high-level concept $$m$$. Another learned softmax vector produces

$$
\beta_{mk}=\frac{\exp(b_{mk})}
{\sum_{u\in\mathcal G_m}\exp(b_{mu})},
\qquad
z_{im}=\sum_{k\in\mathcal G_m}\beta_{mk}s_{ik}.
$$

This stage yields one scalar per broad concept. Examples include immune-cell programs, stromal programs, and functional pathways. The hierarchy also includes a Reference concept built from reference-gene signatures, providing a named control coordinate rather than a patient-level ground-truth target; the 43 coordinates should not all be described as distinct immune programs. It does not concatenate all constituent genes back into a high-dimensional vector.

Because $$\beta$$ is nonnegative and sums to one, the high-level scalar is a convex combination of its constituent signature scores. It lies between their minimum and maximum for that patient. This is an algebraic property of the published aggregation equation, not an empirical claim about biology.

### 6.4 Add the cancer-derived score

The contextual cancer token is reduced to a scalar and incorporated as the additional channel:

$$
z_i=(z_{i1},\ldots,z_{i43},z_{i,\mathrm{cancer}})
\in\mathbb R^{44}.
$$

The response head receives this representation. There is no direct gene-to-classifier bypass in the main concept-bottleneck design.

### 6.5 A small worked projector example

Consider a teaching signature containing three contextual vectors:

$$
h_1=(1,0),\quad h_2=(0,2),\quad h_3=(1,1),
\qquad \alpha=(0.5,0.3,0.2).
$$

Its weighted vector is $$u=(0.7,0.8)$$. If the shared scalar readout is $$v=(2,-1)$$ and $$b=0.1$$, then

$$
s=2(0.7)-0.8+0.1=0.7.
$$

If this signature and another signature with score $$-0.2$$ feed a high-level concept with weights $$(0.75,0.25)$$, the concept score is

$$
z=0.75(0.7)+0.25(-0.2)=0.475.
$$

This example shows exactly where the dimensional reductions occur: vectors are pooled, then projected to scalars, then scalar scores are pooled again. It also shows why a negative coordinate in the scalar readout can matter even though the pooling weights themselves are nonnegative. [Main Methods, PDF pp. 15–16 and 20](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=16).

## 7. What the concept bottleneck constrains
{: #bottleneck }

The classifier must compute its prediction from the 44 features. That provides a compact interface for comparing patients and examining concept-level contributions. The fixed hierarchy also makes it possible to trace which gene sets directly feed each concept.

However, the concepts are **not trained against patient-level ground-truth concept labels**. There is no reported target saying that a particular patient's “TGFβ” score must equal a measured TGFβ pathway activity or that a “B cell” score must equal a measured B-cell fraction. Biological names and memberships are supplied; numerical values emerge from contrastive pretraining and supervised adaptation.

This differs from a supervised concept bottleneck in which human concept annotations are explicit intermediate targets. COMPASS grounds its representations structurally through prior knowledge. The named coordinates can still absorb other useful signals because the encoder contextualizes genes globally and the training losses reward patient representation and response prediction.

Three interpretation rules follow:

1. **Named does not mean calibrated.** A score of 0.8 is not 80% cell abundance or an 80% chance that a pathway is active.
2. **Changing a concept numerically is a model intervention.** It reveals how a classifier reacts to that coordinate under the chosen manipulation; it is not the same as a feasible biological intervention on a patient.
3. **Pooling weights, concept importance, and map edges are different objects.** Pooling weights are learned parameters; SHAP values describe prediction attribution; displayed map edges use cohort correlations. None should be substituted for another.

A useful architecture-level check is to ask whether the output can be reproduced entirely from the exported concept vector and the head. A biological validity check is harder: it requires comparison against independent assays, perturbations, or other relevant measurements. The paper explicitly identifies experimental validation and explanation-faithfulness testing as unfinished work. [Main Discussion, PDF p. 11](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=11).

## 8. Contrastive pretraining and negative sampling
{: #pretraining }

### 8.1 Construct a triplet, then reuse the same model three times

Each pretraining example consists of an anchor tumor $$x_a$$, a perturbed version $$\tilde x_a$$, and a different tumor $$x_n$$. All three pass through the **same encoder and projector**, yielding $$z_a,z_p,z_n\in\mathbb R^{44}$$. There are not three separately trained encoders.

<pre class="mermaid">
flowchart TD
    A["Anchor tumor"] --> F["Shared encoder + projector"]
    A --> P["Positive: mask or jitter expression"]
    P --> F
    N["Negative: another tumor"] --> F
    F --> Z["Three 44-dimensional concept vectors"]
    Z --> L["Triplet loss: pull anchor toward positive; separate negative"]
    L --> U["Update encoder and projector"]
</pre>

The main Methods describe negatives from another patient within the same cancer type and balanced sampling with replacement to reduce TCGA cancer-type imbalance. A same-cancer negative makes it harder to solve the task merely by separating cancer categories: tumors of the same type must also receive informative representations. The supplementary hard-negative experiment introduces a different, more explicit neighborhood-selection mechanism discussed below.

### 8.2 Make a positive view

The manuscript describes randomly selecting a masking or Gaussian-jitter transformation. Masking sets each gene value to zero with probability 0.1. Jitter adds Gaussian noise. The main equation writes $$\epsilon\sim\mathcal N(0,0.1)$$, while Supplementary Method S5 names a jitter **standard deviation** parameter; the distribution convention should be checked in the implementation rather than silently interpreting the second argument as variance or standard deviation.

Only the positive view is perturbed in the supplementary sensitivity design; the anchor remains unchanged. The perturbations express an assumption: modest measurement corruption should preserve the important representation of that patient's tumor. This is a modeling choice. A masked measurement is not necessarily biologically equivalent to a gene knockout, and arbitrary Gaussian noise is not a mechanistic model of transcriptional regulation.

### 8.3 Optimize cosine-distance separation

Using $$d(u,v)=1-\cos(u,v)$$, the triplet objective is

$$
\mathcal L_{\mathrm{triplet}}
=\max\{d(z_a,z_p)-d(z_a,z_n)+m,0\}.
$$

With the reported margin $$m=1$$, zero loss requires

$$
\cos(z_a,z_p)-\cos(z_a,z_n)\geq1.
$$

**Teaching example:** an anchor–positive similarity of 0.9 and anchor–negative similarity of 0.4 give loss $$0.5$$. If the negative similarity decreases to $$-0.2$$, the loss becomes zero. The objective rewards a separation gap, not simply a high positive-pair similarity.

The response classifier is not trained at this stage because the objective does not require response labels. It is also not an expression-reconstruction loss: masking generates a positive view, but COMPASS is not asked in this objective to predict each masked gene's original abundance. That distinction separates the core method from the masked-feature Clinical Transformer extension.

### 8.4 Reported training schedule and sensitivity settings

| Setting | Main COMPASS pretraining | Supplementary sensitivity experiments |
| --- | --- | --- |
| Genes | Full 15,672-gene panel | 2,475-gene subset including all concept genes |
| Validation split | 1% | 10%, stratified by cancer type |
| Optimization | Adam; learning rate $$10^{-3}$$; batch size 128 | Architecture, optimizer, and schedule held fixed within each sweep |
| Stopping/checkpoint | Stop after 10 epochs without validation-loss improvement; select lowest validation loss | Compare held-out self-supervised loss and downstream performance |
| Randomness | Seeds 24, 42, and 64 reported | Fixed seeds within comparisons |
| Hardware | A100 80 GB reported | Reduced panel used to lower computation |
| Downstream assessment | Main transfer benchmarks | NFT and PFT under LOCO in ten medium/large cohorts |

These settings should not be combined into a fictitious single experiment. Supplementary Method S5 explicitly identifies `immuno-compass` v2.0.5 for its sensitivity analyses.

### 8.5 Hard negatives change the task's difficulty

Supplementary Method S5 defines $$K\in[0.1,1]$$ as the fraction of the dataset considered in a nearest-neighbor candidate pool in expression space. At $$K=0.1$$, negatives come from the nearest 10% of samples; at $$K=1$$, the pool includes all other samples. Thus $$K$$ is a **fraction**, not a literal count of ten neighbors or a number of negative classes.

Smaller pools select more transcriptionally similar, difficult negatives. Supplementary Fig. S37 shows an instructive pattern: larger pools make the self-supervised objective easier while generally worsening downstream performance. Lower pretraining loss therefore does not automatically imply a more transferable clinical representation. Section 17 distinguishes this experiment from the current code's available samplers. [Main Methods, PDF p. 17](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=17); [Supplement, Methods S5, S50–S51/PDF pp. 51–52](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=51).

## 9. The supervised response head
{: #classifier }

The parametric head receives $$z_i\in\mathbb R^{44}$$. The main Methods describe batch normalization, a dense predictor producing two logits, and temperature scaling:

$$
\tilde z_i=\operatorname{BatchNorm}(z_i),\qquad
\ell_i=\operatorname{Head}(\tilde z_i)\in\mathbb R^2,
$$

$$
\tau=\exp(t)>0,\qquad
P(Y=c\mid x_i)=\frac{\exp(\ell_{ic}/\tau)}
{\sum_{c'}\exp(\ell_{ic'}/\tau)}.
$$

The head's training objective is cross-entropy against observed binary response labels. Larger temperature makes the probability vector less sharp; smaller temperature makes it more concentrated. Scaling all logits by one positive temperature does not change their ordering, so it does not change the winning class for fixed logits. It can change the confidence attached to that class.

A learned temperature is not proof of external calibration. For a new cohort, calibration depends on whether predicted probabilities correspond to observed frequencies under that cohort's distribution. Supplementary Fig. S35 evaluates calibration and decision curves; it should be read as evidence from those test settings rather than a universal property of temperature scaling.

Batch normalization also creates a deployment requirement. Inference must use the saved normalization state in evaluation mode, rather than recomputing arbitrary batch statistics from a new single patient. With clinical training batches of only 8–16, normalization behavior and handling of small final batches deserve explicit attention in a reproduction.

**Head specification caveat:** the main fine-tuning paragraph mentions 16 hidden units and reports 182 trainable parameters for LFT. These do not transparently describe the same ordinary $$44\rightarrow16\rightarrow2$$ MLP: its two affine layers alone have 754 parameters. Treat the parameter counts as reported figures and consult the actual checkpoint and versioned head configuration before reconstructing an exact head. Section 17 gives the inspected implementation details. [Main Methods, PDF pp. 16–17](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=16).

## 10. NFT, LFT, PFT, and FFT: what changes and what stays frozen
{: #adaptation }

| Mode | Gene encoder | Hierarchical projector | Response mechanism | Interpretation |
| --- | --- | --- | --- | --- |
| NFT: no fine-tuning | Frozen | Frozen | Cosine comparison with labeled class prototypes | No gradient updates; labeled support data are still required |
| LFT: linear probing | Frozen | Frozen | Train the response head | Tests the usefulness of the pretrained concepts for a clinical target |
| PFT: partial fine-tuning | Frozen | Trainable | Train the response head | Adapt the concept readout while preserving the gene encoder |
| FFT: full fine-tuning | Trainable | Trainable | Train the response head | Permit end-to-end adaptation to the response task |

PFT is particularly informative architecturally. It allows response labels to adjust which signature members matter and how signatures combine into concepts, without changing the large contextual encoder. It is not necessarily LoRA, low-rank attention adaptation, or prompt tuning; its parameter efficiency comes from choosing which existing modules are trainable.

Under the paper's strict LFT freezing definition, with fixed preprocessing and evaluation-mode normalization/dropout state, the same input retains the same pretrained concept vector and only the classifier changes. With PFT, the input patient's concept scores can change even though the encoder is frozen. With FFT, both the contextual gene representation and the concept mapping can change. Consequently, scores from a TCGA-pretrained model and a clinically adapted model should not be treated as identical measurements simply because they have the same concept names.

The paper reports approximately 1,018,784 trainable parameters for FFT, 2,144 for PFT, 182 for LFT, and none for NFT. These are reported configuration-specific counts, not universal constants of the four strategies. Exact counts depend on gene panel, embedding size, tokenization, projector variant, and head architecture.

For supervised modes, the article reports learning rates between $$10^{-3}$$ and $$10^{-2}$$, batches of 8–16, and weight-decay settings of $$10^{-2}$$ or $$10^{-4}$$, with epoch selection based on internal validation. There is no universal cohort-size threshold that automatically selects the mathematically optimal strategy. Freezing more parameters reduces flexibility; updating more parameters may improve adaptation but increases overfitting risk. The study evaluates these tradeoffs rather than proving one mode is optimal for every use case. [Main Fig. 1e and Methods, PDF p. 17](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=17).

## 11. Prototype inference and a worked patient example
{: #prototypes }

NFT keeps the pretrained encoder and projector frozen, but it still uses **reference patients with known response labels**. It does not discover which region means “response” from unlabeled TCGA data alone.

For each class $$c$$, first normalize each support vector, then average:

$$
\tilde z_j=\frac{z_j}{\|z_j\|_2},\qquad
\bar p_c=\frac{1}{N_c}\sum_{j:y_j=c}\tilde z_j,
\qquad
p_c=\frac{\bar p_c}{\|\bar p_c\|_2}.
$$

For a new patient $$q$$, encode and normalize $$z_q$$, compare it with both prototypes, and apply a softmax over cosine similarities:

$$
a_c=\frac{\cos(z_q,p_c)}{\tau_{\mathrm{NFT}}},\qquad
P_q(c)=\frac{\exp(a_c)}{\sum_{c'}\exp(a_{c'})}.
$$

The main Methods describe a typical fixed NFT temperature of 0.1. The class with the more similar prototype wins. Class sample sizes affect how accurately the prototypes are estimated, but averaging separately by class does not itself multiply the score by class prevalence.

**Teaching example.** Suppose a patient's cosine similarity to the responder prototype is 0.8 and to the non-responder prototype is 0.6. With temperature 0.1, the logits are 8 and 6, giving

$$
P(R)=\frac{e^8}{e^8+e^6}\approx0.881.
$$

With temperature 1, the same relative geometry gives approximately 0.550. This difference shows why a strong-looking NFT probability is partly a consequence of score scaling, not just distance from a clinical decision boundary. Both settings choose the responder class.

The averaging order matters. Averaging unit-normalized patient vectors gives each support patient equal directional influence. Averaging raw vectors would let large-norm patients contribute more strongly. Normalizing the resulting mean again ensures that subsequent comparison uses direction rather than prototype magnitude.

In the within-cohort leave-one-patient-out experiment, the query patient's label must be excluded from the support set. In cross-cohort NFT, reference patients come from allowed training cohorts. An illustrative “2-way 4-shot” picture in Supplementary Fig. S1 does not establish that every experiment used exactly four support examples per class.

A valid implementation also needs nonempty support examples for both classes and protection against zero-norm vectors. These are practical requirements of the formula, not evidence that the authors encountered those edge cases. [Main Methods, PDF p. 16](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=16); [Supplement, Fig. S1, S3/PDF p. 4](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=4).

## 12. Multi-stage adaptation to a drug or indication
{: #multistage }

Multi-stage fine-tuning (MSFT) changes the sequence of training datasets, not the core token–encoder–projector architecture:

$$
\text{TCGA pretraining}
\longrightarrow\text{broad ICI adaptation}
\longrightarrow\text{target-drug or target-indication adaptation}.
$$

The two comparison strategies are SSFT1, which adapts directly to the target-specific data, and SSFT2, which adapts to the broad ICI data without the final target-specific stage. MSFT asks whether a general response-prediction task provides a better starting point than moving directly from unlabeled transcriptomes to a small target cohort.

For a drug-specific assessment, the broad ICI stage excludes drugs sharing the target checkpoint mechanism. The target-specific data are then separated into adaptation and test cohorts. These exclusions matter: retaining highly overlapping therapies in the earlier stage would answer a different transfer question.

A worked design example is pembrolizumab adaptation: the reported target-specific training group contains melanoma patients, while the test group contains gastric/lung cancer cases. The held-out group's labels must remain unused in checkpoint selection and in both supervised stages. Supplementary Table S7 is the appropriate source for the exact cohort composition, rather than inferring it from a schematic arrow.

Disease-specific LUAD adaptation is a different experiment. Its final training and test subsets are separated by therapy within the same Ravi-1 cohort; the broad adaptation stage excludes LUAD. That evaluates a useful therapy-transfer setting, but it should not be described as the same external-study holdout design as every drug-specific comparison.

The main Methods and supplementary table contain inconsistent atezolizumab test counts, discussed in Section 17. The conceptual training sequence is clear even when a particular reported sample total needs verification. [Main Fig. 4 and Methods, PDF p. 18](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=18); [Supplement, Table S7, S44/PDF p. 45](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=45).

## 13. Validation designs and what generalization means
{: #evaluation }

The architecture can be evaluated under several different information boundaries. Their names should not substitute for a description of what the model was allowed to see.

| Design | Training/support data | Test data | Main question |
| --- | --- | --- | --- |
| Within-cohort LOPO | Other patients in the same study | One excluded patient | Can the representation predict another patient from that study? |
| Leave-one-cohort-out, LOCO | All permitted cohorts except one | The entire excluded cohort | Does it transfer across clinical studies? |
| Cohort-to-cohort | One source cohort | A different target cohort | Can a single source support transfer? |
| Leave-one-indication-out | Exclude a cancer category from ICI adaptation | That cancer category | Does supervised response knowledge transfer across indications? |
| Leave-one-drug/target-out | Exclude a therapy or checkpoint-target category | The excluded category | Does it transfer across treatment contexts? |
| Platform/site holdout | Exclude a sequencing platform or biopsy-site category | That category | How robust is prediction to these observed shifts? |

The 16-cohort transfer matrix contains $$16\times15=240$$ ordered source–target pairs. These pairs share cohorts and are therefore not 240 independent clinical studies. Likewise, repeated random seeds quantify optimization variability under the chosen data, not uncertainty across a new population of hospitals.

### Metrics and the reference-accuracy definition

Accuracy uses a fixed response-probability threshold of 0.5. AUROC measures ranking across thresholds; AUPRC emphasizes precision–recall behavior and is sensitive to response prevalence. Matthews correlation coefficient uses all four confusion-matrix cells and is useful under class imbalance. None of these alone measures probability calibration.

For a target-cohort responder fraction $$p$$, the paper defines

$$
\operatorname{ReferenceAccuracy}=p^2+(1-p)^2,
\qquad
\operatorname{ReferencePrecision}=p.
$$

The first is the expected accuracy of random labels sampled according to that cohort's prevalence. It is **not** the majority-class accuracy $$\max(p,1-p)$$. For example, at $$p=0.2$$, the reference is 0.68 whereas always predicting non-response gives 0.80. Consequently, “successful transfer,” defined as exceeding the paper's reference accuracy, should not be read as automatically exceeding the majority rule, being statistically significant, or delivering clinical utility.

### Baselines answer different comparison questions

The main benchmark includes gene markers, immune signatures, and integrative approaches. Many are passed through logistic-regression predictors; this compares feature systems under a common predictor family rather than simply using every historical tool's original decision threshold. The additional ENLIGHT/EaSIeR/IRnet comparison has its own constraints: retrainable methods use LOCO fitting, while some released predictors are applied as fixed tools.

A particularly useful architectural control is Supplementary Method S2: supply **the same logistic-regression model family** with fixed signature scores or learned COMPASS features. This isolates representation quality more directly than changing both the representation and classifier simultaneously. In the ten cohort rows reported in Tables S9–S10, high-level learned features yield mean AUROC 0.777 and AUPRC 0.642; high-level ssGSEA gives 0.695 and 0.528. These are averages across the displayed cohorts, not pooled patient-level metrics, and COMPASS does not win every cohort.

The main paper reports strong average improvements, but Supplementary Table S3 also shows substantially weaker performance in its six small cohorts: PFT AUROC is approximately 0.532 there. The evidence supports useful transfer on average under specified study splits, with important variation across target populations. [Main Methods, PDF pp. 17–18](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=18); [Supplement, Tables S3 and S9–S10, PDF pp. 43 and 46](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=46).

## 14. Ablations: which architectural choices matter
{: #ablations }

### 14.1 Granularity of the exported representation

Supplementary Fig. S1 compares NFT using 15,672 gene features, 133 granular features, and 44 high-level features. High-level representations generally perform favorably, but the comparisons do not show statistically significant superiority on every metric. For high-level versus gene features, the reported p-values are approximately 0.084 for accuracy, 0.0023 for MCC, 0.048 for AUROC, and 0.078 for PR-AUC, without multiplicity adjustment.

This is evidence about how useful a particular representation is under prototype inference. It does not prove that compressing any gene-expression model to 44 features will improve all downstream tasks.

### 14.2 Learned pooling versus conventional scoring

The supplement's “Average” comparator computes the mean of $$\log_2(\mathrm{TPM}+1)$$ across a gene set. It should not be casually rewritten as the geometric mean of untransformed TPM. The ssGSEA comparator instead uses rank/enrichment-based signature scores. Both provide fixed scoring rules, whereas COMPASS learns contextual gene vectors and a weighted hierarchical readout.

The common-classifier comparison therefore asks whether learning the representation adds value beyond merely choosing biologically sensible gene sets. Tables S9–S10 favor learned features on average, but Methods S2 refers to 16 cohorts while these tables display ten; numerical summaries should identify the population actually tabulated.

### 14.3 Cancer-type ablation

Removing the cancer input leaves substantial predictive performance under indication and checkpoint-target holdouts. This weakens a simple explanation that the full model only remembers cancer-specific response prevalence. It does not eliminate every route by which cancer type, assay, or cohort identity can be inferred from transcriptomic data.

The effect is also not uniformly positive in every category: in the small combination-target comparison, the ablated model has slightly higher reported average precision. Treat the ablation as a controlled comparison of an input feature under particular splits, not proof that the feature is always necessary.

### 14.4 Augmentation strength and negative hardness

Supplementary Figs. S36–S37 distinguish two aims that can conflict:

- **Frozen-feature usefulness:** strong perturbation generally hurts NFT, because the pretrained representation must work without clinical adaptation.
- **Adaptability after supervision:** stronger perturbation can improve PFT, particularly in the jitter sweep, even when frozen performance is worse.
- **Discriminating difficult neighbors:** local hard negatives generally improve transfer despite a harder self-supervised objective.

These sweeps use the reduced 2,475-gene setup and ten medium/large cohorts. They are controlled sensitivity experiments, not a license to transplant the best-looking point to every full-panel model or new dataset.

### 14.5 Fixed-score controls and holdout language

Supplementary Fig. S19 compares selected concept scores on a 226-patient holdout. Although its caption calls this external validation, Method S1 describes a random 20% split of the pooled 1,133 patients. It is a held-out patient subset, not a newly collected external cohort. This distinction matters because patients from the same study can remain in both partitions.

Together, these analyses support the value of learned biological representations and selected transfer strategies, while leaving questions about optimal concept definitions, alternative gene encoders, explanation faithfulness, and prospective transportability. [Supplement, Methods S1–S2 and S5, PDF pp. 48–52](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=48).

## 15. Concept interpretation, SHAP, and patient response maps
{: #interpretation }

The paper offers several complementary views of a prediction. They answer different questions and use different computations.

### 15.1 Concept scores describe the learned representation

A named score is the output of the encoder–projector, not an independent clinical measurement. Some concepts associated with non-response have inverse relationships with conventional infiltration or activity scores. For example, a learned B-cell-related coordinate may act as a deficiency-associated feature; a large positive value need not mean more B cells. Supplementary Fig. S23 is particularly helpful for understanding this orientation issue.

Overlapping signature membership also creates dependencies among concepts. In addition, encoder attention can distribute information across genes before pooling. Concepts therefore should not be assumed to be statistically independent simply because they appear as separate axes in a radar plot.

### 15.2 Kernel SHAP attributes model predictions

The Methods use Kernel SHAP, with a background formed by 100 k-means centroids, or all samples when fewer than 100 are available, to rank 44 concept features by mean absolute attribution. The reported pan-cancer analysis uses a PFT model trained on all ICI cohorts. It explains that fitted predictor; it is not a held-out performance estimate.

A SHAP value is defined relative to the model, background distribution, and missing-feature treatment. With correlated concepts, the allocation of attribution can depend on these choices. A high SHAP importance does not identify the effect of experimentally increasing or decreasing a biological pathway.

### 15.3 Response maps show several layers of patient features

The map follows an expression layer, contextual gene scores, granular signature scores, high-level scores, and the predicted response. A gene score is obtained by projecting a contextual gene vector through the scalar readout, treating that gene as a singleton set.

There is a useful algebraic reason this can be coherent. With a shared linear readout and normalized pooling weights,

$$
v^\top\!\left(\sum_g\alpha_g h_g\right)+b
=\sum_g\alpha_g(v^\top h_g+b),
$$

because $$\sum_g\alpha_g=1$$. Thus weighted vector pooling followed by this linear readout equals weighted pooling of the corresponding scalar gene scores. This is a teaching derivation; it does not turn a visualization edge into a causal coefficient.

### 15.4 Displayed edges are not the transformer's attention matrix

The response-map Methods state that displayed edge weights are estimated from **Pearson correlations across patients** between source and target node z-scores. The maps also show cohort-standardized node values, selecting genes or concepts by display thresholds such as $$\lvert z\rvert>1$$ or $$\lvert z\rvert>0.5$$.

Therefore:

- A patient's colored node describes a relative value compared with the chosen cohort.
- A map edge summarizes cross-patient covariation under the visualization procedure.
- A projector weight is a trainable aggregation parameter.
- A transformer attention weight is a patient-conditioned encoder computation.

These four quantities may be related, but they are not identical. Correlating a concept with the model's predicted response also examines internal representation–output association, not independent validation of the proposed mechanism.

### 15.5 What an interpretable prediction can support

A map can point to a testable hypothesis, such as an exclusion-associated program coexisting with cytotoxic activity. Establishing that this program causes resistance requires additional evidence. The paper acknowledges that explanation faithfulness was not established through concept perturbation/ablation and that learned concepts were not experimentally validated. This is a central limit of the architecture's interpretability claim, not merely a general caveat about AI. [Main Methods, PDF pp. 18–20](https://www.nature.com/articles/s41591-026-04502-7.pdf#page=19); [Supplement, Figs. S18 and S21–S27](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=21).

## 16. Survival analysis and the separate Clinical Transformer extension
{: #survival }

**The original COMPASS response classifier and the Clinical Transformer survival extension are different models.** The supplement evaluates whether learned COMPASS features are useful outside the original binary-response head. Reading every transformer hyperparameter in the supplement as a COMPASS encoder setting would give the wrong architecture.

### 16.1 Four routes from expression to a survival-related result

| Route | Representation | Prediction module | What is trained/predicted |
| --- | --- | --- | --- |
| Original response score | COMPASS concept vector | COMPASS response head | Response probability, subsequently assessed as a survival ranking/stratification score |
| Concept-based Cox model | COMPASS granular or high-level features | Ridge-regularized Cox model | A survival risk score fitted with survival outcomes |
| Fixed signatures + Clinical Transformer | 29 conventional or 43 COMPASS-defined ssGSEA signatures | Separate Clinical Transformer | Survival risk trained with a survival-specific objective |
| COMPASS + Clinical Transformer | Learned COMPASS concept features | Separate Clinical Transformer | A modular survival predictor using the learned representation |

The first route does not become a survival-time model merely because a C-index or Kaplan–Meier plot is computed from its predictions. Conversely, the other routes introduce a new prediction head and a new training objective.

### 16.2 The original response-score and ridge-Cox analyses

For the main IMvigor210 holdout, COMPASS-PFT is trained excluding that cohort. Its response probabilities split patients at $$P_R=0.5$$. The separate ridge-Cox analysis trains on other patients with available survival data, standardizes input features using training-fitted scalers, tunes regularization with five-fold validation, and applies the saved transformations to the test cohort.

The published Cox-group description refers to a “top 10% risk score cutoff,” while its reported test-group sizes place roughly 10% in the low-risk group. That wording does not uniquely specify a quantile rule under distribution shift. A reproduction should inspect the analysis code before assigning a precise cutoff direction from the caption alone.

Survival differences between predicted responders and non-responders demonstrate prognostic association among ICI-treated patients. Without a suitable non-ICI comparator, they do not isolate the incremental benefit attributable to ICI treatment.

### 16.3 Clinical Transformer architecture and training

**These settings belong to the Clinical Transformer experiment:** eight transformer layers, two attention heads, embedding dimension 128, masked-feature self-supervised pretraining, and selection of a 20,000-step checkpoint. They are not the original COMPASS Performer settings or its triplet objective.

The supplement compares 29 fixed ssGSEA inputs, 43 fixed scores from COMPASS's biological gene sets, and learned COMPASS concept inputs. In the last configuration, a pretrained COMPASS encoder–projector supplies features to a separately pretrained Clinical Transformer. Models are also evaluated without Clinical Transformer pretraining.

For each held-out clinical cohort, internal training/validation splits select the downstream duration, with ten independent splits and up to 300 epochs. A final model is fitted on the outer training data for the selected duration. The stated survival loss approximates the C-index. The source describes 860 patients with overall survival across 11 cohorts; TMB comparisons use a smaller, partly different subset.

### 16.4 Separate validation from held-out test results

Supplementary Table S11 reports validation performance; Table S12 reports held-out test performance. The COMPASS + Clinical Transformer transfer setup has mean validation C-index 0.638, but its mean held-out test C-index is 0.605. The original COMPASS-PFT response score has mean held-out C-index 0.610 in the reported table.

These numbers support the usefulness of learned concepts as transferable features, but they do not show that adding the Clinical Transformer universally outperforms the original response predictor. They also should not be combined with differently selected TMB subsets as if every score were evaluated on exactly the same patients.

The CSP pathway transformer is another external baseline applied from its released checkpoint; it is neither the COMPASS encoder nor an identical retraining control. [Supplement, Fig. S29, S31/PDF p. 32](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=32); [Methods S4 and Tables S11–S12, PDF pp. 47–51](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-026-04502-7/MediaObjects/41591_2026_4502_MOESM1_ESM.pdf#page=47).

## 17. Paper–code differences and reproduction requirements
{: #implementation }

The public implementation was inspected at commit [`0e5c87665247e3a300f28282c8bbcc14e26973bd`](https://github.com/mims-harvard/COMPASS/tree/0e5c87665247e3a300f28282c8bbcc14e26973bd), whose package version is **2.5.3**. The immutable [v2.0.5 source archive](https://files.pythonhosted.org/packages/e2/31/3ccc47c6c7227c4fc48ebb6736a20f827e2bc38f2e5f54b043a48881ce64/immuno_compass-2.0.5.tar.gz) was also inspected because the supplement names that version for sensitivity analyses. This was a source audit: checkpoints were not loaded and experiments were not rerun. The inspected code does not establish which exact configuration generated a published result.

### 17.1 Concrete implementation details

**Preprocessing.** `Datascaler` transforms gene values by $$\log_2(\mathrm{TPM}+1)$$, then applies the selected scaler, with MinMax scaling as the default. The cancer-code column is excluded. The shown pretraining path fits the scaler on training data, and the fine-tuner inherits it. This is different from the within-cohort z-scores used to color response maps. [Pinned scaler](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/model/scaler.py#L46).

**Extra token.** The code prepends a shared learned PID/CLS token in addition to the cancer token. The input sequence is therefore $$[\mathrm{PID},\mathrm{cancer},\mathrm{genes}]$$, of length $$L+2$$. PID is not a separately learned identifier for each patient: the same learned starting vector is expanded across the batch, then contextualized. The default projector excludes its scalar output but retains the cancer scalar, so the usual final representation remains 44-dimensional. The paper's main equations instead show $$L+1$$ tokens. [Pinned encoder](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/encoder/encoder.py#L135).

**Performer dimensions.** When the inspected pretrainer selects Performer with its default dimension settings, the model uses token width 32, one encoder layer, and two heads. However, the actual Performer head width defaults to **32 per head**, not $$32/2=16$$: query/key/value projections expand 32 to 64, reshape into two 32-dimensional heads, then project the concatenated result back to 32. The feedforward path is 32→64→32 with GELU, residual connections, and layer normalization. These are properties of the inspected implementation, not independently verified settings for every paper experiment. [Pinned attention implementation](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/encoder/layer/performer.py#L486).

**Projector.** Fixed membership is implemented through index gathering. The scalar reduction is shared across gene sets, with a separate cancer-token scalar projection. Current output ordering places the cancer score first; explanatory equations in these notes place it last only for readability. A saved classifier must receive the checkpoint's exact feature order. [Pinned projector](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/projector/projector.py#L189), [shared scalar readout](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/projector/genesetscorer.py#L55).

### 17.2 Material differences that affect algorithm behavior

| Item | Paper description | Inspected software behavior | Consequence for reproduction |
| --- | --- | --- | --- |
| LFT/PFT parameter control | Strictly freeze encoder and/or projector as specified in Section 10 | Core fine-tuner uses lower learning rates for those parameter groups, with default factor 0.1, rather than disabling their gradients | A mode name alone does not guarantee frozen weights |
| NFT class prototype | Mean of normalized support vectors within binary classes | Coordinatewise median by available RECIST category, then normalization | Different reference geometry |
| NFT query comparison | Cosine similarity of query and binary prototypes; typical temperature 0.1 | Remove the query's component along the mean-prototype direction; default temperature 0.001; combine category probabilities into R/NR | Different scores and potentially different predictions |
| Negative selection | Another tumor of the same cancer type in main pretraining prose | Core dataset samples expression-space neighbors without an explicit same-cancer restriction | Different contrastive learning problem |
| Encoder choice | Performer reported | Current constructor defaults to ordinary Transformer; notebook explicitly selects Performer | Loading current defaults is not sufficient to recreate the reported encoder |
| Response head | Equations show normalization and dense logits; prose mentions 16 hidden units and 182 LFT parameters | Current configurable head and historical v2.0.5 head differ; the reported width/count are not directly reconcilable | Inspect the checkpoint and model configuration |

The LFT/PFT distinction is especially consequential. A parameter with a small positive learning rate can still change. Setting batch-normalization or dropout modules to evaluation mode also does not disable parameter gradients; it controls their forward behavior. The inspected training loop calls `model.train()` as well. Strict reproduction of the paper's freeze definitions requires verifying parameter-group membership, `requires_grad`, and actual before/after weights. The historical v2.0.5 archive also contains the differential-learning-rate pattern, so attributing it solely to a later version would be unsupported. [Pinned optimizer groups](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/main.py#L742), [training loop](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/model/tune.py#L37).

Similarly, both inspected releases contain the median/projection-based NFT implementation. Section 11 explains the **reported paper algorithm**; it should not be used as a line-by-line description of this different decoder. [Pinned NFT decoder](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/decoder/decoder.py#L202).

For the parametric head, the current `[16]` configuration uses a hidden layer with normalization and ReLU; the no-hidden configuration follows a different path. The v2.0.5 decoder instead uses a gated linear component and a tanh residual branch. Consequently, “LFT has 182 parameters” should remain an author-reported number, not an arithmetic verification of the current head. [Pinned current decoder](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/compass/decoder/decoder.py#L24).

The current pretraining constructor, demonstration notebook, main Methods, and supplementary sweeps also use different learning rates, augmentation strengths, validation fractions, and optional loss settings. For example, the inspected constructor has learning rate $$10^{-5}$$, whereas the notebook sets $$10^{-4}$$ and the article reports $$10^{-3}$$. These are source-specific settings; none should silently replace another. The notebook's optional batch-correction setting likewise should not be promoted into a required component of the main paper's triplet objective. [Pinned pretraining notebook](https://github.com/mims-harvard/COMPASS/blob/0e5c87665247e3a300f28282c8bbcc14e26973bd/paper/00_pretrain/run_scripts/00_pretraining.ipynb).

### 17.3 Smaller reporting discrepancies to preserve

- **Atezolizumab test size:** the main Methods say 176 while listing 165+2 patients; Supplementary Table S7 gives 167. Another Results passage uses 89. These do not identify one unambiguous test denominator. Use the table-specific population when quoting that table, and verify analysis data for exact replication.
- **Signature benchmark size:** Methods S2 says 16 cohorts; Tables S9–S10 display ten. The means quoted in these notes refer to those ten rows.
- **Clinical Transformer caption:** Fig. S32's prose is inconsistent with the direction of changes in Table S11. Use the actual table values and distinguish validation from held-out testing.
- **Disease abbreviations:** Table S4 swaps BLCA and KIRC labels in two rows. BLCA denotes bladder/urothelial cancer and KIRC renal clear-cell cancer; do not reproduce the swapped labels.

These discrepancies limit exact reproduction from prose alone. They do not by themselves show that the scientific results are invalid, or identify which code path produced them.

## 18. A practical reconstruction of the pipeline
{: #recipe }

The following is **teaching pseudocode for the paper-described method**, not a claim that it reproduces every branch of the distributed package.

```text
Define the representation interface
    fix gene order and cancer-code vocabulary
    load gene-to-signature and signature-to-concept memberships
    construct encoder, hierarchical projector, and response head
    record checkpoint-compatible expression preprocessing

Pretrain
    split TCGA patients into training and validation sets
    fit preprocessing using training data only
    sample anchor, perturbed positive, and permitted negative patient
    encode all three with shared encoder/projector parameters
    compute triplet loss in final concept space
    update encoder and projector; choose checkpoint using validation loss

For each outer clinical holdout
    reserve the complete test cohort or target category
    choose training-only validation splits and adaptation settings
    if NFT:
        keep encoder/projector fixed
        derive prototypes using labeled training/support patients
    if LFT:
        keep encoder/projector fixed; train response head
    if PFT:
        keep encoder fixed; train projector and response head
    if FFT:
        train encoder, projector, and response head
    select settings without test labels
    apply saved preprocessing and evaluation-mode model to test patients
    report discrimination, calibration, prevalence, and uncertainty

For a new patient
    align genes and check supported cancer coding
    transform expression using the saved preprocessing object
    obtain contextual gene vectors and named concept scores
    apply the chosen trained head or labeled-support prototype rule
    return response score with the model version and feature definitions
```

Several implementation checks are essential to making this architecture concrete: confirm token and concept order; separate biological scores from the cancer channel; inspect whether “frozen” modules actually remain unchanged; ensure the NFT support set excludes the query label; preserve scalers and batch-normalization state; and state whether the predictor is a response head, a Cox model, or the Clinical Transformer extension.

A trustworthy reproduction should also save the outer cohort assignments and inner model-selection records. Otherwise, an accurately implemented neural network can still be evaluated under the wrong information boundary.

## 19. Methodological assessment and source map
{: #assessment }

COMPASS is most useful to understand as a **contextual expression encoder with a constrained, named readout interface**. Biological prior knowledge defines the hierarchy, while learning determines the representation values and their usefulness for prediction. The small output vector makes transfer and inspection practical; contrastive pretraining provides a way to learn that vector before collecting response labels.

The strongest architectural lesson is the separation of **representation learning**, **biological aggregation**, and **task adaptation**. Each can be examined independently: frozen-feature probes assess the pretrained representation; common-classifier controls compare feature systems; partial adaptation asks whether concept readout changes are sufficient; survival extensions test whether the same features help another outcome model.

The central interpretive limit is equally specific: named coordinates do not become experimentally validated mechanisms merely because the classifier has no bypass. Global contextualization can mix signals upstream, the concept scores have learned orientation, and response-map correlations are not causal effects. The lack of non-ICI comparator arms also means the response/prognosis signals cannot be cleanly separated into treatment-specific benefit. These constraints should guide how the architecture is studied and extended.

| Topic to revisit | Most useful source location |
| --- | --- |
| Complete model and transfer modes | Main Fig. 1, PDF pp. 2–3 |
| Gene tokenization and Performer | Main Methods, PDF p. 15 |
| Hierarchical weighted pooling and scalar bottleneck | Main Methods, PDF pp. 15–16 and 20 |
| Contrastive loss and adaptation settings | Main Methods, PDF p. 17 |
| NFT support and feature-level comparisons | Supplement Fig. S1, S3/PDF p. 4 |
| Validation and multi-stage adaptation | Main Methods, PDF p. 18; Supplement Table S7, S44/PDF p. 45 |
| Fixed-signature versus learned representations | Supplement Methods S1–S2, S47–S48/PDF pp. 48–49; Tables S9–S10, S45/PDF p. 46 |
| Interpretation and response maps | Main Methods, PDF pp. 18–20; Supplement Figs. S18 and S21–S27 |
| Clinical Transformer integration | Supplement Fig. S29, S31/PDF p. 32; Method S4, S48–S50/PDF pp. 49–51 |
| Survival validation versus test performance | Supplement Tables S11–S12, S46/PDF p. 47 |
| Calibration and decision curves | Supplement Fig. S35, S37/PDF p. 38 |
| Augmentation and hard-negative sweeps | Supplement Figs. S36–S37, S38–S39/PDF pp. 39–40; Method S5, S50–S51/PDF pp. 51–52 |
| Version-specific implementation behavior | [Pinned COMPASS source](https://github.com/mims-harvard/COMPASS/tree/0e5c87665247e3a300f28282c8bbcc14e26973bd), with file links in Section 17 |

The equations and small numerical examples in these notes explain the computational operations. They are not newly fitted patient results. The source audit identifies reproducibility questions rather than claiming an independent replication of the paper's reported performance.
