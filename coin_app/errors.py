class SendCoinsError(Exception):
    '''
    Ошибка при транзакции перевода монет между пользователями
    '''

    def __init__(self, info):
        self.info = info


class InsufficientCoins(Exception):
    '''
    Ошибка недостаточно монет
    '''

    def __init__(self, info):
        self.info = info


class RecipientNotExist(Exception):
    '''
    Ошибка недостаточно монет
    '''

    def __init__(self, info):
        self.info = info


class UserAlreadyExist(Exception):
    '''
    Ошибка пользователь уже существует в БД
    '''

    def __init__(self, info):
        self.info = info
