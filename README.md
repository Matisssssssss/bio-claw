# Biotech Scout

Biotech Scout is a production-oriented biotech catalyst intelligence system for event-driven biotech equity research.

## TL;DR
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev] && cp .env.example .env
python -m app.storage.database && PYTHONPATH=. pytest
```

## Why this project exists
Biotech catalyst workflows are noisy, fragmented, and often inconsistent across data sources.
Biotech Scout provides a single engine to:
- normalize catalysts and entities,
- detect what changed over time,
- score setup quality/risk,
- and expose it all through API, CLI, and Streamlit surfaces.

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

## Architecture (quick view)
```text
Collectors/Providers -> Parsers/Canonicalization -> Scoring/Similarity
       -> Research Orchestrator -> API/CLI/UI/OpenClaw surfaces
       -> Storage (SQLAlchemy models + repositories)
```

Core modules:
- `app/research`: orchestration and response schemas
- `app/catalysts`, `app/clinical`, `app/financing`, `app/scoring`: domain engines
- `app/master_data`: security master + entity aliasing
- `app/similarity`, `app/archetypes`, `app/portfolio`: decision support layers
- `app/api`, `app/cli`, `app/ui`, `app/openclaw`: delivery surfaces

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
python -m app.storage.database
```

## Quality checks
```bash
PYTHONPATH=. pytest
ruff check .
mypy app
```

## Demo mode (no API keys)
- Run without provider credentials using mock providers + `data/demo_setups.json`.
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

## API quickstart
```bash
uvicorn app.api.main:api --reload
```

## API endpoint map
| Method | Path | Description | Example |
|---|---|---|---|
| GET | `/companies/{ticker}/changes` | Structured what-changed feed | `/companies/NBIX/changes` |
| GET | `/catalysts/canonical/{ticker}` | Canonical catalyst timeline | `/catalysts/canonical/NBIX` |
| GET | `/financing/{ticker}` | Financing extraction + risk | `/financing/NBIX` |
| GET | `/similarity/{ticker}` | Historical comparable setups | `/similarity/NBIX` |
| GET | `/archetypes/{ticker}` | Setup archetype classification | `/archetypes/NBIX` |
| POST | `/portfolio/suggestions` | Portfolio construction proposal | body: ticker list |

## OpenClaw integration
Dedicated OpenClaw adapter with tool registry and execution contract.

### OpenClaw API
- `GET /openclaw/health`
- `GET /openclaw/tools`
- `POST /openclaw/execute`

### OpenClaw CLI
```bash
biotech-scout openclaw-tools
biotech-scout openclaw-exec "biotech.research_ticker" "{\"ticker\":\"NBIX\"}"
```

These are the default machine-to-machine integration surfaces for OpenClaw orchestrations.

## Production notes
- Provider runtime utilities support retry/backoff and TTL caching.
- DB schemas are migration-ready and include canonical catalyst + alias/security-master entities.
- Current extraction paths use robust heuristics and mock fallbacks when external providers are unavailable.

## Troubleshooting
### `pip install -e .[dev]` fails during package discovery
This repository includes non-package top-level folders (for example `data/`).
Package discovery is explicitly configured in `pyproject.toml` to include only `app*` packages.

### Tests fail with import errors
Use:
```bash
PYTHONPATH=. pytest
```

### API starts but routes fail on missing env vars
Copy `.env.example` to `.env`, then restart server:
```bash
cp .env.example .env
uvicorn app.api.main:api --reload
```
