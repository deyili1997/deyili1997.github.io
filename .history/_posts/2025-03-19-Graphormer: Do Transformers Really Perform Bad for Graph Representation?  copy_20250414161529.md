---
layout: post
title: (2024 NeurIPS) Leveraging Contrastive Learning for Enhanced Node Representations in Tokenized Graph Transformers
description: A graph transformer model leveraging contrastive learning.
date: 2025-04-14 19:51:00 +0300
image: '/images/post_6_1.png'
tags: [Method, Graph, Graph Transformer]
---

This study still focuses on new design of graph transformer for caputuring local and global information of a graph. The performance is measured by node prediciton tasks.

![Precedures]({{site.baseurl}}/images/post_6_1.png)
*Model architecture.*

In addition to the original node features, the authors employed multiple layers of a traditional Graph Neural Network (GNN) to incorporate topological information into node representations—that is, each node’s representation was updated to reflect its local neighborhood structure. The subsequent procedures were applied in parallel to both the original feature space and the topology-enriched feature space.

To implement contrastive learning, the model selected the top-k most similar nodes to a given target node based on cosine similarity computed across all node pairs, resulting in a computational complexity of O(N²). These top-k nodes constituted the positive set, while the remaining nodes formed the negative set.

For both the original and topology-based features, the target node, its positive set, and its negative set were concatenated into a sequence. Each sequence was then passed through a dense layer to produce the input embeddings for a Transformer encoder. Next, within this resutling sequence, the target node and its positive set were separated from the negative set. A virtual token was prepended to the negative sequence to encode global context information across the negative set.

The final representation of the target node based on the original feature space was derived by subtracting the output representation of the virtual token (from the negative set) from the final-layer representation of the target node. This subtraction aims to adjust the target node representation by accounting for global negative context, though the precise theoretical motivation requires further investigation and may draw on prior contrastive learning literature.

The same process was performed on the topology-based features, and the two resulting target node representations (original feature-based and topology-based) were linearly combined using a learnable or fixed weighting factor (treated as a hyperparameter).

The model was trained using a combination of contrastive loss and supervised classification loss to jointly optimize the quality of node representations and predictive performance.