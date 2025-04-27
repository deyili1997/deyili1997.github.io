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
(1) External features or labels: Using external features allows HNNs to capture information that may not be transparent in hypergraph structure alone. When available, using external node features X and hyperedge features Y as HNN input is the standard practice.

2. How to encode HOIs with training objectives, especially when external labels are scarce or absent?