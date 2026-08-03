from pydantic import BaseModel
from typing import List

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    diagnosis: str
    therapy_goal: str
    triggers: List[str]
    safe_objects: List[str]