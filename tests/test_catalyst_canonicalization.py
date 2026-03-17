from app.catalysts.engine import CanonicalCatalystEngine


def test_canonical_catalyst_merges_duplicates() -> None:
    engine = CanonicalCatalystEngine()
    recs = [
        {'ticker': 'NBIX', 'type': 'pdufa', 'title': 'PDUFA date for lead asset', 'source': 'reg', 'confidence': 0.7},
        {'ticker': 'NBIX', 'type': 'pdufa', 'title': 'PDUFA date for lead asset', 'source': 'news', 'confidence': 0.8},
    ]
    out = engine.normalize(recs)
    assert len(out) == 1
    assert out[0].confidence == 0.8
    assert len(out[0].source_records) == 2
