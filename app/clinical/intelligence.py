from __future__ import annotations

from app.clinical.schemas import ClinicalAssessment, TrialIntelligence


class ClinicalAssessmentEngine:
    def assess(self, trial: TrialIntelligence) -> ClinicalAssessment:
        design = 0.4
        endpoints = 0.4
        interpretability = 0.5
        maturity = 0.4
        strengths: list[str] = []
        weaknesses: list[str] = []
        flags: list[str] = []

        if trial.randomized:
            design += 0.25
            strengths.append('Randomized design improves causal interpretability')
        else:
            weaknesses.append('Non-randomized design elevates bias risk')
        if trial.masking and 'double' in trial.masking.lower():
            design += 0.15
        if trial.control_type and trial.control_type.lower() in {'placebo', 'active'}:
            design += 0.1
        if any('survival' in ep.lower() or 'mortality' in ep.lower() for ep in trial.primary_endpoints):
            endpoints += 0.3
            strengths.append('Clinically meaningful primary endpoint')
        elif trial.primary_endpoints:
            endpoints += 0.15
        else:
            flags.append('Primary endpoint missing')

        if trial.enrollment_target and trial.enrollment_target >= 150:
            interpretability += 0.2
            maturity += 0.2
        if trial.actual_enrollment and trial.enrollment_target:
            ratio = trial.actual_enrollment / max(1, trial.enrollment_target)
            if ratio < 0.7:
                flags.append('Under-enrollment risk')
                maturity -= 0.1
            else:
                maturity += 0.1

        ambiguity = 1 - min(1.0, (design + interpretability) / 2)
        relevance = min(1.0, (endpoints * 0.7 + design * 0.3))
        if ambiguity > 0.55:
            weaknesses.append('Readout likely to be interpretation-sensitive')

        return ClinicalAssessment(
            trial_id=trial.trial_id,
            design_quality_score=min(1.0, design),
            endpoint_quality_score=min(1.0, endpoints),
            interpretability_score=min(1.0, interpretability),
            ambiguity_risk=max(0.0, min(1.0, ambiguity)),
            regulatory_relevance=max(0.0, min(1.0, relevance)),
            data_maturity_score=max(0.0, min(1.0, maturity)),
            strengths=strengths,
            weaknesses=weaknesses,
            risk_flags=flags,
            confidence=0.6 if trial.primary_endpoints else 0.4,
            likely_catalyst_window=trial.results_posting_date or trial.primary_completion_date,
        )

    def infer_trial_catalyst(self, trial: TrialIntelligence) -> dict:
        near_term = trial.primary_completion_date or trial.results_posting_date
        return {
            'trial_id': trial.trial_id,
            'inferred_catalyst_type': 'topline' if near_term else 'milestone',
            'likely_window': near_term or 'unknown',
            'actionable': bool(near_term and trial.phase.lower() in {'phase 2', 'phase 3'}),
        }
