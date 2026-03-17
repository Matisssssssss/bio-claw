from __future__ import annotations

from typing import Any, Dict

from app.agents.base import ResearchAgent
from app.archetypes.engine import ArchetypeEngine
from app.catalysts.engine import CanonicalCatalystEngine
from app.clinical.intelligence import ClinicalAssessmentEngine
from app.clinical.schemas import TrialIntelligence
from app.financing.parser import FilingFinancingParser
from app.financing.risk import FinancingRiskEngine
from app.master_data.security_master import SecurityMaster
from app.memory.engine import ChangeDetectionEngine
from app.research.schemas import AgentOutput
from app.similarity.engine import HistoricalSetup, SimilarityEngine


class EntityResolutionAgent(ResearchAgent):
    name = 'EntityResolutionAgent'

    def __init__(self) -> None:
        self.master = SecurityMaster()
        self.master.load_demo_records()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        company = self.master.resolve_company(ticker)
        resolved = self.master.resolve(company_mention=ticker)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'company_id': company.company_id if company else None, 'resolution': resolved.model_dump(mode='json')})


class CanonicalCatalystAgent(ResearchAgent):
    name = 'CanonicalCatalystAgent'

    def __init__(self) -> None:
        self.engine = CanonicalCatalystEngine()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        raw = state.get('RegulatoryCatalystAgent', {}).get('catalysts', []) + [
            {'ticker': ticker, 'type': 'topline', 'title': 'Phase 3 topline readout window', 'date_precision': 'quarter', 'event_window_start': None, 'event_window_end': None, 'confidence': 0.55, 'source': 'trial-transformer'}
        ]
        canonical = self.engine.normalize(raw)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'canonical_catalysts': [c.model_dump(mode='json') for c in canonical]})


class ClinicalAssessmentAgent(ResearchAgent):
    name = 'ClinicalAssessmentAgent'

    def __init__(self) -> None:
        self.engine = ClinicalAssessmentEngine()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        trials = state.get('ClinicalTrialsAgent', {}).get('trials', [])
        assessments = []
        for t in trials:
            ti = TrialIntelligence(
                trial_id=t['trial_id'],
                phase=t['phase'],
                status=t.get('status'),
                study_design=t.get('design'),
                randomized='randomized' in (t.get('design', '').lower()),
                masking='double-blind' if 'double-blind' in t.get('design', '').lower() else None,
                control_type='placebo',
                primary_endpoints=[t.get('primary_endpoint')] if t.get('primary_endpoint') else [],
                enrollment_target=250,
                actual_enrollment=220,
                primary_completion_date='2026-11-30',
                results_posting_date='2027-01-15',
            )
            assn = self.engine.assess(ti)
            assessments.append({'assessment': assn.model_dump(mode='json'), 'inferred_catalyst': self.engine.infer_trial_catalyst(ti)})
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'clinical_assessments': assessments})


class FinancingRiskAgent(ResearchAgent):
    name = 'FinancingRiskAgent'

    def __init__(self) -> None:
        self.parser = FilingFinancingParser()
        self.engine = FinancingRiskEngine()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        filings = state.get('FinancialHealthAgent', {}).get('filings', [])
        parsed = []
        for f in filings:
            text = str(f)
            parsed.extend(self.parser.parse_text(text, source_filing=f.get('form', 'unknown')))
        runway = state.get('FinancialHealthAgent', {}).get('financial', {}).get('runway_quarters')
        risk = self.engine.assess(parsed, runway_quarters=runway, catalyst_days=55)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'financing_events': [x.model_dump() for x in parsed], 'financing_risk': risk.model_dump()})


class SimilarityAgent(ResearchAgent):
    name = 'SimilarityAgent'

    def __init__(self) -> None:
        self.engine = SimilarityEngine()
        self.demo = [
            HistoricalSetup('hist_001', 'pdufa', 'mid', 'phase 3', 'small_molecule', 0.14, 5.1, 0.2, 0.45, 0.22),
            HistoricalSetup('hist_002', 'topline', 'small', 'phase 2', 'gene_therapy', 0.22, 3.0, -0.1, 0.7, -0.18),
            HistoricalSetup('hist_003', 'topline', 'small', 'phase 3', 'small_molecule', 0.18, 4.2, 0.05, 0.55, 0.11),
        ]

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        current = {
            'catalyst_type': (state.get('RegulatoryCatalystAgent', {}).get('catalysts', [{}])[0].get('type', 'topline')),
            'phase': 'phase 3',
            'modality': 'small_molecule',
            'short_interest': 0.16,
            'runway_quarters': state.get('FinancialHealthAgent', {}).get('financial', {}).get('runway_quarters', 4.0),
            'sentiment': state.get('NewsSentimentAgent', {}).get('sentiment_score', 0),
            'dilution_risk': state.get('FinancialHealthAgent', {}).get('financial', {}).get('dilution_risk_score', 0.5),
        }
        nearest = self.engine.nearest(current, self.demo)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'similar_setups': nearest})


class ArchetypeAgent(ResearchAgent):
    name = 'ArchetypeAgent'

    def __init__(self) -> None:
        self.engine = ArchetypeEngine()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        dossier_like = {
            'score_breakdown': state.get('score_breakdown', {}),
            'financial': state.get('FinancialHealthAgent', {}).get('financial', {}),
            'catalysts': state.get('RegulatoryCatalystAgent', {}).get('catalysts', []),
        }
        a = self.engine.classify(dossier_like)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'archetype': a.model_dump()})


class ChangeDetectionAgent(ResearchAgent):
    name = 'ChangeDetectionAgent'

    def __init__(self) -> None:
        self.engine = ChangeDetectionEngine()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        current = {
            'catalysts': state.get('RegulatoryCatalystAgent', {}).get('catalysts', []),
            'financial': state.get('FinancialHealthAgent', {}).get('financial', {}),
            'score_breakdown': state.get('score_breakdown', {}),
        }
        previous = state.get('MemoryAgent', {}).get('previous_snapshot')
        changes = self.engine.diff(previous, current)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'changes': changes})
