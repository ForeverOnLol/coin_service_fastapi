from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from coin_app import models, schemas, crud
from coin_app.auth import authenticate_user, get_current_user
from coin_app.business_logic import UserPreRegistrationFeatures
from coin_app.db import ENGINE
from coin_app.errors import (
    RecipientNotExist, InsufficientCoins, SendCoinsError, UserAlreadyExist)
from coin_app.security import utils, jwt

models.BASE.metadata.create_all(bind=ENGINE)  # type: ignore
app = FastAPI()


@app.post('/register/', status_code=201)
async def register(username: str, password: str):
    password_hash = utils.get_password_hash(password)
    user = models.User(username=username,
                       password_hash=password_hash, balance=0)
    user = UserPreRegistrationFeatures.make(user=user)
    try:
        crud.create_user(user=user)
    except UserAlreadyExist:
        raise HTTPException(status_code=409,
                            detail=f'Пользователь {username} уже существует.')
    return 'Пользователь успешно создан'


@app.post('/token/')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверные учетные данные',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = jwt.create_access_token(
        data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/me/balance/')
async def get_own_balance(
        current_user:
        Annotated[schemas.CurrentUser, Depends(get_current_user)]
):
    user = crud.get_user(username=current_user.username)
    return [{'username': f'{user.username}',
             'balance': f'{user.balance}'}]


@app.post('/me/send_coins/', status_code=200)
async def send_coins(
        current_user:
        Annotated[schemas.CurrentUser, Depends(get_current_user)],
        transfer_info: schemas.CoinTransfer
):
    try:
        crud.transfer_coins(
            username_current_user=current_user.username,
            username_recipient=transfer_info.username_recipient,
            amount=transfer_info.amount
        )
    except RecipientNotExist:
        raise HTTPException(
            status_code=409,
            detail=f'Получатель {transfer_info.username_recipient} '
                   f'не существует.'
        )
    except InsufficientCoins:
        raise HTTPException(
            status_code=402,
            detail='Недостаточно средств для выполнения операции.'
        )
    except SendCoinsError:
        raise HTTPException(status_code=500, detail='Ошибка транзакции')
    return 'Успешно'
