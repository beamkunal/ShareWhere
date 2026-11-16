
# ==================================================
# SHAREWHERE
# DATABASE MANAGER
# ==================================================

import sqlite3
import secrets

from pathlib import Path
from datetime import datetime


# ==================================================
# DATABASE FILE LOCATION
# ==================================================

# Project ke main folder ka location find karna
PROJECT_FOLDER = Path(__file__).resolve().parents[2]

# Database file ka naam aur location
DATABASE_PATH = PROJECT_FOLDER / "sharewhere.db"


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_database_connection():

    # SQLite database se connection create karna
    connection = sqlite3.connect(DATABASE_PATH)

    # Query results ko column names ke through access karna
    connection.row_factory = sqlite3.Row

    return connection


# ==================================================
# CREATE DATABASE TABLES
# ==================================================

def initialize_database():

    # Database connection open karna
    connection = get_database_connection()

    # Database mein rooms table create karna
    connection.execute("""
        CREATE TABLE IF NOT EXISTS rooms (

            room_id TEXT PRIMARY KEY,

            room_name TEXT NOT NULL,

            role TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
    """)

    # Changes database mein save karna
    connection.commit()

    # Database connection close karna
    connection.close()


# ==================================================
# GENERATE UNIQUE ROOM ID
# ==================================================

def generate_room_id():

    # Six-digit numeric room ID generate karna
    room_id = str(secrets.randbelow(900000) + 100000)

    return room_id


# ==================================================
# CREATE NEW ROOM
# ==================================================

def create_room(room_name):

    # Database connection open karna
    connection = get_database_connection()

    try:

        # Unique room ID generate karna
        room_id = generate_room_id()

        # Current date and time lena
        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Room information database mein insert karna
        connection.execute(
            """
            INSERT INTO rooms (
                room_id,
                room_name,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                room_id,
                room_name,
                "Admin",
                created_at
            )
        )

        # Database changes save karna
        connection.commit()

        return room_id

    finally:

        # Connection close karna
        connection.close()


# ==================================================
# GET ALL CREATED ROOMS
# ==================================================

def get_all_rooms():

    # Database connection open karna
    connection = get_database_connection()

    try:

        # Saare saved rooms retrieve karna
        cursor = connection.execute(
            """
            SELECT *
            FROM rooms
            ORDER BY created_at DESC
            """
        )

        # Saare records ki list return karna
        rooms = cursor.fetchall()

        return rooms

    finally:

        # Connection close karna
        connection.close()


# ==================================================
# CHECK WHETHER ROOM EXISTS
# ==================================================

def room_exists(room_id):

    # Database connection open karna
    connection = get_database_connection()

    try:

        # Given room ID search karna
        cursor = connection.execute(
            """
            SELECT room_id
            FROM rooms
            WHERE room_id = ?
            """,
            (room_id,)
        )

        # Record milne par True return hoga
        room = cursor.fetchone()

        return room is not None

    finally:

        # Connection close karna
        connection.close()


# ==================================================
# DELETE A ROOM
# ==================================================

def delete_room(room_id):

    # Database connection open karna
    connection = get_database_connection()

    try:

        # Room ko database se delete karna
        cursor = connection.execute(
            """
            DELETE FROM rooms
            WHERE room_id = ?
            """,
            (room_id,)
        )

        # Changes save karna
        connection.commit()

        # Batana ki room delete hua ya nahi
        return cursor.rowcount > 0

    finally:

        # Connection close karna
        connection.close()
