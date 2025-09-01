from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QMessageBox
)
from utils.models import get_users, logout_user


class LogoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔒 Cerrar Sesión de Usuario")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        title = QLabel("Cerrar Sesión de Usuario")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ffea; text-align: center;")
        layout.addWidget(title)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar usuario...")
        self.search_input.textChanged.connect(self.filter_users)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2e;
                color: white;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #000000;
                color: #00ffea;
                font-weight: bold;
                border: 1px solid #00ffea;
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #00ffea;
                color: black;
            }
        """)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Usuario", "Tiempo restante"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.cellClicked.connect(self.select_user_from_table)
        layout.addWidget(self.table)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario seleccionado")
        self.user_input.setReadOnly(True)
        layout.addWidget(self.user_input)

        self.btn_logout = QPushButton("Cerrar Sesión")
        self.btn_logout.clicked.connect(self.apply_logout)
        layout.addWidget(self.btn_logout)

        self.setStyleSheet("background-color: #121212; color: white; font-family: Consolas;")
        self.setLayout(layout)

        self.selected_user = None
        self.all_users = get_users() or []
        self.table.setRowCount(0)

    def load_users(self, users):
        self.table.setRowCount(0)
        for u in users:
            if not u or "username" not in u:
                continue
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(u["username"])))
            tiempo_horas = u.get("tiempo", 0) or 0
            total_seconds = int(tiempo_horas * 3600)
            horas = total_seconds // 3600
            minutos = (total_seconds % 3600) // 60
            segundos = total_seconds % 60
            formatted_time = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            self.table.setItem(row, 1, QTableWidgetItem(formatted_time))

    def filter_users(self):
        text = self.search_input.text().lower()
        if not text:
            self.table.setRowCount(0)
            return
        filtered = [u for u in self.all_users if text in u.get("username", "").lower()]
        self.load_users(filtered)

    def select_user_from_table(self, row, col):
        username = self.table.item(row, 0).text()
        for u in self.all_users:
            if u.get("username") == username:
                self.selected_user = u
                self.user_input.setText(username)
                break

    def apply_logout(self):
        if not self.selected_user:
            return
        confirm = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Cerrar sesión del usuario '{self.selected_user['username']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            logout_user(self.selected_user["id"])
            QMessageBox.information(self, "Éxito", "Sesión cerrada correctamente")
            self.accept()
