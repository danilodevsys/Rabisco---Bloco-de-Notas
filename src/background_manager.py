#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Rabisco - Um simples bloco de notas
Gerenciador de cores de fundo e temas
'''

from PyQt5.QtWidgets import QColorDialog, QInputDialog, QMessageBox
from PyQt5.QtGui import QColor

# --- Constantes de Cores ---
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

class GerenciadorFundo:
    '''Classe responsável por gerenciar as cores de fundo do editor'''
    
    def __init__(self, janela_principal):
        '''Inicializa o gerenciador de fundo'''
        self.janela = janela_principal
    
    def mudar_cor_fundo(self):
        '''
        Altera a cor de fundo do editor atual para uma das cores pré-definidas
        similar ao Sticky Notes do Windows
        '''
        editor = self.janela._obter_editor_atual()
        if not editor:
            QMessageBox.warning(self.janela, 'Aviso', 'Nenhuma aba de edição ativa.')
            return
        
        # Obter lista de cores disponíveis
        cores_nomes = list(CORES_STICKY.keys())
        
        # Exibir diálogo para escolha da cor
        cor_nome, ok = QInputDialog.getItem(
            self.janela, 
            'Escolher Cor de Fundo', 
            'Selecione uma cor:', 
            cores_nomes, 
            0,  # índice inicial
            False  # não editável
        )
        
        # Se uma cor foi selecionada, aplicar ao editor
        if ok and cor_nome:
            cor_hex = CORES_STICKY[cor_nome]
            editor.setStyleSheet(f'background-color: {cor_hex};')
            
            # Salvar a preferência de cor para esta aba
            editor.setProperty('cor_fundo', cor_hex)


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
    
    def aplicar_tema_atual(self):
        '''Aplica o tema atual (claro ou escuro) à interface'''
        if self.tema_escuro:
            # Tema escuro
            self.janela.setStyleSheet('''
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
            ''')
            # Salvar preferência
            self.janela.setProperty('tema_atual', 'Escuro')
        else:
            # Tema claro (padrão)
            self.janela.setStyleSheet('')
            # Salvar preferência
            self.janela.setProperty('tema_atual', 'Claro')
