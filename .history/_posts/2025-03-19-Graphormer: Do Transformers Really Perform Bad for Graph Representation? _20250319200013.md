---
layout: post
title: (2021 NeurIPS) Graphormer - Do Transformers Really Perform Bad for Graph Representation?
description: A foundational paper on graph transformers, proposing centrality encoding and positional encoding.
date: 2025-03-19 19:51:00 +0300
image: '/images/post_5_1.png'
tags: [Method, Graph, Graph Transformer]
---

The Transformer architecture has become a dominant choice in various domains, such as natural language processing and computer vision. However, it has not achieved competitive performance on popular leaderboards for graph-level prediction compared to mainstream GNN variants, leaving its effectiveness in graph representation learning an open question. This paper addresses this challenge by introducing Graphormer, a model built upon the standard Transformer architecture that achieves outstanding results across a broad range of graph representation learning tasks, particularly in the recent OGB Large-Scale Challenge. The key insight behind utilizing Transformers for graphs lies in the necessity of effectively encoding structural information into the model. To this end, several simple yet effective structural encoding methods are proposed to enhance Graphormer’s ability to model graph-structured data.


![Precedures]({{site.baseurl}}/images/post_4_1.png)
*Model architecture.*

The authors first used a graph learner, chosen from two methods: full graph parametrization (using parameters to fill in the entire adjacency matrix, assuming independence between edges) and metric learning. The input to metric learning can be obtained from GNN and FFNN (which consist of several layers of feature abstraction).

Next, the node embeddings and the sketched adjacency matrix undergo post-processing, which includes the following steps: sparsification (using k-NN), symmetrization, activation (applying activation first, then averaging the symmetric positions in the matrix), and normalization (ensuring that the edge weights of a node sum to 1).

Since the authors are dealing with unsupervised graph structure learning, it is critical to derive a supervision signal from the data. They proposed a contrastive learning approach, where the learned graph structure serves as the learner view, and the graph structure from the data serves as the anchor view. If the original data does not contain a graph structure, the identity matrix is used as the anchor view.

Both the learner view and the anchor view graphs then undergo two post-processing steps: feature masking and edge dropping. Afterward, the node embeddings from both views pass through several layers of GNNs or FFNNs. Finally, the contrastive loss encourages the embeddings of the same node from both views to be similar. They employed a symmetric normalized temperature-scaled cross-entropy loss (NT-Xent).

Additionally, they gradually update the anchor view graph for two reasons: A fixed anchor graph contains limited information for guiding structure learning and may lead to overfitting to the anchor structure. The update is performed by adding the learned structure to the anchor graph every few steps.