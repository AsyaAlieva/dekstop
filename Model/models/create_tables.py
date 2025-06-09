import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from warehouse_balance import Base
from tariff import Base


load_dotenv()
db_url = os.getenv("DB_URL")


if __name__ == '__main__':
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)