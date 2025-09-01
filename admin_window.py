from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QHBoxLayout,
    QVBoxLayout, QPushButton, QAction, QLabel, QSizePolicy
)
from dialogs.create_user import CreateUserDialog
from dialogs.recharge import RechargeDialog
from dialogs.create_promo import CreatePromoDialog
from utils.models import init_caja, get_caja
from dialogs.history import HistoryDialog


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎮 Cyber Control - Administrador")
        self.setGeometry(200, 200, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
                color: #ffffff;
                font-family: Consolas, monospace;
            }
            QMenuBar {
                background-color: #000000;
                color: #00ffea;
                font-weight: bold;
            }
            QMenuBar::item:selected {
                background-color: #00ffea;
                color: #000000;
            }
        """)
        self.promotions = []
        self.pc_status = {}  # estado de cada PC

        menubar = self.menuBar()
        menu_caja = menubar.addMenu("Caja")
        menu_usuarios = menubar.addMenu("Usuarios")
        menu_promos = menubar.addMenu("Promociones")

        action_crear_usuario = QAction("Crear Usuario", self)
        action_crear_usuario.triggered.connect(self.open_create_user)
        menu_usuarios.addAction(action_crear_usuario)

        action_recargar = QAction("Recargar Tiempo", self)
        action_recargar.triggered.connect(self.open_recharge)
        menu_usuarios.addAction(action_recargar)

        action_crear_promo = QAction("Crear Promoción", self)
        action_crear_promo.triggered.connect(self.open_create_promo)
        menu_promos.addAction(action_crear_promo)

        action_historial = QAction("Historial de Recargas", self)
        action_historial.triggered.connect(self.open_history)
        menu_caja.addAction(action_historial)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        grid = QGridLayout()
        self.pc_buttons = []
        num_pcs = 24
        for i in range(num_pcs):
            btn = QPushButton(f"PC {i+1}")
            btn.setMinimumSize(100, 80)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda _, idx=i: self.toggle_pc(idx))
            self.pc_buttons.append(btn)
            self.pc_status[i] = "libre"
            self.update_pc_style(i)
            grid.addWidget(btn, i // 6, i % 6)

        central_container = QWidget()
        central_container.setLayout(grid)

        right_panel = QVBoxLayout()
        label_title = QLabel("💰 Caja del Administrador")
        label_title.setStyleSheet("font-size: 16px; font-weight: bold; color: gold;")
        self.label_caja = QLabel("$0.00")
        self.label_caja.setStyleSheet("font-size: 20px; color: #00ff00; font-weight: bold;")

        init_caja()
        saldo = get_caja()
        self.label_caja.setText(f"${saldo:.2f}")

        right_panel.addWidget(label_title)
        right_panel.addWidget(self.label_caja)
        right_panel.addStretch()

        right_container = QWidget()
        right_container.setLayout(right_panel)
        right_container.setFixedWidth(260)

        main_layout.addWidget(central_container, 5)
        main_layout.addWidget(right_container, 1)

    def update_pc_style(self, idx):
        btn = self.pc_buttons[idx]
        if self.pc_status[idx] == "libre":
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff0044;
                    color: white;
                    font-weight: bold;
                    border-radius: 10px;
                    border: 2px solid #00ffea;
                }
                QPushButton:hover {
                    background-color: #00ffea;
                    color: black;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #00ff44;
                    color: black;
                    font-weight: bold;
                    border-radius: 10px;
                    border: 2px solid #ffffff;
                }
                QPushButton:hover {
                    background-color: #ffaa00;
                    color: black;
                }
            """)

    def toggle_pc(self, idx):
        if self.pc_status[idx] == "libre":
            self.pc_status[idx] = "ocupado"
        else:
            self.pc_status[idx] = "libre"
        self.update_pc_style(idx)

    def refresh_caja(self):
        saldo = get_caja()
        self.label_caja.setText(f"${saldo:.2f}")

    def open_create_user(self):
        dialog = CreateUserDialog(self)
        dialog.exec_()

    def open_recharge(self):
        dialog = RechargeDialog(self)
        if dialog.exec_():
            self.refresh_caja()

    def open_create_promo(self):
        dialog = CreatePromoDialog(self)
        if dialog.exec_():
            promo = dialog.promotion
            if promo:
                self.promotions.append(promo)
    def open_history(self):
        dialog = HistoryDialog(self)
        dialog.exec_()
