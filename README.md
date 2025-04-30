# Rabisco - Editor de Texto

![Rabisco Logo](assets/icons/logo_rabisco.ico)

## Descrição

Rabisco é um editor de texto simples e prático desenvolvido em Python com PyQt5. Ele oferece funcionalidades essenciais de edição de texto com uma interface amigável e intuitiva, ideal para anotações rápidas e documentos simples.

## Funcionalidades

### Arquivo
- Criar, abrir, salvar e imprimir documentos
- Suporte a múltiplas abas
- Fechamento seguro com alerta para documentos não salvos

### Edição
- Operações básicas: cortar, copiar, colar
- Desfazer e refazer alterações
- Localizar e substituir texto

### Formatação
- Formatação de texto: negrito, itálico, sublinhado, tachado
- Listas com marcadores
- Alinhamento de texto (esquerda, centro, direita, justificado)
- Alteração de cor do texto
- Aumentar e diminuir tamanho da fonte

### Ferramentas
- Calculadora integrada
- Calendário para inserção de datas
- Personalização de cores de fundo
- Alternância entre temas claro e escuro

## Requisitos

- Python 3.6 ou superior
- PyQt5
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório ou baixe os arquivos fonte
2. Instale as dependências:
```
pip install -r requirements.txt
```
3. Execute o aplicativo:
```
python main.py
```

## Criando um Executável

Para criar um executável do Rabisco, use o script `build.bat` incluído no projeto:

1. Certifique-se de que o PyInstaller está instalado
2. Execute o arquivo `build.bat`
3. O executável será criado na pasta `dist/Rabisco`

## Estrutura do Projeto

```
Rabisco/
├── assets/
│   └── icons/         # Ícones e recursos visuais
├── src/
│   ├── tela.ui        # Interface gráfica principal
│   ├── sobre.ui       # Interface da janela Sobre
│   ├── rabisco_app.py # Classe principal do aplicativo
│   ├── rabisco_funcoes.py # Implementação das funcionalidades
│   └── editor_texto.py # Classe de gerenciamento do editor
├── main.py            # Ponto de entrada do aplicativo
├── build.bat          # Script para criar executável
└── requirements.txt   # Dependências do projeto
```

## Atalhos de Teclado

- **Ctrl+N**: Novo documento
- **Ctrl+O**: Abrir arquivo
- **Ctrl+S**: Salvar
- **Ctrl+Shift+S**: Salvar como
- **Ctrl+P**: Imprimir
- **Ctrl+Z**: Desfazer
- **Ctrl+Y**: Refazer
- **Ctrl+X**: Recortar
- **Ctrl+C**: Copiar
- **Ctrl+V**: Colar
- **Ctrl+F**: Localizar
- **Ctrl+B**: Negrito
- **Ctrl+I**: Itálico
- **Ctrl+U**: Sublinhado
- **Ctrl+T**: Tachado
- **Ctrl+L**: Lista
- **Ctrl+Shift+F**: Formatação
- **F1**: Sobre
- **Shift+F1**: Ajuda

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

Danilo (danilodevsys)

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
