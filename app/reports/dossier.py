from __future__ import annotations

import json
from pathlib import Path

from app.research.schemas import Dossier


def to_markdown(dossier: Dossier) -> str:
    lines = [
        f"# {dossier.company.ticker} Research Dossier",
        '',
        '## Executive Summary',
        f"- Final score: {dossier.score_breakdown.final_opportunity_score:.2f}",
        f"- Setup archetype: {dossier.archetype.get('archetype', 'n/a')}",
        f"- Why now: {dossier.neutral_committee_view}",
        '',
        '## Catalyst Timeline',
    ]
    for c in dossier.canonical_catalysts:
        lines.append(f"- {c.get('catalyst_type')}: {c.get('event_date') or c.get('event_window_start')} ({c.get('status')})")

    lines += [
        '',
        '## Program / Asset Map',
        f"- Entity resolution: {dossier.entity_resolution}",
        '',
        '## Clinical Trial Quality',
    ]
    for a in dossier.clinical_assessment:
        raw_assessment = a.get('assessment', {})
        assn = raw_assessment if isinstance(raw_assessment, dict) else {}
        lines.append(f"- {assn.get('trial_id')}: design={assn.get('design_quality_score')}, endpoint={assn.get('endpoint_quality_score')}, ambiguity={assn.get('ambiguity_risk')}")

    lines += [
        '',
        '## Financing & Dilution',
        f"- Runway (quarters): {dossier.financial.runway_quarters}",
        f"- Financing risk: {dossier.financing_risk}",
        '',
        '## Historical Analogs',
    ]
    for h in dossier.historical_analogs:
        lines.append(f"- {h.get('setup_id')}: distance={h.get('distance')} outcome={h.get('outcome_return')}")

    lines += [
        '',
        '## Bull / Bear / Committee',
        f"- Bull: {dossier.bull_thesis}",
        f"- Bear: {dossier.bear_thesis}",
        f"- Committee: {dossier.neutral_committee_view}",
        '',
        '## What Changed',
    ]
    lines.extend([f"- {x}" for x in dossier.what_changed])
    return '\n'.join(lines)


def save_dossier(dossier: Dossier, output_dir: Path, fmt: str = 'markdown') -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    if fmt == 'markdown':
        p = output_dir / f'{dossier.company.ticker}_dossier.md'
        p.write_text(to_markdown(dossier))
        return p
    if fmt == 'json':
        p = output_dir / f'{dossier.company.ticker}_dossier.json'
        p.write_text(json.dumps({'schema_version': '2.0', 'dossier': dossier.model_dump(mode='json')}, indent=2, default=str))
        return p
    if fmt in {'html', 'pdf-html'}:
        p = output_dir / f'{dossier.company.ticker}_dossier.html'
        body = to_markdown(dossier).replace('\n', '<br/>\n')
        p.write_text(f'<html><head><style>body{{font-family:Arial;padding:20px}}h1,h2{{color:#0b3d91}}</style></head><body>{body}</body></html>')
        return p
    raise ValueError(f'Unsupported format: {fmt}')
