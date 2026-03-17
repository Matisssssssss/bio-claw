from app.event_studies.analytics import summarize_event_window


def test_event_summary_stats() -> None:
    out = summarize_event_window([0.1, -0.05, 0.02, 0.03])
    assert 'win_rate' in out
    assert out['p90'] >= out['p10']
