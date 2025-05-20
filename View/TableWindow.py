from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel

from PySide6.QtGui import QStandardItem

from PySide6.QtGui import QStandardItemModel


class TableWin(QWidget):
   def __init__(self,
                datalists: list,
                input_doc_names: str,
                output_doc_name: str='какая-то таблица'):
      super().__init__()
      self.datalists = datalists
      self.input_doc_names = input_doc_names
      self.setWindowTitle(output_doc_name)
      self.resize(700, 600)
      self.construct_window()

   def construct_window(self):
      self.clear_cell_btn = QPushButton("Очистить выбранное")
      self.clear_all_btn = QPushButton("Очистить всё")
      self.delete_row_tbn = QPushButton("Удалить строку")
      self.save_data_btn = QPushButton("Сохранить")
      self.calculate_btn = QPushButton("Вычислить")
      self.back_from_tab_btn = QPushButton("Назад")

      self.vbox = QVBoxLayout()
      for table_data, table_name in zip(self.datalists, self.input_doc_names):
         self.vbox.addWidget(QLabel(str(table_name)))
         self.create_and_add_table(datalist=table_data)
         self.vbox.addWidget(QLabel("-"*50))
      hbox = QHBoxLayout()
      hbox.addWidget(self.clear_cell_btn)
      hbox.addWidget(self.clear_all_btn)
      hbox.addWidget(self.save_data_btn)
      hbox.addWidget(self.delete_row_tbn)
      hbox.addWidget(self.calculate_btn)
      hbox.addWidget(self.back_from_tab_btn)
      self.vbox.addLayout(hbox)
      self.setLayout(self.vbox)

   def create_and_add_table(self, datalist: list):
      """Функция-конструктор таблиц"""
      row_count = len(datalist) - 1
      column_count = len(datalist[0])
      headers = datalist[0]

      self.tableView = QTableView()
      self.tableView.setCornerButtonEnabled(True)
      self.tableView.setSortingEnabled(True)
      self.model = QStandardItemModel(row_count, column_count)
      self.model.setHorizontalHeaderLabels(headers)

      for row_index, row in enumerate(datalist[1:]):
         for column_index, cell in enumerate(row):
            self.model.setItem(row_index, column_index, QStandardItem(cell))

      self.tableView.setModel(self.model)
      self.tableView.horizontalHeader().setSectionResizeMode(
         QHeaderView.ResizeMode.Stretch
      )
      self.vbox.addWidget(self.tableView)
