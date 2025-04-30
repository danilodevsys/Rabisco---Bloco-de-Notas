#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Rabisco - Um simples bloco de notas
Implementação das funcionalidades solicitadas:
1. Colorir fundo (estilo Sticky Notes)
2. Mudar tema (claro/escuro)
3. Abrir calculadora do sistema
4. Imprimir documento
'''

import os
import subprocess
import webbrowser
from PyQt5.QtWidgets import (QInputDialog, QMessageBox, QDialog, 
                           QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QLineEdit, QColorDialog)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5.QtCore import Qt
from PyQt5 import uic

# --- Constantes ---
# CORES_STICKY: Dicionário de cores disponíveis para o fundo do editor
CORES_STICKY = {
    'Amarelo': '#FFF9C4',
    'Verde': '#C8E6C9',
    'Azul': '#BBDEFB',
    'Rosa': '#F8BBD0',
    'Roxo': '#E1BEE7',
    'Laranja': '#FFE0B2',
    'Cinza': '#F5F5F5',
    'Branco': '#FFFFFF'
}

# TEMA_ESCURO: Estilo CSS para o tema escuro
TEMA_ESCURO = '''
    QMainWindow, QDialog, QMessageBox {
        background-color: #2D2D30;
        color: #F0F0F0;
    }
    QMenuBar, QStatusBar {
        background-color: #1E1E1E;
        color: #F0F0F0;
    }
    QMenu {
        background-color: #2D2D30;
        color: #F0F0F0;
        border: 1px solid #3E3E40;
    }
    QMenu::item:selected {
        background-color: #3E3E40;
    }
    QToolBar {
        background-color: #2D2D30;
        border: 1px solid #3E3E40;
    }
    QTabWidget::pane {
        border: 1px solid #3E3E40;
    }
    QTabBar::tab {
        background-color: #2D2D30;
        color: #F0F0F0;
        border: 1px solid #3E3E40;
        padding: 5px;
    }
    QTabBar::tab:selected {
        background-color: #3E3E40;
    }
'''

class GerenciadorFundo:
    '''Classe responsável por gerenciar as cores de fundo do editor'''
    
    def __init__(self, janela_principal):
        '''Inicializa o gerenciador de fundo'''
        self.janela = janela_principal
    
    def mudar_cor_fundo(self):
        '''
        Altera a cor de fundo do editor atual para uma das cores pré-definidas
        similar ao Sticky Notes do Windows, usando uma interface gráfica intuitiva
        '''
        editor = self.janela._obter_editor_atual()
        if not editor:
            QMessageBox.warning(self.janela, 'Aviso', 'Nenhuma aba de edição ativa.')
            return
        
        try:
            # Carregar a interface do arquivo UI
            base_dir = os.path.dirname(os.path.dirname(__file__))
            ui_file_path = os.path.join(os.path.dirname(__file__), 'cores_fundo.ui')
            
            if not os.path.exists(ui_file_path):
                QMessageBox.warning(self.janela, 'Erro', f'Arquivo de interface não encontrado: {ui_file_path}')
                return
                
            # Criar diálogo
            dialogo = QDialog(self.janela)
            uic.loadUi(ui_file_path, dialogo)
            
            # Conectar sinais dos botões de cores
            dialogo.btnAmarelo.clicked.connect(lambda: self._aplicar_cor(editor, 'Amarelo', dialogo))
            dialogo.btnVerde.clicked.connect(lambda: self._aplicar_cor(editor, 'Verde', dialogo))
            dialogo.btnAzul.clicked.connect(lambda: self._aplicar_cor(editor, 'Azul', dialogo))
            dialogo.btnRosa.clicked.connect(lambda: self._aplicar_cor(editor, 'Rosa', dialogo))
            dialogo.btnRoxo.clicked.connect(lambda: self._aplicar_cor(editor, 'Roxo', dialogo))
            dialogo.btnLaranja.clicked.connect(lambda: self._aplicar_cor(editor, 'Laranja', dialogo))
            dialogo.btnCinza.clicked.connect(lambda: self._aplicar_cor(editor, 'Cinza', dialogo))
            dialogo.btnBranco.clicked.connect(lambda: self._aplicar_cor(editor, 'Branco', dialogo))
            dialogo.btnPersonalizado.clicked.connect(lambda: self._escolher_cor_personalizada(editor, dialogo))
            dialogo.btnCancelar.clicked.connect(dialogo.reject)
            
            # Mostrar diálogo
            dialogo.exec_()
            
        except Exception as e:
            QMessageBox.critical(self.janela, 'Erro', f'Erro ao abrir diálogo de cores: {str(e)}')
    
    def _aplicar_cor(self, editor, cor_nome, dialogo):
        '''Aplica a cor selecionada ao editor'''
        if cor_nome in CORES_STICKY:
            cor_hex = CORES_STICKY[cor_nome]
            editor.setStyleSheet(f'background-color: {cor_hex};')
            editor.setProperty('cor_fundo', cor_hex)
            dialogo.accept()
    
    def _escolher_cor_personalizada(self, editor, dialogo):
        '''Permite escolher uma cor personalizada'''
        cor = QColorDialog.getColor()
        if cor.isValid():
            editor.setStyleSheet(f'background-color: {cor.name()};')
            editor.setProperty('cor_fundo', cor.name())
            dialogo.accept()
            
    def mudar_cores(self):
        '''Alias para mudar_cor_fundo para compatibilidade'''
        self.mudar_cor_fundo()


class GerenciadorTema:
    '''Classe responsável por gerenciar os temas da aplicação'''
    
    def __init__(self, janela_principal):
        '''Inicializa o gerenciador de tema'''
        self.janela = janela_principal
        self.tema_escuro = False
    
    def alternar_tema(self):
        '''Alterna entre tema claro e escuro'''
        self.tema_escuro = not self.tema_escuro
        self.aplicar_tema_atual()
        
    def mudar_tema(self):
        '''Alias para alternar_tema para compatibilidade'''
        self.alternar_tema()
    
    def aplicar_tema_atual(self):
        '''Aplica o tema atual (claro ou escuro) à interface'''
        if self.tema_escuro:
            # Tema escuro
            self.janela.setStyleSheet(TEMA_ESCURO)
            # Salvar preferência
            self.janela.setProperty('tema_atual', 'Escuro')
        else:
            # Tema claro (padrão)
            self.janela.setStyleSheet('')
            # Salvar preferência
            self.janela.setProperty('tema_atual', 'Claro')


class FerramentasSistema:
    '''Classe para gerenciar ferramentas do sistema'''
    
    def __init__(self, janela_principal):
        '''Inicializa o gerenciador de ferramentas'''
        self.janela = janela_principal
    
    def abrir_calculadora(self):
        '''Executa a calculadora do sistema operacional Windows'''
        try:
            # Executa calc.exe sem esperar que termine (non-blocking)
            subprocess.Popen('calc.exe')
        except Exception as e:
            QMessageBox.critical(
                self.janela, 
                'Erro', 
                f'Não foi possível abrir a calculadora: {str(e)}'
            )
    
    def imprimir_documento(self):
        '''Imprime o documento da aba atual'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            QMessageBox.warning(self.janela, 'Aviso', 'Nenhuma aba de edição ativa para imprimir.')
            return
            
        # Criar impressora e diálogo de impressão
        impressora = QPrinter(QPrinter.HighResolution)
        dialogo = QPrintDialog(impressora, self.janela)
        
        # Se o usuário confirmar a impressão, imprimir o documento
        if dialogo.exec() == QDialog.Accepted:
            editor.print_(impressora)
    
    def mudar_cor_texto(self):
        '''Muda a cor do texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            QMessageBox.warning(self.janela, 'Aviso', 'Nenhuma aba de edição ativa.')
            return
        
        # Abrir diálogo de seleção de cor
        cor = QColorDialog.getColor()
        if cor.isValid():
            # Criar formato com a cor
            formato = QTextCharFormat()
            formato.setForeground(cor)
            
            # Aplicar o formato
            cursor = editor.textCursor()
            cursor.mergeCharFormat(formato)
            editor.mergeCurrentCharFormat(formato)


class CalendarioManager:
    '''Classe para gerenciar o calendário'''
    
    def __init__(self, janela_principal):
        '''Inicializa o gerenciador de calendário'''
        self.janela = janela_principal
    
    def mostrar_calendario(self):
        '''Mostra um calendário para inserir a data no texto'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            QMessageBox.warning(self.janela, 'Aviso', 'Nenhuma aba de edição ativa.')
            return
            
        try:
            # Criar diálogo
            dialogo = QDialog(self.janela)
            dialogo.setWindowTitle('Calendário')
            dialogo.setMinimumWidth(300)
            
            # Criar componentes
            layout = QVBoxLayout(dialogo)
            
            # Adicionar o widget de calendário
            from PyQt5.QtWidgets import QCalendarWidget
            calendario = QCalendarWidget(dialogo)
            calendario.setGridVisible(True)
            
            # Botões
            btn_inserir = QPushButton('Inserir Data', dialogo)
            btn_fechar = QPushButton('Fechar', dialogo)
            
            # Adicionar ao layout
            layout.addWidget(calendario)
            layout.addWidget(btn_inserir)
            layout.addWidget(btn_fechar)
            
            # Conectar sinais
            btn_inserir.clicked.connect(lambda: self._inserir_data(calendario, editor, dialogo))
            btn_fechar.clicked.connect(dialogo.accept)
            
            # Mostrar diálogo
            dialogo.exec_()
            
        except Exception as e:
            QMessageBox.critical(self.janela, 'Erro', f'Erro ao abrir calendário: {str(e)}')
    
    def _inserir_data(self, calendario, editor, dialogo):
        '''Insere a data selecionada no editor'''
        data = calendario.selectedDate()
        data_formatada = data.toString('dd/MM/yyyy')
        
        # Inserir no cursor atual
        cursor = editor.textCursor()
        cursor.insertText(data_formatada)
        dialogo.accept()


class SobreManager:
    '''Classe para gerenciar a janela Sobre'''
    
    def __init__(self, janela_principal):
        '''Inicializa o gerenciador da janela Sobre'''
        self.janela = janela_principal
    
    def mostrar_sobre(self):
        '''Mostra a janela Sobre com informações do aplicativo'''
        try:
            # Carregar a interface do arquivo UI
            ui_file_path = os.path.join(os.path.dirname(__file__), 'sobre.ui')
            
            if not os.path.exists(ui_file_path):
                QMessageBox.warning(self.janela, 'Erro', f'Arquivo de interface não encontrado: {ui_file_path}')
                return
                
            # Criar diálogo
            dialogo = QDialog(self.janela)
            uic.loadUi(ui_file_path, dialogo)
            
            # Conectar sinais
            dialogo.btnFechar.clicked.connect(dialogo.accept)
            
            # Configurar link do GitHub para ser clicável
            dialogo.labelGithub.linkActivated.connect(self._abrir_link)
            
            # Mostrar diálogo
            dialogo.exec_()
            
        except Exception as e:
            QMessageBox.critical(self.janela, 'Erro', f'Erro ao abrir janela Sobre: {str(e)}')
    
    def _abrir_link(self, url):
        '''Abre um link externo no navegador padrão'''
        try:
            webbrowser.open(url)
        except Exception as e:
            QMessageBox.warning(self.janela, 'Aviso', f'Não foi possível abrir o link: {str(e)}')


class DialogoBusca(QDialog):
    '''Diálogo para busca e substituição de texto'''
    
    def __init__(self, editor, parent=None):
        '''Inicializa o diálogo de busca'''
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle('Localizar e Substituir')
        self.setMinimumWidth(400)
        
        # Criar componentes
        self.label_busca = QLabel('Texto a buscar:')
        self.texto_busca = QLineEdit()
        
        self.label_subst = QLabel('Substituir por:')
        self.texto_subst = QLineEdit()
        
        self.btn_buscar = QPushButton('Localizar')
        self.btn_substituir = QPushButton('Substituir')
        self.btn_substituir_tudo = QPushButton('Substituir Tudo')
        self.btn_cancelar = QPushButton('Cancelar')
        
        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_busca)
        layout.addWidget(self.texto_busca)
        layout.addWidget(self.label_subst)
        layout.addWidget(self.texto_subst)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_buscar)
        btn_layout.addWidget(self.btn_substituir)
        btn_layout.addWidget(self.btn_substituir_tudo)
        btn_layout.addWidget(self.btn_cancelar)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Conectar sinais
        self.btn_buscar.clicked.connect(self.localizar)
        self.btn_substituir.clicked.connect(self.substituir)
        self.btn_substituir_tudo.clicked.connect(self.substituir_tudo)
        self.btn_cancelar.clicked.connect(self.reject)
    
    def localizar(self):
        '''Localiza o texto no editor'''
        texto = self.texto_busca.text()
        if texto:
            # Salvar a posição atual do cursor
            cursor_atual = self.editor.textCursor()
            
            # Tentar buscar a partir da posição atual
            encontrado = self.editor.find(texto)
            
            # Se não encontrou, voltar ao início e tentar novamente
            if not encontrado:
                # Mover para o início do documento
                cursor = self.editor.textCursor()
                cursor.movePosition(cursor.Start)
                self.editor.setTextCursor(cursor)
                
                # Tentar buscar novamente a partir do início
                encontrado = self.editor.find(texto)
                
                # Se ainda não encontrou, restaurar a posição original e mostrar mensagem
                if not encontrado:
                    self.editor.setTextCursor(cursor_atual)
                    QMessageBox.information(self, 'Busca', f'Texto "{texto}" não encontrado.')
    
    def substituir(self):
        '''Substitui a ocorrência atual do texto'''
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.texto_subst.text())
            # Buscar a próxima ocorrência
            self.localizar()
    
    def substituir_tudo(self):
        '''Substitui todas as ocorrências do texto'''
        texto_buscar = self.texto_busca.text()
        texto_substituir = self.texto_subst.text()
        
        if not texto_buscar:
            return
            
        # Salvar posição atual do cursor
        cursor_original = self.editor.textCursor()
        
        # Mover para o início do documento
        self.editor.moveCursor(cursor_original.Start)
        
        # Contador de substituições
        contador = 0
        
        # Substituir todas as ocorrências
        while self.editor.find(texto_buscar):
            cursor = self.editor.textCursor()
            cursor.insertText(texto_substituir)
            contador += 1
        
        # Informar resultado
        if contador > 0:
            QMessageBox.information(
                self, 
                'Substituir', 
                f'{contador} ocorrência(s) substituída(s).'
            )
        else:
            QMessageBox.information(
                self, 
                'Substituir', 
                f'Texto "{texto_buscar}" não encontrado.'
            )
