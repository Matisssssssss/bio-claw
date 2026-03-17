from __future__ import annotations

from datetime import datetime

from app.catalysts.schemas import CanonicalCatalyst, CatalystChange, CatalystSourceRecord, CatalystStatus, DatePrecision


class CanonicalCatalystEngine:
    def _key(self, rec: dict) -> str:
        return '|'.join([
            rec.get('ticker', 'unknown'),
            rec.get('type', 'unknown'),
            (rec.get('title') or '').lower().strip(),
        ])

    def normalize(self, records: list[dict]) -> list[CanonicalCatalyst]:
        grouped: dict[str, CanonicalCatalyst] = {}
        now = datetime.utcnow()
        for idx, r in enumerate(records):
            key = self._key(r)
            src = CatalystSourceRecord(
                source=r.get('source', 'unknown'),
                source_id=str(r.get('source_id', idx)),
                raw_title=r.get('title', 'untitled catalyst'),
            )
            if key not in grouped:
                grouped[key] = CanonicalCatalyst(
                    catalyst_id=f'cat_{abs(hash(key)) % 10_000_000}',
                    catalyst_type=r.get('type', 'unknown'),
                    confidence=float(r.get('confidence', 0.5)),
                    status=CatalystStatus(r.get('status', 'expected')),
                    event_date=r.get('event_date'),
                    event_window_start=r.get('event_window_start'),
                    event_window_end=r.get('event_window_end'),
                    date_precision=DatePrecision(r.get('date_precision', 'vague')),
                    source_records=[src],
                    evidence_links=list(r.get('evidence_links', [])),
                    earliest_seen_at=now,
                    latest_updated_at=now,
                )
            else:
                c = grouped[key]
                c.source_records.append(src)
                c.confidence = min(1.0, max(c.confidence, float(r.get('confidence', 0.5))))
                c.latest_updated_at = now
                if r.get('event_date') and not c.event_date:
                    c.event_date = r['event_date']
                    c.date_precision = DatePrecision.EXACT
                c.evidence_links = sorted(set(c.evidence_links + list(r.get('evidence_links', []))))
        return list(grouped.values())

    def detect_changes(self, old: list[CanonicalCatalyst], new: list[CanonicalCatalyst]) -> list[CatalystChange]:
        old_map = {c.catalyst_id: c for c in old}
        changes: list[CatalystChange] = []
        for c in new:
            previous = old_map.get(c.catalyst_id)
            if not previous:
                changes.append(CatalystChange(catalyst_id=c.catalyst_id, change_type='new_catalyst', new_value=c.catalyst_type))
                continue
            if previous.event_date != c.event_date:
                changes.append(CatalystChange(catalyst_id=c.catalyst_id, change_type='date_moved', old_value=str(previous.event_date), new_value=str(c.event_date)))
            if previous.status != c.status:
                changes.append(CatalystChange(catalyst_id=c.catalyst_id, change_type='status_changed', old_value=previous.status.value, new_value=c.status.value))
            if previous.confidence != c.confidence:
                changes.append(CatalystChange(catalyst_id=c.catalyst_id, change_type='confidence_changed', old_value=str(previous.confidence), new_value=str(c.confidence)))
        return changes
