from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression


class SignUp(QDialog):
   def __init__(self, auth_service, parent=None):
      super().__init__(parent)
      self.auth_service = auth_service

      self.init_ui()

      self.rep_passwd_edit.setVisible(False)

      self.no_acc_button.clicked.connect(self.show_rep_password)
      self.sign_up_button.clicked.connect(self.handle_register)
      self.sign_in_button.clicked.connect(self.handle_sign_in)

   def init_ui(self):
      self.setWindowTitle("Окно авторизации пользователя")
      self.setFixedSize(250, 180)
      sign_grid = QGridLayout()
      self.text = QLabel("Вход в аккаунт")
      email_label = QLabel("email:")
      passwd_label = QLabel("пароль:")
      self.rep_passwd_label = QLabel("повторите пароль:")
      self.rep_passwd_label.setVisible(False)

      self.email_edit = QLineEdit()
      email_regex = QRegularExpression(
         "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
      self.email_edit.setValidator(QRegularExpressionValidator(email_regex))

      self.passwd_edit = QLineEdit()
      self.passwd_edit.setEchoMode(QLineEdit.Password)
      self.rep_passwd_edit = QLineEdit()
      self.rep_passwd_edit.setEchoMode(QLineEdit.Password)
      self.no_acc_button = QPushButton("Нет аккаунта")
      self.sign_in_button = QPushButton("Войти")
      self.sign_up_button = QPushButton("Зарегистрироваться")
      self.sign_up_button.setVisible(False)

      sign_grid.addWidget(self.text, 1, 1, 1, 3)
      sign_grid.addWidget(email_label, 2, 0, 1, 1)
      sign_grid.addWidget(self.email_edit, 2, 1, 1, 2)
      sign_grid.addWidget(passwd_label, 3, 0, 1, 1)
      sign_grid.addWidget(self.passwd_edit, 3, 1, 1, 2)
      sign_grid.addWidget(self.rep_passwd_label, 4, 0, 1, 1)
      sign_grid.addWidget(self.rep_passwd_edit, 4, 1, 1, 2)
      sign_grid.addWidget(self.no_acc_button, 5, 0, 1, 2)
      sign_grid.addWidget(self.sign_in_button, 5, 2, 1, 1)
      sign_grid.addWidget(self.sign_up_button, 5, 0, 1, 3)

      self.setLayout(sign_grid)

      self.show()

   def handle_sign_in(self):
      password = self.passwd_edit.text()
      username = self.email_edit.text()

      if not password:
         QMessageBox.warning(self, "Ошибка", "Не вписан пароль!")
         return

      if not username:
         QMessageBox.warning(self, "Ошибка", "Не вписан логин!")
         return

      if password and username:
         user = self.auth_service.authenticate_user(username, password)

         if user:
            self.accept()
            self.user = user
         else:
            reply = QMessageBox.question(
               self,
               "Регистрация",
               "Аккаунт не найден. Хотите создать новый?",
               QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
               self.sign_in_button.setVisible(False)
               self.rep_passwd_label.setVisible(True)
               self.rep_passwd_edit.setVisible(True)
               self.handle_register()
            else:
               QMessageBox.information(self, "Информация", "Вы можете попробовать другие учетные данные")

   def show_rep_password(self):
      self.text.setText("Регистрация аккаунта")
      self.rep_passwd_label.setVisible(True)
      self.rep_passwd_edit.setVisible(True)
      self.sign_up_button.setVisible(True)
      self.sign_in_button.setVisible(False)
      self.no_acc_button.setVisible(False)

   def handle_register(self):
      password = self.passwd_edit.text()
      rep_password = self.rep_passwd_edit.text()
      username = self.email_edit.text()
      if not password:
         QMessageBox.warning(self, "Ошибка", "Не вписан пароль!")
         return
      if not rep_password:
         QMessageBox.warning(self, "Ошибка", "Не вписан повторный пароль!")
         return
      if not username:
         QMessageBox.warning(self, "Ошибка", "Не вписан логин!")
         return
      if password != rep_password:
         QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
         return
      if username and password and password == rep_password:
         try:
            if self.rep_passwd_edit.text():
               new_user = self.auth_service.create_user(username, password)
               QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
               self.accept()
               self.user = new_user
         except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать пользователя: {str(e)}")

