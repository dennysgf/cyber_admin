from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.models import create_promotion   # 👈 importar

class CreatePromoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎁 Crear Promoción")
        self.setFixedSize(350, 220)

        layout = QVBoxLayout()

        title = QLabel("✨ Nueva Promoción")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ffea; text-align: center;")
        layout.addWidget(title)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Precio en USD (ej: 2)")
        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText("Horas (ej: 3)")

        self.btn_save = QPushButton("✅ Guardar Promoción")
        self.btn_save.clicked.connect(self.save_promo)

        layout.addWidget(QLabel("Precio:"))
        layout.addWidget(self.price_input)
        layout.addWidget(QLabel("Horas:"))
        layout.addWidget(self.hours_input)
        layout.addWidget(self.btn_save)

        self.setStyleSheet("background-color: #121212; color: white; font-family: Consolas;")
        self.setLayout(layout)

        self.promotion = None

    def save_promo(self):
        price = self.price_input.text().strip()
        hours = self.hours_input.text().strip()

        if not price or not hours:
            QMessageBox.warning(self, "Error", "Debe completar todos los campos")
            return

        try:
            price = float(price)
            hours = int(hours)
        except ValueError:
            QMessageBox.warning(self, "Error", "Precio y horas deben ser numéricos")
            return

        success = create_promotion(price, hours)
        if success:
            self.promotion = {"price": price, "hours": hours}
            QMessageBox.information(self, "Éxito", f"Promoción guardada en DB: {price} USD = {hours} horas")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la promoción en la DB")
