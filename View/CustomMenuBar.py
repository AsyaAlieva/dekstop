import os

from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QPushButton

from PySide6.QtGui import QAction
from PySide6.QtGui import QActionGroup
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtGui import QGuiApplication

from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtCore import QFile
from PySide6.QtCore import QTextStream
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QMenuBar


class CustomMenuBar(QMenuBar):
   def __init__(self, parent):
      super().__init__(parent)
      self.parent = parent
      self.themes_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'static', 'themes'
      )
      self.current_theme = None
      self._create_menu_bar()
      self.set_theme(theme_name="light", window=self)


   def _create_menu_bar(self):
      # Вкладка - Файл
      file_menu = QMenu("Файл", self)
      self.open_action = QAction("Войти в профиль", self)
      self.change_action = QAction("Сменить профиль", self)
      self.exit_action = QAction("Выход", self)
      file_menu.addAction(self.open_action)
      file_menu.addAction(self.change_action)
      file_menu.addSeparator()
      file_menu.addAction(self.exit_action)
      self.addMenu(file_menu)

      # Вкладка - Справка
      edit_menu = QMenu("Справка", self)
      self.help_action = QAction("Руководство пользователя", self)
      self.about_action = QAction("О программе", self)
      edit_menu.addAction(self.help_action)
      edit_menu.addAction(self.about_action)
      self.addMenu(edit_menu)

      # Вкладка - Вид
      view_menu = QMenu("Вид", self)

      self.theme_menu = QMenu("Тема интерфейса", self)
      view_menu.addMenu(self.theme_menu)
      self.addMenu(view_menu)

      # Создаем группу действий (для исключающего выбора)
      self.theme_action_group = QActionGroup(self)
      self.theme_action_group.setExclusive(True)  # Только одна тема активна
      self.set_themes_names()
      # self.theme_menu.addMenu(self.theme_action_group)

      language_action = QAction("Язык интерфейса", self)
      self.full_window_action = QAction("Полноэкранный режим", self)
      view_menu.addAction(language_action)
      view_menu.addAction(self.full_window_action)

      # Установка сочетания клавиш
      # action.setShortcut("Ctrl+O")
      # action.setShortcuts(["Ctrl+E", "Ctrl+Shift+E"])
      # action.setShortcut(QKeySequence.Print)

      # Добавление на панель инструментов
      # toolbar = self.addToolBar("File")
      # toolbar.addAction(action)

      # Подсказки
      # action.setStatusTip("Открывает файл")  # Подсказка в статусбаре
      # action.setToolTip("Открыть файл")     # Подсказка при наведении
      # action.setWhatsThis("Эта кнопка открывает файл...")  # Подробное описание

      # триггеры
      # как работают переопределяемые функции фреймворка ↓
      self.exit_action.triggered.connect(self.parent.closeEvent)

      self.about_action.triggered.connect(self.show_about)
      self.open_action.triggered.connect(self.open_sign_up_win)

   def change_theme(self):
      pass

   def get_theme_names(self) -> list[str]:
      return [folder for folder in os.listdir(
         self.themes_path) if os.path.isdir(
         os.path.join(self.themes_path, folder)
      ) and folder != '__pycache__']

   def set_themes_names(self):
      themes = self.get_theme_names()
      print(themes)
      for theme_name in themes:
         action = QAction(theme_name, self)
         action.setCheckable(True)
         action.setData(theme_name)
      self.theme_menu.addAction(action)
      self.theme_action_group.addAction(action)

      if theme_name == "light":
         action.setChecked(True)

   def _get_qss_style_path(self, theme_name: str) -> str:
      try:
         path = os.path.join(
               os.path.join(
                  self.themes_path, theme_name
               ), 'styles.qss').replace("\\", "/")
         return path
      except Exception as e:
         print("Проблема с путями к теме")

   def set_theme(self, theme_name: str, window=None):
      qss_path = self._get_qss_style_path(theme_name)

      if qss_path is None:
         print("Тема не найдена!")
         return

      file = QFile(qss_path)
      if file.open(QFile.ReadOnly | QFile.Text):
         stream = QTextStream(file)
         window.setStyleSheet(stream.readAll())
         file.close()
         self.current_theme = theme_name
      else:
         print(f"Не удалось открыть файл темы: {qss_path}")

   def open_sign_up_win(self):
      self.signing_window = QDialog()
      self.signing_window.setWindowTitle("Окно авторизации пользователя")
      sign_grid = QGridLayout()
      text = QLabel("Авторизация")
      email_label = QLabel("email:")
      passwd_label = QLabel("пароль:")
      rep_passwd_label = QLabel("повторите пароль:")

      self.email_edit = QLineEdit()
      email_regex = QRegularExpression(
         "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
      self.email_edit.setValidator(QRegularExpressionValidator(email_regex))

      self.passwd_edit = QLineEdit()
      self.passwd_edit.setEchoMode(QLineEdit.Password)
      self.rep_passwd_edit = QLineEdit()
      self.rep_passwd_edit.setEchoMode(QLineEdit.Password)
      self.sign_up_button = QPushButton("Зарегистрироваться")

      sign_grid.addWidget(text, 1, 1, 1, 3)
      sign_grid.addWidget(email_label, 2, 0, 1, 1)
      sign_grid.addWidget(self.email_edit, 2, 1, 1, 2)
      sign_grid.addWidget(passwd_label, 3, 0, 1, 1)
      sign_grid.addWidget(self.passwd_edit, 3, 1, 1, 2)
      sign_grid.addWidget(rep_passwd_label, 4, 0, 1, 1)
      sign_grid.addWidget(self.rep_passwd_edit, 4, 1, 1, 2)
      sign_grid.addWidget(self.sign_up_button, 5, 0, 1, 3)

      self.signing_window.setLayout(sign_grid)

      self.signing_window.show()

   def show_about(self):
      QMessageBox.about(
         self,
         "О программе",
         "Модуль для работы с документами отдела сбыта. Версия 1.0"
      )
