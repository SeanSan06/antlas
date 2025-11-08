# Antlas
Antlas is a web based application allowing users to create events. Users can choose what to name their event and display their name so others can identify who is hosting it. Furthermore, the time of the event can also be set. User can use the built in map to pinpoint the exact location they want their event to be.

## Pictures of website
![Example Image](/frontend/images/home.png)
![Example Image](/frontend/images/map-demo.png)
![Example Image](/frontend/images/about.png)

## How it's made
Technology used: HTML, CSS, JavaScript, FastAPI, Python, SQLite, and OpenStreetMap API

**HTML**: We used HTML to layout all of the content for each of the web pages(Home, Events, and About)

**CSS**: We used CSS to style our entire website and add color and nice formatting. We utilize modern CSS tools like flexbox to further style each page, add animations, and better UX(like the cursor changing to a pointer when hovering over buttons).

**JavaScript**: We used JS to give dynamic functionality to our website. By using JS, we were able to update the DOM and add overlays, popups, and send fetch requests to the backend(which is built with FastAPI).

**FastAPI with Python**: We used FastAPI to create a custom API that allows for real-time communication between the frontend and the backend. The frontend sends fetch requests for each webpage or event creation data. The backend has multiple endpoints that listen for requests from the frontend. Each endpoint has their own method that will be run once it captures a matching fetch request. We have endpoints that talk to the SQLite, some write data to the database, while other endpoints get data from the database. We also have endpoints that serve up each of the web pages(Home, Events, and About) as needed.

**SQLite**: We used SQLite as our database, as we wanted something that integrates well with Python. Our SQLite contains a database that holds all the event data information(id, name, host, time, location).

**OpenStreetMap**: We used OpenStreetMap to have a nice visual UI that users can interact with. Users can double click to place a pin on the map, and a pop up will show up allowing them to make an event. Users can then see their event on the map along with everyone else's events.


## What We learned
We learned a lot about how to utilize HTML, CSS, and JS to style and design our website from the ground up. We learned how to lay out each component, whether it be a navigation bar, landing area, hero area, or map area. We also learned how to send fetch requests through JS and what format the data should be sent in. From there, we learned about make simple SQLite databases that could store data such as names, time, and geocoordinates(long, lat).

## Credits
Thank you to OpenStreetMap for the map API
