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

events_db = [2,3]

@app.post("/events", response_model=Event)
def create_item(new_event: Event):
    for event_index in events_db:
        if event_index.id == new_event.id:
            raise HTTPException(status_code=400, detail="Event with this ID already exists")
    events_db.append(new_event)

    return new_event

@app.get("/events", response_model=List[Event])
def get_all_events():
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