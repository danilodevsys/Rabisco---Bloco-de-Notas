import os
import json

CAMINHO_CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config_rabisco.json')

DEFAULT_CONFIG = {
    'tema_escuro': False,
    'cor_fundo': '#ffffff',
    'tamanho_fonte': 12
}

def carregar_configuracoes():
    if not os.path.exists(CAMINHO_CONFIG):
        return DEFAULT_CONFIG.copy()
    try:
        with open(CAMINHO_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        for chave in DEFAULT_CONFIG:
            if chave not in config:
                config[chave] = DEFAULT_CONFIG[chave]
        return config
    except Exception:
        return DEFAULT_CONFIG.copy()

def salvar_configuracoes(config):
    try:
        with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Erro ao salvar configurações: {e}')
