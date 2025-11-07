from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import List
from database import create_tables, get_connection

app = FastAPI()
create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify e.g. ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event class object, inherit from BaseModel for pydantic type checking/conversion
class Event(BaseModel):
    id:  int | None = None
    name: str
    host: str
    time: str
    location: str

""" Communicates with the SQLite database """
# Adds an event to the SQLite database, attributes must be passed in
@app.post("/events", response_model=Event)
def create_event(new_event: Event):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO events (name, host, time, location) VALUES (?, ?, ?, ?)",
        (new_event.name, new_event.host, new_event.time, new_event.location),
    )
    connection.commit()
    new_event.id = cursor.lastrowid
    connection.close()

    return new_event

# Return an event given a specific ID #
@app.get("/events/{event_id}", response_model=Event)
def get_specific_event(event_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail = "Event not found")

    return {
        "id": row[0],
        "name": row[1],
        "host": row[2],
        "time": row[3],
        "location": row[4]
    }

# Returns all events in events_db
@app.get("/events", response_model=List[Event])
def get_all_events():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    connection.close()

    all_events = []
    for row in rows:
        all_events.append({
            "id": row[0],
            "name": row[1],
            "host": row[2],
            "time": row[3],
            "location": row[4]
        })

    return all_events

""" Serves up each page on the website to the user as needed """
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

app.mount("/static", StaticFiles(directory=ROOT_DIR / "frontend"), name="static")

@app.get("/")
def serve_home():
    return FileResponse(ROOT_DIR / "frontend" / "html" / "index.html")

@app.get("/about")
def serve_about():
    return FileResponse(ROOT_DIR / "frontend" / "html" / "about.html")

@app.get("/map")
def serve_map():
    return FileResponse(ROOT_DIR / "frontend" / "html" / "map.html")

