"""
database.py
------------
Sets up the connection to our database and provides a session
that the rest of the app can use to talk to it.

We're using SQLite here because it needs no separate server/install —
perfect for an assignment or small project. It's just a single file
called `patients.db` that gets created automatically.

If you ever wanted to switch to PostgreSQL or MySQL for a real project,
you'd only need to change the SQLALCHEMY_DATABASE_URL below — nothing
else in the app would need to change. That's the whole point of using
SQLAlchemy as an ORM (Object Relational Mapper).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database URL ---
# "sqlite:///./patients.db" means: use SQLite, and store the database
# file as "patients.db" in the current folder.
SQLALCHEMY_DATABASE_URL = "sqlite:///./patients.db"

# --- Engine ---
# The engine is the actual connection point to the database.
# connect_args is only needed for SQLite (it disallows multi-threaded
# access by default, and FastAPI can use multiple threads).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# --- Session ---
# A SessionLocal is what we use to actually send queries to the database.
# Each request in FastAPI will get its own session (see get_db() in main.py).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base ---
# All our database models (tables) will inherit from this Base class.
Base = declarative_base()
