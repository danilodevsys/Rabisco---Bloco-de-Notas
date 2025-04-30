# run_v7_parte1.py

import os
import sys
import subprocess
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QTextEdit, QInputDialog, QMessageBox, QDialog, QLineEdit, QPushButton, QVBoxLayout)
from PyQt6.QtGui import QIcon
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6 import uic

# --- Classes Auxiliares ---

class FundoEditorManager:
    """Gerencia a cor de fundo do editor"""
    def __init__(self, parent):
        self.parent = parent

    def mudar_cor_fundo(self):
        editor = self.parent._obter_editor_atual()
        if editor:
            cores = {
                "Amarelo": "#FFF9C4",
                "Verde": "#C8E6C9",
                "Azul": "#BBDEFB",
                "Rosa": "#F8BBD0",
                "Roxo": "#E1BEE7",
                "Branco": "#FFFFFF",
            }
            cor_nome, ok = QInputDialog.getItem(self.parent, "Escolher Cor de Fundo", "Cores disponíveis:", list(cores.keys()), 0, False)
            if ok and cor_nome:
                cor_hex = cores[cor_nome]
                editor.setStyleSheet(f"background-color: {cor_hex};")
        else:
            QMessageBox.warning(self.parent, "Aviso", "Nenhuma aba de edição ativa.")

class FerramentasSistemaManager:
    """Gerencia ferramentas do sistema"""
    def __init__(self, parent):
        self.parent = parent

    def abrir_calculadora(self):
        try:
            subprocess.Popen('calc.exe')
        except Exception as e:
            QMessageBox.critical(self.parent, "Erro", f"Não foi possível abrir a calculadora: {str(e)}")

    def imprimir_documento(self):
        editor = self.parent._obter_editor_atual()
        if editor:
            printer = QPrinter()
            dialog = QPrintDialog(printer, self.parent)
            if dialog.exec():
                editor.print(printer)
        else:
            QMessageBox.warning(self.parent, "Aviso", "Nenhuma aba de edição ativa para imprimir.")

class EditorBuscaManager(QDialog):
    """Janela de busca e substituição"""
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("Localizar e Substituir")

        self.busca_input = QLineEdit(self)
        self.busca_input.setPlaceholderText("Texto para localizar")

        self.substituir_input = QLineEdit(self)
        self.substituir_input.setPlaceholderText("Texto para substituir")

        self.botao_buscar = QPushButton("Localizar", self)
        self.botao_substituir = QPushButton("Substituir", self)

        layout = QVBoxLayout()
        layout.addWidget(self.busca_input)
        layout.addWidget(self.substituir_input)
        layout.addWidget(self.botao_buscar)
        layout.addWidget(self.botao_substituir)
        self.setLayout(layout)

        self.botao_buscar.clicked.connect(self.localizar)
        self.botao_substituir.clicked.connect(self.substituir)

    def localizar(self):
        texto = self.busca_input.text()
        if texto:
            self.editor.find(texto)

    def substituir(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.substituir_input.text())

# run_v7_parte2.py (continuação)

import os
import sys
import subprocess
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QTextEdit, QInputDialog, QMessageBox, QDialog, QLineEdit, QPushButton, QVBoxLayout)
from PyQt6.QtGui import QIcon
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6 import uic

# --- Classes Auxiliares ---
# (FundoEditorManager, FerramentasSistemaManager, EditorBuscaManager já definidos acima)

# --- Classe Principal RabiscoApp ---

class RabiscoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(__file__)
        ui_file_path = os.path.join(base_dir, "tela.ui")
        uic.loadUi(ui_file_path, self)

        self.gerenciador_fundo = FundoEditorManager(self)
        self.ferramentas = FerramentasSistemaManager(self)

        self._configurar_icones()
        self._conectar_sinais()

        if self.tabWidget.count() == 0:
            self.nova_aba()
        else:
            widget_inicial = self.tabWidget.widget(0)
            if not isinstance(widget_inicial, QTextEdit):
                self.tabWidget.removeTab(0)
                self.nova_aba()
            else:
                self.atualizar_estado_aba(0)

    def _obter_editor_atual(self):
        editor = self.tabWidget.currentWidget()
        if isinstance(editor, QTextEdit):
            return editor
        return None

    def nova_aba(self):
        nova = QTextEdit()
        index = self.tabWidget.addTab(nova, "Nova Nota")
        self.tabWidget.setCurrentIndex(index)

    def atualizar_estado_aba(self, index):
        self.tabWidget.setCurrentIndex(index)

# (continua... Parte 3: Métodos Salvar, Abrir, Cortar, Colar...)


# run_v7_parte3.py (continuação)

import os
import sys
import subprocess
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QTextEdit, QInputDialog, QMessageBox, QDialog, QLineEdit, QPushButton, QVBoxLayout, QFileDialog)
from PyQt6.QtGui import QIcon
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6 import uic

# --- Classes Auxiliares ---
# (FundoEditorManager, FerramentasSistemaManager, EditorBuscaManager já definidos acima)

# --- Classe Principal RabiscoApp ---

class RabiscoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(__file__)
        ui_file_path = os.path.join(base_dir, "tela.ui")
        uic.loadUi(ui_file_path, self)

        self.gerenciador_fundo = FundoEditorManager(self)
        self.ferramentas = FerramentasSistemaManager(self)

        self._configurar_icones()
        self._conectar_sinais()

        if self.tabWidget.count() == 0:
            self.nova_aba()
        else:
            widget_inicial = self.tabWidget.widget(0)
            if not isinstance(widget_inicial, QTextEdit):
                self.tabWidget.removeTab(0)
                self.nova_aba()
            else:
                self.atualizar_estado_aba(0)

    def _obter_editor_atual(self):
        editor = self.tabWidget.currentWidget()
        if isinstance(editor, QTextEdit):
            return editor
        return None

    def nova_aba(self):
        nova = QTextEdit()
        index = self.tabWidget.addTab(nova, "Nova Nota")
        self.tabWidget.setCurrentIndex(index)

    def atualizar_estado_aba(self, index):
        self.tabWidget.setCurrentIndex(index)

    def salvar_arquivo(self):
        editor = self._obter_editor_atual()
        if editor:
            caminho, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Texto (*.txt)")
            if caminho:
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())

    def abrir_arquivo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Texto (*.txt)")
        if caminho:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            self.nova_aba()
            editor = self._obter_editor_atual()
            editor.setPlainText(conteudo)

    def cortar_texto(self):
        editor = self._obter_editor_atual()
        if editor:
            editor.cut()

    def copiar_texto(self):
        editor = self._obter_editor_atual()
        if editor:
            editor.copy()

    def colar_texto(self):
        editor = self._obter_editor_atual()
        if editor:
            editor.paste()

# (continua... Parte 4: Toolbar, Botões e Sinais)

# run_v7_parte4.py (continuação)

# Continua após a definição dos métodos básicos do RabiscoApp

    def _configurar_icones(self):
        """Configura os ícones da barra de ferramentas"""
        base_dir = os.path.dirname(__file__)
        icon_folder_path = os.path.join(base_dir, "assets", "icons")

        self.actionSalvar.setIcon(QIcon(os.path.join(icon_folder_path, "salvar.png")))
        self.actionAbrir.setIcon(QIcon(os.path.join(icon_folder_path, "abrir.png")))
        self.actionCortar.setIcon(QIcon(os.path.join(icon_folder_path, "cortar.png")))
        self.actionColar.setIcon(QIcon(os.path.join(icon_folder_path, "colar.png")))
        self.actionLocalizar.setIcon(QIcon(os.path.join(icon_folder_path, "localizar.png")))
        self.actionCalculadora.setIcon(QIcon(os.path.join(icon_folder_path, "calculadora.png")))
        self.actionMudarTema.setIcon(QIcon(os.path.join(icon_folder_path, "tema.png")))
        self.actionColorir.setIcon(QIcon(os.path.join(icon_folder_path, "colorir.png")))
        self.actionImprimir.setIcon(QIcon(os.path.join(icon_folder_path, "imprimir.png")))

    def _conectar_sinais(self):
        """Conecta os botões e ações"""
        self.actionSalvar.triggered.connect(self.salvar_arquivo)
        self.actionAbrir.triggered.connect(self.abrir_arquivo)
        self.actionCortar.triggered.connect(self.cortar_texto)
        self.actionColar.triggered.connect(self.colar_texto)
        self.actionLocalizar.triggered.connect(self.abrir_localizar_substituir)
        self.actionCalculadora.triggered.connect(self.ferramentas.abrir_calculadora)
        self.actionMudarTema.triggered.connect(self.alternar_tema)
        self.actionColorir.triggered.connect(self.gerenciador_fundo.mudar_cor_fundo)
        self.actionImprimir.triggered.connect(self.ferramentas.imprimir_documento)

    def abrir_localizar_substituir(self):
        editor = self._obter_editor_atual()
        if editor:
            dialogo = EditorBuscaManager(editor)
            dialogo.exec()

    def alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        if self.styleSheet():
            self.setStyleSheet("")
        else:
            self.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")

# (continua... Parte 5: função main para rodar o aplicativo)

