#!/usr/bin/env python3
"""
Privacy Posture Evaluator
==========================
Master evaluation runner that:
  1. Runs the static privacy checker for each use case vs its manifest.
  2. Runs the FSM simulation for each use case (3 days each).
  3. Runs the monitor on each simulation log.
  4. Generates a consolidated evaluation report.

Usage:
    python privacy_evaluator.py [--output evaluation_report.json]
"""

import json
import os
import sys
import argparse
from datetime import datetime

# Add the framework directory to path
sys.path.insert(0, os.path.dirname(__file__))

from privacy_checker import run_checks
from privacy_fsm_simulation import USE_CASE_CONFIGS, run_fsm
from privacy_monitor import run_pipeline

BASE_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


USE_CASES = [
    {
        "uc_file":       os.path.join(BASE_DIR, "use_case_gp.json"),
        "manifest_file": os.path.join(BASE_DIR, "manifest_gp.json"),
        "sim_key":       "GP",
    },
    {
        "uc_file":       os.path.join(BASE_DIR, "use_case_school.json"),
        "manifest_file": os.path.join(BASE_DIR, "manifest_school.json"),
        "sim_key":       "SCHOOL",
    },
    {
        "uc_file":       os.path.join(BASE_DIR, "use_case_hotel.json"),
        "manifest_file": os.path.join(BASE_DIR, "manifest_hotel.json"),
        "sim_key":       "HOTEL",
    },
]


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def run_all_evaluations(days: int = 3, seed: int = 42) -> dict:
    results = []

    for uc_cfg in USE_CASES:
        print(f"\n{'─'*60}")
        use_case = load_json(uc_cfg["uc_file"])
        manifest = load_json(uc_cfg["manifest_file"])
        sim_key  = uc_cfg["sim_key"]
        uc_name  = use_case["use_case_name"]

        print(f"[1/3] Static Check — {uc_name}")
        check_report = run_checks(use_case, manifest)
        check_out = os.path.join(LOGS_DIR, f"{sim_key.lower()}_check_report.json")
        with open(check_out, "w") as f:
            json.dump(check_report, f, indent=2)

        print(f"[2/3] FSM Simulation — {uc_name} ({days} days)")
        cfg    = USE_CASE_CONFIGS[sim_key]
        events = run_fsm(cfg, days, seed)
        log_data = {
            "simulation_id": f"SIM-{cfg['use_case_id']}-eval",
            "use_case": cfg["name"],
            "days_simulated": days,
            "total_events": len(events),
            "seed": seed,
            "generated_at": datetime.now().isoformat(),
            "events": events,
        }
        log_out = os.path.join(LOGS_DIR, f"{sim_key.lower()}_activity_log.json")
        with open(log_out, "w") as f:
            json.dump(log_data, f, indent=2)

        print(f"[3/3] Monitor — {uc_name}")
        monitor_report = run_pipeline(log_data)
        mon_out = os.path.join(LOGS_DIR, f"{sim_key.lower()}_monitor_report.json")
        with open(mon_out, "w") as f:
            json.dump(monitor_report, f, indent=2)

        # Combined scoring
        check_score   = check_report["summary"]["posture_score_percent"]
        check_rating  = check_report["summary"]["posture_rating"]
        mon_compliance = monitor_report["compliance_rate_percent"]
        mon_posture   = monitor_report["overall_posture"]
        combined_score = round((check_score + mon_compliance) / 2, 1)

        if combined_score >= 90:
            combined_rating = "STRONG"
        elif combined_score >= 75:
            combined_rating = "MODERATE"
        elif combined_score >= 55:
            combined_rating = "WEAK"
        else:
            combined_rating = "CRITICAL"

        results.append({
            "use_case_id":   use_case["use_case_id"],
            "use_case_name": uc_name,
            "static_check": {
                "score_percent":    check_score,
                "posture_rating":   check_rating,
                "total_checks":     check_report["summary"]["total_checks"],
                "pass":             check_report["summary"]["pass"],
                "fail":             check_report["summary"]["fail"],
                "critical_failures": check_report["summary"]["critical_failures"],
            },
            "simulation": {
                "days":         days,
                "total_events": len(events),
                "state_distribution": {
                    st: sum(1 for e in events if e["event_type"] == st)
                    for st in set(e["event_type"] for e in events)
                },
            },
            "monitor": {
                "events_processed":    monitor_report["total_events_processed"],
                "violations_detected": monitor_report["total_violations_detected"],
                "compliance_rate":     mon_compliance,
                "posture":             mon_posture,
                "severity_breakdown":  monitor_report["severity_breakdown"],
                "top_violation_types": dict(
                    sorted(monitor_report["violation_types"].items(),
                           key=lambda x: x[1], reverse=True)[:5]
                ),
            },
            "combined_evaluation": {
                "combined_score_percent": combined_score,
                "combined_rating":        combined_rating,
            },
            "check_report_path":   check_out,
            "log_path":            log_out,
            "monitor_report_path": mon_out,
        })

        print(f"  Static check score : {check_score}% [{check_rating}]")
        print(f"  Monitor compliance : {mon_compliance}% [{mon_posture}]")
        print(f"  Combined rating    : {combined_score}% [{combined_rating}]")

    # Cross-case comparison
    best  = max(results, key=lambda x: x["combined_evaluation"]["combined_score_percent"])
    worst = min(results, key=lambda x: x["combined_evaluation"]["combined_score_percent"])

    overall_report = {
        "evaluation_id":  f"EVAL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generated_at":   datetime.now().isoformat(),
        "days_simulated": days,
        "seed":           seed,
        "use_case_results": results,
        "cross_case_comparison": {
            "best_posture":  {"use_case": best["use_case_name"],
                              "score": best["combined_evaluation"]["combined_score_percent"]},
            "worst_posture": {"use_case": worst["use_case_name"],
                              "score": worst["combined_evaluation"]["combined_score_percent"]},
            "average_combined_score": round(
                sum(r["combined_evaluation"]["combined_score_percent"] for r in results) / len(results), 1
            ),
        },
    }
    return overall_report


def main():
    parser = argparse.ArgumentParser(description="Privacy Posture Evaluator")
    parser.add_argument("--days",   type=int, default=3)
    parser.add_argument("--seed",   type=int, default=42)
    parser.add_argument("--output", default=os.path.join(LOGS_DIR, "evaluation_report.json"))
    args = parser.parse_args()

    report = run_all_evaluations(args.days, args.seed)

    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  OVERALL EVALUATION COMPLETE")
    print(f"{'='*60}")
    cc = report["cross_case_comparison"]
    print(f"  Average combined score : {cc['average_combined_score']}%")
    print(f"  Best posture  : {cc['best_posture']['use_case']} ({cc['best_posture']['score']}%)")
    print(f"  Worst posture : {cc['worst_posture']['use_case']} ({cc['worst_posture']['score']}%)")
    print(f"  Full report   : {args.output}")


if __name__ == "__main__":
    main()
