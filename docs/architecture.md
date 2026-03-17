# Architecture Notes

This repository implements a domain-oriented architecture:
- Data ingestion adapters are isolated in `app/clients`.
- Agents transform provider data into structured payloads.
- Orchestrator maintains shared state and executes deterministic sequencing.
- Scoring engine computes explainable, strategy-dependent score decomposition.
- Report layer emits dossier artifacts for analysts and downstream systems.
