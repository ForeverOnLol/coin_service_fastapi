import os
import dotenv

dotenv.load_dotenv()

postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_host = os.environ.get('POSTGRES_HOST')
postgres_db = os.environ.get('POSTGRES_DB')


postgres_test_user = os.environ.get('POSTGRES_TEST_USER')
postgres_test_password = os.environ.get('POSTGRES_TEST_PASSWORD')
postgres_test_host = os.environ.get('POSTGRES_TEST_HOST')
postgres_test_db = os.environ.get('POSTGRES_TEST_DB')
