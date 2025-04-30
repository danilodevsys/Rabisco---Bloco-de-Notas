'''
Módulo para gerenciar o editor de texto do Rabisco
Contém as funcionalidades de formatação de texto
'''

from PyQt5.QtWidgets import QTextEdit, QColorDialog
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QTextCursor, QTextListFormat
from PyQt5.QtCore import Qt


class EditorTexto:
    '''Classe para gerenciar as funcionalidades do editor de texto'''
    
    def __init__(self, janela_principal):
        '''Inicializa o gerenciador de editor de texto'''
        self.janela = janela_principal
        
    def formatar_negrito(self):
        '''Aplica ou remove formatação de negrito ao texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Obter o cursor e formato atual
        cursor = editor.textCursor()
        formato = QTextCharFormat()
        
        # Se não há seleção, aplicar ao próximo caractere digitado
        if cursor.hasSelection():
            # Obter o formato atual
            formato = cursor.charFormat()
            
            # Alternar negrito
            if formato.fontWeight() == QFont.Bold:
                formato.setFontWeight(QFont.Normal)
            else:
                formato.setFontWeight(QFont.Bold)
                
            # Aplicar formato
            cursor.mergeCharFormat(formato)
            editor.mergeCurrentCharFormat(formato)
        else:
            # Alternar negrito para próximos caracteres
            formato = editor.currentCharFormat()
            if formato.fontWeight() == QFont.Bold:
                formato.setFontWeight(QFont.Normal)
            else:
                formato.setFontWeight(QFont.Bold)
            
            editor.setCurrentCharFormat(formato)
    
    def formatar_italico(self):
        '''Aplica ou remove formatação de itálico ao texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Obter o cursor e formato atual
        cursor = editor.textCursor()
        formato = QTextCharFormat()
        
        # Se não há seleção, aplicar ao próximo caractere digitado
        if cursor.hasSelection():
            # Obter o formato atual
            formato = cursor.charFormat()
            
            # Alternar itálico
            formato.setFontItalic(not formato.fontItalic())
                
            # Aplicar formato
            cursor.mergeCharFormat(formato)
            editor.mergeCurrentCharFormat(formato)
        else:
            # Alternar itálico para próximos caracteres
            formato = editor.currentCharFormat()
            formato.setFontItalic(not formato.fontItalic())
            editor.setCurrentCharFormat(formato)
    
    def formatar_sublinhado(self):
        '''Aplica ou remove formatação de sublinhado ao texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Obter o cursor e formato atual
        cursor = editor.textCursor()
        formato = QTextCharFormat()
        
        # Se não há seleção, aplicar ao próximo caractere digitado
        if cursor.hasSelection():
            # Obter o formato atual
            formato = cursor.charFormat()
            
            # Alternar sublinhado
            formato.setFontUnderline(not formato.fontUnderline())
                
            # Aplicar formato
            cursor.mergeCharFormat(formato)
            editor.mergeCurrentCharFormat(formato)
        else:
            # Alternar sublinhado para próximos caracteres
            formato = editor.currentCharFormat()
            formato.setFontUnderline(not formato.fontUnderline())
            editor.setCurrentCharFormat(formato)
    
    def mudar_cor_texto(self):
        '''Muda a cor do texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Abrir diálogo de cor
        cor = QColorDialog.getColor(editor.textColor(), self.janela, 'Selecionar Cor do Texto')
        
        if cor.isValid():
            # Obter o cursor e formato atual
            cursor = editor.textCursor()
            formato = QTextCharFormat()
            
            # Definir cor
            formato.setForeground(cor)
            
            # Se não há seleção, aplicar ao próximo caractere digitado
            if cursor.hasSelection():
                cursor.mergeCharFormat(formato)
            
            # Aplicar formato para próximos caracteres
            editor.mergeCurrentCharFormat(formato)
    
    def aumentar_fonte(self):
        '''Aumenta o tamanho da fonte do texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Obter o cursor e formato atual
        cursor = editor.textCursor()
        formato = QTextCharFormat()
        
        # Se não há seleção, aplicar ao próximo caractere digitado
        if cursor.hasSelection():
            # Obter o formato atual
            formato = cursor.charFormat()
            
            # Aumentar tamanho da fonte
            tamanho_atual = formato.font().pointSize()
            if tamanho_atual < 0:
                tamanho_atual = editor.font().pointSize()
            
            formato.setFontPointSize(tamanho_atual + 1)
                
            # Aplicar formato
            cursor.mergeCharFormat(formato)
            editor.mergeCurrentCharFormat(formato)
        else:
            # Aumentar tamanho para próximos caracteres
            formato = editor.currentCharFormat()
            tamanho_atual = formato.font().pointSize()
            if tamanho_atual < 0:
                tamanho_atual = editor.font().pointSize()
                
            formato.setFontPointSize(tamanho_atual + 1)
            editor.setCurrentCharFormat(formato)
    
    def diminuir_fonte(self):
        '''Diminui o tamanho da fonte do texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Obter o cursor e formato atual
        cursor = editor.textCursor()
        formato = QTextCharFormat()
        
        # Se não há seleção, aplicar ao próximo caractere digitado
        if cursor.hasSelection():
            # Obter o formato atual
            formato = cursor.charFormat()
            
            # Diminuir tamanho da fonte (mínimo 8)
            tamanho_atual = formato.font().pointSize()
            if tamanho_atual < 0:
                tamanho_atual = editor.font().pointSize()
            
            novo_tamanho = max(8, tamanho_atual - 1)
            formato.setFontPointSize(novo_tamanho)
                
            # Aplicar formato
            cursor.mergeCharFormat(formato)
            editor.mergeCurrentCharFormat(formato)
        else:
            # Diminuir tamanho para próximos caracteres
            formato = editor.currentCharFormat()
            tamanho_atual = formato.font().pointSize()
            if tamanho_atual < 0:
                tamanho_atual = editor.font().pointSize()
                
            novo_tamanho = max(8, tamanho_atual - 1)
            formato.setFontPointSize(novo_tamanho)
            editor.setCurrentCharFormat(formato)
            
    def formatar_tachado(self):
        '''Aplica ou remove formatação de tachado ao texto selecionado'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Obter o cursor e formato atual
        cursor = editor.textCursor()
        formato = QTextCharFormat()
        
        # Se não há seleção, aplicar ao próximo caractere digitado
        if cursor.hasSelection():
            # Obter o formato atual
            formato = cursor.charFormat()
            
            # Alternar tachado
            formato.setFontStrikeOut(not formato.fontStrikeOut())
                
            # Aplicar formato
            cursor.mergeCharFormat(formato)
            editor.mergeCurrentCharFormat(formato)
        else:
            # Alternar tachado para próximos caracteres
            formato = editor.currentCharFormat()
            formato.setFontStrikeOut(not formato.fontStrikeOut())
            editor.setCurrentCharFormat(formato)
    
    def inserir_lista(self):
        '''Insere uma lista no texto'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
            
        # Obter o cursor atual
        cursor = editor.textCursor()
        
        # Criar formato de lista
        lista_formato = cursor.currentList()
        
        # Se já estiver em uma lista, remover
        if lista_formato:
            cursor.beginEditBlock()
            cursor.createList(QTextListFormat())
            cursor.endEditBlock()
        else:
            # Criar novo formato de lista
            formato = QTextListFormat()
            formato.setStyle(QTextListFormat.ListDisc)  # Pontos (bullet points)
            
            cursor.beginEditBlock()
            cursor.createList(formato)
            cursor.endEditBlock()
        
        # Atualizar o editor
        editor.setTextCursor(cursor)
    
    def alinhar_esquerda(self):
        '''Alinha o texto à esquerda'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
        editor.setAlignment(Qt.AlignLeft)
    
    def alinhar_direita(self):
        '''Alinha o texto à direita'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
        editor.setAlignment(Qt.AlignRight)
    
    def alinhar_centro(self):
        '''Centraliza o texto'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
        editor.setAlignment(Qt.AlignCenter)
    
    def alinhar_justificado(self):
        '''Justifica o texto'''
        editor = self.janela._obter_editor_atual()
        if not editor:
            return
        editor.setAlignment(Qt.AlignJustify)
