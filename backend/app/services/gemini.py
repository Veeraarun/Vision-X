import json
import re

import google.generativeai as genai

from app.config import PROMPTS_DIR, settings


def _load_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.txt"
    return path.read_text(encoding="utf-8")


def _configure_client() -> None:
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured")
    genai.configure(api_key=settings.gemini_api_key)


def _extract_json(text: str) -> dict:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return json.loads(text[start : end + 1])

    raise ValueError("Model response did not contain valid JSON")


async def generate_text(prompt: str) -> str:
    _configure_client()
    model = genai.GenerativeModel(settings.gemini_model)
    response = await model.generate_content_async(prompt)
    return response.text or ""


async def run_intake(
    *,
    patient_context: str,
    therapist_notes: str,
    conversation: str,
) -> str:
    template = _load_prompt("intake")
    prompt = template.format(
        patient_context=patient_context,
        therapist_notes=therapist_notes or "None",
        conversation=conversation or "None yet",
    )
    return await generate_text(prompt)


async def generate_therapy_blueprint(
    *,
    patient_profile: str,
    intake_summary: str,
    therapist_notes: str,
) -> dict:
    template = _load_prompt("therapy")
    prompt = template.format(
        patient_profile=patient_profile,
        intake_summary=intake_summary or "Not available",
        therapist_notes=therapist_notes or "None",
    )
    text = await generate_text(prompt)
    return _extract_json(text)


async def generate_session_report(
    *,
    patient_profile: str,
    therapy_blueprint: str,
    session_duration: int,
    heart_rate_data: str,
    voice_commands: str,
    session_events: str,
    therapist_notes: str,
) -> dict:
    template = _load_prompt("report")
    prompt = template.format(
        patient_profile=patient_profile,
        therapy_blueprint=therapy_blueprint,
        session_duration=session_duration,
        heart_rate_data=heart_rate_data or "None recorded",
        voice_commands=voice_commands or "None recorded",
        session_events=session_events or "None recorded",
        therapist_notes=therapist_notes or "None",
    )
    text = await generate_text(prompt)
    return _extract_json(text)
