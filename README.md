# Privacy Posture Framework (PPF)

A policy-driven framework for modelling, checking, simulating and
monitoring organisational privacy posture.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-research-orange)

---

## Overview

The **Privacy Posture Framework (PPF)** is a research prototype for
assessing how effectively an organisation's privacy controls protect
personal data across its lifecycle.

The framework combines:

- machine-readable privacy schemas;
- policy-driven privacy manifests;
- static privacy control checking;
- lifecycle-based workflow simulation;
- DEAR-inspired monitoring;
- violation detection;
- simulated remediation;
- quantitative posture scoring; and
- cross-domain evaluation.

The current implementation demonstrates the approach using three
synthetic organisational environments:

1. **GP Surgery**
2. **School**
3. **Hotel**

The framework is intended for:

- academic research;
- privacy engineering experimentation;
- reproducible evaluation;
- teaching and demonstration; and
- development of policy-aware privacy assessment techniques.

It is **not** intended to provide legal advice or certify regulatory
compliance.

---

# Research Motivation

Traditional privacy assessments are often:

- document-centric;
- manually performed;
- difficult to reproduce;
- dependent on expert interpretation; and
- separated from operational system behaviour.

PPF explores an alternative approach in which privacy requirements are
represented as machine-readable policies and evaluated against
structured organisational scenarios.

The framework treats privacy posture as a combination of:

```text
Organisation
      |
      +-- Policies
      |
      +-- Security Controls
      |
      +-- Infrastructure
      |
      +-- Actors
      |
      +-- Personal Data
      |
      +-- Data Flows
      |
      +-- Processing Activities
      |
      +-- Privacy Events
      |
      +-- Violations