const backendURL = "http://127.0.0.1:8000/events"; 

const createEventButton = document.querySelector("#create-event-button");
createEventButton.addEventListener("click", () => {
    // Capture the input, log them, and clear the text box fields
    const eventName = document.querySelector("#event-name").value.trim();
    const hostName = document.querySelector("#host-name").value.trim();
    const eventTime = document.querySelector("#event-time").value.trim();
    const eventLocation = document.querySelector("#event-location").value.trim();

    fetch(backendURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            event_name: eventName,
            host_name: hostName,
            event_time: eventTime,
            event_location: eventLocation
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from backend:", data);
    })
    .catch(error => {
        console.error("Error sending event:", error);
    });

    document.querySelector("#event-name").value = "";
    document.querySelector("#host-name").value = "";
    document.querySelector("#event-time").value = "";
    document.querySelector("#event-location").value = "";
});