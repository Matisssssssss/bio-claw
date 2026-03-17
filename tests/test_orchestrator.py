from app.research.orchestrator import BiotechResearchOrchestrator


def test_orchestrator_builds_dossier() -> None:
    d = BiotechResearchOrchestrator().run_ticker('ABIO')
    assert d.company.ticker == 'ABIO'
    assert len(d.catalysts) >= 1
    assert d.score_breakdown.final_opportunity_score >= 0
