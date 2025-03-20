---
layout: post
title: (2021 NeurIPS) Graphormer - Do Transformers Really Perform Bad for Graph Representation?
description: A foundational paper on graph transformers, proposing centrality encoding and positional encoding.
date: 2025-02-22 19:12:00 +0300
image: '/images/post_4_1.png'
tags: [Method, Graph]
---

The authors present graph neural networks (GNNs) as a powerful tool for various graph-related applications but highlight their vulnerability to noisy connections in original graph structures and their dependency on explicit structures, which limits their applicability to unstructured scenarios. To address these challenges, they discuss deep graph structure learning (GSL) methods that jointly optimize graph structures with GNNs under the supervision of a node classification task; however, they note that existing methods suffer from reliance on labels, edge distribution bias, and limitations on application tasks. In response, the authors propose a more practical paradigm, unsupervised graph structure learning (GSL), where the learned graph topology is optimized solely by the data itself without external guidance. They introduce StrUcture Bootstrapping contrastive LearnIng fraMEwork (SUBLIME), a novel approach that incorporates self-supervised contrastive learning by generating an “anchor graph” from the original data and applying contrastive loss to maximize agreement between the anchor graph and the learned graph. To ensure continuous improvement, they design a bootstrapping mechanism that updates the anchor graph with learned structures during training, along with various graph learners and post-processing schemes to model structural learning effectively. Through extensive experiments on eight benchmark datasets, the authors demonstrate the significant effectiveness of SUBLIME and the high quality of the optimized graphs.

![Precedures]({{site.baseurl}}/images/post_4_1.png)
*Model architecture.*

The authors first used a graph learner, chosen from two methods: full graph parametrization (using parameters to fill in the entire adjacency matrix, assuming independence between edges) and metric learning. The input to metric learning can be obtained from GNN and FFNN (which consist of several layers of feature abstraction).

Next, the node embeddings and the sketched adjacency matrix undergo post-processing, which includes the following steps: sparsification (using k-NN), symmetrization, activation (applying activation first, then averaging the symmetric positions in the matrix), and normalization (ensuring that the edge weights of a node sum to 1).

Since the authors are dealing with unsupervised graph structure learning, it is critical to derive a supervision signal from the data. They proposed a contrastive learning approach, where the learned graph structure serves as the learner view, and the graph structure from the data serves as the anchor view. If the original data does not contain a graph structure, the identity matrix is used as the anchor view.

Both the learner view and the anchor view graphs then undergo two post-processing steps: feature masking and edge dropping. Afterward, the node embeddings from both views pass through several layers of GNNs or FFNNs. Finally, the contrastive loss encourages the embeddings of the same node from both views to be similar. They employed a symmetric normalized temperature-scaled cross-entropy loss (NT-Xent).

Additionally, they gradually update the anchor view graph for two reasons: A fixed anchor graph contains limited information for guiding structure learning and may lead to overfitting to the anchor structure. The update is performed by adding the learned structure to the anchor graph every few steps.