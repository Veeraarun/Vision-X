from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.schemas import SessionReport, SessionReportRequest
from app.routers.ai import get_blueprint_store
from app.routers.patients import get_patient_store
from app.services import therapy_engine

router = APIRouter(prefix="/reports", tags=["reports"])

_reports: dict[str, SessionReport] = {}


@router.post("", response_model=SessionReport, status_code=201)
async def create_report(payload: SessionReportRequest) -> SessionReport:
    patients = get_patient_store()
    blueprints = get_blueprint_store()

    patient = patients.get(payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    blueprint = blueprints.get(payload.blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Therapy blueprint not found")

    generated = await therapy_engine.generate_report(
        patient=patient,
        blueprint=blueprint,
        session_duration_minutes=payload.session_duration_minutes,
        heart_rate_readings=payload.heart_rate_readings,
        voice_commands=payload.voice_commands,
        session_events=payload.session_events,
        therapist_notes=payload.therapist_notes,
    )

    report = SessionReport(
        id=str(uuid4()),
        patient_id=payload.patient_id,
        blueprint_id=payload.blueprint_id,
        summary=generated["summary"],
        patient_response=generated["patient_response"],
        physiological_insights=generated["physiological_insights"],
        recommendations=generated.get("recommendations", []),
        risk_flags=generated.get("risk_flags", []),
        created_at=datetime.now(UTC),
    )
    _reports[report.id] = report
    return report


@router.get("/{report_id}", response_model=SessionReport)
def get_report(report_id: str) -> SessionReport:
    report = _reports.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/patient/{patient_id}", response_model=list[SessionReport])
def list_patient_reports(patient_id: str) -> list[SessionReport]:
    if patient_id not in get_patient_store():
        raise HTTPException(status_code=404, detail="Patient not found")
    return [report for report in _reports.values() if report.patient_id == patient_id]
