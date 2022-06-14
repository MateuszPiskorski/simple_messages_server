"""Script for database creation"""
from psycopg2 import connect, errorcodes, OperationalError

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
    cnx = connect(user=USER, host=HOST, password=PASSWORD)
    cnx.autocommit = True

    cursor = cnx.cursor()
    try:
        cursor.execute(CREATE_DB)
        print("Database created")
    except OperationalError as e:
        if e.pgcode == errorcodes.DUPLICATE_DATABASE:
            print("Database already exists - stage skipped")
    cnx.close()
except OperationalError as e:
    print("Connection error, try again: ", e)

try:
    cnx = connect(user=USER, host=HOST, password=PASSWORD, database="msg_server_db")
    cnx.autocommit = True

    cursor = cnx.cursor()
    try:
        cursor.execute(USERS_TABLE)
        print("Table Users created")
    except OperationalError as e:
        if e.pgcode == errorcodes.DUPLICATE_TABLE:
            print("Table already exists - stage skipped")
            pass
    try:
        cursor.execute(MSG_TABLE)
        print("Table Messages created")
    except OperationalError as e:
        if e.pgcode == errorcodes.DUPLICATE_TABLE:
            print("Table already exists - stage skipped")
            pass
    cnx.close()
except OperationalError as e:
    print("Connection error, try again: ", e)
