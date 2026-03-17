from __future__ import annotations

from typing import Any


class ChangeDetectionEngine:
    def diff(self, previous: dict[str, Any] | None, current: dict[str, Any]) -> list[dict[str, str]]:
        if not previous:
            return [{'category': 'baseline', 'message': 'Initial snapshot created'}]
        changes: list[dict[str, str]] = []

        prev_score = previous.get('score_breakdown', {}).get('final_opportunity_score')
        curr_score = current.get('score_breakdown', {}).get('final_opportunity_score')
        if prev_score is not None and curr_score is not None and abs(curr_score - prev_score) >= 0.1:
            changes.append({'category': 'score_moved', 'message': f'Score changed from {prev_score:.2f} to {curr_score:.2f}'})

        prev_runway = previous.get('financial', {}).get('runway_quarters')
        curr_runway = current.get('financial', {}).get('runway_quarters')
        if prev_runway != curr_runway:
            changes.append({'category': 'runway_changed', 'message': f'Runway changed from {prev_runway} to {curr_runway}'})

        prev_cats = {f"{x.get('type')}|{x.get('title')}" for x in previous.get('catalysts', [])}
        curr_cats = {f"{x.get('type')}|{x.get('title')}" for x in current.get('catalysts', [])}
        for added in sorted(curr_cats - prev_cats):
            changes.append({'category': 'new_catalyst', 'message': f'Added catalyst {added}'})
        for dropped in sorted(prev_cats - curr_cats):
            changes.append({'category': 'catalyst_dropped', 'message': f'Dropped catalyst {dropped}'})

        return changes or [{'category': 'no_material_change', 'message': 'No material changes detected'}]
