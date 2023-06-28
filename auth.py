from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


auth = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(auth)):
    # TODO:
    #  - Use better auth approach then basic username and password.
    #  - Use a db to keep usernames and salted passwords, tokens etc.
    correct_username = "admin"
    correct_password = "password"
    if (
        credentials.username != correct_username
        or credentials.password != correct_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
