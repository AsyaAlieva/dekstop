from __future__ import annotations
import pandas as pd


from Model.docx_parser import DocxParser

from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox

from PySide6.QtGui import QStandardItem
from PySide6.QtGui import QStandardItemModel


class TableWin(QWidget):
   def __init__(self,
                datalists: list,
                input_doc_names: str,
                output_doc_name: str='какая-то таблица'):
      super().__init__()
      self.docx_parser = DocxParser()
      self.datalists = datalists
      self.input_doc_names = input_doc_names
      self.setWindowTitle(output_doc_name)
      self.resize(700, 600)
      self.construct_window()

      self.clicked_buttons()

   def construct_window(self):
      self.clear_cell_btn = QPushButton("Очистить выбранное")
      self.clear_all_btn = QPushButton("Очистить всё")
      self.delete_row_tbn = QPushButton("Удалить строку")
      self.save_data_btn = QPushButton("Сохранить")
      self.calculate_btn = QPushButton("Вычислить")
      self.back_from_tab_btn = QPushButton("Назад")

      vbox = QVBoxLayout()
      self.tabledata_dict = {}
      self.dfs_list = []
      for i, (table_data, table_name) in enumerate(zip(self.datalists, self.input_doc_names)):
         vbox.addWidget(QLabel(str(table_name)))
         self.create_and_add_table(datalist=table_data, vbox=vbox)
         self.tabledata_dict[(i+1, table_name)] = table_data
         df = pd.DataFrame(columns=table_data[0], data=table_data[2:])
         self.dfs_list.append(df)
      hbox = QHBoxLayout()
      hbox.addWidget(self.clear_cell_btn)
      hbox.addWidget(self.clear_all_btn)
      hbox.addWidget(self.save_data_btn)
      hbox.addWidget(self.delete_row_tbn)
      hbox.addWidget(self.calculate_btn)
      hbox.addWidget(self.back_from_tab_btn)
      vbox.addLayout(hbox)
      self.setLayout(vbox)

   @staticmethod
   def create_and_add_table(datalist: list, vbox: QVBoxLayout):
      """Функция-конструктор таблиц"""
      row_count = len(datalist) - 1
      column_count = len(datalist[0])
      headers = datalist[0]

      tableView = QTableView()
      tableView.setCornerButtonEnabled(True)
      tableView.setSortingEnabled(True)
      model = QStandardItemModel(row_count, column_count)
      model.setHorizontalHeaderLabels(headers)

      for row_index, row in enumerate(datalist[1:]):
         for column_index, cell in enumerate(row):
            model.setItem(row_index, column_index, QStandardItem(cell))

      tableView.setModel(model)
      tableView.horizontalHeader().setSectionResizeMode(
         QHeaderView.ResizeMode.Stretch
      )
      vbox.addWidget(tableView)
      return tableView

   def construct_output_table(self):
      self.output_tab_win = QWidget()
      output_df = self.docx_parser.compute_for_output_table_4(self.dfs_list)
      self.clear_cell_btn_4 = QPushButton("Очистить выбранное")
      self.clear_all_btn_4 = QPushButton("Очистить всё")
      self.delete_row_tbn_4 = QPushButton("Удалить строку")
      self.save_data_btn_4 = QPushButton("Сохранить")
      self.back_from_tab_btn_4 = QPushButton("Назад")

      vbox = QVBoxLayout()
      table_data = [list(output_df.columns)] + output_df.values.tolist()
      self.output_table_4 = self.create_and_add_table(datalist=table_data, vbox=vbox)
      hbox = QHBoxLayout()
      hbox.addWidget(self.clear_cell_btn_4)
      hbox.addWidget(self.clear_all_btn_4)
      hbox.addWidget(self.save_data_btn_4)
      hbox.addWidget(self.delete_row_tbn_4)
      hbox.addWidget(self.back_from_tab_btn_4)
      vbox.addLayout(hbox)
      self.output_tab_win.setLayout(vbox)
      self.output_tab_win.show()

      self.back_from_tab_btn_4.clicked.connect(
         lambda: self.back_win_clicked(
            close_win=self.output_tab_win,
            back_to_win=self
            )
         )
      self.clear_cell_btn_4.clicked.connect(lambda: self.clear_selected_cells(self.output_table_4))
      self.clear_all_btn_4.clicked.connect(lambda: self.clear_entire_table(self.output_table_4))
      self.delete_row_tbn_4.clicked.connect(lambda: self.delete_row(self.output_table_4))

   @staticmethod
   def back_win_clicked(close_win, back_to_win):
      close_win.close()
      back_to_win.setVisible(True)

   def save_data_to_db(self):
      pass

   @staticmethod
   def clear_entire_table(table_view: QTableView):
      """
      Очищает все содержимое таблицы, кроме заголовков.
      
      Args:
         table_view (QTableView): Таблица, которую нужно очистить
      """
      model = table_view.model()
      if model is None:
         return
      row_count = model.rowCount()
      col_count = model.columnCount()
      for row in range(row_count):
         for col in range(col_count):
               index = model.index(row, col)
               if index.isValid():
                  model.setData(index, None)

   @staticmethod
   def clear_selected_cells(table_view: QTableView):
      """
      Очищает содержимое выбранных ячеек в QTableView.
      
      Args:
         table_view (QTableView): Таблица, в которой нужно очистить ячейки
      """
      model = table_view.model()
      if model is None:
         return
      selected_indexes = table_view.selectionModel().selectedIndexes()
      for index in selected_indexes:
         if index.isValid():
               model.setData(index, None)

   @staticmethod
   def delete_row(table_view: QTableView):
      model = table_view.model()
      if model is None:
         QMessageBox.warning(table_view, "Ошибка", "Нет данных для удаления")
         return
      selected_indexes = table_view.selectionModel().selectedIndexes()
      if not selected_indexes:
        QMessageBox.warning(table_view, "Ошибка", "Не выбрана строка для удаления")
        return
      rows_to_delete = {index.row() for index in selected_indexes}
      for row in sorted(rows_to_delete, reverse=True):
         model.removeRow(row)
      model.layoutChanged.emit()


   def clicked_buttons(self):
      self.calculate_btn.clicked.connect(self.construct_output_table)
      # self.save_data_btn_4.clicked.connect(self.save_data_to_db)

      # self.clear_cell_btn.clicked.connect(lambda: self.clear_selected_cells())
      # self.clear_all_btn.clicked.connect(lambda: self.clear_entire_table())
      # self.delete_row_tbn.clicked.connect(lambda: self.delete_row())
      # self.back_from_tab_btn.clicked.connect(
      #    lambda: self.back_win_clicked(
      #       close_win=self,
      #       back_to_win=
      #       )
      #    )
