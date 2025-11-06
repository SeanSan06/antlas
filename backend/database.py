import sqlite3

def get_connection():
    connection = sqlite3.connect("events.db")
    connection.row_event_attributes = sqlite3.Row
    return connection

def create_tables():
    connECTION = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id EVENTS PRIMARY KEY AUTOINCREMENT,     
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
