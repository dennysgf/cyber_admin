from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from utils.models import (
    get_users, get_promotions, add_time_to_user,
    insert_recarga, add_to_caja
)


class RechargeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⏳ Recargar Tiempo")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        title = QLabel("⚡ Recargar Tiempo")
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
                background-color: #1e1e1e;
                color: white;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #2a2a2a;
                color: white;
                font-weight: bold;
                border: 1px solid #444;
                padding: 4px;
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

        self.combo_time = QComboBox()
        promos = get_promotions() or []
        for promo in promos:
            if promo and "id" in promo:
                self.combo_time.addItem(f"{promo['price']} USD = {promo['hours']} horas", promo)
        layout.addWidget(self.combo_time)

        self.btn_apply = QPushButton("Aplicar Recarga")
        self.btn_apply.clicked.connect(self.apply_recharge)
        layout.addWidget(self.btn_apply)

        self.setStyleSheet("background-color: #121212; color: white; font-family: Consolas;")
        self.setLayout(layout)

        self.recharge_amount = 0
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
            tiempo_segundos = int(u.get("tiempo", 0) or 0)
            horas = tiempo_segundos // 3600
            minutos = (tiempo_segundos % 3600) // 60
            segundos = tiempo_segundos % 60
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

    def apply_recharge(self):
        if not self.selected_user:
            return
        promo = self.combo_time.currentData()
        if not promo or not promo.get("id"):
            return

        add_time_to_user(self.selected_user["id"], promo["hours"] * 3600)
        insert_recarga(self.selected_user["id"], promo["id"], promo["price"])
        add_to_caja(promo["price"])  # 👈 se suma a la caja del día

        for u in self.all_users:
            if u["id"] == self.selected_user["id"]:
                u["tiempo"] = (u.get("tiempo", 0) or 0) + (promo["hours"] * 3600)
                self.selected_user = u
                break

        self.filter_users()
        self.recharge_amount = promo["price"]
