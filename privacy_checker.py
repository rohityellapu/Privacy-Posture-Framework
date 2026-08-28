#!/usr/bin/env python3
"""
Privacy Posture Checker — Static Analysis Tool
================================================
Checks a privacy posture use-case instance against its corresponding manifest.
Produces a detailed compliance report listing PASS / FAIL / WARNING findings
for every control category.

Usage:
    python privacy_checker.py <use_case_json> <manifest_json> [--output <report.json>]
"""
from jsonschema import Draft202012Validator
import json
import sys
import os
import argparse
from datetime import datetime
from typing import Any, Dict, List, Tuple
DEFAULT_SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "privacy_schema.json"
)

# ─────────────────────────────────────────────
#  Severity constants
# ─────────────────────────────────────────────
PASS    = "PASS"
FAIL    = "FAIL"
WARNING = "WARNING"
INFO    = "INFO"

def validate_against_schema(
    use_case: dict,
    schema_path: str = DEFAULT_SCHEMA_PATH
) -> List[dict]:

    findings = []

    if not os.path.exists(schema_path):
        findings.append({
            "control": "schema.validation",
            "status": FAIL,
            "severity": "critical",
            "detail": f"Schema file not found: {schema_path}"
        })
        return findings

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        validator = Draft202012Validator(schema)

        errors = sorted(
            validator.iter_errors(use_case),
            key=lambda error: list(error.path)
        )

        if not errors:
            findings.append({
                "control": "schema.validation",
                "status": PASS,
                "detail": "Use-case conforms to Privacy Posture Framework schema."
            })
        else:
            for error in errors:
                path = ".".join(str(p) for p in error.path)

                findings.append({
                    "control": f"schema.validation.{path or 'root'}",
                    "status": FAIL,
                    "severity": "critical",
                    "detail": error.message
                })

    except json.JSONDecodeError as exc:
        findings.append({
            "control": "schema.validation",
            "status": FAIL,
            "severity": "critical",
            "detail": f"Invalid JSON schema: {exc}"
        })

    except Exception as exc:
        findings.append({
            "control": "schema.validation",
            "status": FAIL,
            "severity": "critical",
            "detail": f"Schema validation failed: {exc}"
        })

    return findings

def _get(obj: dict, *keys, default=None):
    """Safe nested key access."""
    for k in keys:
        if not isinstance(obj, dict):
            return default
        obj = obj.get(k, default)
        if obj is None:
            return default
    return obj


# ─────────────────────────────────────────────
#  Individual check functions
# ─────────────────────────────────────────────

def check_encryption(uc: dict, man: dict) -> List[dict]:
    findings = []
    uc_enc  = _get(uc,  "environment", "encryption", default={})
    man_enc = _get(man, "required_controls", "encryption", default={})

    # At-rest
    uc_at_rest = _get(uc_enc, "at_rest", "enabled", default=False)
    man_at_rest = _get(man_enc, "at_rest_required", default=True)
    if man_at_rest:
        if uc_at_rest:
            findings.append({"control": "encryption.at_rest", "status": PASS,
                              "detail": "Encryption at rest is enabled."})
        else:
            findings.append({"control": "encryption.at_rest", "status": FAIL,
                              "detail": "Encryption at rest is REQUIRED but NOT enabled.",
                              "severity": "critical"})
    # In-transit
    uc_transit = _get(uc_enc, "in_transit", "enabled", default=False)
    man_transit = _get(man_enc, "in_transit_required", default=True)
    if man_transit:
        if uc_transit:
            uc_proto = _get(uc_enc, "in_transit", "protocol", default="")
            man_proto = _get(man_enc, "in_transit_min_protocol", default="TLS 1.2")
            tls_versions = {"TLS 1.0": 10, "TLS 1.1": 11, "TLS 1.2": 12, "TLS 1.3": 13}
            uc_v  = tls_versions.get(uc_proto, 0)
            man_v = tls_versions.get(man_proto, 12)
            if uc_v >= man_v:
                findings.append({"control": "encryption.in_transit_protocol", "status": PASS,
                                  "detail": f"Protocol {uc_proto} meets minimum {man_proto}."})
            else:
                findings.append({"control": "encryption.in_transit_protocol", "status": FAIL,
                                  "detail": f"Protocol {uc_proto} is BELOW required minimum {man_proto}.",
                                  "severity": "high"})
        else:
            findings.append({"control": "encryption.in_transit", "status": FAIL,
                              "detail": "Encryption in transit is REQUIRED but NOT enabled.",
                              "severity": "critical"})

    # Key rotation
    uc_rot  = _get(uc_enc, "key_management", "rotation_days", default=None)
    man_rot = _get(man_enc, "key_rotation_max_days", default=None)
    if man_rot and uc_rot:
        if uc_rot <= man_rot:
            findings.append({"control": "encryption.key_rotation", "status": PASS,
                              "detail": f"Key rotation every {uc_rot} days meets maximum {man_rot} days."})
        else:
            findings.append({"control": "encryption.key_rotation", "status": FAIL,
                              "detail": f"Key rotation every {uc_rot} days EXCEEDS maximum allowed {man_rot} days.",
                              "severity": "medium"})
    return findings


def check_authentication(uc: dict, man: dict) -> List[dict]:
    findings = []
    uc_auth  = _get(uc,  "environment", "authentication", default={})
    man_auth = _get(man, "required_controls", "authentication", default={})

    # MFA
    man_mfa = _get(man_auth, "mfa_required", default=True)
    uc_mfa  = _get(uc_auth,  "mfa_required", default=False)
    if man_mfa:
        if uc_mfa:
            findings.append({"control": "authentication.mfa", "status": PASS,
                              "detail": "Multi-factor authentication is enabled."})
        else:
            findings.append({"control": "authentication.mfa", "status": FAIL,
                              "detail": "MFA is REQUIRED but NOT enabled.",
                              "severity": "critical"})

    # Password length
    man_pwd_len = _get(man_auth, "min_password_length", default=10)
    uc_pwd_len  = _get(uc_auth, "password_policy", "min_length", default=0)
    if uc_pwd_len >= man_pwd_len:
        findings.append({"control": "authentication.password_length", "status": PASS,
                          "detail": f"Password min length {uc_pwd_len} meets required {man_pwd_len}."})
    else:
        findings.append({"control": "authentication.password_length", "status": FAIL,
                          "detail": f"Password min length {uc_pwd_len} is BELOW required {man_pwd_len}.",
                          "severity": "medium"})

    # Session timeout
    man_timeout = _get(man_auth, "session_timeout_max_minutes", default=60)
    uc_timeout  = _get(uc_auth, "session_timeout_minutes", default=None) or \
                  _get(uc_auth, "session_policy", "timeout_minutes", default=None)
    if uc_timeout is not None and man_timeout:
        if uc_timeout <= man_timeout:
            findings.append({"control": "authentication.session_timeout", "status": PASS,
                              "detail": f"Session timeout {uc_timeout} min meets maximum {man_timeout} min."})
        else:
            findings.append({"control": "authentication.session_timeout", "status": WARNING,
                              "detail": f"Session timeout {uc_timeout} min EXCEEDS maximum {man_timeout} min.",
                              "severity": "low"})
    return findings


def check_access_control(uc: dict, man: dict) -> List[dict]:
    findings = []
    uc_ac  = _get(uc,  "environment", "access_control", default={})
    man_ac = _get(man, "required_controls", "access_control", default={})

    bool_checks = [
        ("rbac_required",         "model",           "RBAC", "Access control model is RBAC."),
        ("least_privilege_required", "least_privilege", True, "Least privilege is enforced."),
        ("audit_logging_required",   "audit_logging",  True, "Audit logging is enabled."),
    ]
    for man_key, uc_key, expected, pass_msg in bool_checks:
        if _get(man_ac, man_key, default=False):
            uc_val = _get(uc_ac, uc_key, default=None)
            if uc_val == expected or (isinstance(uc_val, bool) and uc_val):
                findings.append({"control": f"access_control.{uc_key}", "status": PASS, "detail": pass_msg})
            else:
                findings.append({"control": f"access_control.{uc_key}", "status": FAIL,
                                  "detail": f"'{uc_key}' is REQUIRED but not satisfied (found: {uc_val}).",
                                  "severity": "high"})

    # Safeguarding (school-specific)
    if _get(man_ac, "safeguarding_restricted_access", default=False):
        uc_sg = _get(uc_ac, "safeguarding_restricted_access") or \
                _get(uc, "data_flows", "access", "safeguarding_restricted_access", default=False)
        if uc_sg:
            findings.append({"control": "access_control.safeguarding", "status": PASS,
                              "detail": "Safeguarding restricted access is in place."})
        else:
            findings.append({"control": "access_control.safeguarding", "status": FAIL,
                              "detail": "Safeguarding restricted access is REQUIRED but not implemented.",
                              "severity": "high"})
    return findings


def check_pseudonymisation(uc: dict, man: dict) -> List[dict]:
    findings = []
    man_pseudo = _get(man, "required_controls", "pseudonymisation", default={})
    uc_pseudo  = _get(uc,  "environment", "anonymisation_pseudonymisation") or \
                 _get(uc,  "environment", "anonymisation", default={})

    if _get(man_pseudo, "required", default=False):
        uc_enabled = _get(uc_pseudo, "pseudonymisation_required") or \
                     _get(uc_pseudo, "pseudonymisation", default=False)
        if uc_enabled:
            findings.append({"control": "pseudonymisation.enabled", "status": PASS,
                              "detail": "Pseudonymisation is implemented."})
        else:
            findings.append({"control": "pseudonymisation.enabled", "status": FAIL,
                              "detail": "Pseudonymisation is REQUIRED but NOT implemented.",
                              "severity": "high"})
    else:
        findings.append({"control": "pseudonymisation.enabled", "status": INFO,
                          "detail": "Pseudonymisation not required for this use case."})
    return findings


def check_policies(uc: dict, man: dict) -> List[dict]:
    findings = []
    man_pol = _get(man, "required_controls", "policies", default={})
    uc_pol  = _get(uc,  "environment", "policies", default={})

    policy_map = {
        "privacy_policy_published": "privacy_policy_published",
        "data_retention_policy": "data_retention_policy",
        "breach_response_plan": "data_breach_response_plan",
        "staff_training": "staff_training_required",
        "dsar_procedure": "data_subject_rights_procedure",
    }
    for man_key, uc_key in policy_map.items():
        if _get(man_pol, man_key, default=False):
            uc_val = _get(uc_pol, uc_key, default=False)
            if uc_val:
                findings.append({"control": f"policies.{man_key}", "status": PASS,
                                  "detail": f"Policy '{man_key}' is in place."})
            else:
                findings.append({"control": f"policies.{man_key}", "status": FAIL,
                                  "detail": f"Policy '{man_key}' is REQUIRED but NOT implemented.",
                                  "severity": "medium"})
    return findings


def check_consent(uc: dict, man: dict) -> List[dict]:
    findings = []
    man_con = _get(man, "required_controls", "consent", default={})
    uc_con  = _get(uc,  "environment", "consent_management", default={})

    consent_fields = [
        ("explicit_consent_required",    "explicit_consent_required"),
        ("withdrawal_mechanism_required", "consent_withdrawal_mechanism"),
        ("consent_audit_trail_required",  "consent_audit_trail"),
    ]
    for man_key, uc_key in consent_fields:
        man_val = _get(man_con, man_key, default=False)
        if man_val:
            uc_val = _get(uc_con, uc_key, default=False)
            if uc_val:
                findings.append({"control": f"consent.{man_key}", "status": PASS,
                                  "detail": f"Consent control '{man_key}' is satisfied."})
            else:
                findings.append({"control": f"consent.{man_key}", "status": FAIL,
                                  "detail": f"Consent control '{man_key}' is REQUIRED but NOT implemented.",
                                  "severity": "high"})

    # Parental consent (school)
    if _get(man_con, "parental_consent_for_minors", default=False):
        uc_parental = _get(uc_con, "parental_consent_for_minors", default=False)
        if uc_parental:
            findings.append({"control": "consent.parental_consent", "status": PASS,
                              "detail": "Parental consent for minors is in place."})
        else:
            findings.append({"control": "consent.parental_consent", "status": FAIL,
                              "detail": "Parental consent is REQUIRED but NOT implemented.",
                              "severity": "critical"})
    return findings


def check_data_flows(uc: dict, man: dict) -> List[dict]:
    findings = []
    man_df = _get(man, "required_controls", "data_flows", default={})
    uc_df  = _get(uc, "data_flows", default={})

    # Collection
    if _get(man_df, "collection", "consent_at_collection", default=False):
        uc_val = _get(uc_df, "collection", "consent_captured", default=False)
        findings.append({
            "control": "data_flows.collection.consent",
            "status": PASS if uc_val else FAIL,
            "detail": "Consent captured at collection." if uc_val else "Consent NOT captured at collection — REQUIRED.",
            "severity": None if uc_val else "high"
        })
    if _get(man_df, "collection", "data_minimisation", default=False):
        uc_val = _get(uc_df, "collection", "data_minimisation", default=False)
        findings.append({
            "control": "data_flows.collection.minimisation",
            "status": PASS if uc_val else FAIL,
            "detail": "Data minimisation applied at collection." if uc_val else "Data minimisation NOT applied — REQUIRED.",
            "severity": None if uc_val else "medium"
        })

    # Storage
    if _get(man_df, "storage", "encrypted", default=False):
        uc_val = _get(uc_df, "storage") is not None
        uc_enc = _get(uc, "environment", "encryption", "at_rest", "enabled", default=False)
        findings.append({
            "control": "data_flows.storage.encrypted",
            "status": PASS if uc_enc else FAIL,
            "detail": "Storage encryption confirmed." if uc_enc else "Storage encryption REQUIRED but not confirmed.",
            "severity": None if uc_enc else "critical"
        })

    # Access
    if _get(man_df, "access", "logged", default=False):
        uc_val = _get(uc_df, "access", "access_logging", default=False)
        findings.append({
            "control": "data_flows.access.logging",
            "status": PASS if uc_val else FAIL,
            "detail": "Access logging in place." if uc_val else "Access logging REQUIRED but not enabled.",
            "severity": None if uc_val else "high"
        })

    # Sharing
    if _get(man_df, "sharing", "dpa_required", default=False):
        uc_val = _get(uc_df, "sharing", "dpa_in_place", default=False)
        findings.append({
            "control": "data_flows.sharing.dpa",
            "status": PASS if uc_val else FAIL,
            "detail": "Data Processing Agreement in place." if uc_val else "DPA REQUIRED but not in place.",
            "severity": None if uc_val else "high"
        })

    # Deletion
    if _get(man_df, "deletion", "audit_trail", default=False):
        uc_val = _get(uc_df, "deletion", "audit_trail", default=False)
        findings.append({
            "control": "data_flows.deletion.audit_trail",
            "status": PASS if uc_val else FAIL,
            "detail": "Deletion audit trail maintained." if uc_val else "Deletion audit trail REQUIRED but not maintained.",
            "severity": None if uc_val else "medium"
        })
    return findings


def check_dpo(uc: dict, man: dict) -> List[dict]:
    findings = []
    man_dpo = _get(man, "required_controls", "dpo_required", default=False)
    uc_dpo  = _get(uc, "organisation", "dpo_appointed", default=False)
    if man_dpo:
        findings.append({
            "control": "governance.dpo",
            "status": PASS if uc_dpo else FAIL,
            "detail": "DPO appointed." if uc_dpo else "DPO is REQUIRED but NOT appointed.",
            "severity": None if uc_dpo else "critical"
        })
    return findings


def check_non_negotiables(uc: dict, man: dict) -> List[dict]:
    """Check non-negotiable controls using heuristic mapping."""
    findings = []
    nns = _get(man, "non_negotiable_controls", default=[])
    uc_env = _get(uc, "environment", default={})

    control_map = {
        "at_rest_encryption":        ("encryption.at_rest.enabled",         True),
        "in_transit_encryption":     ("encryption.in_transit.enabled",      True),
        "mfa":                       ("authentication.mfa_required",         True),
        "rbac_with_least_privilege": ("access_control.least_privilege",      True),
        "rbac":                      ("access_control.model",                "RBAC"),
        "pseudonymisation":          ("anonymisation.pseudonymisation",       True),
        "access_audit_logging":      ("access_control.audit_logging",        True),
        "breach_response_plan":      ("policies.data_breach_response_plan",  True),
        "staff_training":            ("policies.staff_training_required",    True),
        "consent_mechanism":         ("consent_management.explicit_consent_required", True),
        "parental_consent_for_minors": ("consent_management.parental_consent_for_minors", True),
        "dsar_procedure":            ("policies.data_subject_rights_procedure", True),
    }
    for nn in nns:
        if nn in control_map:
            path, expected = control_map[nn]
            keys = path.split(".")
            val = uc_env
            for k in keys:
                val = val.get(k, None) if isinstance(val, dict) else None
            met = (val == expected) or (isinstance(expected, bool) and bool(val) == expected)
            if met:
                findings.append({"control": f"non_negotiable.{nn}", "status": PASS,
                                  "detail": f"Non-negotiable control '{nn}' is satisfied."})
            else:
                findings.append({"control": f"non_negotiable.{nn}", "status": FAIL,
                                  "detail": f"NON-NEGOTIABLE control '{nn}' is NOT satisfied (found: {val}).",
                                  "severity": "critical"})
    return findings

def calculate_posture_rating(
    posture_score: float,
    critical_failures: int
) -> str:

    if critical_failures > 0:
        if posture_score < 50:
            return "CRITICAL"
        return "WEAK"

    if posture_score >= 90:
        return "STRONG"

    if posture_score >= 70:
        return "MODERATE"

    if posture_score >= 50:
        return "WEAK"

    return "CRITICAL"
# ─────────────────────────────────────────────
#  Main checker
# ─────────────────────────────────────────────

def run_checks(
    use_case: dict,
    manifest: dict,
    schema_path: str = DEFAULT_SCHEMA_PATH
) -> dict:

    all_findings = []

    # Stage 0 — structural schema validation
    all_findings.extend(
        validate_against_schema(
            use_case,
            schema_path
        )
    )

    # Stage 1 — privacy posture checks
    all_findings.extend(check_encryption(use_case, manifest))
    all_findings.extend(check_authentication(use_case, manifest))
    all_findings.extend(check_access_control(use_case, manifest))
    all_findings.extend(check_pseudonymisation(use_case, manifest))
    all_findings.extend(check_policies(use_case, manifest))
    all_findings.extend(check_consent(use_case, manifest))
    all_findings.extend(check_data_flows(use_case, manifest))
    all_findings.extend(check_dpo(use_case, manifest))
    all_findings.extend(check_non_negotiables(use_case, manifest))

    totals = {PASS: 0, FAIL: 0, WARNING: 0, INFO: 0}
    for f in all_findings:
        totals[f["status"]] = totals.get(f["status"], 0) + 1

    critical_fails = [f for f in all_findings if f.get("severity") == "critical" and f["status"] == FAIL]
    posture_score  = round(totals[PASS] / max(totals[PASS] + totals[FAIL] + totals[WARNING], 1) * 100, 1)

    return {
        "report_id": f"CHK-{use_case.get('use_case_id','?')}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "use_case_id": use_case.get("use_case_id"),
        "use_case_name": use_case.get("use_case_name"),
        "manifest_id": manifest.get("manifest_id"),
        "checked_at": datetime.now().isoformat(),
        "summary": {
            "total_checks": sum(totals.values()),
            "pass": totals[PASS],
            "fail": totals[FAIL],
            "warning": totals[WARNING],
            "info": totals[INFO],
            "posture_score_percent": posture_score,
            "posture_rating": calculate_posture_rating(posture_score, len(critical_fails)),
            "critical_failures": len(critical_fails),
        },
        "findings": all_findings,
        "critical_failures": critical_fails,
    }


def main():
    parser = argparse.ArgumentParser(description="Privacy Posture Static Checker")
    parser.add_argument("use_case", help="Path to use-case JSON file")
    parser.add_argument("manifest", help="Path to manifest JSON file")
    parser.add_argument("--output", default=None, help="Path to save the report JSON")
    args = parser.parse_args()

    with open(args.use_case)  as f: use_case = json.load(f)
    with open(args.manifest)  as f: manifest = json.load(f)

    report = run_checks(use_case, manifest)

    # Pretty-print summary
    s = report["summary"]
    print(f"\n{'='*60}")
    print(f"  Privacy Posture Check — {report['use_case_name']}")
    print(f"{'='*60}")
    print(f"  Manifest : {report['manifest_id']}")
    print(f"  Checked  : {report['checked_at']}")
    print(f"  Score    : {s['posture_score_percent']}%  [{s['posture_rating']}]")
    print(f"  PASS: {s['pass']}  FAIL: {s['fail']}  WARN: {s['warning']}  INFO: {s['info']}")
    print(f"  Critical failures: {s['critical_failures']}")
    print(f"{'='*60}\n")

    print("FINDINGS:")
    for f in report["findings"]:
        icon = {"PASS": "✓", "FAIL": "✗", "WARNING": "!", "INFO": "i"}.get(f["status"], "?")
        sev = f" [{f['severity'].upper()}]" if f.get("severity") else ""
        print(f"  {icon} [{f['status']}]{sev}  {f['control']}: {f['detail']}")

    if report["critical_failures"]:
        print("\nCRITICAL FAILURES:")
        for f in report["critical_failures"]:
            print(f"  !! {f['control']}: {f['detail']}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {args.output}")

    return 0 if s["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
