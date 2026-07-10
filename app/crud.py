"""
crud.py
-------
CRUD = Create, Read, Update, Delete.

This file holds all the actual database logic, kept separate from
main.py (which just handles the API routes/endpoints). This separation
is good practice: main.py stays clean and readable, and this file can
be tested or reused independently.
"""

from sqlalchemy.orm import Session
from app import models, schemas


def create_patient(db: Session, patient: schemas.PatientCreate):
    """CREATE: adds a new patient row to the database."""
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)  # refresh to get the auto-generated id
    return db_patient


def get_patient(db: Session, patient_id: int):
    """READ (one): fetch a single patient by id, or None if not found."""
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    """READ (all): fetch a list of patients, with pagination support."""
    return db.query(models.Patient).offset(skip).limit(limit).all()


def update_patient(db: Session, patient_id: int, patient_update: schemas.PatientUpdate):
    """UPDATE: change only the fields the client actually provided."""
    db_patient = get_patient(db, patient_id)
    if db_patient is None:
        return None

    update_data = patient_update.dict(exclude_unset=True)  # only fields that were set
    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    """DELETE: remove a patient by id. Returns the deleted object, or None."""
    db_patient = get_patient(db, patient_id)
    if db_patient is None:
        return None

    db.delete(db_patient)
    db.commit()
    return db_patient
