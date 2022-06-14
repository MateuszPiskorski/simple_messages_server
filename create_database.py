"""Script for database creation"""
from psycopg2 import connect, errorcodes, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable


CREATE_DB = """CREATE DATABASE msg_server_db;"""

USERS_TABLE = """
CREATE TABLE Users(
    id serial,
    username varchar(255),
    hashed_password varchar(80),
    PRIMARY KEY (id)
);
"""

MSG_TABLE = """
CREATE TABLE Messages(
    id serial,
    from_id int,
    to_id int,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text varchar(255),
    PRIMARY KEY (id),
    FOREIGN KEY (from_id) REFERENCES Users(id) ON DELETE CASCADE, 
    FOREIGN KEY (to_id) REFERENCES Users(id) ON DELETE CASCADE
);
"""

USER = "postgres"
HOST = "localhost"
PASSWORD = "asdf11"

try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(CREATE_DB)
        print("Database created")
    except DuplicateDatabase as e:
        print("Database exists ", e)
    cnx.close()
except OperationalError as e:
    print("Connection Error: ", e)


try:
    cnx = connect(database="msg_server_db", user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()

    try:
        cursor.execute(USERS_TABLE)
        print("Table users created")
    except DuplicateTable as e:
        print("Table exists ", e)

    try:
        cursor.execute(MSG_TABLE)
        print("Table messages created")
    except DuplicateTable as e:
        print("Table exists ", e)
    cnx.close()
except OperationalError as e:
    print("Connection Error: ", e)
