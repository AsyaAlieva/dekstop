import os
import pandas as pd
from Model.services.docx_parser import DocxParser
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
db_url = os.getenv("DB_URL")
engine = create_engine(db_url)


file_path = os.path.join('View', 'тариф.docx')

parser = DocxParser()
doc = parser.load_document(file_path)
table_data = parser.get_table_as_lists(doc)
df = pd.DataFrame(table_data)
df.to_sql('tariff', engine, if_exists='append', index=False)