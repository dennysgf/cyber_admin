from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox


class RechargeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⏳ Recargar Tiempo")
        self.setFixedSize(350, 220)

        layout = QVBoxLayout()

        title = QLabel("⚡ Recarga de Tiempo")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ffea; text-align: center;")
        layout.addWidget(title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setStyleSheet("""
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

        self.combo_time = QComboBox()
        self.combo_time.addItems([
            "1 USD = 1 hora",
            "2 USD = 3 horas",
            "5 USD = 8 horas"
        ])
        self.combo_time.setStyleSheet("""
            QComboBox {
                background-color: #1e1e2e;
                color: #ffffff;
                border: 2px solid #00ffea;
                border-radius: 8px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        self.btn_apply = QPushButton("✅ Aplicar Recarga")
        self.btn_apply.setStyleSheet("""
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
        self.btn_apply.clicked.connect(self.apply_recharge)

        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Promoción:"))
        layout.addWidget(self.combo_time)
        layout.addWidget(self.btn_apply)

        self.setStyleSheet("background-color: #121212; color: white; font-family: Consolas;")
        self.setLayout(layout)

        self.recharge_amount = 0

    def apply_recharge(self):
        username = self.user_input.text().strip()
        promo = self.combo_time.currentText()

        if not username:
            QMessageBox.warning(self, "Error", "Debe ingresar el usuario")
            return

        if "1 USD" in promo:
            self.recharge_amount = 1
        elif "2 USD" in promo:
            self.recharge_amount = 2
        elif "5 USD" in promo:
            self.recharge_amount = 5

        QMessageBox.information(self, "Éxito", f"Se recargó {promo} al usuario '{username}'")
        self.accept()
