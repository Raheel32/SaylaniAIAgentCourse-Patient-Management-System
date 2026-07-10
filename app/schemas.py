"""
schemas.py
----------
Defines the "shape" of the data that comes IN to our API (requests)
and goes OUT of our API (responses). These are Pydantic models —
different from the SQLAlchemy models in models.py.

Why do we need both models.py AND schemas.py?
- models.py  -> describes the database TABLE (used internally)
- schemas.py -> describes the JSON that clients send/receive (used at the API boundary)

Keeping them separate means we control exactly what a client can send
us and what we send back (e.g., we might not want to expose every DB
column, or we might want extra validation like "age must be positive").
"""

from pydantic import BaseModel, Field
from typing import Optional


class PatientBase(BaseModel):
    """Fields shared between creating and reading a patient."""
    name: str = Field(..., example="Ayesha Khan")
    age: int = Field(..., gt=0, lt=150, example=32)
    gender: str = Field(..., example="Female")
    disease: Optional[str] = Field(None, example="Diabetes")
    contact_number: Optional[str] = Field(None, example="03001234567")
    address: Optional[str] = Field(None, example="Karachi, Pakistan")
    height_cm: Optional[float] = Field(None, example=165.0)
    weight_kg: Optional[float] = Field(None, example=68.5)


class PatientCreate(PatientBase):
    """Used when a client is CREATING a new patient (POST)."""
    pass


class PatientUpdate(BaseModel):
    """
    Used when a client is UPDATING a patient (PUT).
    All fields optional here so the client can send only what changed.
    """
    name: Optional[str] = None
    age: Optional[int] = Field(None, gt=0, lt=150)
    gender: Optional[str] = None
    disease: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None


class PatientResponse(PatientBase):
    """Used when SENDING a patient back to the client (includes the id)."""
    id: int

    class Config:
        # Allows Pydantic to read data straight from SQLAlchemy objects
        from_attributes = True
