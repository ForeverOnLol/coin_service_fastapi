import pytest
from datetime import timedelta

from coin_app import models
from coin_app.security.jwt import create_access_token, decode_access_token
from coin_app.security.utils import verify_password, get_password_hash
from coin_app.business_logic import UserPreRegistrationFeatures


@pytest.fixture
def secret_key():
    return 'test_secret_key'


@pytest.fixture
def algorithm():
    return 'HS256'


@pytest.fixture
def access_token_expire_minutes():
    return timedelta(minutes=60)


@pytest.fixture
def data_for_token():
    return {'sub': 'test_user'}


class TestJwt:
    def test_create_access_token(
            self, secret_key, algorithm,
            access_token_expire_minutes, data_for_token
    ):
        expires_delta = timedelta(minutes=30)
        access_token = create_access_token(data_for_token, expires_delta)

        assert access_token is not None

        decoded_token = decode_access_token(access_token)

        assert decoded_token['sub'] == data_for_token['sub']
        assert 'exp' in decoded_token

    def test_decode_access_token(self, secret_key, algorithm,
                                 access_token_expire_minutes, data_for_token
                                 ):
        expires_delta = timedelta(minutes=30)
        access_token = create_access_token(data_for_token, expires_delta)

        decoded_token = decode_access_token(access_token)
        # Проверка правильности данных
        assert decoded_token['sub'] == data_for_token['sub']
        assert 'exp' in decoded_token


class TestUtils:
    def test_verify_password(self):
        hashed_password = get_password_hash('password123')

        assert verify_password('password123', hashed_password) is True

        assert verify_password('wrongpassword', hashed_password) is False

    def test_get_password_hash(self):
        hashed_password = get_password_hash('password123')

        assert hashed_password is not None
        assert len(hashed_password) > 0


class TestUserPreregFeatures():
    def test_bonus_coins(self):
        user = models.User(username='johndoe',
                           password_hash=get_password_hash('random1'),
                           balance=0
                           )
        # проверка значения бонусных монет по умолчанию
        user = UserPreRegistrationFeatures.bonus_coins(user)
        assert user.balance == 200

        user = models.User(username='johndoe2',
                           password_hash=get_password_hash('random2'),
                           balance=200
                           )
        # проверка значения в 300 бонусных монет
        user = UserPreRegistrationFeatures.bonus_coins(user, 300)
        assert user.balance == 500

    def test_all_features(self):
        user = models.User(username='johndoe',
                           password_hash=get_password_hash('random1'),
                           balance=0
                           )
        user = UserPreRegistrationFeatures.make(user)
        assert user.balance == 200
