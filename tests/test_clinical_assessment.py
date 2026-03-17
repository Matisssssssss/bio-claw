from app.clinical.intelligence import ClinicalAssessmentEngine
from app.clinical.schemas import TrialIntelligence


def test_clinical_design_scoring() -> None:
    trial = TrialIntelligence(
        trial_id='NCT123', phase='Phase 3', randomized=True, masking='double-blind', control_type='placebo', primary_endpoints=['Overall survival'], enrollment_target=300, actual_enrollment=280
    )
    out = ClinicalAssessmentEngine().assess(trial)
    assert out.design_quality_score > 0.6
    assert out.endpoint_quality_score > 0.6
