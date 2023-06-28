from pymongo import MongoClient


def get_database():
    # TODO:
    #  - Get this from system environment or some kind of secret manager.
    #  - Use type safe config library
    conn_string = "mongodb://127.0.0.1:27017/"

    client = MongoClient(conn_string)

    return client["audit_log"]
