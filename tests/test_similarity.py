from app.similarity.engine import HistoricalSetup, SimilarityEngine


def test_similarity_returns_ranked_neighbors() -> None:
    history = [
        HistoricalSetup('a', 'pdufa', 'mid', 'phase 3', 'small', 0.1, 5, 0.1, 0.4, 0.2),
        HistoricalSetup('b', 'topline', 'small', 'phase 2', 'gene', 0.3, 2, -0.2, 0.8, -0.3),
    ]
    current = {'catalyst_type': 'pdufa', 'phase': 'phase 3', 'short_interest': 0.12, 'runway_quarters': 4.8, 'sentiment': 0.08, 'dilution_risk': 0.45}
    out = SimilarityEngine().nearest(current, history, k=1)
    assert out[0]['setup_id'] == 'a'
