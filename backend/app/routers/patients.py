from fastapi import APIRouter
from app.models.patient import Patient

router = APIRouter()

patients_db = []

@router.post("/patients")
def create_patient(patient: Patient):
    patients_db.append(patient)
    return {
        "message": "Patient created successfully",
        "patient": patient
    }

@router.get("/patients")
def get_patients():
    return patients_db