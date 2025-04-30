#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rabisco - Um simples bloco de notas
Arquivo que gerencia os elementos visuais da aplicação
"""

import os
from PyQt5.QtWidgets import (QTextEdit, QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QListWidget, 
                           QMessageBox, QColorDialog, QFontDialog, QComboBox)
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5 import uic

class InterfaceRabisco:
    """Classe responsável por gerenciar os elementos visuais da aplicação"""
    
    def __init__(self, janela_principal):
        """Inicializa a interface do Rabisco"""
        self.janela = janela_principal
    
    def criar_novo_editor(self):
        """
        Cria um novo componente de edição de texto
        
        Returns:
            QTextEdit: Novo editor de texto configurado
        """
        editor = QTextEdit()
        editor.setAcceptRichText(True)
        editor.setLineWrapMode(QTextEdit.WidgetWidth)
        editor.setTabStopWidth(40)  # 4 espaços para tabulação
        
        # Configurar fonte padrão
        fonte = QFont("Aptos (Corpo)", 12)
        editor.setFont(fonte)
        
        return editor
    
    def aplicar_negrito(self, editor):
        """
        Aplica ou remove formatação de negrito ao texto selecionado
        
        Args:
            editor: Editor de texto atual
        """
        if not editor:
            return
            
        # Obter o formato atual
        cursor = editor.textCursor()
        formato = cursor.charFormat()
        
        # Inverter estado do negrito
        formato.setFontWeight(
            QFont.Normal if formato.fontWeight() == QFont.Bold else QFont.Bold
        )
        
        # Aplicar o formato
        cursor.mergeCharFormat(formato)
        editor.mergeCurrentCharFormat(formato)
    
    def aplicar_italico(self, editor):
        """
        Aplica ou remove formatação de itálico ao texto selecionado
        
        Args:
            editor: Editor de texto atual
        """
        if not editor:
            return
            
        # Obter o formato atual
        cursor = editor.textCursor()
        formato = cursor.charFormat()
        
        # Inverter estado do itálico
        formato.setFontItalic(not formato.fontItalic())
        
        # Aplicar o formato
        cursor.mergeCharFormat(formato)
        editor.mergeCurrentCharFormat(formato)
    
    def aplicar_sublinhado(self, editor):
        """
        Aplica ou remove formatação de sublinhado ao texto selecionado
        
        Args:
            editor: Editor de texto atual
        """
        if not editor:
            return
            
        # Obter o formato atual
        cursor = editor.textCursor()
        formato = cursor.charFormat()
        
        # Inverter estado do sublinhado
        formato.setFontUnderline(not formato.fontUnderline())
        
        # Aplicar o formato
        cursor.mergeCharFormat(formato)
        editor.mergeCurrentCharFormat(formato)
    
    def aplicar_cor_texto(self, editor, cor):
        """
        Aplica cor ao texto selecionado
        
        Args:
            editor: Editor de texto atual
            cor: Cor a ser aplicada
        """
        if not editor or not cor.isValid():
            return
            
        # Criar formato com a cor
        formato = QTextCharFormat()
        formato.setForeground(cor)
        
        # Aplicar o formato
        cursor = editor.textCursor()
        cursor.mergeCharFormat(formato)
        editor.mergeCurrentCharFormat(formato)
    
    def exibir_dialogo_notificacao(self, mensagem, titulo="Notificação"):
        """
        Exibe um diálogo de notificação personalizado
        
        Args:
            mensagem: Mensagem a ser exibida
            titulo: Título do diálogo (opcional)
            
        Returns:
            bool: True se o usuário clicou em OK, False caso contrário
        """
        try:
            # Carregar o diálogo a partir do arquivo .ui
            dialogo = QDialog(self.janela)
            uic.loadUi("notificacao.ui", dialogo)
            
            # Configurar o diálogo
            dialogo.setWindowTitle(titulo)
            dialogo.labelMensagem.setText(mensagem)
            
            # Conectar os botões
            dialogo.btnOk.clicked.connect(dialogo.accept)
            dialogo.btnCancelar.clicked.connect(dialogo.reject)
            
            # Exibir o diálogo e retornar o resultado
            resultado = dialogo.exec_()
            return resultado == QDialog.Accepted
        except Exception as e:
            # Em caso de erro, usar uma caixa de diálogo padrão
            QMessageBox.information(self.janela, titulo, mensagem)
            return True
    
    def dialogo_busca(self):
        """
        Cria e exibe um diálogo de busca de texto
        
        Returns:
            str: Texto a ser pesquisado ou None se cancelado
        """
        dialogo = QDialog(self.janela)
        dialogo.setWindowTitle("Buscar")
        dialogo.setMinimumWidth(300)
        
        # Criar componentes
        label = QLabel("Texto a buscar:")
        texto_busca = QLineEdit()
        
        btn_ok = QPushButton("Buscar")
        btn_cancelar = QPushButton("Cancelar")
        
        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(texto_busca)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialogo.setLayout(layout)
        
        # Conectar sinais
        btn_ok.clicked.connect(dialogo.accept)
        btn_cancelar.clicked.connect(dialogo.reject)
        
        # Exibir diálogo
        resultado = dialogo.exec_()
        
        if resultado == QDialog.Accepted:
            return texto_busca.text()
        else:
            return None
    
    def buscar_texto(self, editor, texto_buscar, direcao_avante=True):
        """
        Busca texto no editor
        
        Args:
            editor: Editor de texto atual
            texto_buscar: Texto a ser buscado
            direcao_avante: True para buscar para frente, False para trás
            
        Returns:
            bool: True se o texto foi encontrado
        """
        if not editor or not texto_buscar:
            return False
            
        # Definir opções de busca
        opcoes = QTextDocument.FindFlags()
        if not direcao_avante:
            opcoes |= QTextDocument.FindBackward
        
        # Realizar a busca
        encontrado = editor.find(texto_buscar, opcoes)
        
        return encontrado
    
    def substituir_texto(self, editor, texto_buscar, texto_substituir):
        """
        Substitui o texto selecionado
        
        Args:
            editor: Editor de texto atual
            texto_buscar: Texto a ser buscado
            texto_substituir: Texto de substituição
            
        Returns:
            int: Número de substituições realizadas
        """
        if not editor or not texto_buscar:
            return 0
            
        # Guardar posição do cursor
        cursor = editor.textCursor()
        posicao_inicial = cursor.position()
        
        # Mover para o início
        cursor.movePosition(QTextCursor.Start)
        editor.setTextCursor(cursor)
        
        # Realizar as substituições
        contador = 0
        encontrado = True
        
        while encontrado:
            encontrado = editor.find(texto_buscar)
            if encontrado:
                cursor = editor.textCursor()
                cursor.insertText(texto_substituir)
                contador += 1
        
        # Restaurar posição
        cursor = editor.textCursor()
        cursor.setPosition(posicao_inicial)
        editor.setTextCursor(cursor)
        
        return contador
    
    def dialogo_substituir(self):
        """
        Cria e exibe um diálogo de substituição de texto
        
        Returns:
            tuple: (texto_buscar, texto_substituir) ou (None, None) se 
                  cancelado
        """
        dialogo = QDialog(self.janela)
        dialogo.setWindowTitle("Substituir")
        dialogo.setMinimumWidth(400)
        
        # Criar componentes
        label_busca = QLabel("Texto a buscar:")
        texto_busca = QLineEdit()
        
        label_subst = QLabel("Substituir por:")
        texto_subst = QLineEdit()
        
        btn_ok = QPushButton("Substituir")
        btn_cancelar = QPushButton("Cancelar")
        
        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(label_busca)
        layout.addWidget(texto_busca)
        layout.addWidget(label_subst)
        layout.addWidget(texto_subst)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialogo.setLayout(layout)
        
        # Conectar sinais
        btn_ok.clicked.connect(dialogo.accept)
        btn_cancelar.clicked.connect(dialogo.reject)
        
        # Exibir diálogo
        resultado = dialogo.exec_()
        
        if resultado == QDialog.Accepted:
            return (texto_busca.text(), texto_subst.text())
        else:
            return (None, None)
    
    def dialogo_selecao_fonte(self, fonte_atual=None):
        """
        Exibe diálogo para seleção de fonte
        
        Args:
            fonte_atual: Fonte atual (opcional)
            
        Returns:
            QFont: Fonte selecionada ou None se cancelado
        """
        if fonte_atual is None:
            fonte_atual = QFont("Aptos (Corpo)", 12)
            
        # Abrir diálogo de seleção de fonte
        ok, fonte = QFontDialog.getFont(fonte_atual, self.janela)
        
        if ok:
            return fonte
        else:
            return None
    
    def dialogo_categorias(self, categorias_existentes=None, categoria_atual=None):
        """
        Exibe diálogo para gestão de categorias
        
        Args:
            categorias_existentes: Lista de categorias existentes (opcional)
            categoria_atual: Categoria atual (opcional)
            
        Returns:
            str: Categoria selecionada ou None se cancelado
        """
        dialogo = QDialog(self.janela)
        dialogo.setWindowTitle("Categorias")
        dialogo.setMinimumWidth(300)
        
        # Criar componentes
        label = QLabel("Selecione ou crie uma categoria:")
        combo_categorias = QComboBox()
        
        if categorias_existentes:
            combo_categorias.addItems(categorias_existentes)
            
        label_nova = QLabel("Nova categoria:")
        texto_nova = QLineEdit()
        
        btn_ok = QPushButton("OK")
        btn_cancelar = QPushButton("Cancelar")
        
        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(combo_categorias)
        layout.addWidget(label_nova)
        layout.addWidget(texto_nova)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialogo.setLayout(layout)
        
        # Definir categoria atual, se houver
        if categoria_atual and categoria_atual in categorias_existentes:
            index = combo_categorias.findText(categoria_atual)
            combo_categorias.setCurrentIndex(index)
        
        # Conectar sinais
        btn_ok.clicked.connect(dialogo.accept)
        btn_cancelar.clicked.connect(dialogo.reject)
        
        # Exibir diálogo
        resultado = dialogo.exec_()
        
        if resultado == QDialog.Accepted:
            # Verificar se foi selecionada uma categoria existente ou criada uma nova
            nova_categoria = texto_nova.text().strip()
            if nova_categoria:
                return nova_categoria
            else:
                return combo_categorias.currentText()
        else:
            return None