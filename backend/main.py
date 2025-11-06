from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Event(BaseModel):
    id:  int
    name: str
    host: str
    time: str #ISO datetime
    location: str
    attendees: List[str] = []

events_db = []

@app.post("/events", response_model=Event)
def create_item(event: Event):
    for e in events_db:
        if e.id == event.id:
            raise HTTPException(status_code=400, detail="Event with this ID already exists")
    events_db.append(event)

    return event

@app.get("/events", response_model=List[Event])
def get_events():
    return events_db

@app.post("/events/{event_id}/join")
def join_event(event_id: int, attendee: str):
    for event in events_db:
        if event.id == event_id:
            if attendee not in event.attendees:
                event.attendees.append(attendee)
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@app.post("/events/{event_id}/leave")
def leave_event(event_id: int, attendee: str):
    for event in events_db:
        if event.id == event_id:
            if attendee in event.attendees:
                event.attendees.remove(attendee)
            return event
    raise HTTPException(status_code=404, detail="Event not found")