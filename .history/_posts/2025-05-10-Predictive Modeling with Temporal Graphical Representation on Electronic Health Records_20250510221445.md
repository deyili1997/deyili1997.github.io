---
layout: post
title: (2024 IJCAI) Predictive Modeling with Temporal Graphical Representation on Electronic Health Records
description: A Novel Electronic Health Record Modeling Framework Using Heterogeneous Graph Representations and Temporally-Aware Attention Mechanisms.
image: '/images/post_8_1.png'
tags: [Method, EHR, Graph]
---

Deep learning-based predictive models that leverage Electronic Health Records (EHR) are gaining increasing attention in the healthcare domain. An effective representation of a patient’s EHR should hierarchically capture both the temporal relationships among historical visits and medical events, as well as the inherent structural information within these elements. Existing methods for patient representation can be broadly categorized into sequential and graphical approaches. Sequential representation methods primarily focus on the temporal relationships among longitudinal visits, whereas graphical representation methods are effective at extracting graph-structured relationships among medical events but often fail to adequately incorporate temporal dynamics. To address this limitation, the authors propose modeling a patient’s EHR as a novel temporal heterogeneous graph that includes nodes for both historical visits and medical events. This graph structure enables the propagation of structured information from medical event nodes to visit nodes and employs time-aware visit nodes to capture changes in the patient’s health status over time. Additionally, the authors introduce a temporal graph transformer (TRANS), which integrates temporal edge features, global positional encoding, and local structural encoding within a heterogeneous graph convolution framework to jointly capture temporal and structural information. The effectiveness of the proposed TRANS model is validated through extensive experiments on three real-world datasets, demonstrating state-of-the-art performance.



1. Prediction task: visit-level diagnosis prediciton, code-level diagnosis prediciton.
2. Datasets: MIMIC-III, MIMIC-IV and CCAE.
3. Graph Construction: There are three types of medical codes: diagnosis, medication, and procedure. Each patient visit is represented by a separate node. Every medical code is connected to its corresponding patient visit node via an undirected edge. Additionally, each patient visit node points to the subsequent visit node, forming a directed edge. Interestingly, if two adjacent visits share the same medical code, they appear to share the same code node.

![Precedures]({{site.baseurl}}/images/post_8_2.png)
*Model architecture.*

4. Temporal encoding: Embeddings derived from Time2vec was concatenated with patient visit node features.
5. Spatial encoding: 

