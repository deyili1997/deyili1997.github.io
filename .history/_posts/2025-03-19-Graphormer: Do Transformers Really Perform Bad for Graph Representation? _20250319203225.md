---
layout: post
title: (2021 NeurIPS) Graphormer - Do Transformers Really Perform Bad for Graph Representation?
description: A foundational paper on graph transformers, proposing centrality encoding, positional encoding and edge encoding.
date: 2025-03-19 19:51:00 +0300
image: '/images/post_5_1.png'
tags: [Method, Graph, Graph Transformer]
---

The Transformer architecture has become a dominant choice in various domains, such as natural language processing and computer vision. However, it has not achieved competitive performance on popular leaderboards for graph-level prediction compared to mainstream GNN variants, leaving its effectiveness in graph representation learning an open question. This paper addresses this challenge by introducing Graphormer, a model built upon the standard Transformer architecture that achieves outstanding results across a broad range of graph representation learning tasks, particularly in the recent OGB Large-Scale Challenge. The key insight behind utilizing Transformers for graphs lies in the necessity of effectively encoding structural information into the model. To this end, several simple yet effective structural encoding methods are proposed to enhance Graphormer’s ability to model graph-structured data.

![Precedures]({{site.baseurl}}/images/post_5_1.png)
*Model architecture.*

1. Centrality encoding
The attention distribution of the original Transformer is based on the semantic relationships between nodes. However, traditional attention calculation ignores node degree, which is crucial in graph structures. To address this, the authors introduce centrality encoding, where each node is assigned two real-valued embedding vectors representing in-degree and out-degree. For undirected graphs, a single degree embedding is used.

2. Spatial encoding
The authors propose using a bias term to adjust the attention scores before applying softmax. For a given node attending to others, the shortest path between each pair of nodes is computed, with different shortest paths corresponding to different learnable scalar parameters. In other words, the bias term is parameterized by a set of learnable scalar parameters, with the number of parameters determined by the maximum of all shortest path lengths. Each parameter corresponds to the shortest path distance between the row node and the column node in the attention matrix.

3. Edge encoding
The authors further propose edge encoding to incorporate edge information into the attention score matrix. Similarly, a bias term is added to the attention score between a pair of nodes in addition to the spatial encoding. Like spatial encoding, each shortest path distance is associated with a unique learnable weight vector. For each edge along the shortest path between a pair of nodes, the sum of the products of the corresponding weight vector and the edge feature at each distance is computed, effectively integrating edge attributes into the attention mechanism.