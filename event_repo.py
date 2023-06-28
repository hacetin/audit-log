import datetime
import logging

from dateutil import parser

import db
from contract import EventContract, QueryEventContract

_events_db = db.get_database()

_events_collection = _events_db["events"]

# Create indices for common fields if not exist
# See https://stackoverflow.com/a/48337318/6900838
_events_collection.create_index("username")
_events_collection.create_index("time")
_events_collection.create_index("event_type")


def write(event_contract: EventContract, username):
    item = {
        "event_type": event_contract.event_type,
        "username": username,
        "time": datetime.datetime.now(),
        "event_fields": event_contract.event_fields,
    }

    logging.debug(f"db - write - item: {item}")

    _events_collection.insert_one(item)


def search(query_event_contract: QueryEventContract, username):
    time = {"$gte": parser.parse(query_event_contract.time_start)}
    if query_event_contract.time_stop:
        time["$lt"] = parser.parse(query_event_contract.time_stop)
    query = {
        "event_type": query_event_contract.event_type,
        "username": username,
        "time": time,
    }

    for k, v in query_event_contract.query_params.items():
        query[f"event_fields.{k}"] = v

    logging.debug(f"db - search - query: {query}")

    result = _events_collection.find(query)
    items = []
    for item in result:
        del item["_id"]
        items.append(item)

    logging.debug(f"db - search - items: {items}")

    return items
