import json
from datetime import UTC, datetime
from uuid import uuid4

from app.models.schemas import (
    HeartRateReading,
    Patient,
    SessionEvent,
    TherapyBlueprint,
    TherapyBlueprintRequest,
    VREnvironmentStep,
    VoiceCommand,
)
from app.services import gemini

ELEVATED_HR_THRESHOLD = 100
HIGH_HR_THRESHOLD = 120


def _patient_summary(patient: Patient) -> str:
    return json.dumps(
        {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "diagnosis": patient.diagnosis,
            "notes": patient.notes,
            "goals": patient.goals,
        },
        indent=2,
    )


def _format_heart_rate(readings: list[HeartRateReading]) -> str:
    if not readings:
        return "None recorded"
    lines = [f"- {reading.bpm} BPM" for reading in readings]
    return "\n".join(lines)


def _format_voice_commands(commands: list[VoiceCommand]) -> str:
    if not commands:
        return "None recorded"
    return "\n".join(f"- {command.transcript}" for command in commands)


def _format_session_events(events: list[SessionEvent]) -> str:
    if not events:
        return "None recorded"
    return "\n".join(f"- {event.type}: {json.dumps(event.payload)}" for event in events)


def assess_physiological_state(readings: list[HeartRateReading]) -> dict:
    if not readings:
        return {"status": "unknown", "adaptation": None}

    latest = readings[-1].bpm
    if latest >= HIGH_HR_THRESHOLD:
        return {
            "status": "elevated",
            "adaptation": "Reduce VR intensity, switch to grounding scene, notify therapist",
        }
    if latest >= ELEVATED_HR_THRESHOLD:
        return {
            "status": "moderate",
            "adaptation": "Slow pacing and add breathing guidance",
        }
    return {"status": "stable", "adaptation": None}


def evaluate_voice_adaptation(command: VoiceCommand) -> dict | None:
    lowered = command.transcript.lower()
    distress_terms = ("stop", "help", "anxious", "scared", "panic", "too much")
    if any(term in lowered for term in distress_terms):
        return {
            "action": "de-escalate",
            "reason": f"Distress language detected: {command.transcript}",
        }
    return None


async def create_blueprint(
    patient: Patient,
    request: TherapyBlueprintRequest,
) -> TherapyBlueprint:
    payload = await gemini.generate_therapy_blueprint(
        patient_profile=_patient_summary(patient),
        intake_summary=request.intake_summary or "",
        therapist_notes=request.therapist_notes or "",
    )

    return TherapyBlueprint(
        id=str(uuid4()),
        patient_id=patient.id,
        title=payload["title"],
        approach=payload["approach"],
        vr_environment=[VREnvironmentStep(**step) for step in payload["vr_environment"]],
        safety_notes=payload.get("safety_notes", []),
        approved=False,
        created_at=datetime.now(UTC),
    )


async def generate_report(
    *,
    patient: Patient,
    blueprint: TherapyBlueprint,
    session_duration_minutes: int,
    heart_rate_readings: list[HeartRateReading],
    voice_commands: list[VoiceCommand],
    session_events: list[SessionEvent],
    therapist_notes: str | None,
) -> dict:
    return await gemini.generate_session_report(
        patient_profile=_patient_summary(patient),
        therapy_blueprint=blueprint.model_dump_json(indent=2),
        session_duration=session_duration_minutes,
        heart_rate_data=_format_heart_rate(heart_rate_readings),
        voice_commands=_format_voice_commands(voice_commands),
        session_events=_format_session_events(session_events),
        therapist_notes=therapist_notes or "",
    )
