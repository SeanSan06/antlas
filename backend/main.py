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

@app.post("/events")
def create_item(item: Item):
    pass