from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QHBoxLayout,
    QVBoxLayout, QPushButton, QAction, QLabel, QSizePolicy, QMenu
)
from PyQt5.QtCore import Qt, QTimer
from dialogs.create_user import CreateUserDialog
from dialogs.recharge import RechargeDialog
from dialogs.create_promo import CreatePromoDialog
from utils.models import (
    init_caja, get_caja, logout_user, get_active_sessions,
    remove_time, reset_password, get_historial_cajas
)
from PyQt5.QtGui import QIcon
from dialogs.history import HistoryDialog, HistoryCajaDialog
from dialogs.logout import LogoutDialog
from datetime import date
import os



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
        self.pc_status = {}
        self.pc_users = {}
        self.pc_hosts = {}
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icons8-administrador-de-redes-64.png")
        self.setWindowIcon(QIcon(icon_path))

        # Menú superior
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

        action_historial_cajas = QAction("Historial de Cajas", self)
        action_historial_cajas.triggered.connect(self.open_historial_cajas)
        menu_caja.addAction(action_historial_cajas)

        action_logout = QAction("Cerrar Sesión", self)
        action_logout.triggered.connect(self.open_logout)
        menu_usuarios.addAction(action_logout)

        # Layout principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Panel central con PCs
        grid = QGridLayout()
        self.pc_buttons = []
        num_pcs = 24
        for i in range(num_pcs):
            btn = QPushButton(f"PC {i+1}")
            btn.setMinimumSize(100, 80)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, idx=i: self.pc_context_menu(idx, pos))
            self.pc_buttons.append(btn)
            self.pc_status[i] = "libre"
            self.update_pc_style(i)
            grid.addWidget(btn, i // 6, i % 6)

        central_container = QWidget()
        central_container.setLayout(grid)

        # Panel derecho con caja
        right_panel = QVBoxLayout()
        today = date.today().strftime("%d/%m/%Y")
        label_title = QLabel(f"💰 Caja del {today}")
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

        # Timer para refrescar PCs
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_pc_grid)
        self.refresh_timer.start(2000)

        self.refresh_pc_grid()

    # ===== Estilos de botones =====
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

    # ===== Menú contextual en PCs =====
    def pc_context_menu(self, idx, pos):
        if self.pc_status[idx] == "ocupado":
            menu = QMenu()
            action_logout = menu.addAction("Cerrar Sesión")
            action_shutdown = menu.addAction("Apagar Computadora")
            action_remove_time = menu.addAction("Quitar Tiempo")
            action_reset_pass = menu.addAction("Resetear/Cambiar Clave")
            action = menu.exec_(self.pc_buttons[idx].mapToGlobal(pos))

            if action == action_logout:
                user_id = self.pc_users.get(idx)
                if user_id:
                    logout_user(user_id)
                self.pc_status[idx] = "libre"
                self.update_pc_style(idx)
                self.pc_users.pop(idx, None)
                self.pc_hosts.pop(idx, None)

            elif action == action_shutdown:
                hostname = self.pc_hosts.get(idx)
                if hostname:
                    os.system(f"shutdown /s /m \\\\{hostname} /t 0 /f")

            elif action == action_remove_time:
                user_id = self.pc_users.get(idx)
                if user_id:
                    from PyQt5.QtWidgets import QInputDialog
                    hours, ok = QInputDialog.getInt(self, "Quitar Tiempo", "Horas a restar:", 0, 0)
                    if ok and hours > 0:
                        seconds = hours * 60 * 60
                        remove_time(user_id, seconds)

            elif action == action_reset_pass:
                user_id = self.pc_users.get(idx)
                if user_id:
                    from PyQt5.QtWidgets import QInputDialog
                    new_pass, ok = QInputDialog.getText(self, "Resetear Clave", "Nueva contraseña:")
                    if ok and new_pass.strip():
                        reset_password(user_id, new_pass.strip())

    # ===== Refrescar PCs =====
    def refresh_pc_grid(self):
        for i, btn in enumerate(self.pc_buttons):
            self.pc_status[i] = "libre"
            self.pc_users.pop(i, None)
            self.pc_hosts.pop(i, None)
            btn.setText(f"PC {i+1}")
            self.update_pc_style(i)

        sessions = get_active_sessions()
        for s in sessions:
            idx = s["pc_number"] - 1
            if 0 <= idx < len(self.pc_buttons):
                self.pc_status[idx] = "ocupado"
                self.pc_users[idx] = s["user_id"]
                self.pc_hosts[idx] = s["hostname"]
                h = s["tiempo"] // 3600
                m = (s["tiempo"] % 3600) // 60
                sec = s["tiempo"] % 60
                self.pc_buttons[idx].setText(
                    f"PC {s['pc_number']}\n{s['username']}\n{h:02d}:{m:02d}:{sec:02d}"
                )
                self.update_pc_style(idx)

    # ===== Refrescar Caja =====
    def refresh_caja(self):
        saldo = get_caja()
        self.label_caja.setText(f"${saldo:.2f}")

    # ===== Ventanas auxiliares =====
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

    def open_logout(self):
        dialog = LogoutDialog(self)
        dialog.exec_()

    def open_historial_cajas(self):
        dialog = HistoryCajaDialog(self)
        dialog.exec_()
