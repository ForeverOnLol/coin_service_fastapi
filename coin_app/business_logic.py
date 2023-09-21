from coin_app.models import User


class UserPreRegistrationFeatures():
    '''
    Реализация бизнес-логики перед регистрацией пользователя.
    Пример: дать пользователю дополнительные монеты при регистрации.
    '''
    @staticmethod
    def make(user: User) -> User:
        task_queue = [UserPreRegistrationFeatures.bonus_coins]
        for task in task_queue:
            task(user)
        return user

    @staticmethod
    def bonus_coins(user: User, count: int = 200):
        user.balance += count  # type: ignore
        return user
