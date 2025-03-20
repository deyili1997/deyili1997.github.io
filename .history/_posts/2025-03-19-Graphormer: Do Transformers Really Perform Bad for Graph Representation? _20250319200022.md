---
layout: post
title: (2021 NeurIPS) Graphormer - Do Transformers Really Perform Bad for Graph Representation?
description: A foundational paper on graph transformers, proposing centrality encoding and positional encoding.
date: 2025-03-19 19:51:00 +0300
image: '/images/post_5_1.png'
tags: [Method, Graph, Graph Transformer]
---

The Transformer architecture has become a dominant choice in various domains, such as natural language processing and computer vision. However, it has not achieved competitive performance on popular leaderboards for graph-level prediction compared to mainstream GNN variants, leaving its effectiveness in graph representation learning an open question. This paper addresses this challenge by introducing Graphormer, a model built upon the standard Transformer architecture that achieves outstanding results across a broad range of graph representation learning tasks, particularly in the recent OGB Large-Scale Challenge. The key insight behind utilizing Transformers for graphs lies in the necessity of effectively encoding structural information into the model. To this end, several simple yet effective structural encoding methods are proposed to enhance Graphormer’s ability to model graph-structured data.

![Precedures]({{site.baseurl}}/images/post_5_1.png)
*Model architecture.*

