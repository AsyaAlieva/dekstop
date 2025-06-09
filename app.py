import os
import sys

from PySide6.QtCore import QFile
from PySide6.QtCore import QTextStream
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox

from View.SignUp import SignUp
from View.main_interface import MainInterface

from Model.auth.service import AuthService
from Model.database.data_service import SessionFactory




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

      auth_service = AuthService(SessionFactory)

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
