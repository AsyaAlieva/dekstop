import os
from pathlib import Path

from View.TableWindow import TableWin
from View.DropFile import DropFileWindow
from View.CustomMenuBar import CustomMenuBar

from Model.services.docx_parser import DocxParser

from View.static.config import DOCS_TASK_1
from View.static.config import DOCS_TASK_2
from View.static.config import DOCS_TASK_3
from View.static.config import DOCS_TASK_4

from PySide6.QtCore import Qt
from PySide6.QtCore import QUrl

from PySide6.QtGui import QPixmap
from PySide6.QtGui import QDesktopServices

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton

from Model.models.users import User


class MainInterface(QMainWindow):
   def __init__(self, user: User):
      super().__init__()
      self.user = user

      self.init_main_ui()
      self.menu_bar = CustomMenuBar(self)
      self.setMenuBar(self.menu_bar)
      self.parser = DocxParser()

      self.menu_bar.help_action.triggered.connect(self.open_documentation)

   def init_main_ui(self):
      self.setWindowTitle("Модуль для работы с документами")
      self.setFixedSize(650, 300)

      # Центральный виджет
      central_widget = QWidget()
      central_widget.setObjectName("centralwidget")
      self.setCentralWidget(central_widget)

      # Группа слева
      groupbox_left = QGroupBox("Функции")
      left_grid_layout = QGridLayout()
      self.docxgen_button = QPushButton("Модуль формирования документов для отдела сбыта")
      self.loader_button = QPushButton("Сразу загрузить все входные документы")
      self.layout_maker = QPushButton("Сформировать макет для задачи")
      left_grid_layout.addWidget(self.docxgen_button, 0, 0, alignment=Qt.AlignTop)
      left_grid_layout.addWidget(self.loader_button, 1, 0)
      left_grid_layout.addWidget(self.layout_maker, 2, 0)
      groupbox_left.setLayout(left_grid_layout)

      # Группа справа
      groupbox_right = QGroupBox("Доп. функции")
      right_layout = QVBoxLayout()
      self.icon_label = QLabel(self)
      right_layout.addWidget(self.icon_label)
      groupbox_right.setLayout(right_layout)

      hbox = QHBoxLayout()
      hbox.addWidget(groupbox_left)
      hbox.addWidget(groupbox_right)
      central_widget.setLayout(hbox)

      self.docxgen_button.clicked.connect(self.open_tasks_win)

   def open_tasks_win(self):
      self.tasks_win = QDialog()
      self.tasks_win.setWindowTitle("Задачи отдела сбыта")

      grid_layout = QGridLayout()
      self.transport_plan_btn = QPushButton(DOCS_TASK_1.get("short_task_name"))
      self.product_delivery_plan_btn = QPushButton(
         DOCS_TASK_2.get("short_task_name")
      )
      self.report_product_delivery_plan_btn = QPushButton(
         DOCS_TASK_3.get("short_task_name")
      )
      self.stock_balances_report_btn = QPushButton(
         DOCS_TASK_4.get("short_task_name")
      )
      self.back_btn = QPushButton("Назад")
      self.directory_btn = QPushButton("Справочники")

      grid_layout.addWidget(self.transport_plan_btn, 0, 0, 1, 2)
      grid_layout.addWidget(self.product_delivery_plan_btn, 1, 0, 1, 2)
      grid_layout.addWidget(self.report_product_delivery_plan_btn, 2, 0, 1, 2)
      grid_layout.addWidget(self.stock_balances_report_btn, 3, 0, 1, 2)
      grid_layout.addWidget(self.directory_btn, 4, 0, 1, 2)
      grid_layout.addWidget(self.back_btn, 4, 4, 1, 1)

      self.tasks_win.setLayout(grid_layout)

      self.tasks_win.show()
      self.setVisible(False)

      self.back_btn.clicked.connect(
         lambda: self.back_win_clicked(close_win=self.tasks_win,
                                       back_to_win=self)
      )
      self.transport_plan_btn.clicked.connect(
         lambda: self.open_win_for_load_files(
            DOCS_TASK_1.get("input_doc_names"),
            DOCS_TASK_1.get("short_task_name")
         )
      )
      self.product_delivery_plan_btn.clicked.connect(
         lambda: self.open_win_for_load_files(
            DOCS_TASK_2.get("input_doc_names"),
            DOCS_TASK_2.get("short_task_name")
         )
      )
      self.report_product_delivery_plan_btn.clicked.connect(
         lambda: self.open_win_for_load_files(
            DOCS_TASK_3.get("input_doc_names"),
            DOCS_TASK_3.get("short_task_name")
         )
      )
      self.stock_balances_report_btn.clicked.connect(
         lambda: self.open_win_for_load_files(
            DOCS_TASK_4.get("input_doc_names"),
            DOCS_TASK_4.get("short_task_name")
         )
      )

      self.directory_btn.clicked.connect(
         self.open_directories
      )

   def open_directories(self):
      self.directory_tab_win = QWidget()
      self.directory_tab_win.setWindowTitle("Справочник цен")
      self.directory_tab_win.setFixedSize(550, 600)
      doc = self.parser.load_document(os.path.join("View", "тариф.docx"))
      dir_list = self.parser.get_table_as_lists(doc)
      close_from_tab_btn = QPushButton("Закрыть")
      vbox = QVBoxLayout()
      TableWin.create_and_add_table(datalist=dir_list, vbox=vbox)
      hbox = QHBoxLayout()
      hbox.addWidget(close_from_tab_btn)
      vbox.addLayout(hbox)
      self.directory_tab_win.setLayout(vbox)

      close_from_tab_btn.clicked.connect(
         lambda: self.back_win_clicked(
            close_win=self.directory_tab_win, back_to_win=self)
      )
      self.directory_tab_win.show()


   @staticmethod
   def back_win_clicked(close_win, back_to_win):
      close_win.close()
      back_to_win.setVisible(True)

   def open_win_for_load_files(self, input_doc_names, output_doc_name):
      self.drop_file_win = DropFileWindow(input_doc_names, output_doc_name)
      self.drop_file_win.show()
      self.drop_file_win.tables_loader.clicked.connect(
         lambda: self.set_to_input_tables(output_doc_name)
      )

   def set_to_input_tables(self, output_doc_name: str):
      """Формирование таблиц из входных документов"""
      self.input_tablWin = TableWin(
         datalists=self.get_tables_data(),
         input_doc_names=self.get_table_names(),
         output_doc_name=output_doc_name
      )
      self.input_tablWin.show()

   def get_table_names(self) -> list[str]:
      all_table_names = list()
      docs_paths = self.get_docs_path()
      for path in docs_paths:
         doc =self.parser.load_document(path)
         table_name = self.parser.get_paragraph(doc)
         all_table_names.append(table_name)
      return all_table_names

   def get_tables_data(self) -> list[list[list]]:
      global_data = list()
      docs_paths = self.get_docs_path()
      for path in docs_paths:
         doc =self.parser.load_document(path)
         table_data = self.parser.get_table_as_lists(doc)
         global_data.append(table_data)
         self.parser.transform_to_dataframe(table_data) # !!!!!!!!!!!!!!!!!!
      return global_data

   def get_docs_path(self) -> list[str]:
      """Получение путей к загруженным файлам"""
      paths_str = self.drop_file_win.text_edit.toPlainText()
      paths_strs = paths_str.split('\n')
      new_paths = []
      for path in paths_strs:
         if 'file:///' in path:
            new_path = path.replace('file:///', '')
         elif 'file://' in path:
            new_path = path.replace('file://', '')
         else:
            new_path = path
         if new_path:
            new_paths.append(new_path)
      return new_paths

   def open_documentation(self):
      docs_dir = Path(__file__).parent / "documentation"
      html_file = docs_dir / "user_manual.html"

      if not html_file.exists():
         return

      QDesktopServices.openUrl(QUrl.fromLocalFile(str(html_file)))

   def set_icon(self):
      currdir = os.path.dirname(__file__)
      pixmap = QPixmap(os.path.join(currdir, 'static', 'images', 'icon.png'))
      self.icon_label.setPixmap(pixmap)

   def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите закрыть окно?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
