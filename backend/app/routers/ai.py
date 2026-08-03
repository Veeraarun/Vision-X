from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.schemas import (
    HeartRateReading,
    SessionEvent,
    TherapyBlueprint,
    TherapyBlueprintRequest,
    VoiceCommand,
)
from app.routers.patients import get_patient_store
from app.services import gemini, therapy_engine

router = APIRouter(prefix="/ai", tags=["ai"])

_blueprints: dict[str, TherapyBlueprint] = {}


class IntakeRequest(BaseModel):
    patient_id: str
    message: str
    conversation: str = ""
    therapist_notes: str | None = None


class IntakeResponse(BaseModel):
    reply: str


class BlueprintApproval(BaseModel):
    approved: bool = True


class AdaptationRequest(BaseModel):
    heart_rate_readings: list[HeartRateReading] = Field(default_factory=list)
    voice_command: VoiceCommand | None = None
    session_events: list[SessionEvent] = Field(default_factory=list)


class AdaptationResponse(BaseModel):
    physiological: dict
    voice_adaptation: dict | None = None


@router.post("/intake", response_model=IntakeResponse)
async def run_intake(payload: IntakeRequest) -> IntakeResponse:
    patients = get_patient_store()
    patient = patients.get(payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_context = patient.model_dump_json()
    conversation = f"{payload.conversation}\nTherapist/Patient: {payload.message}".strip()

    reply = await gemini.run_intake(
        patient_context=patient_context,
        therapist_notes=payload.therapist_notes or "",
        conversation=conversation,
    )
    return IntakeResponse(reply=reply)


@router.post("/therapy-blueprint", response_model=TherapyBlueprint, status_code=201)
async def create_therapy_blueprint(payload: TherapyBlueprintRequest) -> TherapyBlueprint:
    patients = get_patient_store()
    patient = patients.get(payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    blueprint = await therapy_engine.create_blueprint(patient, payload)
    _blueprints[blueprint.id] = blueprint
    return blueprint


@router.get("/therapy-blueprint/{blueprint_id}", response_model=TherapyBlueprint)
def get_therapy_blueprint(blueprint_id: str) -> TherapyBlueprint:
    blueprint = _blueprints.get(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Therapy blueprint not found")
    return blueprint


@router.patch("/therapy-blueprint/{blueprint_id}/approval", response_model=TherapyBlueprint)
def approve_therapy_blueprint(blueprint_id: str, payload: BlueprintApproval) -> TherapyBlueprint:
    blueprint = _blueprints.get(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Therapy blueprint not found")

    updated = blueprint.model_copy(update={"approved": payload.approved})
    _blueprints[blueprint_id] = updated
    return updated


@router.post("/adapt", response_model=AdaptationResponse)
def evaluate_adaptation(payload: AdaptationRequest) -> AdaptationResponse:
    physiological = therapy_engine.assess_physiological_state(payload.heart_rate_readings)
    voice_adaptation = None
    if payload.voice_command:
        voice_adaptation = therapy_engine.evaluate_voice_adaptation(payload.voice_command)

    return AdaptationResponse(
        physiological=physiological,
        voice_adaptation=voice_adaptation,
    )


def get_blueprint_store() -> dict[str, TherapyBlueprint]:
    return _blueprints
