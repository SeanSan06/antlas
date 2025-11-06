import sqlite3

# Creates a new events.db, if it already exists the connect to it
def get_connection():
    connection = sqlite3.connect("events.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    '''
    Connects to database(events.db) and fills the database with parameters 
    that allow an Event object's attributes to be stored. The attendees are
    stored on a seperate table under the same database and are connected
    through FOREIGN KEY
    '''
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,     
            name TEXT NOT NULL,
            host TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT NOT NULL     
        )          
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events (id)
        ) 
    """)
    
    connection.commit()
    connection.close()
