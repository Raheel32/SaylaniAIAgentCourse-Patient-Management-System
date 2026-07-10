"""
main.py
-------
Entry point of the app. This is where FastAPI is created and where
all the API endpoints (routes) are defined.

To run this app (from the project's root folder, one level above `app/`):

    uvicorn app.main:app --reload

Then open your browser at:
    http://127.0.0.1:8000/docs

That gives you FastAPI's automatic interactive documentation (Swagger UI)
where you can test every endpoint directly — no separate tool like
Postman needed, though Postman works too.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud
from app.database import engine, SessionLocal

# This line creates the actual "patients" table in patients.db
# the first time the app runs (if it doesn't already exist).
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Patient Management System",
    description="A simple CRUD API to manage patient records, built with FastAPI + SQLAlchemy.",
    version="1.0.0",
)


def get_db():
    """
    Dependency that provides a database session to each request,
    and makes sure it's closed afterwards (even if an error happens).
    FastAPI calls this automatically for any endpoint that has
    `db: Session = Depends(get_db)` as a parameter.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
def read_root():
    """A simple welcome message — useful to check the server is running."""
    return {"message": "Welcome to the Patient Management System API. Visit /docs to try it out."}


# ---------- CREATE ----------
@app.post("/patients/", response_model=schemas.PatientResponse, status_code=status.HTTP_201_CREATED, tags=["Patients"])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """Add a new patient record."""
    return crud.create_patient(db=db, patient=patient)


# ---------- READ (all) ----------
@app.get("/patients/", response_model=List[schemas.PatientResponse], tags=["Patients"])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all patients (supports pagination via skip/limit)."""
    return crud.get_patients(db, skip=skip, limit=limit)


# ---------- READ (one) ----------
@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse, tags=["Patients"])
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get a single patient by their id."""
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


# ---------- UPDATE ----------
@app.put("/patients/{patient_id}", response_model=schemas.PatientResponse, tags=["Patients"])
def update_patient(patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(get_db)):
    """Update one or more fields of an existing patient."""
    db_patient = crud.update_patient(db, patient_id=patient_id, patient_update=patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


# ---------- DELETE ----------
@app.delete("/patients/{patient_id}", response_model=schemas.PatientResponse, tags=["Patients"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient record by id."""
    db_patient = crud.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient
