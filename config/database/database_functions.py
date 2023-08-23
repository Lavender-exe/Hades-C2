import sqlite3

def database_connect(sqlite_db: str):
    connect = sqlite3.connect(sqlite_db)
    cursor = connect.cursor()


# def add_target_db(NULL, NULL, NULL, NULL, NULL, NULL, NULL):
#     pass


# def delete_target_db(NULL, NULL, NULL, NULL, NULL, NULL, NULL):
#     pass


# def update_target_db(NULL, NULL, NULL, NULL, NULL, NULL, NULL):
#     pass