from app.archetypes.engine import ArchetypeEngine
from app.portfolio.construction import build_portfolio


def test_archetype_classification_and_portfolio_constraints() -> None:
    dossier = {'score_breakdown': {'final_opportunity_score': 0.65, 'risk_penalty': 0.7}, 'financial': {'runway_quarters': 3.5}, 'catalysts': [{'type': 'topline'}]}
    archetype = ArchetypeEngine().classify(dossier)
    assert archetype.archetype in {'pre-topline-binary', 'financing-overhang-rebound', 'de-risked-post-data-continuation', 'broken-biotech-special-situation'}
    portfolio = build_portfolio([
        {'ticker': 'A', 'score': 0.8, 'archetype': 'pre-topline-binary', 'liquidity_score': 1.0},
        {'ticker': 'B', 'score': 0.6, 'archetype': 'pre-topline-binary', 'liquidity_score': 1.0},
    ], max_binary_bucket=0.12)
    assert sum(x['suggested_weight'] for x in portfolio) <= 0.12 + 1e-6
