from typing import Union
from pydantic import BaseModel, PositiveInt


class UserCreate(BaseModel):
    username: str
    password: str


class CurrentUser(BaseModel):
    username: str
    balance: int
    disabled: Union[bool, None] = None


class CoinTransfer(BaseModel):
    username_recipient: str
    amount: PositiveInt
