from app.config.settings import get_settings
from app.scoring.engine import BiotechScoringEngine


def test_scoring_outputs_range() -> None:
    state = {
        'MarketDataAgent': {'price_change_30d': 0.1, 'rel_volume': 2.0},
        'RegulatoryCatalystAgent': {'catalysts': [{'event_date': '2030-01-01'}]},
        'ClinicalTrialsAgent': {'trials': [{'phase': 'Phase 2'}]},
        'FinancialHealthAgent': {'financial': {'dilution_risk_score': 0.3}},
        'NewsSentimentAgent': {'sentiment_score': 0.2},
        'InsiderAndFlowAgent': {'insider_score': 0.7},
        'ScienceAndMechanismAgent': {'science_score': 0.8},
        'CompetitiveLandscapeAgent': {'crowded': True},
        'CatalystRiskAgent': {'risk_score': 0.3, 'red_flags': []},
    }
    out = BiotechScoringEngine(get_settings()).score(state)
    assert 0 <= out.final_opportunity_score <= 1
    assert out.data_completeness_score > 0.5
