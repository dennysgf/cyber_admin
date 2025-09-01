from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QHBoxLayout,
    QVBoxLayout, QPushButton, QAction, QLabel, QSizePolicy
)
from dialogs.create_user import CreateUserDialog
from dialogs.recharge import RechargeDialog


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cyber Control - Administrador")
        self.setGeometry(200, 200, 1200, 800)

        menubar = self.menuBar()
        menu_caja = menubar.addMenu("Caja")
        menu_usuarios = menubar.addMenu("Usuarios")

        action_crear_usuario = QAction("Crear Usuario", self)
        action_crear_usuario.triggered.connect(self.open_create_user)
        menu_usuarios.addAction(action_crear_usuario)

        action_recargar = QAction("Recargar Tiempo", self)
        action_recargar.triggered.connect(self.open_recharge)
        menu_usuarios.addAction(action_recargar)

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
            btn.setStyleSheet("background-color: #fbc8c1; color: white; font-weight: bold;")
            grid.addWidget(btn, i // 6, i % 6)
            self.pc_buttons.append(btn)

        central_container = QWidget()
        central_container.setLayout(grid)

        right_panel = QVBoxLayout()
        label_title = QLabel("💰 Caja del Administrador")
        label_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.label_caja = QLabel("$0.00")
        self.label_caja.setStyleSheet("font-size: 18px; color: green; font-weight: bold;")

        right_panel.addWidget(label_title)
        right_panel.addWidget(self.label_caja)
        right_panel.addStretch()

        right_container = QWidget()
        right_container.setLayout(right_panel)
        right_container.setFixedWidth(200)

        main_layout.addWidget(central_container, 5)
        main_layout.addWidget(right_container, 1)

    def open_create_user(self):
        dialog = CreateUserDialog(self)
        dialog.exec_()

    def open_recharge(self):
        dialog = RechargeDialog(self)
        if dialog.exec_():
            amount = dialog.recharge_amount
            if amount > 0:
                current_value = float(self.label_caja.text().replace("$", ""))
                current_value += amount
                self.label_caja.setText(f"${current_value:.2f}")
