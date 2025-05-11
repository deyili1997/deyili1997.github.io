---
layout: post
title: (2024 IJCAI) Predictive Modeling with Temporal Graphical Representation on Electronic Health Records
description: A Novel Electronic Health Record Modeling Framework Using Heterogeneous Graph Representations and Temporally-Aware Attention Mechanisms.
image: '/images/post_8_1.png'
tags: [Method, EHR, Graph]
---

Deep learning-based predictive models that leverage Electronic Health Records (EHR) are gaining increasing attention in the healthcare domain. An effective representation of a patient’s EHR should hierarchically capture both the temporal relationships among historical visits and medical events, as well as the inherent structural information within these elements. Existing methods for patient representation can be broadly categorized into sequential and graphical approaches. Sequential representation methods primarily focus on the temporal relationships among longitudinal visits, whereas graphical representation methods are effective at extracting graph-structured relationships among medical events but often fail to adequately incorporate temporal dynamics. To address this limitation, the authors propose modeling a patient’s EHR as a novel temporal heterogeneous graph that includes nodes for both historical visits and medical events. This graph structure enables the propagation of structured information from medical event nodes to visit nodes and employs time-aware visit nodes to capture changes in the patient’s health status over time. Additionally, the authors introduce a temporal graph transformer (TRANS), which integrates temporal edge features, global positional encoding, and local structural encoding within a heterogeneous graph convolution framework to jointly capture temporal and structural information. The effectiveness of the proposed TRANS model is validated through extensive experiments on three real-world datasets, demonstrating state-of-the-art performance.

![Precedures]({{site.baseurl}}/images/post_8_1.png)
*Model architecture.*

1. How do HNNs effectively capture HOIs?
1.1. Design features to reflect HOIs
(1) External features or labels: Using external features allows HNNs to capture information that may not be transparent in hypergraph structure alone. When available, using external node features X and hyperedge features Y as HNN input is the standard practice. respectively. Since external hyperedge features are typically missing in the benchmark datasets, in practice, input features can be obtained by averaging its constituent nodes.

(2) Structural features: On top of external features, studies have also utilized structural features as HNN input features. Structural features are typically derived from the input hypergraph structure E to capture structural proximity or similarity between nodes. While leveraging them in addition to the structure E may seem redundant, several studies have highlighted their theoretical and empirical advantages, particularly for hyperedge prediction and for transformer-based HNNs. See HyperGT, WHATsNet, THTN.

(3) Identity features: Some HNNs use identity features, especially for recommendation applications. Generally, identity features refer to features uniquely assigned to each node (and hyperedge), enabling HNNs to learn distinct embeddings for each node (and hyperedge). Prior studies have typically used randomly generated features or separately learnable ones.

![Precedures]({{site.baseurl}}/images/post_7_3.png)
*Summary of hypergraph neural networks (HNNs).*

1.2. Express hypergraphs to reflect HOIs
(1) Reductive transformation: Clique expansion.
(2) Non-reductive transformation: Star expansion (resulting a bipartile graph, without information loss) 

1.3. Pass messages to reflect HOIs
Three questions arise: (i) whose messages should be aggregated? (ii) what messages should be aggregated? (iii) how should they be aggregated?
(i) On star-expansion graph: sequentially (ED-HNN) or simultaneously (HDS_ODE).
(ii) What messages to aggregate: HNNs typically use embeddings from the previous layer as messages, which are termed hyperedge-consistent messages. In contrast, several recent studies propose adaptive message transformation based on the target, referred to as hyperedge-dependent messages.
(iii) How to aggregate messages: Fixed pooling, Learnable pooling (Target-agnostic attention functions consider the relations among messages themselves. e.g., AllSetTransformer. Target-aware attention approaches, target information is incorporated to compute attention weights. e.g., HyGNN).


2. How to encode HOIs with training objectives, especially when external labels are scarce or absent?
2.1. Learning to classify: Classify manually-created fake hyperedges.
2.2. Learning to contrast: Apply contrastive loss for both nodes and hyperedges.
2.3. Learning to generate: HNNs can also be trained by learning to generate hyperedges. Existing HNNs aim to generate either ground-truth hyperedges to capture their characteristics or latent hyperedges potentially beneficial for designated downstream tasks.

