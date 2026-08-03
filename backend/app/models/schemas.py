from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SessionStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class PatientCreate(BaseModel):
    name: str
    age: int = Field(ge=1, le=120)
    diagnosis: str | None = None
    notes: str | None = None
    goals: list[str] = Field(default_factory=list)


class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = Field(default=None, ge=1, le=120)
    diagnosis: str | None = None
    notes: str | None = None
    goals: list[str] | None = None


class Patient(PatientCreate):
    id: str
    created_at: datetime


class TherapyBlueprintRequest(BaseModel):
    patient_id: str
    intake_summary: str | None = None
    therapist_notes: str | None = None


class VREnvironmentStep(BaseModel):
    scene: str
    duration_minutes: int = Field(ge=1)
    objectives: list[str] = Field(default_factory=list)
    adaptation_triggers: list[str] = Field(default_factory=list)


class TherapyBlueprint(BaseModel):
    id: str
    patient_id: str
    title: str
    approach: str
    vr_environment: list[VREnvironmentStep]
    safety_notes: list[str] = Field(default_factory=list)
    approved: bool = False
    created_at: datetime


class HeartRateReading(BaseModel):
    bpm: int = Field(ge=30, le=220)
    timestamp: datetime | None = None


class VoiceCommand(BaseModel):
    transcript: str
    timestamp: datetime | None = None


class SessionEvent(BaseModel):
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime | None = None


class SessionReportRequest(BaseModel):
    patient_id: str
    blueprint_id: str
    session_duration_minutes: int = Field(ge=1)
    heart_rate_readings: list[HeartRateReading] = Field(default_factory=list)
    voice_commands: list[VoiceCommand] = Field(default_factory=list)
    session_events: list[SessionEvent] = Field(default_factory=list)
    therapist_notes: str | None = None


class SessionReport(BaseModel):
    id: str
    patient_id: str
    blueprint_id: str
    summary: str
    patient_response: str
    physiological_insights: str
    recommendations: list[str]
    risk_flags: list[str] = Field(default_factory=list)
    created_at: datetime
