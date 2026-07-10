# SaylaniAIAgentCourse-Patient-Management-System
A simple REST API for managing patient records, built with FastAPI and SQLAlchemy

# Patient Management System — FastAPI CRUD API

A simple REST API for managing patient records, built with FastAPI and
SQLAlchemy (using SQLite as the database, so no separate database
server setup is needed).

## Folder Structure

```
patient_management_system/
├── app/
│   ├── __init__.py      # marks `app` as a Python package
│   ├── main.py          # FastAPI app + all API routes/endpoints
│   ├── database.py      # database connection/session setup
│   ├── models.py        # SQLAlchemy model (the "patients" table)
│   ├── schemas.py        # Pydantic schemas (request/response validation)
│   └── crud.py           # Create/Read/Update/Delete database logic
├── requirements.txt      # Python dependencies
└── README.md
```

## Setup Instructions

1. Create a virtual environment (recommended, keeps dependencies isolated):
   ```bash
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server (from the project's root folder, the one containing `app/`):
   ```bash
   uvicorn app.main:app --reload
   ```
   `--reload` auto-restarts the server whenever you change the code — handy while developing.

4. Open the interactive docs in your browser:
   ```
   http://127.0.0.1:8000/docs
   ```
   This is FastAPI's built-in Swagger UI. You can test every endpoint here
   directly, with no extra tools needed.

A file called `patients.db` will be created automatically the first
time you run the app — that's your SQLite database.

## API Endpoints

| Method | Endpoint              | Description                     |
|--------|-----------------------|----------------------------------|
| GET    | `/`                    | Welcome message                 |
| POST   | `/patients/`           | Create a new patient             |
| GET    | `/patients/`           | Get all patients (paginated)     |
| GET    | `/patients/{id}`       | Get one patient by id            |
| PUT    | `/patients/{id}`       | Update a patient by id           |
| DELETE | `/patients/{id}`       | Delete a patient by id           |

## Example: Creating a Patient

Sample JSON body for `POST /patients/`:

```json
{
  "name": "Ayesha Khan",
  "age": 32,
  "gender": "Female",
  "disease": "Diabetes",
  "contact_number": "03001234567",
  "address": "Karachi, Pakistan",
  "height_cm": 165.0,
  "weight_kg": 68.5
}
```

## Testing the API

You have two easy options:

1. Swagger UI (`/docs`) — click on any endpoint, hit "Try it out", fill
   in the fields, and click "Execute". This is the fastest way and needs
   no extra software.
2. Postman or curl — for example:
   ```bash
   curl -X POST "http://127.0.0.1:8000/patients/" \
     -H "Content-Type: application/json" \
     -d '{"name":"Ayesha Khan","age":32,"gender":"Female"}'
   ```

## Notes on Design Choices (useful if asked in a viva/demo)

- SQLite was chosen for simplicity — perfect for an assignment. Switching
  to PostgreSQL/MySQL later only requires changing the URL in `database.py`.
- schemas.py vs models.py: `models.py` defines the database table;
  `schemas.py` defines what the API accepts/returns. Keeping them separate
  is standard FastAPI practice and gives you control over API validation.
- crud.py keeps database logic out of `main.py`, so routes stay short
  and readable, and the CRUD functions could be reused or tested separately.
