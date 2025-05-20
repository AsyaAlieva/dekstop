import json
from pathlib import Path

from View.DropFile import DropFileWindow
from View.CustomMenuBar import CustomMenuBar

from PySide6.QtCore import Qt
from PySide6.QtCore import QUrl

from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QDesktopServices

from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMenuBar
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QProgressDialog


class MainInterface(QMainWindow):
   def __init__(self):
      super().__init__()

      self.init_main_ui()
      self.menu_bar = CustomMenuBar(self)
      self.setMenuBar(self.menu_bar)

      self.menu_bar.help_action.triggered.connect(self.open_documentation)

   def init_main_ui(self):
      self.setWindowTitle("Модуль для работы с документами")
      self.setFixedSize(600, 300)

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
      right_layout.addWidget(QLabel("Для дополнительных функций"))
      groupbox_right.setLayout(right_layout)

      hbox = QHBoxLayout()
      hbox.addWidget(groupbox_left)
      hbox.addWidget(groupbox_right)
      central_widget.setLayout(hbox)

      self.docxgen_button.clicked.connect(self.open_tasks_win)

   def open_tasks_win(self):
      self.tasks_win = QDialog()
      self.tasks_win.setWindowTitle("Задачи отдела сбыта")

      docs_for_task_1 = [
          "Договор поставки",
          "Отчет об остатках на складе",
      ]
      docs_for_task_2 = [
          "Договор поставки",
          "План выпуска продукции",
      ]
      docs_for_task_3 = [
          "План отгрузки готовой продукции заказчикам",
          "Акт приемки готовой продукции",
          "План перевозки продукции",
      ]
      docs_for_task_4 = [
          "Недельный отчет об отгрузке продукции заказчикам",
          "Акт поступления готовой продукции",
          "Отчет об остатках на складе на конец прошлого года",
      ]

      grid_layout = QGridLayout()
      self.transport_plan_btn = QPushButton("Составление плана перевозки")
      self.product_delivery_plan_btn = QPushButton(
         "Составление плана поставки готовой продукции заказчикам"
      )
      self.report_product_delivery_plan_btn = QPushButton(
         "Отчет о выполнении плана поставки готовой продукции закзачикам"
      )
      self.stock_balances_report_btn = QPushButton(
         "Отчет об остатках на складе"
      )
      self.back_btn = QPushButton("Назад")

      grid_layout.addWidget(self.transport_plan_btn, 0, 0, 1, 2)
      grid_layout.addWidget(self.product_delivery_plan_btn, 1, 0, 1, 2)
      grid_layout.addWidget(self.report_product_delivery_plan_btn, 2, 0, 1, 2)
      grid_layout.addWidget(self.stock_balances_report_btn, 3, 0, 1, 2)
      grid_layout.addWidget(self.back_btn, 3, 3, 1, 1)

      self.tasks_win.setLayout(grid_layout)

      self.tasks_win.show()
      self.setVisible(False)

      self.back_btn.clicked.connect(
         lambda: self.back_win_clicked(close_win=self.tasks_win,
                                       back_to_win=self)
      )
      self.product_delivery_plan_btn.clicked.connect(
         lambda: self.open_win_for_load_files(docs_for_task_1)
      )
      self.transport_plan_btn.clicked.connect(
          lambda: self.open_win_for_load_files(docs_for_task_2)
      )
      self.report_product_delivery_plan_btn.clicked.connect(
         lambda: self.open_win_for_load_files(docs_for_task_3)
      )
      self.stock_balances_report_btn.clicked.connect(
         lambda: self.open_win_for_load_files(docs_for_task_4)
      )

   def back_win_clicked(self, close_win, back_to_win):
      close_win.close()
      back_to_win.setVisible(True)

   def open_win_for_load_files(self, need_doc_names):
      self.drop_file_win = DropFileWindow(need_doc_names)
      self.drop_file_win.show()

   def open_documentation(self):
      docs_dir = Path(__file__).parent / "documentation"
      html_file = docs_dir / "user_manual.html"

      if not html_file.exists():
         return

      QDesktopServices.openUrl(QUrl.fromLocalFile(str(html_file)))

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
