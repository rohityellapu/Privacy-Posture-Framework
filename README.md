# Privacy Posture Framework (PPF)

A policy-driven framework for modelling, checking, simulating and monitoring organisational privacy posture.


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


# Install Dependencies

With the virtual environment activated, run:

```bash
pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
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
``

If they do not exist, create them.



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
total_violations_detected
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




This repository is an academic research prototype.


All organisational environments and operational events used by the framework are synthetic.

The framework's posture scores and runtime metrics are experimental measurements intended for research and comparative evaluation.