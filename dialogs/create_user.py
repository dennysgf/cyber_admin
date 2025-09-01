from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.models import create_user


class CreateUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎮 Crear Usuario")
        self.setFixedSize(350, 220)

        layout = QVBoxLayout()

        title = QLabel("👤 Registro de Usuario")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ffea; text-align: center;")
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de usuario")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e2e;
                color: #ffffff;
                border: 2px solid #00ffea;
                border-radius: 8px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #ff00ea;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e2e;
                color: #ffffff;
                border: 2px solid #00ffea;
                border-radius: 8px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #ff00ea;
            }
        """)

        self.btn_save = QPushButton("✅ Guardar Usuario")
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #00ffea;
                color: #000000;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #ff00ea;
                color: #ffffff;
            }
        """)
        self.btn_save.clicked.connect(self.save_user)

        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_save)

        self.setStyleSheet("background-color: #121212; color: white; font-family: Consolas;")
        self.setLayout(layout)

    def save_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Debe completar todos los campos")
            return

        success = create_user(username, password)

        if success:
            QMessageBox.information(self, "Éxito", f"Usuario '{username}' creado correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo crear el usuario")
