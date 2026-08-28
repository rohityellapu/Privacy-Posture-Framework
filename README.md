# Privacy Posture Framework (PPF)

A policy-driven framework for modelling, checking, simulating and monitoring organisational privacy posture.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![JSON%20Schema](https://img.shields.io/badge/JSON%20Schema-Draft%202020--12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Research Motivation](#research-motivation)
3. [Framework Architecture](#framework-architecture)
4. [Core Components](#core-components)
5. [Privacy Lifecycle](#privacy-lifecycle)
6. [Repository Structure](#repository-structure)
7. [System Requirements](#system-requirements)
8. [Installation](#installation)
9. [Virtual Environment Setup](#virtual-environment-setup)
10. [Install Dependencies](#install-dependencies)
11. [Verify Installation](#verify-installation)
12. [Project Configuration](#project-configuration)
13. [Validate the JSON Schema](#validate-the-json-schema)
14. [Validate All Use Cases](#validate-all-use-cases)
15. [Run the Privacy Checker](#run-the-privacy-checker)
16. [Run the GP Simulation](#run-the-gp-simulation)
17. [Run the School Simulation](#run-the-school-simulation)
18. [Run the Hotel Simulation](#run-the-hotel-simulation)
19. [Run the Runtime Monitor](#run-the-runtime-monitor)
20. [Run the Integrated Evaluator](#run-the-integrated-evaluator)
21. [Run the Complete Experiment](#run-the-complete-experiment)
22. [Testing](#testing)
23. [Reproducibility](#reproducibility)
24. [Generated Outputs](#generated-outputs)
25. [Understanding the Results](#understanding-the-results)
26. [Static Posture Score](#static-posture-score)
27. [Runtime Compliance](#runtime-compliance)
28. [DEAR Monitoring](#dear-monitoring)
29. [Use Cases](#use-cases)
30. [Regulatory Context](#regulatory-context)
31. [Example Workflow](#example-workflow)
32. [Docker](#docker)
33. [Troubleshooting](#troubleshooting)
34. [Limitations](#limitations)
35. [Future Work](#future-work)
36. [Research Contribution](#research-contribution)
37. [Security and Privacy](#security-and-privacy)
38. [Citation](#citation)
39. [License](#license)
40. [Disclaimer](#disclaimer)

---

# Overview

The **Privacy Posture Framework (PPF)** is a research prototype for representing, evaluating, simulating and monitoring organisational privacy posture across the personal-data lifecycle.

The framework combines:

- machine-readable privacy schemas;
- privacy manifests;
- static privacy-control checking;
- lifecycle-based workflow simulation;
- Finite State Machine (FSM) modelling;
- DEAR-inspired runtime monitoring;
- privacy violation detection;
- simulated remediation;
- quantitative posture scoring; and
- cross-sector evaluation.

The current prototype demonstrates the framework using three synthetic organisational environments:

1. **GP Surgery**
2. **School**
3. **Hotel**

PPF is intended for academic research, privacy engineering experimentation, reproducible evaluation and demonstration.

> **Important:** PPF is a research prototype. It does not provide legal advice, regulatory certification, or assurance that a real organisation is compliant with GDPR, the UK Data Protection Act 2018, NHS DSPT, DfE requirements, PCI-DSS or any other regulatory framework.

---

# Research Motivation

Privacy assessment is often performed using:

- documentation;
- manual audits;
- questionnaires;
- policy reviews; and
- isolated technical assessments.

These approaches can make it difficult to continuously connect:

```text
Privacy Policy
      |
      v
Organisational Controls
      |
      v
System Configuration
      |
      v
Operational Behaviour
      |
      v
Privacy Violations
```

PPF explores a policy-driven alternative in which privacy requirements are represented as machine-readable policies and evaluated against structured organisational environments.

The framework additionally introduces a simulated operational layer to evaluate how privacy posture behaves during data-processing activities.

---

# Framework Architecture

The overall architecture is:

```text
                     +----------------------+
                     |   Privacy Schema     |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |    Use Case JSON     |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |  Privacy Manifest    |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |  Static Privacy     |
                     |      Checker        |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Static Posture Score |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |    FSM Simulator     |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |   Activity Logs      |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |   DEAR Monitor       |
                     | Detect                |
                     | Evaluate              |
                     | Act - Simulated      |
                     | Report               |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Runtime Metrics      |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Integrated Evaluator |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Combined Evaluation  |
                     +----------------------+
```

---

# Core Components

## 1. Privacy Schema

The JSON Schema defines the structure of an organisational privacy use case.

The schema represents:

```text
Organisation
Environment
System
Data Flows
Personal Data
Regulatory Context
Privacy Controls
```

The project uses JSON Schema Draft 2020-12.

---

## 2. Privacy Manifest

A manifest defines the privacy requirements expected for a particular use case.

Examples include:

```text
Encryption
Authentication
Access Control
Pseudonymisation
Consent
Retention
Deletion
Data Sharing
DPO
PIA/DPIA
Organisational Policies
```

The manifest therefore represents the expected privacy posture.

---

## 3. Static Privacy Checker

The static checker compares the use-case configuration against its manifest.

The checker evaluates controls such as:

```text
Encryption
Authentication
Access Control
Pseudonymisation
Policies
Consent
Data Flows
DPO
Non-negotiable Controls
```

Each finding is classified as:

```text
PASS
FAIL
WARNING
INFO
```

---

## 4. FSM Simulator

The FSM simulator generates synthetic privacy-related activity.

The lifecycle contains states such as:

```text
IDLE
DATA_COLLECTION
DATA_STORAGE
DATA_ACCESS
DATA_SHARING
DATA_RETENTION_REVIEW
DATA_DELETION
COMPLIANCE_CHECK
INCIDENT_DETECTED
INCIDENT_RESOLVED
```

The simulator generates structured events containing information such as:

```text
Timestamp
Lifecycle State
Actor
Role
Data Type
Event Type
Privacy Flags
```

---

## 5. DEAR Monitor

The runtime monitor follows a DEAR-inspired process:

```text
D = Detect
E = Evaluate
A = Act
R = Report
```

### Detect

Identifies privacy-relevant signals.

Examples:

```text
CONSENT_MISSING
SENSITIVE_DATA_UNENCRYPTED
UNAUTHENTICATED_ACCESS
UNLOGGED_ACCESS
DPA_MISSING
NO_LEGAL_BASIS_FOR_SHARING
RETENTION_POLICY_NOT_APPLIED
INSECURE_DELETION
COMPLIANCE_CHECK_FAILED
```

### Evaluate

The monitor evaluates the detected event and determines:

- violation type;
- severity;
- lifecycle stage;
- recommended action; and
- compliance context.

### Act

The current implementation **simulates** remediation.

Examples include:

```text
SESSION_REVOKED
SHARING_SUSPENDED
DATA_SUPPRESSED
TRANSFER_BLOCKED
RETENTION_REVIEW_TRIGGERED
COMPLIANCE_ESCALATION
```

The prototype does not modify live organisational systems.

### Report

The monitor produces structured reports containing:

- violation signals;
- violating events;
- compliance;
- severity;
- lifecycle distribution;
- violation categories; and
- simulated remediation actions.

---

# Privacy Lifecycle

PPF models the personal-data lifecycle as:

```text
+----------------+
| Data Collection|
+-------+--------+
        |
        v
+----------------+
| Data Storage   |
+-------+--------+
        |
        v
+----------------+
| Data Access    |
+-------+--------+
        |
        v
+----------------+
| Data Sharing   |
+-------+--------+
        |
        v
+----------------+
| Retention      |
+-------+--------+
        |
        v
+----------------+
| Data Deletion  |
+----------------+
```

Privacy controls can therefore be evaluated at different points in the data lifecycle.

---

# Repository Structure

The repository is organised into implementation, configuration, documentation, testing and experimental components.

```text
privacy-posture-framework/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── Dockerfile
├── docker-compose.yml
│
├── privacy_schema.json
│
├── manifest_gp.json
├── manifest_school.json
├── manifest_hotel.json
│
├── use_case_gp.json
├── use_case_school.json
├── use_case_hotel.json
│
├── privacy_checker.py
├── privacy_fsm_simulation.py
├── privacy_monitor.py
├── privacy_evaluator.py
│
├── docs/
│   ├── architecture.md
│   ├── schema.md
│   ├── manifests.md
│   ├── checker.md
│   ├── simulator.md
│   ├── monitor.md
│   ├── evaluation.md
│   └── diagrams/
│
├── configs/
│   ├── gp_surgery.yaml
│   ├── school.yaml
│   ├── hotel.yaml
│   └── default.yaml
│
├── manifests/
│   ├── gp_manifest.yaml
│   ├── school_manifest.yaml
│   ├── hotel_manifest.yaml
│   └── rules.yaml
│
├── data/
│   ├── logs/
│   ├── reports/
│   └── samples/
│
├── src/
│   └── ppf/
│       ├── __init__.py
│       │
│       ├── schema/
│       │   ├── models.py
│       │   ├── parser.py
│       │   ├── validator.py
│       │   ├── ontology.py
│       │   └── enums.py
│       │
│       ├── manifests/
│       │   ├── loader.py
│       │   ├── compiler.py
│       │   └── generator.py
│       │
│       ├── checker/
│       │   ├── checker.py
│       │   ├── report.py
│       │   ├── posture.py
│       │   ├── engine.py
│       │   └── rules/
│       │       ├── base_rule.py
│       │       ├── encryption.py
│       │       ├── authentication.py
│       │       ├── retention.py
│       │       ├── deletion.py
│       │       ├── sharing.py
│       │       ├── access.py
│       │       ├── consent.py
│       │       └── minimisation.py
│       │
│       ├── simulator/
│       │   ├── graph.py
│       │   ├── fsm.py
│       │   ├── workflow.py
│       │   ├── actors.py
│       │   ├── generator.py
│       │   ├── logger.py
│       │   └── scenarios/
│       │       ├── gp.py
│       │       ├── school.py
│       │       └── hotel.py
│       │
│       ├── monitor/
│       │   ├── lifecycle.py
│       │   ├── monitor.py
│       │   ├── alerts.py
│       │   ├── compliance.py
│       │   └── correlation.py
│       │
│       ├── evaluation/
│       │   ├── metrics.py
│       │   ├── benchmark.py
│       │   ├── experiments.py
│       │   ├── plots.py
│       │   └── posture_score.py
│       │
│       ├── utils/
│       │   ├── logging.py
│       │   ├── yaml.py
│       │   ├── graph.py
│       │   └── timer.py
│       │
│       └── cli.py
│
├── tests/
│   ├── schema/
│   ├── checker/
│   ├── simulator/
│   ├── monitor/
│   └── evaluation/
│
├── notebooks/
│   ├── experiment1.ipynb
│   ├── experiment2.ipynb
│   ├── experiment3.ipynb
│   └── benchmark.ipynb
│
└── examples/
    ├── gp_demo.py
    ├── school_demo.py
    └── hotel_demo.py
```

---

# System Requirements

## Operating System

PPF can be run on:

- Windows 10/11
- Linux
- macOS

## Python

Recommended:

```text
Python 3.11 or later
```

Check your Python version:

```bash
python --version
```

If `python` does not work on Linux/macOS, try:

```bash
python3 --version
```

---

# Installation

## Step 1 — Clone the Repository

Open a terminal or PowerShell window.

Run:

```bash
git clone https://github.com/rohityellapu/Privacy-Posture-Framework.git
```

Move into the project directory:

```bash
cd Privacy-Posture-Framework
```

Verify that you are in the correct directory:

```bash
dir
```

On Linux/macOS:

```bash
ls
```

You should see files such as:

```text
README.md
requirements.txt
privacy_schema.json
privacy_checker.py
privacy_fsm_simulation.py
privacy_monitor.py
privacy_evaluator.py
```

---

# Virtual Environment Setup

Using a virtual environment is recommended.

## Windows

Create the environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

You should now see something similar to:

```text
(.venv)
```

at the beginning of your terminal prompt.

---

## Linux/macOS

Create the environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## Deactivate the environment

When finished:

```bash
deactivate
```

---

# Install Dependencies

With the virtual environment activated, run:

```bash
pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

If the project metadata is configured for package installation, you can also install the project in editable mode:

```bash
pip install -e .
```

---

# Verify Installation

Check Python:

```bash
python --version
```

Check installed packages:

```bash
pip list
```

The environment should contain the packages specified by:

```text
requirements.txt
```

The framework uses dependencies for areas including:

```text
JSON Schema validation
YAML processing
Graph processing
Numerical evaluation
Data analysis
Plotting
Testing
```

---

# Project Configuration

Before running experiments, verify the following files exist:

```text
privacy_schema.json

manifest_gp.json
manifest_school.json
manifest_hotel.json

use_case_gp.json
use_case_school.json
use_case_hotel.json
```

Also verify the data directories:

```text
data/
data/logs/
data/reports/
data/samples/
```

If they do not exist, create them.

### Windows

```powershell
mkdir data
mkdir data\logs
mkdir data\reports
mkdir data\samples
```

### Linux/macOS

```bash
mkdir -p data/logs
mkdir -p data/reports
mkdir -p data/samples
```

---

# Validate the JSON Schema

The first step before running the framework is validating the use-case files against the schema.

The schema file is:

```text
privacy_schema.json
```

The use-case files are:

```text
use_case_gp.json
use_case_school.json
use_case_hotel.json
```

---

## Python validation method

You can validate a use case using the Python `jsonschema` package.

Example:

```bash
python -c "import json; from jsonschema import Draft202012Validator; s=json.load(open('privacy_schema.json')); d=json.load(open('use_case_gp.json')); e=list(Draft202012Validator(s).iter_errors(d)); print('VALID' if not e else e)"
```

For School:

```bash
python -c "import json; from jsonschema import Draft202012Validator; s=json.load(open('privacy_schema.json')); d=json.load(open('use_case_school.json')); e=list(Draft202012Validator(s).iter_errors(d)); print('VALID' if not e else e)"
```

For Hotel:

```bash
python -c "import json; from jsonschema import Draft202012Validator; s=json.load(open('privacy_schema.json')); d=json.load(open('use_case_hotel.json')); e=list(Draft202012Validator(s).iter_errors(d)); print('VALID' if not e else e)"
```

Expected result:

```text
VALID
```

---

# Validate All Use Cases

Run all three checks:

```bash
python -c "import json; from jsonschema import Draft202012Validator; s=json.load(open('privacy_schema.json')); [print(f'{f}:', 'VALID' if not list(Draft202012Validator(s).iter_errors(json.load(open(f)))) else 'INVALID') for f in ['use_case_gp.json','use_case_school.json','use_case_hotel.json']]"
```

Expected:

```text
use_case_gp.json: VALID
use_case_school.json: VALID
use_case_hotel.json: VALID
```

If any use case is invalid, fix the schema/use-case mismatch before continuing.

---

# Run the Privacy Checker

The static checker evaluates the declared privacy posture of each environment.

The basic command is:

```bash
python privacy_checker.py <use_case> <manifest>
```

---

## GP Surgery

Run:

```bash
python privacy_checker.py use_case_gp.json manifest_gp.json
```

---

## School

Run:

```bash
python privacy_checker.py use_case_school.json manifest_school.json
```

---

## Hotel

Run:

```bash
python privacy_checker.py use_case_hotel.json manifest_hotel.json
```

---

# Save Checker Reports

If the checker supports an output argument, save the report.

Example:

```bash
python privacy_checker.py use_case_gp.json manifest_gp.json --output data/reports/gp_static_report.json
```

School:

```bash
python privacy_checker.py use_case_school.json manifest_school.json --output data/reports/school_static_report.json
```

Hotel:

```bash
python privacy_checker.py use_case_hotel.json manifest_hotel.json --output data/reports/hotel_static_report.json
```

If your current CLI does not expose `--output`, simply run the checker and retain the terminal output or use the report functionality already provided by the implementation.

---

# Expected Static Checker Output

A typical result contains information similar to:

```text
==================================================
PRIVACY POSTURE CHECK
==================================================

Use Case: GP Surgery

Schema Validation ........ PASS
Encryption ............... PASS
Authentication .......... PASS
Access Control .......... PASS
Pseudonymisation ........ PASS
Policies ................ PASS
Consent ................. PASS
Data Flows .............. PASS
DPO ..................... PASS

Posture Score: 100.0%
Posture Rating: STRONG
```

The exact number of checks depends on the active manifest.

---

# Run the GP Simulation

The FSM simulation generates synthetic GP activity.

Run:

```bash
python privacy_fsm_simulation.py --use-case GP --days 5 --seed 99
```

Parameters:

```text
--use-case GP
--days 5
--seed 99
```

The seed is important for reproducibility.

---

# Run the School Simulation

Run:

```bash
python privacy_fsm_simulation.py --use-case SCHOOL --days 5 --seed 99
```

---

# Run the Hotel Simulation

Run:

```bash
python privacy_fsm_simulation.py --use-case HOTEL --days 5 --seed 99
```

---

# Simulation Parameters

The primary research experiment uses:

```text
Simulation duration: 5 days
Random seed:         99
```

The expected number of events depends on the configured events-per-day value for each scenario.

Do not manually alter the seed when reproducing the dissertation experiment unless you are deliberately running a separate experiment.

---

# Check Generated Logs

After running the simulation, inspect:

```text
data/logs/
```

Typical outputs include:

```text
gp_activity_log.json
school_activity_log.json
hotel_activity_log.json
```

You can inspect a log using:

```bash
python -m json.tool data/logs/gp_activity_log.json
```

For School:

```bash
python -m json.tool data/logs/school_activity_log.json
```

For Hotel:

```bash
python -m json.tool data/logs/hotel_activity_log.json
```

---

# Run the Runtime Monitor

The monitor processes an activity log generated by the FSM.

---

## GP

Example:

```bash
python privacy_monitor.py data/logs/gp_activity_log.json
```

---

## School

```bash
python privacy_monitor.py data/logs/school_activity_log.json
```

---

## Hotel

```bash
python privacy_monitor.py data/logs/hotel_activity_log.json
```

---

# Save Monitoring Reports

If supported by the CLI:

```bash
python privacy_monitor.py data/logs/gp_activity_log.json --output data/reports/gp_monitor_report.json
```

School:

```bash
python privacy_monitor.py data/logs/school_activity_log.json --output data/reports/school_monitor_report.json
```

Hotel:

```bash
python privacy_monitor.py data/logs/hotel_activity_log.json --output data/reports/hotel_monitor_report.json
```

---

# Inspect a Monitoring Report

Use:

```bash
python -m json.tool data/reports/gp_monitor_report.json
```

The report can contain:

```text
Total events
Violation signal count
Violating event count
Event violation rate
Event compliance rate
Violation signal rate
Severity distribution
Lifecycle distribution
Action distribution
```

---

# Run the Integrated Evaluator

The integrated evaluator combines:

```text
Static Checker
      +
FSM Simulation
      +
Runtime Monitoring
      +
Evaluation Metrics
```

Run:

```bash
python privacy_evaluator.py
```

The evaluator is the preferred entry point for the complete experimental workflow if all components are configured correctly.

---

# Run the Complete Experiment

For the dissertation experiment, use the following sequence.

## Step 1 — Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

---

## Step 2 — Move to the repository

```bash
cd Privacy-Posture-Framework
```

---

## Step 3 — Check Python

```bash
python --version
```

Recommended:

```text
Python 3.11+
```

---

## Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5 — Validate the schema

```bash
python -c "import json; from jsonschema import Draft202012Validator; s=json.load(open('privacy_schema.json')); [print(f'{f}:', 'VALID' if not list(Draft202012Validator(s).iter_errors(json.load(open(f)))) else 'INVALID') for f in ['use_case_gp.json','use_case_school.json','use_case_hotel.json']]"
```

Expected:

```text
use_case_gp.json: VALID
use_case_school.json: VALID
use_case_hotel.json: VALID
```

---

## Step 6 — Run static GP evaluation

```bash
python privacy_checker.py use_case_gp.json manifest_gp.json
```

---

## Step 7 — Run static School evaluation

```bash
python privacy_checker.py use_case_school.json manifest_school.json
```

---

## Step 8 — Run static Hotel evaluation

```bash
python privacy_checker.py use_case_hotel.json manifest_hotel.json
```

---

## Step 9 — Run GP simulation

```bash
python privacy_fsm_simulation.py --use-case GP --days 5 --seed 99
```

---

## Step 10 — Run School simulation

```bash
python privacy_fsm_simulation.py --use-case SCHOOL --days 5 --seed 99
```

---

## Step 11 — Run Hotel simulation

```bash
python privacy_fsm_simulation.py --use-case HOTEL --days 5 --seed 99
```

---

## Step 12 — Run GP monitor

```bash
python privacy_monitor.py data/logs/gp_activity_log.json
```

---

## Step 13 — Run School monitor

```bash
python privacy_monitor.py data/logs/school_activity_log.json
```

---

## Step 14 — Run Hotel monitor

```bash
python privacy_monitor.py data/logs/hotel_activity_log.json
```

---

## Step 15 — Run integrated evaluator

```bash
python privacy_evaluator.py
```

---

## Step 16 — Check generated reports

Inspect:

```text
data/reports/
```

and:

```text
data/logs/
```

---

# Testing

The project contains tests for:

```text
Schema
Checker
Simulator
Monitor
Evaluation
```

Run all tests:

```bash
pytest
```

---

## Run schema tests

```bash
pytest tests/schema/
```

---

## Run checker tests

```bash
pytest tests/checker/
```

---

## Run simulator tests

```bash
pytest tests/simulator/
```

---

## Run monitor tests

```bash
pytest tests/monitor/
```

---

## Run evaluation tests

```bash
pytest tests/evaluation/
```

---

# Run Tests with Verbose Output

```bash
pytest -v
```

---

# Run Tests with Coverage

If `pytest-cov` is installed:

```bash
pytest --cov
```

For a more detailed report:

```bash
pytest --cov=. --cov-report=term-missing
```

---

# Python Syntax Checks

Before running the complete framework, check that the Python files compile.

Run:

```bash
python -m py_compile privacy_checker.py
```

Then:

```bash
python -m py_compile privacy_fsm_simulation.py
```

Then:

```bash
python -m py_compile privacy_monitor.py
```

Then:

```bash
python -m py_compile privacy_evaluator.py
```

If all are successful, there should be no syntax-error output.

---

# Reproducibility

The principal experimental configuration uses:

```text
Seed: 99
Duration: 5 days
```

The fixed seed allows the same simulation configuration to be repeated.

The following should remain unchanged when reproducing the dissertation experiment:

```text
Use-case configuration
Privacy manifest
Schema
FSM transition probabilities
Event-generation probabilities
Random seed
Simulation duration
Monitoring rules
Scoring thresholds
```

---

# Reproducibility Checklist

Before generating final dissertation results:

```text
[ ] Correct Git commit checked out
[ ] Python environment recreated
[ ] Dependencies installed
[ ] Schema validated
[ ] GP use case validated
[ ] School use case validated
[ ] Hotel use case validated
[ ] Privacy checker runs
[ ] FSM runs
[ ] GP log generated
[ ] School log generated
[ ] Hotel log generated
[ ] Monitor runs
[ ] Evaluator runs
[ ] Seed = 99
[ ] Simulation = 5 days
[ ] Reports saved
[ ] Dissertation numbers taken from generated reports
[ ] Figures generated from the same reports
```

---

# Generated Outputs

The framework can generate several categories of output.

## Static Reports

```text
data/reports/
```

Possible reports:

```text
gp_static_report.json
school_static_report.json
hotel_static_report.json
```

---

## Activity Logs

```text
data/logs/
```

Possible files:

```text
gp_activity_log.json
school_activity_log.json
hotel_activity_log.json
```

---

## Runtime Reports

Possible files:

```text
gp_monitor_report.json
school_monitor_report.json
hotel_monitor_report.json
```

---

## Integrated Evaluation

The evaluator may generate:

```text
evaluation_report.json
```

or another configured report name.

Always use the actual generated report as the source of truth for experimental values.

---

# Understanding the Results

The framework produces two major dimensions of privacy posture:

```text
STATIC POSTURE
      +
RUNTIME POSTURE
```

---

# Static Posture Score

Static posture measures how closely the declared use case matches its privacy manifest.

Conceptually:

```text
                  PASS
Static Score = -------------------- × 100
               PASS + FAIL + WARNING
```

Informational findings are not treated as control failures.

---

# Posture Ratings

The framework uses:

| Score | Rating |
|---:|---|
| >= 90% | STRONG |
| >= 75% | MODERATE |
| >= 50% | WEAK |
| < 50% | CRITICAL |

Critical control failures can affect the final classification independently of the percentage score.

---

# Runtime Compliance

Runtime compliance is calculated from simulated operational events.

The framework distinguishes between:

## Violation signal

An individual privacy signal generated by the monitor.

Example:

```text
UNAUTHENTICATED_ACCESS
```

## Violating event

A unique activity event associated with one or more violation signals.

This distinction is important because one event can produce multiple signals.

For example:

```text
Event 101
 |
 +-- UNAUTHENTICATED_ACCESS
 |
 +-- UNLOGGED_ACCESS
 |
 +-- SENSITIVE_DATA_ACCESS
```

This represents:

```text
1 violating event
3 violation signals
```

not three separate violating events.

---

# Runtime Metrics

The monitor can report:

```text
violation_signal_count
violating_event_count
event_violation_rate_percent
event_compliance_rate_percent
violation_signal_rate_percent
```

---

## Event Violation Rate

```text
Event Violation Rate
=
Violating Events
------------------ × 100
Total Events
```

---

## Event Compliance Rate

```text
Event Compliance Rate
=
Non-violating Events
-------------------- × 100
Total Events
```

or:

```text
Event Compliance Rate
=
100 - Event Violation Rate
```

---

# DEAR Monitoring

The monitoring pipeline is:

```text
                    ACTIVITY EVENT
                          |
                          v
                   +-------------+
                   |   DETECT    |
                   +------+------+
                          |
                          v
                   +-------------+
                   |  EVALUATE   |
                   +------+------+
                          |
                          v
                   +-------------+
                   |     ACT     |
                   |  SIMULATED  |
                   +------+------+
                          |
                          v
                   +-------------+
                   |   REPORT    |
                   +-------------+
```

---

# Simulated Remediation

The framework deliberately distinguishes between:

```text
Recommended Action
```

and:

```text
Executed Action
```

The current implementation uses:

```text
action_mode = SIMULATED
action_executed = false
```

Therefore, the framework does not:

- revoke actual user sessions;
- delete actual records;
- block real network traffic;
- modify real databases;
- suspend real sharing;
- change production access controls.

The system records what a remediation layer **would be expected to do**.

---

# Use Cases

## GP Surgery

The GP scenario models a healthcare environment.

Example data categories include:

```text
Patient identity
Health information
Diagnoses
Prescriptions
Laboratory results
Allergies
Vaccination records
```

Example controls include:

```text
Encryption
MFA
RBAC
Least privilege
Audit logging
Healthcare data sharing
Retention
Deletion
DPO
PIA/DPIA
```

---

# School

The School scenario models an education environment.

Example data categories include:

```text
Student identity
Attendance
Grades
Safeguarding information
Special educational needs
Medical information
Parent contact information
```

Example controls include:

```text
Access restrictions
Safeguarding access
Authentication
Audit logging
Consent
Retention
Deletion
DPO
Privacy policies
```

---

# Hotel

The Hotel scenario models a hospitality environment.

Example data categories include:

```text
Guest identity
Contact details
Passport information
Booking information
Payment information
Loyalty information
Meal preferences
CCTV information
```

The Hotel scenario is deliberately configured with weaker controls so that the framework can demonstrate detection of privacy-control deficiencies.

---

# Regulatory Context

The framework provides scenario-specific regulatory context.

## GP Surgery

The synthetic scenario considers:

```text
GDPR
UK Data Protection Act 2018
NHS DSPT
Caldicott Principles
```

## School

The synthetic scenario considers:

```text
GDPR
UK Data Protection Act 2018
KCSIE
DfE data protection guidance
```

## Hotel

The synthetic scenario considers:

```text
GDPR
UK Data Protection Act 2018
PCI-DSS
Applicable hospitality requirements
```

These are represented as policy context for the research scenarios.

They should not be interpreted as a complete automated implementation of the relevant regulatory regimes.

---

# Example Workflow

A complete run can be represented as:

```text
                +--------------------+
                | Privacy Schema     |
                +---------+----------+
                          |
                          v
                +--------------------+
                | Use Case JSON      |
                +---------+----------+
                          |
                          v
                +--------------------+
                | Privacy Manifest   |
                +---------+----------+
                          |
                          v
                +--------------------+
                | Static Checker     |
                +---------+----------+
                          |
                          v
                +--------------------+
                | Static Score       |
                +---------+----------+
                          |
                          v
                +--------------------+
                | FSM Simulator      |
                +---------+----------+
                          |
                          v
                +--------------------+
                | Activity Log       |
                +---------+----------+
                          |
                          v
                +--------------------+
                | DEAR Monitor       |
                +---------+----------+
                          |
                          v
                +--------------------+
                | Runtime Metrics    |
                +---------+----------+
                          |
                          v
                +--------------------+
                | Integrated         |
                | Evaluation         |
                +--------------------+
```

---

# Docker

The repository contains:

```text
Dockerfile
docker-compose.yml
```

Docker provides an alternative execution environment.

---

## Check Docker

```bash
docker --version
```

Check Docker Compose:

```bash
docker compose version
```

---

## Build the Image

From the repository root:

```bash
docker build -t privacy-posture-framework .
```

---

## Run the Container

```bash
docker run --rm privacy-posture-framework
```

---

## Docker Compose

Run:

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```

If your Docker configuration mounts `data/`, generated logs and reports can be retained on the host system.

---

# Examples

Demonstration scripts are located under:

```text
examples/
```

including:

```text
gp_demo.py
school_demo.py
hotel_demo.py
```

Run GP example:

```bash
python examples/gp_demo.py
```

School:

```bash
python examples/school_demo.py
```

Hotel:

```bash
python examples/hotel_demo.py
```

If a demonstration script requires additional arguments, run:

```bash
python examples/gp_demo.py --help
```

---

# Notebooks

Experimental notebooks are located under:

```text
notebooks/
```

including:

```text
experiment1.ipynb
experiment2.ipynb
experiment3.ipynb
benchmark.ipynb
```

Launch Jupyter:

```bash
jupyter notebook
```

or:

```bash
jupyter lab
```

Then open the relevant notebook.

---

# Documentation

Detailed documentation is stored under:

```text
docs/
```

The principal documentation files are:

```text
architecture.md
schema.md
manifests.md
checker.md
simulator.md
monitor.md
evaluation.md
```

---

# Troubleshooting

## `python` is not recognised

### Windows

Try:

```powershell
py --version
```

If that works, use:

```powershell
py -m venv .venv
```

and:

```powershell
.venv\Scripts\activate
```

### Linux/macOS

Try:

```bash
python3 --version
```

---

# `pip` is not recognised

Use:

```bash
python -m pip --version
```

Then install dependencies with:

```bash
python -m pip install -r requirements.txt
```

---

# `ModuleNotFoundError`

Make sure the virtual environment is active.

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

---

# JSON Schema validation failure

If a use case fails validation:

1. Check the JSON syntax.
2. Check required properties.
3. Check property types.
4. Check nested structures.
5. Check the schema version.
6. Run the validator again.

You can first check JSON syntax using:

```bash
python -m json.tool use_case_gp.json
```

---

# Python syntax error

Run:

```bash
python -m py_compile privacy_checker.py
python -m py_compile privacy_fsm_simulation.py
python -m py_compile privacy_monitor.py
python -m py_compile privacy_evaluator.py
```

Fix any reported line before running the complete experiment.

---

# Missing activity log

Make sure the FSM simulation has completed successfully.

For example:

```bash
python privacy_fsm_simulation.py --use-case GP --days 5 --seed 99
```

Then inspect:

```text
data/logs/
```

---

# Monitor cannot find a log

Check the exact filename:

```bash
dir data\logs
```

Windows, or:

```bash
ls data/logs
```

Linux/macOS.

Then pass the correct path:

```bash
python privacy_monitor.py data/logs/<actual-log-file>.json
```

---

# Evaluator failure

If the integrated evaluator fails:

1. Run the schema validation.
2. Run the static checker.
3. Run each FSM simulation separately.
4. Run each monitor separately.
5. Check generated logs.
6. Run the evaluator last.

This isolates the failing component.

Recommended order:

```text
Schema
  ↓
Checker
  ↓
FSM
  ↓
Monitor
  ↓
Evaluator
```

---

# Limitations

PPF is a research prototype.

## Synthetic Data

The organisational environments are synthetic.

They do not represent real GP surgeries, schools or hotels.

## Synthetic Activity

The FSM generates simulated events rather than consuming production telemetry.

## Rule-Based Detection

The monitor uses explicit rules and heuristics.

It does not provide comprehensive semantic understanding of every possible privacy violation.

## Legal Interpretation

The framework does not determine whether a real organisation has selected the legally correct lawful basis or regulatory condition.

## Simulated Remediation

The Act stage records simulated actions rather than modifying live systems.

## Experimental Scoring

The posture score is a research metric.

It is not a recognised regulatory certification score.

## Configuration Dependence

Results depend on:

```text
Schema
Manifest
Use Case
FSM configuration
Event-generation probabilities
Monitoring rules
Scoring configuration
```

---

# Research Contribution

The framework explores the integration of:

```text
Machine-readable Privacy Schema
             +
Privacy Manifest
             +
Static Privacy Verification
             +
Lifecycle FSM Simulation
             +
DEAR-inspired Monitoring
             +
Simulated Remediation
             +
Quantitative Evaluation
```

The research contribution is the design and experimental evaluation of an integrated, policy-driven and lifecycle-aware privacy posture framework.

The framework attempts to connect:

```text
Declared Privacy Controls
           +
Operational Privacy Behaviour
           |
           v
      Privacy Posture
```

rather than treating privacy assessment exclusively as a static documentation exercise.

---

# Future Work

Potential future extensions include:

- real-time event-stream ingestion;
- enterprise infrastructure integration;
- cloud-platform integration;
- identity-provider integration;
- graph-database implementation;
- richer asset-graph analysis;
- automated data-flow discovery;
- ontology-based privacy reasoning;
- formal privacy-policy languages;
- automated policy-to-rule compilation;
- improved lawful-basis modelling;
- automated DPIA support;
- real-time privacy dashboards;
- advanced anomaly detection;
- machine-learning-assisted detection;
- formal verification of lifecycle transitions;
- ISO/IEC 27701 mapping;
- NIST Privacy Framework mapping; and
- controlled real-world case studies.

These capabilities are future work and are not claimed as completed functionality of the current prototype unless implemented in the repository.

---

# Security and Privacy

The repository should contain only synthetic research data.

Do **not** commit:

```text
Real patient information
Real student information
Real guest information
Real payment information
Passwords
API keys
Access tokens
Private certificates
Production credentials
Personally identifiable information
```

Use synthetic values for all demonstrations and experiments.

Before pushing changes to GitHub, check:

```bash
git status
```

and inspect changed files:

```bash
git diff
```

Never commit secrets.

---

# Git Workflow

After making changes:

```bash
git status
```

Review:

```bash
git diff
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Update privacy posture framework"
```

Push:

```bash
git push origin main
```

Before pushing the final dissertation version, verify:

```text
README
Source code
Schema
Manifests
Use cases
Tests
Documentation
Experimental outputs
```

are consistent.

---

# Final Experimental Procedure

For the final dissertation experiment, use the following sequence.

```text
1. Clone repository
        |
        v
2. Create virtual environment
        |
        v
3. Activate virtual environment
        |
        v
4. Install requirements
        |
        v
5. Validate JSON Schema
        |
        v
6. Validate GP / School / Hotel
        |
        v
7. Run static checker
        |
        v
8. Run GP FSM
        |
        v
9. Run School FSM
        |
        v
10. Run Hotel FSM
        |
        v
11. Run GP monitor
        |
        v
12. Run School monitor
        |
        v
13. Run Hotel monitor
        |
        v
14. Run integrated evaluator
        |
        v
15. Save generated reports
        |
        v
16. Extract final metrics
        |
        v
17. Generate dissertation figures
        |
        v
18. Update dissertation tables
        |
        v
19. Verify README
        |
        v
20. Commit final version
```

---

# Final Pre-Submission Checklist

Before submitting the dissertation or tagging a final repository release:

## Code

```text
[ ] All Python files compile
[ ] All tests pass
[ ] FSM runs successfully
[ ] Monitor runs successfully
[ ] Evaluator runs successfully
```

## Schema

```text
[ ] privacy_schema.json validates
[ ] GP use case validates
[ ] School use case validates
[ ] Hotel use case validates
```

## Static Evaluation

```text
[ ] GP checker executed
[ ] School checker executed
[ ] Hotel checker executed
[ ] Static scores recorded
[ ] Rating thresholds consistent
```

## Dynamic Evaluation

```text
[ ] GP simulation executed
[ ] School simulation executed
[ ] Hotel simulation executed
[ ] Seed = 99
[ ] Duration = 5 days
```

## Monitoring

```text
[ ] GP monitor executed
[ ] School monitor executed
[ ] Hotel monitor executed
[ ] Violation signals recorded
[ ] Violating events recorded
[ ] Event compliance recorded
```



## GitHub

```text
[ ] README updated
[ ] LICENSE present
[ ] .gitignore present
[ ] No credentials committed
[ ] No personal data committed
[ ] Source code committed
[ ] Tests committed
[ ] Documentation committed
[ ] Final commit pushed
```

---

# Project Status

```text
Status: Research Prototype
```

The Privacy Posture Framework provides an experimental implementation for:

```text
Privacy Modelling
       +
Policy Representation
       +
Static Checking
       +
Lifecycle Simulation
       +
Runtime Monitoring
       +
Simulated Remediation
       +
Quantitative Evaluation
```

The project is designed to support academic experimentation and further development.


---

# Repository

GitHub:

https://github.com/rohityellapu/Privacy-Posture-Framework

---


# Disclaimer

This repository is an academic research prototype.


All organisational environments and operational events used by the framework are synthetic.

The framework's posture scores and runtime metrics are experimental measurements intended for research and comparative evaluation.