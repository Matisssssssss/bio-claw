from __future__ import annotations


def build_portfolio(ideas: list[dict], max_single_weight: float = 0.08, max_binary_bucket: float = 0.2) -> list[dict]:
    ranked = sorted(ideas, key=lambda x: x.get('score', 0), reverse=True)
    out: list[dict] = []
    binary_used = 0.0
    total = 0.0
    for idea in ranked:
        base = min(max_single_weight, 0.01 + idea.get('score', 0) * 0.08)
        if idea.get('archetype') in {'pre-topline-binary', 'pre-pdufa-runner'}:
            room = max(0.0, max_binary_bucket - binary_used)
            weight = min(base, room)
            binary_used += weight
        else:
            weight = base
        liquidity = idea.get('liquidity_score', 0.5)
        weight *= max(0.5, min(1.0, liquidity))
        out.append({**idea, 'suggested_weight': round(weight, 4)})
        total += weight

    if total > 0:
        for row in out:
            row['normalized_weight'] = round(row['suggested_weight'] / total, 4)
    return out
