import os
import docx
import pandas as pd


TEST_DOC_PATH = ""


class DocxParser:
   def __init__(self):
      self.doc = self.load_document(TEST_DOC_PATH)

   @staticmethod
   def load_document(path_to_docx):
      return docx.Document(docx=path_to_docx)

   @staticmethod
   def transform_to_list_of_lists(document) -> list[list[str | int | float]]:
      table_datalist = list()
      for table in document.tables:
         for row in table.rows:
            row_datalist = list()
            for cell in row.cells:
               row_datalist.append(cell.text)
            table_datalist.append(row_datalist)
      return table_datalist

   @staticmethod
   def transform_to_dataframe(datalist: list[list]) -> pd.DataFrame:
      headers = datalist[0]
      data = datalist[1:]
      return pd.DataFrame(data, columns=headers)
