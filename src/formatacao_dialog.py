#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QGroupBox, QRadioButton, QButtonGroup, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os

class FormatacaoDialog(QDialog):
    '''Diálogo para configuração de formatação de texto'''
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Formatação de Texto')
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.resultado = None
        self.inicializar_ui()
        
    def inicializar_ui(self):
        '''Inicializa a interface do diálogo'''
        layout_principal = QVBoxLayout()
        
        # Grupo de alinhamento
        grupo_alinhamento = QGroupBox('Alinhamento de Texto')
        layout_alinhamento = QVBoxLayout()
        
        # Botões de alinhamento
        self.btn_alinhar_esquerda = QRadioButton('Alinhar à Esquerda')
        self.btn_alinhar_centro = QRadioButton('Centralizar')
        self.btn_alinhar_direita = QRadioButton('Alinhar à Direita')
        self.btn_alinhar_justificado = QRadioButton('Justificar')
        
        # Grupo de botões para alinhamento
        self.grupo_botoes_alinhamento = QButtonGroup()
        self.grupo_botoes_alinhamento.addButton(self.btn_alinhar_esquerda)
        self.grupo_botoes_alinhamento.addButton(self.btn_alinhar_centro)
        self.grupo_botoes_alinhamento.addButton(self.btn_alinhar_direita)
        self.grupo_botoes_alinhamento.addButton(self.btn_alinhar_justificado)
        
        # Adicionar botões ao layout
        layout_alinhamento.addWidget(self.btn_alinhar_esquerda)
        layout_alinhamento.addWidget(self.btn_alinhar_centro)
        layout_alinhamento.addWidget(self.btn_alinhar_direita)
        layout_alinhamento.addWidget(self.btn_alinhar_justificado)
        grupo_alinhamento.setLayout(layout_alinhamento)
        
        # Botões de OK e Cancelar
        layout_botoes = QHBoxLayout()
        self.btn_ok = QPushButton('OK')
        self.btn_cancelar = QPushButton('Cancelar')
        
        self.btn_ok.clicked.connect(self.aceitar)
        self.btn_cancelar.clicked.connect(self.reject)
        
        layout_botoes.addWidget(self.btn_ok)
        layout_botoes.addWidget(self.btn_cancelar)
        
        # Adicionar widgets ao layout principal
        layout_principal.addWidget(grupo_alinhamento)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_botoes)
        
        self.setLayout(layout_principal)
        
        # Definir o alinhamento à esquerda como padrão
        self.btn_alinhar_esquerda.setChecked(True)
        
        # Carregar ícones se disponíveis
        self.carregar_icones()
    
    def carregar_icones(self):
        '''Carrega ícones para os botões de alinhamento'''
        base_dir = os.path.dirname(__file__)
        icon_folder_path = os.path.join(os.path.dirname(base_dir), 'assets', 'icons')
        
        # Definir ícones para os botões de alinhamento
        icones = {
            self.btn_alinhar_esquerda: 'alinhar_esquerda.png',
            self.btn_alinhar_centro: 'alinhar_centro.png',
            self.btn_alinhar_direita: 'alinhar_direita.png',
            self.btn_alinhar_justificado: 'alinhar_justificado.png'
        }
        
        # Aplicar ícones se existirem
        for botao, nome_icone in icones.items():
            caminho_icone = os.path.join(icon_folder_path, nome_icone)
            if os.path.exists(caminho_icone):
                botao.setIcon(QIcon(caminho_icone))
    
    def aceitar(self):
        '''Processa a escolha do usuário e fecha o diálogo'''
        if self.btn_alinhar_esquerda.isChecked():
            self.resultado = 'esquerda'
        elif self.btn_alinhar_centro.isChecked():
            self.resultado = 'centro'
        elif self.btn_alinhar_direita.isChecked():
            self.resultado = 'direita'
        elif self.btn_alinhar_justificado.isChecked():
            self.resultado = 'justificado'
        
        self.accept()
    
    @staticmethod
    def obter_formatacao(parent=None):
        '''
        Método estático para exibir o diálogo e obter a formatação escolhida
        
        Returns:
            str: Tipo de alinhamento escolhido ('esquerda', 'centro', 'direita', 'justificado')
                 ou None se o diálogo for cancelado
        '''
        dialog = FormatacaoDialog(parent)
        resultado = dialog.exec_()
        
        if resultado == QDialog.Accepted:
            return dialog.resultado
        
        return None
