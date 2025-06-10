import os
from dotenv import load_dotenv
from Model.database.db_handler import create_session


load_dotenv()
db_url = os.getenv("DB_URL")
SessionFactory = create_session(db_url)


