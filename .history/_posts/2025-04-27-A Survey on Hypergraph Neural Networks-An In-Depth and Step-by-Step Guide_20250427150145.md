---
layout: post
title: (2024 KDD) A Survey on Hypergraph Neural Networks An In-Depth and Step-by-Step Guide
description: A survey on HNN architectures, training strategies, and applications.
date: 2025-04-27 14:23:00 +0300
image: '/images/post_7_1.png'
tags: [Survey, Graph, Graph Transformer]
---

Higher-order interactions (HOIs) are ubiquitous in real-world complex systems and applications. Consequently, the investigation of deep learning methods for HOIs has become a valuable agenda for the data mining and machine learning communities. As networks of HOIs are mathematically expressed as hypergraphs, hypergraph neural networks (HNNs) have emerged as powerful tools for representation learning on hypergraphs. Given this emerging trend, the authors present the first survey dedicated to HNNs, providing an in-depth and step-by-step guide. Broadly, the survey overviews HNN architectures, training strategies, and applications. First, it breaks existing HNNs down into four design components: (i) input features, (ii) input structures, (iii) message-passing schemes, and (iv) training strategies. Second, it examines how HNNs address and learn HOIs through each of these components. Third, it reviews recent applications of HNNs in areas such as recommendation, bioinformatics and medical science, time series analysis, and computer vision. Lastly, the survey concludes with a discussion on current limitations and future directions.

![Precedures]({{site.baseurl}}/images/post_7_2.png)
*Taxonomy on modeling higher-order interactions.*

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
2.3. Learning to generate: 

