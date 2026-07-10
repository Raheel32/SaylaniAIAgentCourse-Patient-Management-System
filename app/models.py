"""
models.py
---------
Defines the actual database TABLE structure using SQLAlchemy.

Think of this class as a blueprint: every attribute below becomes a
column in the "patients" table inside patients.db.
"""

from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    # Primary key: unique ID for each patient, auto-incremented by the DB
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    disease = Column(String, nullable=True)   # optional: patient may not have one listed yet
    contact_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
