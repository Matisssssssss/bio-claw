# Biotech Scout

Biotech Scout is a production-oriented biotech catalyst intelligence system for event-driven biotech equity research.

## Phase 2 expansion highlights
- Canonical security master with alias/entity resolution for company, asset, and indication references.
- Canonical catalyst normalization/merge engine with status/date precision and change detection.
- Clinical-trial intelligence and quality scoring (design, endpoints, interpretability, ambiguity).
- Financing extraction toolkit and financing-risk engine (shelf/ATM/convertible/warrant heuristics).
- Historical similarity engine with comparable setup retrieval.
- What-changed engine with structured change categories.
- Setup archetype classification and portfolio construction constraints.
- Expanded API/CLI/Streamlit surfaces for catalysts, changes, peers, archetypes, portfolio suggestions.
- Seeded demo dataset runnable in no-key mode.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
python -m app.storage.database
PYTHONPATH=. pytest -q
```

## Demo mode
- Run without API keys using mock providers + `data/demo_setups.json`.
- Seed helper:
```bash
biotech-scout seed-demo-data
```

## CLI examples
```bash
biotech-scout research NBIX
biotech-scout changes NBIX
biotech-scout catalyst-normalize NBIX
biotech-scout peer-group NBIX
biotech-scout archetypes --ticker NBIX
biotech-scout portfolio-build --tickers "NBIX,SRPT,ALNY"
biotech-scout similarity NBIX
```

## API examples
```bash
uvicorn app.api.main:api --reload
# /companies/{ticker}/changes
# /catalysts/canonical/{ticker}
# /financing/{ticker}
# /similarity/{ticker}
# /archetypes/{ticker}
# /portfolio/suggestions
```

## Production notes
- Provider runtime utilities support retry/backoff and TTL caching.
- DB schemas are migration-ready and include canonical catalyst + alias/security-master entities.
- Current data extraction uses robust heuristics and mock fallbacks when external providers are unavailable.


## OpenClaw integration
- Dedicated OpenClaw adapter with tool registry and execution contract.
- API endpoints:
  - `GET /openclaw/health`
  - `GET /openclaw/tools`
  - `POST /openclaw/execute`
- CLI helpers:
  - `biotech-scout openclaw-tools`
  - `biotech-scout openclaw-exec "biotech.research_ticker" "{\"ticker\":\"NBIX\"}"`

These are intended as the default machine-to-machine integration surface for OpenClaw orchestrations.
