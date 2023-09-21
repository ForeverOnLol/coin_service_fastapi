from typing import Annotated
from jose import JWTError
from coin_app import crud
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from coin_app.security import utils, jwt

TOKEN_URL = 'token'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def authenticate_user(username: str, password: str):
    user = crud.get_user(username)
    if not user:
        return False
    if not utils.verify_password(password, user.password_hash):
        return False
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode_access_token(access_token=token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(username)
    if user is None:
        raise credentials_exception
    return user
