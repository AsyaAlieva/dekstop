import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream
from View.main_interface import MainInterface

current_dir = os.path.dirname(__file__)

class App(MainInterface):
   def __init__(self):
      super().__init__()


def load_global_style():
   app = QApplication.instance()
   full_path = os.path.join(current_dir, 'View', 'static',
                            'themes', 'light', 'styles.qss')
   style_file = QFile(full_path)
   if style_file.open(QFile.ReadOnly | QFile.Text):
      stream = QTextStream(style_file)
      app.setStyleSheet(stream.readAll())
      style_file.close()


if __name__ == "__main__":
   app = QApplication([])
   load_global_style()
   window = App()
   window.show()
   app.exec()