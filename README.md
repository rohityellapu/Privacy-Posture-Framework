# Privacy-Posture-Framework
Privacy Posture Framework
privacy-posture-framework/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── docker-compose.yml
├── Dockerfile
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
│
│       ├── __init__.py
│
│       ├── schema/
│       │
│       │   ├── models.py
│       │   ├── parser.py
│       │   ├── validator.py
│       │   ├── ontology.py
│       │   └── enums.py
│       │
│       ├── manifests/
│       │
│       │   ├── loader.py
│       │   ├── compiler.py
│       │   └── generator.py
│       │
│       ├── checker/
│       │
│       │   ├── checker.py
│       │   ├── report.py
│       │   ├── posture.py
│       │   ├── engine.py
│       │   └── rules/
│       │
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
│       │
│       │   ├── graph.py
│       │   ├── fsm.py
│       │   ├── workflow.py
│       │   ├── actors.py
│       │   ├── generator.py
│       │   ├── logger.py
│       │   └── scenarios/
│       │
│       │       ├── gp.py
│       │       ├── school.py
│       │       └── hotel.py
│       │
│       ├── monitor/
│       │
│       │   ├── lifecycle.py
│       │   ├── monitor.py
│       │   ├── alerts.py
│       │   ├── compliance.py
│       │   └── correlation.py
│       │
│       ├── evaluation/
│       │
│       │   ├── metrics.py
│       │   ├── benchmark.py
│       │   ├── experiments.py
│       │   ├── plots.py
│       │   └── posture_score.py
│       │
│       ├── utils/
│       │
│       │   ├── logging.py
│       │   ├── yaml.py
│       │   ├── graph.py
│       │   └── timer.py
│       │
│       └── cli.py
│
├── tests/
│
│   ├── schema/
│   ├── checker/
│   ├── simulator/
│   ├── monitor/
│   └── evaluation/
│
├── notebooks/
│
│   ├── experiment1.ipynb
│   ├── experiment2.ipynb
│   ├── experiment3.ipynb
│   └── benchmark.ipynb
│
└── examples/
    ├── gp_demo.py
    ├── school_demo.py
    └── hotel_demo.py
