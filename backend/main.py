from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    id:  int
    name: str
    host: str
    time: str #ISO datetime
    location: str
    attendees: List[str] = []

events_db = []

# Adds 1 event to events_db
@app.post("/events", response_model=Event)
def create_event(new_event: Event):
    for event_index in events_db:
        if event_index.id == new_event.id:
            raise HTTPException(status_code=400, detail="Event with this ID already exists")
    events_db.append(new_event)

    return new_event

# Remove 1 event to events_db
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

