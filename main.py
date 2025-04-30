#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Rabisco - Um simples bloco de notas
Arquivo principal para inicialização da aplicação

Versão: 1.0.0.1
Autor: Danilo (danilodevsys)
'''

import os
import sys
from PyQt5.QtWidgets import QApplication
from src.rabisco_app import RabiscoApp
from src.splash import RabiscoSplashScreen

# --- Constantes do Sistema ---
# VERSAO: Versão atual do aplicativo
VERSAO = '1.0.0.1'
# AUTOR: Nome do autor do aplicativo
AUTOR = 'Danilo (danilodevsys)'

def iniciar_aplicacao():
    '''Inicia a aplicação Rabisco'''
    # Verificar se a instância do QApplication já existe
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Configurar informações da aplicação
    app.setApplicationName('Rabisco')
    app.setOrganizationName('DaniloDevSys')
    app.setStyle('Fusion')
    
    # Exibir splash screen
    splash = RabiscoSplashScreen()
    splash.show()
    app.processEvents()

    # Criar e mostrar a janela principal
    janela_principal = RabiscoApp()
    janela_principal.mostrar_versao_rodape()
    janela_principal.show()
    splash.finish(janela_principal)

    # Executar o loop de eventos
    return app.exec_()

if __name__ == '__main__':
    sys.exit(iniciar_aplicacao())
