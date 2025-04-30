# -*- coding: utf-8 -*-
"""
Rabisco - Um simples bloco de notas
Arquivo que gerencia a execução da aplicação
"""

import os
import sys
# Importar QWidget explicitamente, pois QMainWindow herda dele
# Importar QLabel para o rodapé
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QColorDialog,
                           QMessageBox, QDialog, QCalendarWidget, QTabWidget,
                           QTextEdit, QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import QDate, Qt, QTimer # Importar QTimer para atualização de ações
from PyQt5.QtGui import QTextCharFormat, QFont, QColor, QIcon, QTextDocument, QTextCursor # Importar QTextDocument e QTextCursor
from PyQt5 import uic # Para carregar o arquivo .ui
from logica import GerenciadorNotas
from tela import InterfaceRabisco
from dados import BancoDados

class RabiscoApp(QMainWindow):
    """Classe principal da aplicação Rabisco"""

    def __init__(self):
        super().__init__()

        # --- Carregar a interface a partir do arquivo .ui ---
        # Garante que o arquivo tela.ui está na mesma pasta ou em um caminho conhecido
        try:
            base_dir = os.path.dirname(__file__)
            # Caminho direto ao lado do run.py
            ui_file_path = os.path.join(base_dir, "tela.ui")

            # Fallback: Tenta procurar um nível acima (se run.py estiver em 'src', por exemplo)
            if not os.path.exists(ui_file_path):
                ui_file_path_alt = os.path.join(os.path.dirname(base_dir), "tela.ui")
                if os.path.exists(ui_file_path_alt):
                    ui_file_path = ui_file_path_alt
                else:
                     # Tenta procurar dentro de uma pasta 'ui' ao lado de run.py
                     ui_file_path_alt_2 = os.path.join(base_dir, "ui", "tela.ui")
                     if os.path.exists(ui_file_path_alt_2):
                         ui_file_path = ui_file_path_alt_2
                     else:
                         raise FileNotFoundError(f"Arquivo de interface 'tela.ui' não encontrado nos locais esperados (ao lado de run.py, um nível acima ou em pasta 'ui'). Verificado: '{os.path.join(base_dir, 'tela.ui')}', '{ui_file_path_alt}', '{ui_file_path_alt_2}'")

            uic.loadUi(ui_file_path, self) # Carrega a UI para 'self'

        except FileNotFoundError as e:
             # Usar None como parent para garantir que a mensagem apareça mesmo se a janela principal falhar
             QMessageBox.critical(None, "Erro de Interface", f"Não foi possível carregar o arquivo de interface: {e}\nCertifique-se de que 'tela.ui' está na pasta correta.")
             sys.exit(1) # Encerrar a aplicação se a UI não carregar
        except Exception as e:
             QMessageBox.critical(None, "Erro de Interface", f"Erro inesperado ao carregar a interface: {e}")
             sys.exit(1)


        # --- Inicializar componentes ---
        # O arquivo do banco de dados será criado na pasta 'dados/' dentro do diretório base
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "dados", "rabisco.db")
        try:
            # Cria o diretório 'dados' se não existir
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.db = BancoDados(db_path) # Passa o caminho completo para o BD
        except Exception as e:
             QMessageBox.critical(None, "Erro de Banco de Dados", f"Não foi possível inicializar o banco de dados em '{db_path}': {e}")
             sys.exit(1) # Encerrar se o BD não inicializar

        self.gerenciador = GerenciadorNotas(self.db)
        self.interface = InterfaceRabisco(self) # Passa a própria janela principal

        # --- Obter referência para o TabWidget (QTabWidget) ---
        # Assumindo que foi criado e nomeado 'tabWidget' no arquivo .ui
        # Se você nomeou diferente no Qt Designer, ajuste 'tabWidget' abaixo
        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')

        # Verificar se o tabWidget foi encontrado (essencial para evitar NoneType errors)
        if not self.tabWidget:
             QMessageBox.critical(self, "Erro Fatal", "Widget 'tabWidget' não encontrado no arquivo UI. Verifique o nome no Qt Designer.")
             # Tentar encontrar QTabWidget sem nome específico como último recurso
             tabs = self.findChildren(QTabWidget)
             if tabs:
                 QMessageBox.warning(self, "Aviso", "Widget QTabWidget encontrado, mas sem o nome 'tabWidget'. Usando o primeiro encontrado.")
                 self.tabWidget = tabs[0]
             else:
                  QMessageBox.critical(self, "Erro Fatal", "Nenhum QTabWidget encontrado na UI.")
                  sys.exit(1)


        # --- Configuração da Interface ---
        self.tabWidget.setTabsClosable(True) # Permitir fechar abas
        self.tabWidget.setMovable(True) # Permitir mover abas

        # --- Configurar Ícones e Footer ---
        self._configurar_icones()
        self._configurar_footer() # Chama a nova função para o rodapé

        # --- Conectar Sinais e Slots ---
        self._conectar_sinais()

        # --- Configuração Inicial ---
        self.setWindowTitle("Rabisco") # Título inicial

        # Carregar configurações salvas (como tema)
        self.carregar_configuracoes()

        # Criar uma aba inicial vazia se não houver nenhuma (útil ao iniciar)
        if self.tabWidget.count() == 0:
            self.nova_aba()
        else:
            widget_inicial = self.tabWidget.widget(0)
            if not isinstance(widget_inicial, QTextEdit):
                self.tabWidget.removeTab(0)
                self.nova_aba()
            else:
                self.atualizar_estado_aba(0)
 
        # Timer para atualizar estado de ações como Copiar/Cortar/Desfazer/Refazer
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(300) # Atualiza a cada 300ms (ajuste conforme necessário)
        self.update_timer.timeout.connect(self._atualizar_disponibilidade_acoes_timer)
        self.update_timer.start()


    def _configurar_footer(self):
        """Configura o rodapé persistente na barra de status"""
        try:
            # Verificar se a statusbar existe (deve ter sido criada pelo .ui)
            if hasattr(self, 'statusbar'):
                # Adiciona um QLabel como widget permanente no lado direito
                footer_label = QLabel("v.1.0.0/25 | danilodevsys")
                self.statusbar.addPermanentWidget(footer_label)
            else:
                print("Aviso: QStatusBar com nome 'statusbar' não encontrado na UI. Rodapé não configurado.")
        except Exception as e:
            print(f"Aviso: Erro ao configurar rodapé: {e}")


    
    def _configurar_icones(self):
        """Configura os ícones para a barra de ferramentas e menus"""
        base_dir = os.path.dirname(__file__)  # Diretório de run.py (src)
        project_root = os.path.dirname(base_dir)
        icon_folder_path = os.path.join(project_root, "assets", "icons")

        print(f"Procurando ícones em: {icon_folder_path}")

        if not os.path.exists(icon_folder_path):
            print(f"AVISO: Pasta de ícones não encontrada em '{icon_folder_path}'")
            icon_folder_path_alt = os.path.join(base_dir, "icons")
            if os.path.exists(icon_folder_path_alt):
                print(f"Usando pasta alternativa: '{icon_folder_path_alt}'")
                icon_folder_path = icon_folder_path_alt
            else:
                print(f"Nenhuma pasta de ícones encontrada.")
                return

        # Atualizado para usar .png
        icon_map = {
            "actionNovaAba": "novo.png",
            "actionAbrir": "abrir.png",
            "actionSalvar": "salva.png",
            "actionCortar": "cortar.png",
            "actionColar": "colar.png",
            "actionMudarCores": "cores.png",
            "actionCalendario": "calendario.png",
            "actionCopiar": "copiar.png",
        }

        print(f"--- Carregando Ícones de: {icon_folder_path} ---")

        for action_name, icon_filename in icon_map.items():
            try:
                action = getattr(self, action_name)
                icon_path = os.path.join(icon_folder_path, icon_filename)
                if os.path.exists(icon_path):
                    action.setIcon(QIcon(icon_path))
                    print(f"✔ Ícone '{icon_filename}' aplicado na ação '{action_name}'")
                else:
                    print(f"⚠ Ícone '{icon_filename}' não encontrado para ação '{action_name}'")
            except AttributeError:
                print(f"⚠ Ação '{action_name}' não encontrada na interface.")

        print("--- Fim do Carregamento de Ícones ---")


    def _conectar_sinais(self):
        """Conecta os sinais aos slots correspondentes"""
        # Helper para conectar uma ação se ela existir
        def conectar_se_existir(action_name, slot_func):
            action = getattr(self, action_name, None)
            if action:
                try: # Desconecta primeiro para evitar conexões múltiplas
                    action.triggered.disconnect()
                except TypeError: pass
                try:
                    action.triggered.connect(slot_func)
                except Exception as e:
                    self.exibir_erro(f"Erro ao conectar ação '{action_name}': {e}")
            # else: # Aviso opcional
            #     print(f"Aviso: Tentativa de conectar ação '{action_name}' que não existe na UI.")

        # --- Conexões ---
        conectar_se_existir("actionNovo", self.novo_arquivo)
        conectar_se_existir("actionAbrir", self.abrir_arquivo)
        conectar_se_existir("actionSalvar", self.salvar_arquivo)
        conectar_se_existir("actionSalvarComo", self.salvar_como)
        conectar_se_existir("actionSair", self.close)
        conectar_se_existir("actionCortar", self.cortar_texto)
        conectar_se_existir("actionCopiar", self.copiar_texto) # Certifique-se que 'actionCopiar' existe no .ui
        conectar_se_existir("actionColar", self.colar_texto)
        conectar_se_existir("actionDesfazer", self.desfazer_texto)
        conectar_se_existir("actionRefazer", self.refazer_texto)
        conectar_se_existir("actionBuscar", self.buscar_texto_dialogo)
        conectar_se_existir("actionSubstituir", self.substituir_texto_dialogo)
        conectar_se_existir("actionNegrito", self.formatar_negrito)
        conectar_se_existir("actionItalico", self.formatar_italico)
        conectar_se_existir("actionSublinhado", self.formatar_sublinhado)
        conectar_se_existir("actionCor_do_Texto", self.mudar_cor_texto)
        conectar_se_existir("actionFonte", self.selecionar_fonte)
        conectar_se_existir("actionNovaAba", self.nova_aba)
        conectar_se_existir("actionMudarCores", self.mudar_paleta_cores)
        conectar_se_existir("actionCalendario", self.exibir_calendario)

        # --- Sinais do TabWidget ---
        if self.tabWidget:
            try: # Desconectar primeiro
                self.tabWidget.tabCloseRequested.disconnect()
                self.tabWidget.currentChanged.disconnect()
            except TypeError: pass
            self.tabWidget.tabCloseRequested.connect(self.fechar_aba)
            self.tabWidget.currentChanged.connect(self.atualizar_estado_aba)
        else:
            self.exibir_erro("Erro Crítico: tabWidget não inicializado, sinais não conectados.")


    # --- Slots de edição padrão (operam na aba atual) ---
    def _obter_editor_atual(self):
        """Retorna o QTextEdit da aba ativa, ou None."""
        if not self.tabWidget or self.tabWidget.count() == 0:
            return None
        widget_atual = self.tabWidget.currentWidget()
        if isinstance(widget_atual, QTextEdit):
            return widget_atual
        return None

    def cortar_texto(self):
        editor = self._obter_editor_atual()
        if editor: editor.cut()

    def copiar_texto(self):
        editor = self._obter_editor_atual()
        if editor: editor.copy()

    def colar_texto(self):
        editor = self._obter_editor_atual()
        if editor and editor.canPaste(): editor.paste()

    def desfazer_texto(self):
        editor = self._obter_editor_atual()
        if editor and editor.document().isUndoAvailable(): editor.undo()

    def refazer_texto(self):
        editor = self._obter_editor_atual()
        if editor and editor.document().isRedoAvailable(): editor.redo()

    # --- Slots de gerenciamento de abas e arquivos ---

    def atualizar_estado_aba(self, index):
        """Atualiza o estado da janela (título, ações) quando a aba muda"""
        # Chamado quando currentChanged é emitido
        # Atualiza as ações imediatamente ao mudar de aba
        QTimer.singleShot(0, self._atualizar_interface_aba_ativa) # Usa singleShot para garantir que ocorra após a mudança

    def _atualizar_interface_aba_ativa(self):
        """Lógica separada para atualizar a UI baseada na aba ativa."""
        editor_atual = self._obter_editor_atual()
        if editor_atual:
            arquivo_associado = editor_atual.property("arquivo_associado")
            nome_base = os.path.basename(arquivo_associado) if arquivo_associado else "Sem título"
            modificado = editor_atual.document().isModified()
            titulo_janela = f"Rabisco - {nome_base}{'*' if modificado else ''}"
            self.setWindowTitle(titulo_janela)
            # Assegura que o título da aba também esteja correto (pode ser redundante se _marcar_modificado funcionar bem)
            idx = self.tabWidget.currentIndex()
            if idx != -1:
                self.tabWidget.setTabText(idx, f"{nome_base}{'*' if modificado else ''}")

        else: # Nenhuma aba de editor ativa
             self.setWindowTitle("Rabisco")
             idx = self.tabWidget.currentIndex()
             if self.tabWidget and idx != -1:
                  self.tabWidget.setTabText(idx, "Inválido") # Ou manter o título existente?

        # Atualiza disponibilidade das ações independentemente de ser editor ou não
        self._atualizar_disponibilidade_acoes()


    def _atualizar_disponibilidade_acoes(self, habilitar_edicao=True):
        """Habilita/desabilita ações com base no estado da aba ativa."""
        # Pega o editor mesmo que habilitar_edicao seja False para verificar se existe
        editor = self._obter_editor_atual()
        tem_editor = editor is not None and habilitar_edicao
        tem_selecao = tem_editor and editor.textCursor().hasSelection()
        pode_colar = tem_editor and QApplication.clipboard().mimeData().hasText()
        pode_desfazer = tem_editor and editor.document().isUndoAvailable()
        pode_refazer = tem_editor and editor.document().isRedoAvailable()
        modificado = tem_editor and editor.document().isModified()

        def set_enabled(action_name, enabled):
            action = getattr(self, action_name, None)
            if action: action.setEnabled(enabled)

        set_enabled('actionSalvar', tem_editor and modificado)
        set_enabled('actionSalvarComo', tem_editor)
        set_enabled('actionCortar', tem_selecao)
        set_enabled('actionCopiar', tem_selecao) # Habilitar ação copiar
        set_enabled('actionColar', pode_colar)
        set_enabled('actionDesfazer', pode_desfazer)
        set_enabled('actionRefazer', pode_refazer)
        set_enabled('actionBuscar', tem_editor)
        set_enabled('actionSubstituir', tem_editor)
        set_enabled('actionNegrito', tem_editor)
        set_enabled('actionItalico', tem_editor)
        set_enabled('actionSublinhado', tem_editor)
        set_enabled('actionCor_do_Texto', tem_editor)
        set_enabled('actionFonte', tem_editor)

    def _atualizar_disponibilidade_acoes_timer(self):
        """Chamado pelo QTimer para atualizar ações que mudam com frequência (ex: Copiar, Desfazer)."""
        # Só atualiza se a janela estiver ativa para economizar recursos
        if self.isActiveWindow():
             self._atualizar_disponibilidade_acoes()


    def carregar_configuracoes(self):
        """Carrega as configurações salvas do aplicativo (Ex: tema)"""
        try:
            nome_tema_salvo = self.db.obter_configuracao('tema', 'Claro')
            self.aplicar_tema(nome_tema_salvo)
        except Exception as e:
            self.exibir_erro(f"Erro ao carregar configurações iniciais: {str(e)}")


    def novo_arquivo(self):
        """Cria uma nova aba em branco"""
        self.nova_aba()


    def nova_aba(self, caminho_arquivo=None, conteudo=""):
        """Adiciona uma nova aba ao tabWidget."""
        try:
            novo_editor = self.interface.criar_novo_editor()
            novo_editor.setPlainText(conteudo)
            novo_editor.setProperty("arquivo_associado", caminho_arquivo)
            novo_editor.document().setModified(False)

            # Conecta sinais específicos desta aba
            novo_editor.document().modificationChanged.connect(
                lambda modificado, editor=novo_editor: self._marcar_modificado(editor, modificado)
            )
            # Atualiza ações baseadas na seleção/cursor
            novo_editor.copyAvailable.connect(lambda available: getattr(self, 'actionCopiar', None) and self.actionCopiar.setEnabled(available))
            novo_editor.copyAvailable.connect(lambda available: getattr(self, 'actionCortar', None) and self.actionCortar.setEnabled(available))
            novo_editor.undoAvailable.connect(lambda available: getattr(self, 'actionDesfazer', None) and self.actionDesfazer.setEnabled(available))
            novo_editor.redoAvailable.connect(lambda available: getattr(self, 'actionRefazer', None) and self.actionRefazer.setEnabled(available))
            # Atualiza Colar baseado no clipboard (timer faz isso)


            nome_base = os.path.basename(caminho_arquivo) if caminho_arquivo else "Sem título"
            indice = self.tabWidget.addTab(novo_editor, nome_base)
            self.tabWidget.setCurrentIndex(indice) # Foca na nova aba

            return novo_editor
        except Exception as e:
            self.exibir_erro(f"Erro ao criar nova aba: {str(e)}")
            return None

    def _marcar_modificado(self, editor, modificado):
        """Slot para atualizar o título da aba e estado de Salvar quando o conteúdo muda."""
        index = -1
        if self.tabWidget:
            for i in range(self.tabWidget.count()):
                if self.tabWidget.widget(i) == editor:
                    index = i
                    break

        if index != -1:
             arquivo_associado = editor.property("arquivo_associado")
             nome_base = os.path.basename(arquivo_associado) if arquivo_associado else "Sem título"
             titulo_aba = f"{nome_base}{'*' if modificado else ''}"
             self.tabWidget.setTabText(index, titulo_aba)
             # Atualiza título da janela se for a aba ativa
             if self.tabWidget.currentIndex() == index:
                  self.setWindowTitle(f"Rabisco - {titulo_aba}")
             # Atualiza disponibilidade da ação Salvar
             if hasattr(self, 'actionSalvar'):
                  self.actionSalvar.setEnabled(modificado)


    def abrir_arquivo(self):
        """Abre um arquivo existente em uma nova aba"""
        try:
            ultimo_diretorio = self.db.obter_configuracao("ultimo_diretorio_aberto", "")
            nome_arquivo, _ = QFileDialog.getOpenFileName(
                self, "Abrir Arquivo", ultimo_diretorio,
                "Arquivos de Texto (*.txt);;Todos os Arquivos (*)"
            )

            if nome_arquivo:
                self.db.salvar_configuracao("ultimo_diretorio_aberto", os.path.dirname(nome_arquivo))

                for i in range(self.tabWidget.count()):
                     widget_aba = self.tabWidget.widget(i)
                     if isinstance(widget_aba, QTextEdit):
                          arquivo_aba_atual = widget_aba.property("arquivo_associado")
                          if arquivo_aba_atual and os.path.abspath(arquivo_aba_atual) == os.path.abspath(nome_arquivo):
                               self.tabWidget.setCurrentIndex(i)
                               self.statusbar.showMessage(f"Arquivo '{os.path.basename(nome_arquivo)}' já está aberto.", 3000)
                               return

                try:
                    conteudo = self.gerenciador.ler_arquivo(nome_arquivo)
                except Exception as e:
                    self.exibir_erro(f"Erro ao ler o arquivo '{os.path.basename(nome_arquivo)}':\n{str(e)}")
                    return

                editor_novo = self.nova_aba(caminho_arquivo=nome_arquivo, conteudo=conteudo)
                if editor_novo:
                    self.statusbar.showMessage(f"Arquivo '{os.path.basename(nome_arquivo)}' aberto.", 3000)
                else:
                    self.exibir_erro(f"Falha ao criar aba para '{os.path.basename(nome_arquivo)}'.")

        except Exception as e:
            self.exibir_erro(f"Erro inesperado ao abrir arquivo: {str(e)}")


    def salvar_arquivo(self):
        """Salva o conteúdo da aba ativa. Chama salvar_como se for um arquivo novo."""
        editor_atual = self._obter_editor_atual()
        if not editor_atual:
            self.statusbar.showMessage("Nenhuma aba de edição ativa.", 1500)
            return False

        caminho_salvar = editor_atual.property("arquivo_associado")
        if caminho_salvar is None:
            return self.salvar_como()
        else:
            try:
                conteudo = editor_atual.toPlainText()
                resultado = self.gerenciador.salvar_arquivo(caminho_salvar, conteudo)
                if resultado:
                    editor_atual.document().setModified(False)
                    self._marcar_modificado(editor_atual, False) # Atualiza título e ação Salvar
                    self.statusbar.showMessage(f"Arquivo salvo: {os.path.basename(caminho_salvar)}", 2000)
                    return True
                else:
                    self.exibir_erro(f"Falha desconhecida ao salvar '{os.path.basename(caminho_salvar)}'.")
                    return False
            except PermissionError:
                 self.exibir_erro(f"Permissão negada para salvar '{os.path.basename(caminho_salvar)}'.")
                 return False
            except Exception as e:
                self.exibir_erro(f"Erro ao salvar '{os.path.basename(caminho_salvar)}': {str(e)}")
                return False


    def salvar_como(self):
        """Salva o arquivo da aba ativa com um novo nome/local."""
        editor_atual = self._obter_editor_atual()
        if not editor_atual:
             self.statusbar.showMessage("Nenhuma aba de edição ativa.", 1500)
             return False

        caminho_atual = editor_atual.property("arquivo_associado")
        diretorio_sugerido = os.path.dirname(caminho_atual) if caminho_atual else self.db.obter_configuracao("ultimo_diretorio_salvo", "")
        nome_sugerido = os.path.basename(caminho_atual) if caminho_atual else "Sem título.txt"
        caminho_sugestao = os.path.join(diretorio_sugerido, nome_sugerido)

        nome_arquivo, _ = QFileDialog.getSaveFileName(
            self, "Salvar Como", caminho_sugestao,
            "Arquivos de Texto (*.txt);;Todos os Arquivos (*)"
        )

        if not nome_arquivo: return False # Cancelado

        self.db.salvar_configuracao("ultimo_diretorio_salvo", os.path.dirname(nome_arquivo))
        conteudo = editor_atual.toPlainText()
        try:
            resultado = self.gerenciador.salvar_arquivo(nome_arquivo, conteudo)
            if resultado:
                editor_atual.setProperty("arquivo_associado", nome_arquivo)
                editor_atual.document().setModified(False)
                self._marcar_modificado(editor_atual, False) # Atualiza título e ação Salvar
                self.statusbar.showMessage(f"Salvo como: {os.path.basename(nome_arquivo)}", 2000)
                return True
            else:
                self.exibir_erro(f"Falha desconhecida ao salvar como '{os.path.basename(nome_arquivo)}'.")
                return False
        except PermissionError:
             self.exibir_erro(f"Permissão negada para salvar '{os.path.basename(nome_arquivo)}'.")
             return False
        except Exception as e:
             self.exibir_erro(f"Erro ao salvar como '{os.path.basename(nome_arquivo)}': {str(e)}")
             return False


    def fechar_aba(self, indice):
        """Fecha a aba no índice especificado, perguntando se deseja salvar."""
        if not self.tabWidget or indice < 0 or indice >= self.tabWidget.count(): return
        editor = self.tabWidget.widget(indice)

        if isinstance(editor, QTextEdit) and editor.document().isModified():
            nome_arquivo = editor.property("arquivo_associado")
            nome_base = os.path.basename(nome_arquivo) if nome_arquivo else "Sem título"
            tab_text = f"{nome_base}*"

            resposta = QMessageBox.question(
                self, "Salvar Alterações?",
                f"Salvar alterações em '{tab_text}'?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if resposta == QMessageBox.Save:
                self.tabWidget.setCurrentIndex(indice) # Foca para salvar
                if not self.salvar_arquivo(): return # Não fecha se salvar falhar/cancelar
            elif resposta == QMessageBox.Cancel:
                return # Não fecha

        # Desconectar sinais antes de remover
        if isinstance(editor, QTextEdit):
            try: editor.document().modificationChanged.disconnect()
            except TypeError: pass
            try: editor.copyAvailable.disconnect()
            except TypeError: pass
            try: editor.undoAvailable.disconnect()
            except TypeError: pass
            try: editor.redoAvailable.disconnect()
            except TypeError: pass

        self.tabWidget.removeTab(indice)
        if self.tabWidget.count() == 0: self._atualizar_interface_aba_ativa()


    # --- Slots de formatação ---
    def formatar_negrito(self):
        editor = self._obter_editor_atual()
        if editor: self.interface.aplicar_negrito(editor)

    def formatar_italico(self):
        editor = self._obter_editor_atual()
        if editor: self.interface.aplicar_italico(editor)

    def formatar_sublinhado(self):
        editor = self._obter_editor_atual()
        if editor: self.interface.aplicar_sublinhado(editor)

    def mudar_cor_texto(self):
        editor = self._obter_editor_atual()
        if editor:
            cor_atual = editor.currentCharFormat().foreground().color()
            cor = QColorDialog.getColor(cor_atual, self, "Cor do Texto")
            if cor.isValid(): self.interface.aplicar_cor_texto(editor, cor)

    def selecionar_fonte(self):
         editor = self._obter_editor_atual()
         if editor:
              fonte_atual = editor.currentCharFormat().font()
              ok, fonte_nova = QFontDialog.getFont(fonte_atual, self, "Selecionar Fonte")
              if ok: self.interface.aplicar_fonte(editor, fonte_nova)


    # --- Slots diversos ---
    def buscar_texto_dialogo(self):
        editor = self._obter_editor_atual()
        if not editor: return
        # Assume que tela.py tem dialogo_busca_avancado
        texto_buscar, case_sensitive, direcao = self.interface.dialogo_busca_avancado(parent=self)
        if texto_buscar:
            opcoes = QTextDocument.FindFlags()
            if case_sensitive: opcoes |= QTextDocument.FindCaseSensitively
            if not direcao: opcoes |= QTextDocument.FindBackward
            encontrado = editor.find(texto_buscar, opcoes)
            if not encontrado: # Tenta do início/fim
                cursor = editor.textCursor()
                cursor.movePosition(QTextCursor.Start if direcao else QTextCursor.End)
                editor.setTextCursor(cursor)
                encontrado = editor.find(texto_buscar, opcoes)
                if not encontrado: QMessageBox.information(self, "Buscar", f"'{texto_buscar}' não encontrado.")

    def substituir_texto_dialogo(self):
         editor = self._obter_editor_atual()
         if not editor: return
         # Assume que tela.py tem dialogo_substituir_avancado
         texto_buscar, texto_substituir, case_sensitive, tudo = self.interface.dialogo_substituir_avancado(parent=self)
         if texto_buscar is not None and texto_substituir is not None:
              opcoes = QTextDocument.FindFlags()
              if case_sensitive: opcoes |= QTextDocument.FindCaseSensitively
              contador = self.interface.substituir_texto_avancado(editor, texto_buscar, texto_substituir, opcoes, tudo)
              if tudo: QMessageBox.information(self, "Substituir Tudo", f"{contador} ocorrência(s) substituída(s).")
              # Se não for 'tudo', a lógica de perguntar fica em substituir_texto_avancado

    def mudar_paleta_cores(self):
        """Muda a paleta de cores (tema) e salva a preferência"""
        try:
            temas = {
                "Claro": {"background": "#FFFFFF", "text": "#000000", "highlight": "#D3D3D3", "widget_bg": "#FFFFFF", "button": "#F0F0F0", "border": "#C0C0C0", "selection_text": "#000000", "tab_sel_bg": "#FFFFFF"},
                "Escuro": {"background": "#2D2D30", "text": "#F0F0F0", "highlight": "#007ACC", "widget_bg": "#3C3C3C", "button": "#555555", "border": "#606060", "selection_text": "#FFFFFF", "tab_sel_bg": "#3C3C3C"},
            }
            tema_atual_nome = self.property("tema_atual") or "Claro"
            lista_temas = list(temas.keys())
            try: indice_atual = lista_temas.index(tema_atual_nome)
            except ValueError: indice_atual = 0
            proximo_indice = (indice_atual + 1) % len(lista_temas)
            proximo_tema_nome = lista_temas[proximo_indice]
            self.aplicar_tema(proximo_tema_nome)
            self.db.salvar_configuracao("tema", proximo_tema_nome)
            self.statusbar.showMessage(f"Tema: {proximo_tema_nome}", 2000)
        except Exception as e:
            self.exibir_erro(f"Erro ao mudar paleta: {str(e)}")


    def aplicar_tema(self, nome_tema):
        """Aplica o tema especificado à interface"""
        try:
            temas = { # Manter consistente
                 "Claro": {"background": "#FFFFFF", "text": "#000000", "highlight": "#D3D3D3", "widget_bg": "#FFFFFF", "button": "#F0F0F0", "border": "#C0C0C0", "selection_text": "#000000", "tab_sel_bg": "#FFFFFF"},
                 "Escuro": {"background": "#2D2D30", "text": "#F0F0F0", "highlight": "#007ACC", "widget_bg": "#3C3C3C", "button": "#555555", "border": "#606060", "selection_text": "#FFFFFF", "tab_sel_bg": "#3C3C3C"},
            }
            tema = temas.get(nome_tema, temas["Claro"])
            # Stylesheet (simplificado para brevidade, use o anterior se preferir mais detalhes)
            estilo = f"""
                QMainWindow, QDialog, QMessageBox {{ background-color: {tema['background']}; color: {tema['text']}; }}
                QWidget {{ color: {tema['text']}; border-color: {tema['border']}; }}
                QTextEdit {{ background-color: {tema['widget_bg']}; color: {tema['text']}; border: 1px solid {tema['border']}; selection-background-color: {tema['highlight']}; selection-color: {tema['selection_text']}; padding: 4px; }}
                QTabWidget::pane {{ border-top: 1px solid {tema['border']}; background-color: {tema['background']}; }}
                QTabBar::tab {{ background-color: {tema['button']}; color: {tema['text']}; border: 1px solid {tema['border']}; border-bottom: none; padding: 5px 10px; margin-right: 1px; border-top-left-radius: 4px; border-top-right-radius: 4px; }}
                QTabBar::tab:selected {{ background-color: {tema['tab_sel_bg']}; border-bottom: 1px solid {tema['tab_sel_bg']}; margin-bottom: -1px; }}
                QTabBar::tab:!selected:hover {{ background-color: {tema['highlight']}; }}
                QMenuBar, QMenu, QToolBar, QStatusBar {{ background-color: {tema['background']}; color: {tema['text']}; border: none; }}
                QMenu::item:selected {{ background-color: {tema['highlight']}; color: {tema['selection_text']}; }}
                QStatusBar QLabel {{ background-color: transparent; color: {tema['text']}; padding: 0 5px; }}
                QPushButton {{ background-color: {tema['button']}; color: {tema['text']}; border: 1px solid {tema['border']}; padding: 4px 12px; border-radius: 3px; min-width: 60px; }}
                QPushButton:hover {{ background-color: {tema['highlight']}; border-color: {tema['highlight']}; color: {tema['selection_text']}; }}
                QPushButton:disabled {{ background-color: {tema['border']}80; color: #808080; border-color: #808080; }}
                QLineEdit, QComboBox {{ background-color: {tema['widget_bg']}; color: {tema['text']}; border: 1px solid {tema['border']}; padding: 3px; selection-background-color: {tema['highlight']}; selection-color: {tema['selection_text']}; }}
                QLabel {{ background-color: transparent; }}
            """
            self.setStyleSheet(estilo)
            self.setProperty("tema_atual", nome_tema)
        except Exception as e:
            self.exibir_erro(f"Erro ao aplicar tema '{nome_tema}': {str(e)}")

    def exibir_calendario(self):
        """Exibe um calendário em um diálogo"""
        try:
            dialogo = QDialog(self)
            dialogo.setWindowTitle("Calendário")
            layout = QVBoxLayout(dialogo)
            calendario = QCalendarWidget(dialogo)
            calendario.setGridVisible(True)
            btn_inserir = QPushButton("Inserir Data", dialogo)
            btn_inserir.clicked.connect(lambda: self._inserir_data_calendario(calendario, dialogo))
            btn_ok = QPushButton("Fechar", dialogo)
            btn_ok.clicked.connect(dialogo.accept)
            layout.addWidget(calendario)
            layout.addWidget(btn_inserir)
            layout.addWidget(btn_ok)
            dialogo.setLayout(layout)
            dialogo.exec_()
        except Exception as e:
            self.exibir_erro(f"Erro ao exibir calendário: {str(e)}")

    def _inserir_data_calendario(self, calendario, dialogo):
        """Insere a data selecionada no calendário na aba ativa."""
        editor = self._obter_editor_atual()
        if editor:
             data_str = calendario.selectedDate().toString(Qt.ISODate)
             editor.insertPlainText(data_str)
             dialogo.accept()
        else:
             QMessageBox.warning(dialogo, "Aviso", "Nenhuma aba de edição ativa.")


    # --- Métodos de utilidade ---
    def exibir_erro(self, mensagem, titulo="Erro"):
        """Exibe uma mensagem de erro crítica."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensagem)
        msg_box.setStandardButtons(QMessageBox.Ok)
        # Tenta aplicar estilo básico
        try:
            if self.property("tema_atual") == "Escuro": msg_box.setStyleSheet("QWidget{color: #F0F0F0; background-color: #2D2D30;} QPushButton{color: #F0F0F0; background-color: #555555; border: 1px solid #606060;}")
            else: msg_box.setStyleSheet("QWidget{color: #000000; background-color: #FFFFFF;} QPushButton{color: #000000; background-color: #F0F0F0; border: 1px solid #C0C0C0;}")
        except: pass
        msg_box.exec_()

    def closeEvent(self, event):
        """Manipula o evento de fechar a janela."""
        abas_modificadas = []
        if self.tabWidget:
             for i in range(self.tabWidget.count()):
                  widget = self.tabWidget.widget(i)
                  if isinstance(widget, QTextEdit) and widget.document().isModified():
                       abas_modificadas.append(i)
        if not abas_modificadas:
             self._fechar_banco_dados()
             event.accept()
             return

        titulos = [f"'{os.path.basename(self.tabWidget.widget(i).property('arquivo_associado') or 'Sem título')}*'" for i in abas_modificadas]
        resposta = QMessageBox.warning(self, "Sair?", f"Salvar alterações?\n{', '.join(titulos)}",
                                     QMessageBox.SaveAll | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
        if resposta == QMessageBox.SaveAll:
            salvo = all(self.tabWidget.setCurrentIndex(i) or self.salvar_arquivo() for i in abas_modificadas)
            if salvo: self._fechar_banco_dados(); event.accept()
            else: QMessageBox.information(self, "Falha", "Não foi possível salvar. Fechamento cancelado."); event.ignore()
        elif resposta == QMessageBox.Discard: self._fechar_banco_dados(); event.accept()
        else: event.ignore()

    def _fechar_banco_dados(self):
         """Fecha a conexão com o BD."""
         print("Fechando BD...")
         try:
              if hasattr(self, 'db') and self.db: self.db.close(); print("BD fechado.")
         except Exception as e: print(f"Erro ao fechar BD: {e}")


# --- Bloco principal ---
if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Rabisco")
    app.setOrganizationName("DaniloDevSys")
    app.setStyle("Fusion")
    main_window = RabiscoApp()
    main_window.show()
    sys.exit(app.exec_())