from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
import os

class RabiscoSplashScreen(QSplashScreen):
    def __init__(self, parent=None):
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons', 'logo_rabisco.ico')
        if not os.path.exists(logo_path):
            # fallback para .png se existir
            logo_path = logo_path.replace('.ico', '.png')
        pixmap = QPixmap(logo_path)
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        self.setFont(QFont('Arial', 14, QFont.Bold))
        self.showMessage('Carregando Rabisco...', Qt.AlignBottom | Qt.AlignCenter, Qt.white)

    def mostrar(self, tempo_ms=2000):
        self.show()
        QTimer.singleShot(tempo_ms, self.close)
