# 📝 Rabisco - Editor de Texto

![Logo Rabisco](assets/icons/logo_rabisco.ico)

## 📋 Descrição

**Rabisco** é um editor de texto leve, intuitivo e completo desenvolvido em Python com PyQt5. Combinando a simplicidade de um bloco de notas com recursos avançados de formatação e personalização, o Rabisco é ideal para anotações rápidas, edição de documentos e desenvolvimento de textos.

## ✨ Características Principais

### 📂 Gerenciamento de Arquivos
- Sistema de múltiplas abas para trabalhar com vários documentos
- Operações completas: criar, abrir, salvar e imprimir
- Salvamento automático do estado das abas
- Alertas de segurança para documentos não salvos

### ✏️ Edição Avançada
- Recursos completos de edição: cortar, copiar, colar
- Sistema robusto de desfazer/refazer
- Localização e substituição de texto
- Suporte a formatação rica (RTF)

### 🎨 Formatação Completa
- Formatação básica: negrito, itálico, sublinhado, tachado
- Listas com marcadores
- Controle de alinhamento de texto
- Coloração de texto personalizada
- Ajuste dinâmico de tamanho de fonte

### 🛠️ Ferramentas Integradas
- Calculadora embutida
- Calendário para inserção de datas
- Temas claro e escuro
- Personalização de cores de fundo

## 📊 Estatísticas do Projeto

```
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          14            946           1363           2969
XML (Qt/GTK)                     4              0              0            949
Markdown                         2             66              0            196
DOS Batch                        3             19             14             93
JSON                             1              0              0              5
Text                             1              0              0              2
-------------------------------------------------------------------------------
SUM:                            25           1031           1377           4214
-------------------------------------------------------------------------------
```

## 🖥️ Requisitos de Sistema

- **Python**: 3.6 ou superior
- **PyQt5**: Interface gráfica
- **Dependências**: Veja `requirements.txt` para a lista completa

## 📥 Instalação

### Método 1: A partir do executável
1. Baixe o arquivo executável da seção [Releases](https://github.com/danilodevsys/Rabisco---Bloco-de-Notas/releases)
2. Execute `Rabisco.exe` diretamente - não é necessária instalação

### Método 2: A partir do código-fonte
1. Clone o repositório:
   ```
   git clone https://github.com/danilodevsys/Rabisco---Bloco-de-Notas.git
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```
   python main.py
   ```

## 🔨 Compilação

Para criar um executável do Rabisco:

1. Certifique-se de que o PyInstaller está instalado:
   ```
   pip install pyinstaller
   ```
2. Execute o script de compilação:
   ```
   build.bat
   ```
3. O executável será gerado na pasta `dist/Rabisco/`

## 📁 Estrutura do Projeto

```
Rabisco/
├── assets/
│   └── icons/           # Ícones e recursos visuais
├── src/
│   ├── tela.ui          # Interface gráfica principal
│   ├── sobre.ui         # Janela "Sobre"
│   ├── rabisco_app.py   # Classe principal da aplicação
│   ├── rabisco_funcoes.py # Implementação das funcionalidades 
│   └── editor_texto.py  # Classe de gerenciamento do editor
├── main.py              # Ponto de entrada da aplicação
├── build.bat            # Script para criar executável
└── requirements.txt     # Dependências do projeto
```

## ⌨️ Atalhos de Teclado

| Ação | Atalho |
|------|--------|
| Novo documento | <kbd>Ctrl</kbd>+<kbd>N</kbd> |
| Abrir arquivo | <kbd>Ctrl</kbd>+<kbd>O</kbd> |
| Salvar | <kbd>Ctrl</kbd>+<kbd>S</kbd> |
| Salvar como | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>S</kbd> |
| Imprimir | <kbd>Ctrl</kbd>+<kbd>P</kbd> |
| Desfazer | <kbd>Ctrl</kbd>+<kbd>Z</kbd> |
| Refazer | <kbd>Ctrl</kbd>+<kbd>Y</kbd> |
| Recortar | <kbd>Ctrl</kbd>+<kbd>X</kbd> |
| Copiar | <kbd>Ctrl</kbd>+<kbd>C</kbd> |
| Colar | <kbd>Ctrl</kbd>+<kbd>V</kbd> |
| Localizar | <kbd>Ctrl</kbd>+<kbd>F</kbd> |
| Negrito | <kbd>Ctrl</kbd>+<kbd>B</kbd> |
| Itálico | <kbd>Ctrl</kbd>+<kbd>I</kbd> |
| Sublinhado | <kbd>Ctrl</kbd>+<kbd>U</kbd> |
| Tachado | <kbd>Ctrl</kbd>+<kbd>T</kbd> |
| Lista | <kbd>Ctrl</kbd>+<kbd>L</kbd> |
| Formatação | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd> |
| Sobre | <kbd>F1</kbd> |
| Ajuda | <kbd>Shift</kbd>+<kbd>F1</kbd> |

## 📘 Guia de Uso

Um manual completo do usuário está disponível em [MANUAL.md](./MANUAL.md) ou através do menu Ajuda dentro da aplicação.

## 👨‍💻 Sobre o Desenvolvedor

**Danilo (danilodevsys)** é estudante de programação e trabalha com tecnologia desde 2011. Atualmente, atua como Suporte N2 em sistema legado Delphi, utilizando seus conhecimentos e experiência para criar ferramentas úteis como o Rabisco.

- GitHub: [github.com/danilodevsys](https://github.com/danilodevsys)
- Repositório do projeto: [github.com/danilodevsys/Rabisco---Bloco-de-Notas](https://github.com/danilodevsys/Rabisco---Bloco-de-Notas)

## 🤝 Contribuições

Contribuições são sempre bem-vindas! Sinta-se à vontade para:

1. Abrir issues reportando bugs ou sugerindo novos recursos
2. Enviar pull requests com melhorias ou correções
3. Melhorar a documentação ou traduções

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

<p align="center">
  <b>Rabisco</b> - Desenvolvido com ❤️ por <a href="https://github.com/danilodevsys">danilodevsys</a>
</p>