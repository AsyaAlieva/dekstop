import os
import sys
from dotenv import load_dotenv

from PySide6.QtCore import QFile
from PySide6.QtCore import QTextStream
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox

from View.SignUp import SignUp
from View.main_interface import MainInterface

from Model.auth.service import AuthService
from Model.database.db_handler import create_session


load_dotenv()
db_url = os.getenv("DB_URL")


def load_styles(app: QApplication):
   current_dir = os.path.dirname(__file__)
   app.setStyleSheet("""
    * {
        transition: background-color 150ms, color 150ms, border-color 150ms;
    }
   """)
   full_path = os.path.join(current_dir, 'View', 'static',
                            'themes', 'light', 'styles.css')
   style_file = QFile(full_path)
   if style_file.open(QFile.ReadOnly | QFile.Text):
      stream = QTextStream(style_file)
      app.setStyleSheet(stream.readAll())
      style_file.close()


def main():
   try:
      app = QApplication(sys.argv)

      load_styles(app)

      db_session = create_session(db_url) # инициализация БДшки

      auth_service = AuthService(db_session) # создание сервиса авторизации

      login_win = SignUp(auth_service)
      if login_win.exec() == QDialog.Accepted:
         window = MainInterface(login_win.user)
         window.show()
         return app.exec()
      else:
         return 0
   except Exception as e:
      QMessageBox.critical(
         None,
         "Fatal Error",
         f"Application crashed: {str(e)}\nSee logs for details."
      )
      return 1


if __name__ == "__main__":
   sys.exit(main())
