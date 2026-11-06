import mysql.connector
from mysql.connector import Error

# Default MySQL configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '@kish1908cd metro_planner',
    'database': 'metro_db'
}

def get_connection():
    """Tries connecting to MySQL; returns connection or None."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error:
        return None
    return None

def load_initial_data_from_db():
    """Loads station list and connection edges from MySQL or returns mock data if offline."""
    conn = get_connection()
    stations_data = []
    connections_data = []

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM stations")
            stations_data = cursor.fetchall()

            cursor.execute("SELECT * FROM connections")
            connections_data = cursor.fetchall()
            cursor.close()
            conn.close()
            return stations_data, connections_data
        except Error as e:
            print(f"Database Query Error: {e}")

    # Fallback Sample Dataset (Ensures app runs even if MySQL is not setup yet)
    stations_data = [
        {'id': 101, 'name': 'Kengeri', 'line': 'Purple', 'x_pos': 100, 'y_pos': 400},
        {'id': 102, 'name': 'Vijayanagar', 'line': 'Purple', 'x_pos': 250, 'y_pos': 400},
        {'id': 103, 'name': 'City Railway Stn', 'line': 'Purple', 'x_pos': 380, 'y_pos': 400},
        {'id': 104, 'name': 'Majestic', 'line': 'Interchange', 'x_pos': 500, 'y_pos': 400},
        {'id': 105, 'name': 'Cubbon Park', 'line': 'Purple', 'x_pos': 620, 'y_pos': 400},
        {'id': 106, 'name': 'MG Road', 'line': 'Purple', 'x_pos': 740, 'y_pos': 400},
        {'id': 107, 'name': 'Trinity', 'line': 'Purple', 'x_pos': 860, 'y_pos': 400},
        {'id': 108, 'name': 'Indiranagar', 'line': 'Purple', 'x_pos': 980, 'y_pos': 400},
        {'id': 109, 'name': 'Baiyappanahalli', 'line': 'Purple', 'x_pos': 1100, 'y_pos': 400},

        {'id': 201, 'name': 'Yeshwanthpur', 'line': 'Green', 'x_pos': 500, 'y_pos': 100},
        {'id': 202, 'name': 'Rajajinagar', 'line': 'Green', 'x_pos': 500, 'y_pos': 200},
        {'id': 203, 'name': 'Sampige Road', 'line': 'Green', 'x_pos': 500, 'y_pos': 300},
        {'id': 204, 'name': 'Chikpet', 'line': 'Green', 'x_pos': 500, 'y_pos': 500},
        {'id': 205, 'name': 'National College', 'line': 'Green', 'x_pos': 500, 'y_pos': 600},
        {'id': 206, 'name': 'Jayanagar', 'line': 'Green', 'x_pos': 500, 'y_pos': 700},
        {'id': 207, 'name': 'Silk Institute', 'line': 'Green', 'x_pos': 500, 'y_pos': 800},

        {'id': 301, 'name': 'Electronic City', 'line': 'Yellow', 'x_pos': 860, 'y_pos': 700},
        {'id': 302, 'name': 'BTM Layout', 'line': 'Yellow', 'x_pos': 700, 'y_pos': 600}
    ]

    connections_data = [
        {'station_a': 'Kengeri', 'station_b': 'Vijayanagar', 'distance': 6.5, 'line': 'Purple'},
        {'station_a': 'Vijayanagar', 'station_b': 'City Railway Stn', 'distance': 4.2, 'line': 'Purple'},
        {'station_a': 'City Railway Stn', 'station_b': 'Majestic', 'distance': 1.2, 'line': 'Purple'},
        {'station_a': 'Majestic', 'station_b': 'Cubbon Park', 'distance': 2.0, 'line': 'Purple'},
        {'station_a': 'Cubbon Park', 'station_b': 'MG Road', 'distance': 1.0, 'line': 'Purple'},
        {'station_a': 'MG Road', 'station_b': 'Trinity', 'distance': 1.5, 'line': 'Purple'},
        {'station_a': 'Trinity', 'station_b': 'Indiranagar', 'distance': 1.7, 'line': 'Purple'},
        {'station_a': 'Indiranagar', 'station_b': 'Baiyappanahalli', 'distance': 2.3, 'line': 'Purple'},

        {'station_a': 'Yeshwanthpur', 'station_b': 'Rajajinagar', 'distance': 3.8, 'line': 'Green'},
        {'station_a': 'Rajajinagar', 'station_b': 'Sampige Road', 'distance': 2.4, 'line': 'Green'},
        {'station_a': 'Sampige Road', 'station_b': 'Majestic', 'distance': 1.5, 'line': 'Green'},
        {'station_a': 'Majestic', 'station_b': 'Chikpet', 'distance': 1.8, 'line': 'Green'},
        {'station_a': 'Chikpet', 'station_b': 'National College', 'distance': 2.1, 'line': 'Green'},
        {'station_a': 'National College', 'station_b': 'Jayanagar', 'distance': 3.0, 'line': 'Green'},
        {'station_a': 'Jayanagar', 'station_b': 'Silk Institute', 'distance': 5.4, 'line': 'Green'},

        {'station_a': 'Trinity', 'station_b': 'BTM Layout', 'distance': 5.2, 'line': 'Yellow'},
        {'station_a': 'BTM Layout', 'station_b': 'Electronic City', 'distance': 8.5, 'line': 'Yellow'},
        {'station_a': 'National College', 'station_b': 'BTM Layout', 'distance': 4.1, 'line': 'Yellow'}
    ]

    return stations_data, connections_data

def add_station_to_db(station_id, name, line):
    """Inserts a new station record into MySQL if connected."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO stations (id, name, line) VALUES (%s, %s, %s)"
            cursor.execute(query, (station_id, name, line))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Error inserting station: {e}")
            return False
    return True

def delete_station_from_db(station_id):
    """Deletes a station record from MySQL if connected."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM stations WHERE id = %s"
            cursor.execute(query, (station_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Error deleting station: {e}")
            return False
    return True

def save_search_to_db(source, destination, algorithm, distance, stops):
    """Saves a route search log to search_history table in MySQL."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """INSERT INTO search_history (source, destination, algorithm, distance, stops)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (source, destination, algorithm, distance, stops))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error saving search history: {e}")
