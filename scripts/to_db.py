import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from Model.services.docx_parser import DocxParser

load_dotenv()
db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

eng_headers = ['price', 'distance', 'city', 'warehouse']


def push_to_database():
   file_path = os.path.join('View', 'тариф.docx')
   parser = DocxParser()
   doc = parser.load_document(file_path)
   table_data = parser.get_table_as_lists(doc)
   final_data = []
   for lis in table_data[2:]:
      data = []
      for value in lis:
         value = value.replace(' ', '')
         if value.isdigit():
            int_value = int(value)
            data.append(int_value)
         else:
            data.append(value)
      final_data.append(data)
   df = pd.DataFrame(final_data, columns=eng_headers)
   print(df)
   df.to_sql('tariff', engine, if_exists='append', index=False)


push_to_database()
