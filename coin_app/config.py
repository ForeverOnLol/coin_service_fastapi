import os
import dotenv

dotenv.load_dotenv()

postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_host = os.environ.get('POSTGRES_HOST')
postgres_db = os.environ.get('POSTGRES_DB')
