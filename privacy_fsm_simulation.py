#!/usr/bin/env python3
"""
Privacy FSM Simulation Framework
==================================
A graph-based Finite State Machine (FSM) that simulates organisational
daily privacy-relevant activities for three use cases:
  UC001 - GP Surgery
  UC002 - School
  UC003 - Hotel

Each use case shares the SAME FSM topology (states & transitions) but
is instantiated with use-case-specific actors, data categories, and event
probabilities.  The simulation generates a structured activity log that
the monitor can then analyse.

Usage:
    python privacy_fsm_simulation.py --use-case GP    --days 3 --seed 42
    python privacy_fsm_simulation.py --use-case SCHOOL --days 3 --seed 42
    python privacy_fsm_simulation.py --use-case HOTEL  --days 3 --seed 42

Output: JSON activity log written to logs/<use_case>_activity_log.json
"""

import json
import random
import argparse
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any


# ─────────────────────────────────────────────────────────────
#  FSM State definitions  (shared across all use cases)
# ─────────────────────────────────────────────────────────────
STATES = [
    "IDLE",
    "DATA_COLLECTION",
    "DATA_STORAGE",
    "DATA_ACCESS",
    "DATA_SHARING",
    "DATA_RETENTION_REVIEW",
    "DATA_DELETION",
    "COMPLIANCE_CHECK",
    "INCIDENT_DETECTED",
    "INCIDENT_RESOLVED",
]

# Graph adjacency: state -> list of (next_state, base_probability)
FSM_GRAPH: Dict[str, List] = {
    "IDLE":                   [("DATA_COLLECTION", 0.40), ("DATA_ACCESS", 0.30),
                                ("COMPLIANCE_CHECK", 0.10), ("IDLE", 0.20)],
    "DATA_COLLECTION":        [("DATA_STORAGE", 0.70), ("INCIDENT_DETECTED", 0.05),
                                ("IDLE", 0.25)],
    "DATA_STORAGE":           [("IDLE", 0.50), ("DATA_ACCESS", 0.30),
                                ("DATA_SHARING", 0.10), ("INCIDENT_DETECTED", 0.05),
                                ("COMPLIANCE_CHECK", 0.05)],
    "DATA_ACCESS":            [("IDLE", 0.50), ("DATA_SHARING", 0.20),
                                ("INCIDENT_DETECTED", 0.08), ("DATA_RETENTION_REVIEW", 0.12),
                                ("COMPLIANCE_CHECK", 0.10)],
    "DATA_SHARING":           [("IDLE", 0.55), ("INCIDENT_DETECTED", 0.10),
                                ("DATA_STORAGE", 0.20), ("COMPLIANCE_CHECK", 0.15)],
    "DATA_RETENTION_REVIEW":  [("DATA_DELETION", 0.30), ("IDLE", 0.60),
                                ("COMPLIANCE_CHECK", 0.10)],
    "DATA_DELETION":          [("IDLE", 0.80), ("COMPLIANCE_CHECK", 0.20)],
    "COMPLIANCE_CHECK":       [("IDLE", 0.70), ("INCIDENT_DETECTED", 0.15),
                                ("DATA_DELETION", 0.15)],
    "INCIDENT_DETECTED":      [("INCIDENT_RESOLVED", 0.60), ("INCIDENT_DETECTED", 0.40)],
    "INCIDENT_RESOLVED":      [("IDLE", 0.90), ("COMPLIANCE_CHECK", 0.10)],
}

# ─────────────────────────────────────────────────────────────
#  Use-case configurations
# ─────────────────────────────────────────────────────────────
USE_CASE_CONFIGS = {
    "GP": {
        "use_case_id": "UC001",
        "name": "GP Surgery",
        "actors": {
            "gp":          {"roles": ["gp"], "data_access_level": "restricted"},
            "nurse":        {"roles": ["nurse"], "data_access_level": "confidential"},
            "receptionist": {"roles": ["receptionist"], "data_access_level": "internal"},
            "admin":        {"roles": ["admin"], "data_access_level": "internal"},
            "it_admin":     {"roles": ["it_admin"], "data_access_level": "system"},
        },
        "personal_data_types": [
            "patient_id", "full_name", "date_of_birth", "diagnosis",
            "prescriptions", "lab_results", "allergies", "vaccination_records",
        ],
        "sensitive_data_types": ["diagnosis", "prescriptions", "lab_results", "allergies"],
        "sharing_recipients": ["hospital_trust", "nhs_spine", "pathology_lab"],
        "lawful_bases": {
            "sharing": {
                "article_6_basis": "..."
                "article_9_condition": "Article 9(2)(h)"
            },
            "collection": {
                "article_6_basis": "..."
                "article_9_condition": "Article 9(2)(h)"
            },
        },
        "expected_events_per_day": 40,
        "incident_labels": [
            "unauthorised_patient_record_access",
            "prescription_data_shared_without_dpa",
            "patient_list_exported_to_usb",
            "gp_accessing_records_outside_caseload",
        ],
         "transition_graph": {...}
    },
    "SCHOOL": {
        "use_case_id": "UC002",
        "name": "School",
        "actors": {
            "headteacher":         {"roles": ["headteacher"], "data_access_level": "restricted"},
            "teacher":              {"roles": ["teacher"], "data_access_level": "confidential"},
            "admin_staff":          {"roles": ["admin_staff"], "data_access_level": "internal"},
            "safeguarding_officer": {"roles": ["safeguarding_officer"], "data_access_level": "restricted"},
            "it_support":           {"roles": ["it_support"], "data_access_level": "system"},
        },
        "personal_data_types": [
            "student_id", "full_name", "date_of_birth", "grades",
            "attendance_records", "special_educational_needs", "disciplinary_records",
            "parent_contact_details", "free_school_meal_eligibility",
        ],
        "sensitive_data_types": [
            "special_educational_needs", "disciplinary_records", "free_school_meal_eligibility",
        ],
        "sharing_recipients": ["DfE_NPD", "ofsted", "exam_boards", "local_authority"],
        "lawful_bases": {
            "sharing": "Article 6(1)(e) GDPR - public task",
            "collection": "Article 6(1)(e) GDPR - public task",
        },
        "expected_events_per_day": 50,
        "incident_labels": [
            "student_records_emailed_unencrypted",
            "safeguarding_file_accessed_by_unauthorised_teacher",
            "grades_shared_with_marketing_agency",
            "parental_consent_not_obtained_before_photo_sharing",
        ],
         "transition_graph": {...}
    },
    "HOTEL": {
        "use_case_id": "UC003",
        "name": "Hotel",
        "actors": {
            "front_desk": {"roles": ["front_desk"], "data_access_level": "internal"},
            "manager":    {"roles": ["manager"],    "data_access_level": "confidential"},
            "housekeeping": {"roles": ["housekeeping"], "data_access_level": "public"},
            "finance":    {"roles": ["finance"],    "data_access_level": "confidential"},
            "it_admin":   {"roles": ["it_admin"],   "data_access_level": "system"},
        },
        "personal_data_types": [
            "full_name", "email_address", "credit_card_number", "passport_number",
            "booking_reference", "room_number", "check_in_date", "check_out_date",
            "loyalty_programme_id", "meal_preferences",
        ],
        "sensitive_data_types": ["credit_card_number", "passport_number"],
        "sharing_recipients": ["booking_com", "payment_gateway", "tax_authority", "marketing_agency"],
        "lawful_bases": {
            "sharing": "Article 6(1)(b) GDPR - contract performance",
            "collection": "Article 6(1)(b) GDPR - contract performance",
        },
        "expected_events_per_day": 60,
        "incident_labels": [
            "guest_credit_card_stored_unencrypted",
            "guest_data_shared_with_marketing_without_consent",
            "cctv_footage_retained_beyond_30_days",
            "loyalty_db_accessible_by_housekeeping_staff",
        ],
         "transition_graph": {...}
    },
}


# ─────────────────────────────────────────────────────────────
#  Event generators per state
# ─────────────────────────────────────────────────────────────

def build_event(state: str, ts: datetime, cfg: dict, rng: random.Random) -> dict:
    """Build a log event for the given FSM state."""
    actor_id = rng.choice(list(cfg["actors"].keys()))
    actor    = cfg["actors"][actor_id]
    data_type = rng.choice(cfg["personal_data_types"])
    is_sensitive = data_type in cfg["sensitive_data_types"]

    base = {
        "timestamp":   ts.isoformat(),
        "use_case_id": cfg["use_case_id"],
        "use_case":    cfg["name"],
        "event_type":  state,
        "actor":       actor_id,
        "actor_role":  actor["roles"][0],
        "data_access_level": actor["data_access_level"],
        "data_type":   data_type,
        "is_sensitive": is_sensitive,
        "flags":       [],
    }

    if state == "DATA_COLLECTION":
        consent = rng.random() < 0.85
        base.update({
            "method": rng.choice(["web_form", "manual_entry", "api", "paper_form"]),
            "consent_obtained": consent,
            "data_minimisation_applied": rng.random() < 0.80,
            "purpose_specified": rng.random() < 0.90,
        })
        if not consent:
            base["flags"].append("CONSENT_MISSING")

    elif state == "DATA_STORAGE":
        encrypted = rng.random() < 0.90
        base.update({
            "storage_system": rng.choice(["primary_db", "backup", "cloud_store", "local_file"]),
            "encrypted": encrypted,
            "geo_restricted": rng.random() < 0.95,
        })
        if not encrypted and is_sensitive:
            base["flags"].append("SENSITIVE_DATA_UNENCRYPTED")

    elif state == "DATA_ACCESS":
        auth = rng.random() < 0.92
        logged = rng.random() < 0.88
        base.update({
            "access_authenticated": auth,
            "access_logged": logged,
            "purpose": rng.choice(["clinical_use", "admin_task", "reporting", "audit", "maintenance"]),
        })
        if not auth:
            base["flags"].append("UNAUTHENTICATED_ACCESS")
        if not logged:
            base["flags"].append("UNLOGGED_ACCESS")

    elif state == "DATA_SHARING":
        recipient = rng.choice(cfg["sharing_recipients"])
        dpa_in_place = rng.random() < 0.75
        legal_basis = rng.choice([cfg["lawful_bases"]["sharing"], "MISSING"])
        base.update({
            "recipient": recipient,
            "dpa_in_place": dpa_in_place,
            "legal_basis": legal_basis,
            "transfer_encrypted": rng.random() < 0.92,
            "cross_border": rng.random() < 0.20,
        })
        if not dpa_in_place:
            base["flags"].append("DPA_MISSING")
        if legal_basis == "MISSING":
            base["flags"].append("NO_LEGAL_BASIS_FOR_SHARING")
        if base.get("cross_border") and not base.get("dpa_in_place"):
            base["flags"].append("CROSS_BORDER_TRANSFER_WITHOUT_DPA")

    elif state == "DATA_RETENTION_REVIEW":
        base.update({
            "retention_policy_applied": rng.random() < 0.70,
            "review_outcome": rng.choice(["retain", "mark_for_deletion", "escalate"]),
        })
        if not base["retention_policy_applied"]:
            base["flags"].append("RETENTION_POLICY_NOT_APPLIED")

    elif state == "DATA_DELETION":
        secure = rng.random() < 0.80
        audited = rng.random() < 0.85
        base.update({
            "deletion_method": "secure_overwrite" if secure else "simple_delete",
            "secure_deletion": secure,
            "deletion_audited": audited,
            "dsar_triggered": rng.random() < 0.15,
        })
        if not secure:
            base["flags"].append("INSECURE_DELETION")
        if not audited:
            base["flags"].append("DELETION_NOT_AUDITED")

    elif state == "COMPLIANCE_CHECK":
        base.update({
            "check_type": rng.choice(["scheduled", "triggered", "audit"]),
            "standards": ["GDPR", "UK_DPA_2018"],
            "passed": rng.random() < 0.80,
            "findings": rng.randint(0, 3),
        })
        if not base["passed"]:
            base["flags"].append("COMPLIANCE_CHECK_FAILED")

    elif state == "INCIDENT_DETECTED":
        label = rng.choice(cfg["incident_labels"])
        base.update({
            "incident_type": label,
            "severity": rng.choice(["low", "medium", "high", "critical"]),
            "auto_detected": rng.random() < 0.60,
            "notified_dpo": rng.random() < 0.70,
        })
        base["flags"].append(f"INCIDENT:{label.upper()}")

    elif state == "INCIDENT_RESOLVED":
        base.update({
            "resolution": rng.choice(["contained", "remediated", "reported_to_ico", "false_positive"]),
            "time_to_resolve_hours": rng.randint(1, 72),
        })

    return base


# ─────────────────────────────────────────────────────────────
#  FSM runner
# ─────────────────────────────────────────────────────────────

def run_fsm(cfg: dict, days: int, seed: int) -> List[dict]:
    rng = random.Random(seed)
    events: List[dict] = []
    current_state = "IDLE"
    ts = datetime(2026, 1, 6, 8, 0, 0)  # Monday morning start

    events_per_day = cfg["expected_events_per_day"]
    total_events   = days * events_per_day

    for i in range(total_events):
        # Advance time
        ts += timedelta(minutes=rng.randint(5, 20))
        # Skip night hours (18:00–08:00)
        if ts.hour >= 18:
            ts = ts.replace(hour=8, minute=0) + timedelta(days=1)

        event = build_event(current_state, ts, cfg, rng)
        events.append(event)

        # Transition
        transitions = FSM_GRAPH.get(current_state, [("IDLE", 1.0)])
        r = rng.random()
        cumulative = 0.0
        next_state = transitions[-1][0]
        for nxt, prob in transitions:
            cumulative += prob
            if r <= cumulative:
                next_state = nxt
                break
        current_state = next_state

    return events


# ─────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Privacy FSM Simulation")
    parser.add_argument("--use-case", choices=["GP", "SCHOOL", "HOTEL"], default="GP")
    parser.add_argument("--days",     type=int, default=3)
    parser.add_argument("--seed",     type=int, default=42)
    parser.add_argument("--output",   default=None)
    args = parser.parse_args()

    cfg    = USE_CASE_CONFIGS[args.use_case]
    events = run_fsm(cfg, args.days, args.seed)

    # Summaries
    flag_counts: Dict[str, int] = {}
    state_counts: Dict[str, int] = {}
    for e in events:
        s = e["event_type"]
        state_counts[s] = state_counts.get(s, 0) + 1
        for flag in e.get("flags", []):
            flag_counts[flag] = flag_counts.get(flag, 0) + 1

    log = {
        "simulation_id": f"SIM-{cfg['use_case_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "use_case": cfg["name"],
        "days_simulated": args.days,
        "total_events": len(events),
        "seed": args.seed,
        "generated_at": datetime.now().isoformat(),
        "state_summary": state_counts,
        "flag_summary": flag_counts,
        "events": events,
    }

    out_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = args.output or os.path.join(out_dir, f"{args.use_case.lower()}_activity_log.json")

    with open(out_path, "w") as f:
        json.dump(log, f, indent=2)

    print(f"\nSimulation complete: {len(events)} events for '{cfg['name']}' over {args.days} day(s).")
    print(f"State distribution: {state_counts}")
    print(f"Flags raised: {flag_counts}")
    print(f"Log saved to: {out_path}")


if __name__ == "__main__":
    main()
