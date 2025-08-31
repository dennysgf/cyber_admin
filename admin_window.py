import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QHBoxLayout,
    QVBoxLayout, QPushButton, QAction, QLabel
)


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cyber Control - Administrador")
        self.setGeometry(200, 200, 1000, 700)

        menubar = self.menuBar()
        menu_caja = menubar.addMenu("Caja")
        menu_usuarios = menubar.addMenu("Usuarios")

        action_crear_usuario = QAction("Crear Usuario", self)
        menu_usuarios.addAction(action_crear_usuario)

        action_recargar = QAction("Recargar Tiempo", self)
        menu_usuarios.addAction(action_recargar)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        grid = QGridLayout()
        self.pc_buttons = []
        num_pcs = 12
        for i in range(num_pcs):
            btn = QPushButton(f"PC {i+1}")
            btn.setFixedSize(120, 100)
            btn.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            grid.addWidget(btn, i // 4, i % 4)
            self.pc_buttons.append(btn)

        right_panel = QVBoxLayout()
        label_title = QLabel("💰 Caja del Administrador")
        label_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.label_caja = QLabel("$0.00")
        self.label_caja.setStyleSheet("font-size: 20px; color: green; font-weight: bold;")

        right_panel.addWidget(label_title)
        right_panel.addWidget(self.label_caja)
        right_panel.addStretch()

        main_layout.addLayout(grid, 4)
        main_layout.addLayout(right_panel, 1)
