from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QMessageBox

from PySide6.QtCore import Qt, QMimeData

from PySide6.QtGui import QDragEnterEvent, QDropEvent


ALLOW_FILE_FORMATS = ["docx"]


class DropFileWindow(QMainWindow):
   def __init__(self, need_docs_names: list, output_doc_name: str):
      super().__init__()

      self.load_docs_paths = list()

      self.setWindowTitle("Загрузчик документов")
      self.setAcceptDrops(True)
      self.setMinimumSize(400, 300)

      central_widget = QWidget()
      self.setCentralWidget(central_widget)

      frame = QFrame()
      vbox = QVBoxLayout()

      layout = QVBoxLayout()
      central_widget.setLayout(layout)

      output_doc_name_label = QLabel(f"<b>{output_doc_name}</b>")
      separator = QLabel("-"*len(output_doc_name)*3)

      default_label = QLabel(
         "Документы которые необходимо загрузить в программу:")
      vbox.addWidget(output_doc_name_label)
      vbox.addWidget(separator)
      vbox.addWidget(default_label)

      for i, name in enumerate(need_docs_names):
         doc_name = QLabel(f"{i+1}. {name}")
         vbox.addWidget(doc_name)

      frame.setLayout(vbox)

      layout.addWidget(frame)

      self.text_edit = QTextEdit()
      self.text_edit.setPlaceholderText("Перетащите файлы сюда...")
      layout.addWidget(self.text_edit)

      self.btn_select = QPushButton("Выбрать файлы вручную")
      self.tables_loader = QPushButton("Выгрузить таблицы")

      layout.addWidget(self.btn_select)
      layout.addWidget(self.tables_loader)

      self.text_edit.setStyleSheet("""
         QTextEdit {
               border: 2px dashed #aaa;
               padding: 10px;
               font-size: 14px;
         }
      """)

      # триггеры
      self.btn_select.clicked.connect(self.select_files)

   def dragEnterEvent(self, event: QDragEnterEvent):
      """Обработка события "перетаскивание над окном" """
      if event.mimeData().hasUrls():
         event.acceptProposedAction()
      else:
         event.ignore()

   def dropEvent(self, event: QDropEvent):
      """Обработка события "отпускание файлов" """
      mime_data = event.mimeData()
      if mime_data.hasUrls():
         file_paths = []
         for url in mime_data.urls():
               file_path = url.toLocalFile()
               file_path = DropFileWindow.validate_path(file_path)
               if file_path is not None:
                  file_paths.append(file_path)
               else:
                  self.show_invalid_file_format_message()
                  return
         self.process_files(file_paths)
         event.acceptProposedAction()

   @staticmethod
   def validate_path(path: str):
      file_format = path.split(".")[-1]
      if file_format in ALLOW_FILE_FORMATS:
         return path
      else:
         return None

   def show_invalid_file_format_message(self):
      QMessageBox.warning(
         self,
         "Ошибка",
         "Внимание, формат файла, который вы пытаетесь загрузить "
         "не поддерживается. Поддерживаются только следующие форматы: "
         f"{', '.join(ALLOW_FILE_FORMATS)}",
         QMessageBox.Ok)

   def select_files(self):
      """Ручной выбор файлов через диалог"""
      files, _ = QFileDialog.getOpenFileNames(
         self, "Выберите файлы", "", "Все файлы (*)"
      )
      if files:
         self.process_files(files)

   def process_files(self, file_paths):
      """Обработка и отображение путей к файлам"""
      self.text_edit.clear()
      for path in file_paths:
         path = DropFileWindow.validate_path(path)
         if path is not None:
            self.text_edit.append(path)
         else:
            self.show_invalid_file_format_message()
            return
