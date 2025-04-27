---
layout: post
title: (2024 KDD) A Survey on Hypergraph Neural Networks An In-Depth and Step-by-Step Guide
description: A survey on HNN architectures, training strategies, and applications.
date: 2025-04-27 14:23:00 +0300
image: '/images/post_7_1.png'
tags: [Survey, Graph, Graph Transformer]
---


![Precedures]({{site.baseurl}}/images/post_7_2.png)
*Taxonomy on modeling higher-order interactions.*

1. How do HNNs effectively capture HOIs?
1.1. Design features to reflect HOIs
(1) External features or labels: Using external features allows HNNs to capture information that may not be transparent in hypergraph structure alone. When available, using external node features X and hyperedge features Y as HNN input is the standard practice. respectively. Since external hyperedge features are typically missing in the benchmark datasets, in practice, input features can be obtained by averaging its constituent nodes.
(2) Structural features: On top of external features, studies have also utilized structural features as HNN input features. Structural features are typically derived from the input hypergraph structure E to capture structural proximity or similarity between nodes. While leveraging them in addition to the structure E may seem redundant, several studies have highlighted their theoretical and empirical advantages, particularly for hyperedge prediction and for transformer-based HNNs. See HyperGT, WHATsNet, THTN.

2. How to encode HOIs with training objectives, especially when external labels are scarce or absent?