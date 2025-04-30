#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Rabisco - Um simples bloco de notas
Arquivo principal da aplicação com integração das novas funcionalidades
'''

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, 
                           QMessageBox, QTabWidget, QTextEdit, QLabel)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor
from PyQt5 import uic

# Importar as novas funcionalidades
from src.rabisco_funcoes import (GerenciadorFundo, GerenciadorTema, 
                               FerramentasSistema, DialogoBusca, SobreManager,
                               CalendarioManager, FerramentasManager)
from src.editor_texto import EditorTexto
from src.formatacao_dialog import FormatacaoDialog

# --- Constantes ---
# VERSAO: Versão atual do aplicativo
VERSAO = '1.0.0.1'
# AUTOR: Nome do autor do aplicativo
AUTOR = 'Danilo (danilodevsys)'

class RabiscoApp(QMainWindow):
    '''Classe principal da aplicação Rabisco'''

    def __init__(self):
        '''Inicializa a aplicação Rabisco'''
        super().__init__()

        # --- Carregar a interface a partir do arquivo .ui ---
        try:
            base_dir = os.path.dirname(__file__)
            ui_file_path = os.path.join(base_dir, 'tela.ui')
            
            # Verificar se o arquivo existe
            if not os.path.exists(ui_file_path):
                raise FileNotFoundError(f'Arquivo de interface "tela.ui" não encontrado em: {ui_file_path}')
                
            # Carregar a interface
            uic.loadUi(ui_file_path, self)
            
        except Exception as e:
            QMessageBox.critical(None, 'Erro de Interface', 
                              f'Erro ao carregar a interface: {str(e)}')
            sys.exit(1)

        # --- Inicializar componentes ---
        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        
        # Inicializar gerenciadores
        self.gerenciador_fundo = GerenciadorFundo(self)
        self.gerenciador_tema = GerenciadorTema(self)
        self.ferramentas = FerramentasSistema(self)
        self.sobre_manager = SobreManager(self)
        self.calendario_manager = CalendarioManager(self)
        self.editor_texto = EditorTexto(self)
        
        # Configurar rodapé
        self.configurar_rodape(VERSAO, AUTOR)
        
        # Configurar ícones
        self.configurar_icones()
        
        # Configurar estilos dos botões de formatação
        self.configurar_estilos_formatacao()
        
        # Conectar sinais
        self.conectar_sinais()
        
        # Verificar se há uma aba inicial vazia
        if self.tabWidget.count() == 1:
            # Verificar se a aba inicial está vazia
            editor = self.tabWidget.widget(0)
            if isinstance(editor, QTextEdit) and not editor.toPlainText():
                # Manter a aba vazia
                pass
            else:
                # Remover a aba inicial e criar uma nova
                self.tabWidget.removeTab(0)
                self.nova_aba()
        else:
            # Criar uma nova aba se não houver nenhuma
            self.nova_aba()
        
        # Timer para atualizar estado de ações
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.atualizar_disponibilidade_acoes_timer)
        self.update_timer.start(500)  # Atualizar a cada 500ms

    def configurar_rodape(self, versao, autor):
        '''Configura o rodapé com informações de versão e autor'''
        self.statusbar.showMessage(f'Versão {versao} | {autor}')

    def configurar_icones(self):
        '''Configura os ícones para a barra de ferramentas e menus'''
        base_dir = os.path.dirname(__file__)
        icon_folder_path = os.path.join(os.path.dirname(base_dir), 'assets', 'icons')
        
        # Verificar se a pasta de ícones existe
        if not os.path.exists(icon_folder_path):
            QMessageBox.warning(self, 'Aviso', f'Pasta de ícones não encontrada: {icon_folder_path}')
            return
            
        # Dicionário de ações e seus ícones
        icones = {
            'actionNovo': 'novo.png',
            'actionAbrir': 'abrir.png',
            'actionSalvar': 'salvar.png',
            'actionSalvarComo': 'salvar_como.png',
            'actionImprimir': 'imprimir.png',
            'actionCortar': 'cortar.png',
            'actionCopiar': 'copiar.png',
            'actionColar': 'colar.png',
            'actionDesfazer': 'desfazer.png',
            'actionRefazer': 'refazer.png',
            'actionLocalizar': 'localizar.png',
            'actionCalculadora': 'calculadora.png',
            'actionCalendario': 'calendario.png',
            'actionNovaAba': 'nova_aba.png',
            'actionCor_do_Texto': 'cor_texto.png',
            'actionAumentarFonte': 'aumentar_fonte.png',
            'actionDiminuirFonte': 'diminuir_fonte.png',
            'actionFormatacao': 'formatacao.png'
        }
        
        # Definir ícones para cada ação
        for action_name, icon_file in icones.items():
            if hasattr(self, action_name):
                action = getattr(self, action_name)
                icon_path = os.path.join(icon_folder_path, icon_file)
                
                if os.path.exists(icon_path):
                    action.setIcon(QIcon(icon_path))
                else:
                    print(f"Ícone não encontrado: {icon_path}")
        
        # Informar que os ícones foram carregados
        print(f"Ícones carregados do diretório: {icon_folder_path}")

    def configurar_estilos_formatacao(self):
        '''Configura os estilos dos botões de formatação de texto'''
        from PyQt5.QtGui import QFont
        
        # Negrito
        fonte_negrito = QFont()
        fonte_negrito.setBold(True)
        self.actionNegrito.setFont(fonte_negrito)
        
        # Itálico
        fonte_italico = QFont()
        fonte_italico.setItalic(True)
        self.actionItalico.setFont(fonte_italico)
        
        # Sublinhado
        fonte_sublinhado = QFont()
        fonte_sublinhado.setUnderline(True)
        self.actionSublinhado.setFont(fonte_sublinhado)
        
        # Tachado
        fonte_tachado = QFont()
        fonte_tachado.setStrikeOut(True)
        self.actionTachado.setFont(fonte_tachado)
        
        # Configurar alinhamento
        if hasattr(self, 'actionFormatacao'):
            self.actionFormatacao.setText('Formatação')
        
        # Configurar aparência do editor
        self.configurar_aparencia_editor()

    def conectar_sinais(self):
        '''Conecta os sinais aos slots correspondentes'''
        def conectar_se_existir(action_name, slot_func):
            '''Conecta uma ação ao slot correspondente se a ação existir'''
            if hasattr(self, action_name):
                action = getattr(self, action_name)
                action.triggered.connect(slot_func)
        
        # Conectar ações de arquivo
        conectar_se_existir('actionNovo', self.novo_arquivo)
        conectar_se_existir('actionAbrir', self.abrir_arquivo)
        conectar_se_existir('actionSalvar', self.salvar_arquivo)
        conectar_se_existir('actionSalvarComo', self.salvar_como)
        conectar_se_existir('actionFechar', lambda: self.fechar_aba(self.tabWidget.currentIndex()))
        conectar_se_existir('actionSair', self.close)
        
        # Conectar ações de edição
        conectar_se_existir('actionDesfazer', lambda: self._obter_editor_atual().undo() if self._obter_editor_atual() else None)
        conectar_se_existir('actionRefazer', lambda: self._obter_editor_atual().redo() if self._obter_editor_atual() else None)
        conectar_se_existir('actionCortar', self.cortar_texto)
        conectar_se_existir('actionCopiar', self.copiar_texto)
        conectar_se_existir('actionColar', self.colar_texto)
        
        # Conectar ações de formatação
        conectar_se_existir('actionNegrito', self.editor_texto.formatar_negrito)
        conectar_se_existir('actionItalico', self.editor_texto.formatar_italico)
        conectar_se_existir('actionSublinhado', self.editor_texto.formatar_sublinhado)
        conectar_se_existir('actionTachado', self.editor_texto.formatar_tachado)
        conectar_se_existir('actionLista', self.editor_texto.inserir_lista)
        conectar_se_existir('actionCor_do_Texto', self.editor_texto.mudar_cor_texto)
        conectar_se_existir('actionAumentarFonte', self.editor_texto.aumentar_fonte)
        conectar_se_existir('actionDiminuirFonte', self.editor_texto.diminuir_fonte)
        
        # Conectar ação de formatação
        conectar_se_existir('actionFormatacao', self.abrir_dialogo_formatacao)
        
        # Conectar novas ações
        conectar_se_existir('actionLocalizar', self.abrir_localizar_substituir)
        conectar_se_existir('actionCalculadora', self.ferramentas.abrir_calculadora)
        conectar_se_existir('actionCalendario', self.calendario_manager.abrir_calendario)
        conectar_se_existir('actionNovaAba', self.nova_aba)
        
        # Conectar sinal de mudança de aba
        self.tabWidget.currentChanged.connect(self.atualizar_estado_aba)
        
        # Conectar sinal de fechamento de aba
        self.tabWidget.tabCloseRequested.connect(self.fechar_aba)

    def _obter_editor_atual(self):
        '''
        Retorna o editor de texto da aba ativa, ou None se não houver
        
        Returns:
            QTextEdit: Editor de texto atual ou None
        '''
        indice_atual = self.tabWidget.currentIndex()
        if indice_atual >= 0:
            editor = self.tabWidget.widget(indice_atual)
            if isinstance(editor, QTextEdit):
                return editor
        return None

    def cortar_texto(self):
        '''Corta o texto selecionado para a área de transferência'''
        editor = self._obter_editor_atual()
        if editor:
            editor.cut()

    def copiar_texto(self):
        '''Copia o texto selecionado para a área de transferência'''
        editor = self._obter_editor_atual()
        if editor:
            editor.copy()

    def colar_texto(self):
        '''Cola o texto da área de transferência no editor'''
        editor = self._obter_editor_atual()
        if editor:
            editor.paste()

    def atualizar_estado_aba(self, index):
        '''
        Atualiza o estado da janela quando a aba muda
        
        Args:
            index: Índice da nova aba ativa
        '''
        self.atualizar_interface_aba_ativa()

    def atualizar_interface_aba_ativa(self):
        '''Atualiza a interface baseada na aba ativa'''
        editor = self._obter_editor_atual()
        if editor:
            # Atualizar título da janela
            arquivo = editor.property('arquivo_associado')
            if arquivo:
                nome_arquivo = os.path.basename(arquivo)
                self.setWindowTitle(f'{nome_arquivo} - Rabisco')
            else:
                self.setWindowTitle('Sem título - Rabisco')
            
            # Habilitar ações de edição
            self.atualizar_disponibilidade_acoes(True)
        else:
            # Desabilitar ações de edição
            self.atualizar_disponibilidade_acoes(False)

    def atualizar_disponibilidade_acoes(self, habilitar_edicao=True):
        '''
        Habilita/desabilita ações com base no estado da aba ativa
        
        Args:
            habilitar_edicao: Se True, habilita ações de edição
        '''
        def set_enabled(action_name, enabled):
            '''Define se uma ação está habilitada ou não'''
            if hasattr(self, action_name):
                getattr(self, action_name).setEnabled(enabled)
        
        # Ações de edição
        set_enabled('actionSalvar', habilitar_edicao)
        set_enabled('actionSalvarComo', habilitar_edicao)
        set_enabled('actionFechar', habilitar_edicao)
        set_enabled('actionDesfazer', habilitar_edicao)
        set_enabled('actionRefazer', habilitar_edicao)
        set_enabled('actionCortar', habilitar_edicao)
        set_enabled('actionCopiar', habilitar_edicao)
        set_enabled('actionColar', habilitar_edicao)
        set_enabled('actionLocalizar', habilitar_edicao)
        
        # Ações de formatação
        set_enabled('actionNegrito', habilitar_edicao)
        set_enabled('actionItalico', habilitar_edicao)
        set_enabled('actionSublinhado', habilitar_edicao)
        set_enabled('actionTachado', habilitar_edicao)
        set_enabled('actionLista', habilitar_edicao)
        set_enabled('actionCor_do_Texto', habilitar_edicao)
        set_enabled('actionFormatacao', habilitar_edicao)

    def atualizar_disponibilidade_acoes_timer(self):
        '''Atualiza ações que mudam com frequência (ex: Copiar, Desfazer)'''
        editor = self._obter_editor_atual()
        if editor:
            # Verificar se há texto selecionado
            tem_selecao = editor.textCursor().hasSelection()
            
            # Atualizar disponibilidade das ações
            if hasattr(self, 'actionCortar'):
                self.actionCortar.setEnabled(tem_selecao)
            if hasattr(self, 'actionCopiar'):
                self.actionCopiar.setEnabled(tem_selecao)

    def novo_arquivo(self):
        '''Cria uma nova aba em branco'''
        self.nova_aba()

    def configurar_aparencia_editor(self):
        '''Configura a aparência do editor com fundo transparente'''
        # Verificar se há abas existentes
        for i in range(self.tabWidget.count()):
            editor = self.tabWidget.widget(i)
            if isinstance(editor, QTextEdit):
                self._configurar_estilo_editor(editor)

    def _configurar_estilo_editor(self, editor):
        '''Configura o estilo visual de um editor específico'''
        from PyQt5.QtGui import QPalette
        import os
        
        # Obter o caminho do ícone de transparência
        base_dir = os.path.dirname(__file__)
        icon_folder_path = os.path.join(os.path.dirname(base_dir), 'assets', 'icons')
        texto_icon_path = os.path.join(icon_folder_path, 'texto.png')
        
        # Verificar se o ícone existe
        if os.path.exists(texto_icon_path):
            # Usar o ícone como fundo com estilo CSS
            estilo = f'''
                QTextEdit {{ 
                    border: 1px solid #cccccc; 
                    border-radius: 3px; 
                    background-image: url({texto_icon_path.replace('\\', '/')}); 
                    background-repeat: no-repeat; 
                    background-position: center; 
                    background-attachment: fixed; 
                    background-color: rgba(240, 240, 255, 230); 
                }}
            '''
            editor.setStyleSheet(estilo)
        else:
            # Criar uma paleta personalizada como fallback
            paleta = editor.palette()
            
            # Definir cor de fundo com leve transparência
            cor_fundo = QColor(240, 240, 255, 230)  # RGB com alfa (transparência)
            paleta.setColor(QPalette.Base, cor_fundo)
            
            # Aplicar a paleta
            editor.setPalette(paleta)
            
            # Adicionar uma borda sutil
            editor.setStyleSheet('QTextEdit { border: 1px solid #cccccc; border-radius: 3px; }')

    def nova_aba(self, caminho_arquivo=None, conteudo=''):
        '''
        Adiciona uma nova aba ao tabWidget
        
        Args:
            caminho_arquivo: Caminho do arquivo associado (opcional)
            conteudo: Conteúdo inicial do editor (opcional)
            
        Returns:
            int: Índice da nova aba
        '''
        # Criar um novo editor
        editor = QTextEdit()
        editor.setProperty('arquivo_associado', caminho_arquivo)
        editor.setProperty('modificado', False)
        
        # Configurar fonte padrão
        fonte = editor.font()
        fonte.setPointSize(12)
        editor.setFont(fonte)
        
        # Configurar aparência do editor
        self._configurar_estilo_editor(editor)
        
        # Definir conteúdo inicial
        if conteudo:
            editor.setPlainText(conteudo)
        
        # Conectar sinal de modificação
        editor.textChanged.connect(lambda: self._marcar_modificado(editor, True))
        
        # Adicionar ao tabWidget
        if caminho_arquivo:
            nome_aba = os.path.basename(caminho_arquivo)
        else:
            nome_aba = 'Nova Nota'
        
        indice = self.tabWidget.addTab(editor, nome_aba)
        self.tabWidget.setCurrentIndex(indice)
        
        # Conectar sinal de modificação
        editor.document().contentsChanged.connect(
            lambda: self._marcar_modificado(editor, True)
        )
        
        return indice

    def _marcar_modificado(self, editor, modificado):
        '''
        Atualiza o título da aba e estado de Salvar quando o conteúdo muda
        
        Args:
            editor: Editor que foi modificado
            modificado: Se o conteúdo foi modificado
        '''
        # Definir a propriedade de modificado
        editor.setProperty('modificado', modificado)
        
        # Encontrar o índice da aba
        for i in range(self.tabWidget.count()):
            if self.tabWidget.widget(i) == editor:
                # Atualizar o título da aba
                titulo = self.tabWidget.tabText(i)
                
                # Remover o asterisco se já existir
                if titulo.endswith('*'):
                    titulo = titulo[:-1]
                
                # Adicionar asterisco se modificado
                if modificado:
                    titulo += '*'
                
                self.tabWidget.setTabText(i, titulo)
                break

    def abrir_arquivo(self):
        '''Abre um arquivo existente em uma nova aba'''
        caminho, _ = QFileDialog.getOpenFileName(
            self, 'Abrir Arquivo', '', 'Arquivos de Texto (*.txt);;Todos os Arquivos (*)'
        )
        
        if not caminho:
            return
            
        try:
            # Verificar se o arquivo já está aberto
            for i in range(self.tabWidget.count()):
                editor = self.tabWidget.widget(i)
                if editor.property('arquivo_associado') == caminho:
                    self.tabWidget.setCurrentIndex(i)
                    return
            
            # Ler o conteúdo do arquivo
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                
            # Criar nova aba com o conteúdo
            self.nova_aba(caminho, conteudo)
            
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao abrir o arquivo: {str(e)}')

    def salvar_arquivo(self):
        '''
        Salva o conteúdo da aba ativa
        
        Returns:
            bool: True se o arquivo foi salvo com sucesso
        '''
        editor = self._obter_editor_atual()
        if not editor:
            return False
            
        # Verificar se já existe um arquivo associado
        caminho = editor.property('arquivo_associado')
        if not caminho:
            return self.salvar_como()
            
        try:
            # Salvar o conteúdo no arquivo
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                arquivo.write(editor.toPlainText())
                
            # Atualizar estado do editor
            editor.document().setModified(False)
            self._marcar_modificado(editor, False)
            return True
            
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao salvar o arquivo: {str(e)}')
            return False

    def salvar_como(self):
        '''
        Salva o arquivo da aba ativa com um novo nome/local
        
        Returns:
            bool: True se o arquivo foi salvo com sucesso
        '''
        editor = self._obter_editor_atual()
        if not editor:
            return False
            
        caminho, _ = QFileDialog.getSaveFileName(
            self, 'Salvar Como', '', 'Arquivos de Texto (*.txt);;Todos os Arquivos (*)'
        )
        
        if not caminho:
            return False
            
        try:
            # Salvar o conteúdo no arquivo
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                arquivo.write(editor.toPlainText())
                
            # Atualizar propriedades do editor
            editor.setProperty('arquivo_associado', caminho)
            editor.document().setModified(False)
            self._marcar_modificado(editor, False)
            
            # Atualizar título da janela
            nome_arquivo = os.path.basename(caminho)
            self.setWindowTitle(f'{nome_arquivo} - Rabisco')
            
            return True
            
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao salvar o arquivo: {str(e)}')
            return False

    def fechar_aba(self, indice):
        '''
        Fecha a aba no índice especificado, perguntando se deseja salvar
        
        Args:
            indice: Índice da aba a ser fechada
        '''
        if indice < 0 or indice >= self.tabWidget.count():
            return
            
        editor = self.tabWidget.widget(indice)
        if not editor:
            return
            
        # Verificar se há alterações não salvas
        if editor.property('modificado'):
            arquivo = editor.property('arquivo_associado')
            nome_arquivo = os.path.basename(arquivo) if arquivo else 'Sem título'
            
            resposta = QMessageBox.question(
                self, 'Salvar alterações?',
                f'O documento "{nome_arquivo}" foi modificado. Deseja salvar as alterações?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if resposta == QMessageBox.Save:
                # Ativar a aba para salvar
                self.tabWidget.setCurrentIndex(indice)
                if not self.salvar_arquivo():
                    return  # Cancelar fechamento se não conseguir salvar
            elif resposta == QMessageBox.Cancel:
                return  # Cancelar fechamento
        
        # Remover a aba
        self.tabWidget.removeTab(indice)
        
        # Criar uma nova aba se não houver mais nenhuma
        if self.tabWidget.count() == 0:
            self.nova_aba()

    def abrir_localizar_substituir(self):
        '''Abre o diálogo de localizar e substituir'''
        editor = self._obter_editor_atual()
        if not editor:
            QMessageBox.warning(self, 'Aviso', 'Nenhuma aba de edição ativa.')
            return
            
        dialogo = DialogoBusca(editor, self)
        dialogo.exec_()
        
    def abrir_dialogo_formatacao(self):
        '''Abre o diálogo de formatação de texto'''
        editor = self._obter_editor_atual()
        if not editor:
            return
            
        # Abrir o diálogo de formatação
        alinhamento = FormatacaoDialog.obter_formatacao(self)
        
        # Aplicar o alinhamento escolhido
        if alinhamento == 'esquerda':
            self.editor_texto.alinhar_esquerda()
        elif alinhamento == 'centro':
            self.editor_texto.alinhar_centro()
        elif alinhamento == 'direita':
            self.editor_texto.alinhar_direita()
        elif alinhamento == 'justificado':
            self.editor_texto.alinhar_justificado()

    def mostrar_versao_rodape(self):
        '''Mostra a versão e autor no rodapé'''
        self.statusbar.showMessage(f'Rabisco v{VERSAO} - {AUTOR}')
