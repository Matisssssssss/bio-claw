from app.memory.engine import ChangeDetectionEngine


def test_change_detection_identifies_new_catalyst() -> None:
    prev = {'catalysts': [{'type': 'pdufa', 'title': 'old'}], 'financial': {'runway_quarters': 5}, 'score_breakdown': {'final_opportunity_score': 0.4}}
    cur = {'catalysts': [{'type': 'pdufa', 'title': 'old'}, {'type': 'topline', 'title': 'new'}], 'financial': {'runway_quarters': 4}, 'score_breakdown': {'final_opportunity_score': 0.6}}
    out = ChangeDetectionEngine().diff(prev, cur)
    cats = {x['category'] for x in out}
    assert 'new_catalyst' in cats
    assert 'runway_changed' in cats
