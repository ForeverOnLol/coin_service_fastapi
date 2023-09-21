from coin_app.db import get_session
from coin_app import models
from coin_app.errors import (RecipientNotExist, SendCoinsError,
                             InsufficientCoins, UserAlreadyExist)


def is_user_exist(username: str, db=get_session()) -> bool:
    '''
    Проверка существования юзера в БД
    :param username:
    :param db:
    :return:
    '''
    user = (db.query(models.User)
            .filter(models.User.username == username)
            .first()
            )
    if user:
        return True
    return False


def get_user(username: str, db=get_session()) -> models.User:
    '''
    Получить юзера из БД
    :param username:
    :param db:
    :return:
    '''
    user = (db.query(models.User)
            .filter(models.User.username == username)
            .first()
            )
    return user


def create_user(user: models.User, db=get_session()) -> models.User:
    '''
    Создать пользователя в БД.
    :param user:
    :param db:
    :return:
    '''
    if is_user_exist(username=str(user.username)):
        raise UserAlreadyExist(
            f'Пользователь {user.username} уже существует в БД.'
        )
    db.add(user)
    db.commit()
    return user


def transfer_coins(username_current_user: str, username_recipient: str,
                   amount: int, db=get_session()) -> None:
    '''
    Перевод монет
    :param username_current_user:
    :param username_recipient:
    :param amount:
    :param db:
    :return:
    '''
    recipient = (db.query(models.User).
                 filter(models.User.username == username_recipient)
                 .first()
                 )
    if not recipient:
        raise RecipientNotExist(f'Пользователь {username_recipient}'
                                f' не существует.')
    user = (db.query(models.User)
            .filter(models.User.username == username_current_user)
            .first()
            )
    if user.balance - amount < 0:
        raise InsufficientCoins('Недостаточно '
                                'средств.'
                                )
    try:
        user = (db.query(models.User)
                .filter(models.User.username == user.username)
                .first()
                )
        user.balance -= amount
        recipient.balance += amount
        db.commit()
    except Exception:
        db.rollback()
        raise SendCoinsError('Ошибка транзакции. Повторите позднее.')
