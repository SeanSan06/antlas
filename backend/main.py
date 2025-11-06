from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import create_tables, get_connection

app = FastAPI()
create_tables()

# Set up CORS for the backend server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event class object, inherit from BaseModl for pydantic type checking/conversion
class Event(BaseModel):
    id:  int | None = None
    name: str
    host: str
    time: str #ISO datetime
    location: str
    attendees: List[str] = []

events_db = []

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

# Remove an event from events_db
@app.post("/events{event_id}")
def remove_event(host: str, event_id:int):
    for i, event in enumerate(events_db):
        if event.id == event_id:
            if event.host == host:
                del events_db[i]
            else:
                raise HTTPException(status_code=403, detail = "Must be host to cancel")
            return {"message": "Event canceled"}
        
    raise HTTPSException(status_code=404, detail = "Event not found")


# Returns all events in events_db
@app.get("/events", response_model=List[Event])
def get_all_events():
    return events_db

# Add an attendee to specific event in events_db
@app.post("/events/{event_id}/join")
def join_event(event_id: int, attendee: str):
    for event in events_db:
        if event.id == event_id:
            if attendee not in event.attendees:
                event.attendees.append(attendee)

            return event
        
    raise HTTPException(status_code=404, detail="Event not found")

# Removes an attendee from specific event in events_db
@app.post("/events/{event_id}/leave")
def leave_event(event_id: int, attendee: str):
    for event in events_db:
        if event.id == event_id:
            if attendee in event.attendees:
                event.attendees.remove(attendee)

            return event
        
    raise HTTPException(status_code=404, detail="Event not found")

