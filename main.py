import logging

from fastapi import FastAPI, HTTPException, Security

import event_repo
from auth import authenticate
from contract import EventContract, QueryEventContract

# TODO:
#  - Use an external service for keeping logs
#  - Use conf file for log configs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

app = FastAPI()


@app.post("/write")
def write(contract: EventContract, username: str = Security(authenticate)):
    try:
        event_repo.write(contract, username)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="check logs")


@app.get("/search")
def search(contract: QueryEventContract, username: str = Security(authenticate)):
    try:
        events = event_repo.search(contract, username)
        return {"events": events}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="check logs")
