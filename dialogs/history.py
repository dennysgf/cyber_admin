from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from utils.models import get_recargas, get_historial_cajas


class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📜 Historial de Recargas")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2e;
                color: white;
                gridline-color: #2a2a2a;
                font-family: Consolas;
            }
            QHeaderView::section {
                background-color: #000000;
                color: #00ffea;
                font-weight: bold;
                border: 1px solid #00ffea;
                padding: 6px;
            }
            QTableWidget::item {
                background-color: #1e1e2e;
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #00ffea;
                color: black;
            }
        """)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Usuario", "Promoción", "Monto", "Fecha"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: white;
                font-family: Consolas;
            }
        """)

        self.setLayout(layout)
        self.load_history()

    def load_history(self):
        recargas = get_recargas()
        self.table.setRowCount(0)
        for r in recargas:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(r["usuario"]))
            self.table.setItem(row, 1, QTableWidgetItem(r["promo"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"${r['monto']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(r["fecha"])))


class HistoryCajaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📦 Historial de Cajas")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2e;
                color: white;
                gridline-color: #2a2a2a;
                font-family: Consolas;
            }
            QHeaderView::section {
                background-color: #000000;
                color: #00ffea;
                font-weight: bold;
                border: 1px solid #00ffea;
                padding: 6px;
            }
            QTableWidget::item {
                background-color: #1e1e2e;
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #00ffea;
                color: black;
            }
        """)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Fecha", "Monto"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: white;
                font-family: Consolas;
            }
        """)

        self.setLayout(layout)
        self.load_history()

    def load_history(self):
        cajas = get_historial_cajas()
        self.table.setRowCount(0)
        for c in cajas:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(c[0])))  # fecha
            self.table.setItem(row, 1, QTableWidgetItem(f"${c[1]:.2f}"))  # monto
