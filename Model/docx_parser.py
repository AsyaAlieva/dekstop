import os
import docx
import pandas as pd


class DocxParser:
   def __init__(self, doc_path: str):
      self.doc = self.load_document(doc_path)

   @staticmethod
   def load_document(path_to_docx):
      return docx.Document(docx=path_to_docx)

   def transform_to_list_of_lists(self) -> list[list[str | int | float]]:
      table_datalist = list()
      for table in self.doc.tables:
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

   def get_table_name(self):
      for paragraph in self.doc.paragraphs:
         if paragraph.text.strip():
            return paragraph.text
