# 📚 Manual do Usuário - Rabisco

![Logo Rabisco](assets/icons/logo_rabisco.ico)

## 📖 Índice
- [Introdução](#-introdução)
- [Instalação](#-instalação)
- [Interface do Usuário](#-interface-do-usuário)
- [Gerenciamento de Arquivos](#-gerenciamento-de-arquivos)
- [Edição de Texto](#-edição-de-texto)
- [Formatação](#-formatação)
- [Ferramentas](#-ferramentas)
- [Personalização](#-personalização)
- [Atalhos de Teclado](#-atalhos-de-teclado)
- [Dicas e Truques](#-dicas-e-truques)
- [Solução de Problemas](#-solução-de-problemas)
- [Suporte e Contato](#-suporte-e-contato)

## 👋 Introdução

Bem-vindo ao **Rabisco**, um editor de texto leve, intuitivo e repleto de funcionalidades desenvolvido para facilitar a criação e edição de documentos de texto. Este manual fornece instruções detalhadas sobre como utilizar todas as funcionalidades do aplicativo de forma eficiente.

O Rabisco foi projetado para combinar a simplicidade de um bloco de notas tradicional com recursos avançados de formatação e personalização, tornando-o ideal para anotações rápidas, edição de documentos e desenvolvimento de textos com formatação rica.

## 🔧 Instalação

### Método 1: A partir do executável
1. Baixe o arquivo `Rabisco.exe` da seção de releases do repositório
2. Execute o arquivo - o aplicativo é portátil e não requer instalação
3. Para criar um atalho na área de trabalho, clique com o botão direito no executável e selecione "Enviar para > Área de trabalho"

### Método 2: A partir do código-fonte
1. Certifique-se de ter o Python 3.6 ou superior instalado
   - Verifique com o comando: `python --version`
2. Clone o repositório ou baixe os arquivos fonte
3. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```
4. Execute o aplicativo:
   ```
   python main.py
   ```

### Requisitos de Sistema
- **Sistema Operacional**: Windows 7/8/10/11
- **Processador**: Intel/AMD 1.0 GHz ou superior
- **Memória RAM**: 256 MB mínimo (512 MB recomendado)
- **Espaço em Disco**: 50 MB disponíveis
- **Python**: 3.6 ou superior (se executando a partir do código-fonte)
- **Resolução de Tela**: 1024x768 ou superior

## 🖥️ Interface do Usuário

A interface do Rabisco foi projetada para ser intuitiva e acessível, mantendo todos os recursos importantes a apenas alguns cliques de distância.

### Componentes Principais

![Interface do Rabisco](assets/images/interface.png)

1. **Barra de Título**: Exibe o nome do arquivo atual e os controles da janela
2. **Barra de Menu**: Acesso a todas as funcionalidades organizadas em categorias
3. **Barra de Ferramentas**: Ícones para operações frequentes
4. **Sistema de Abas**: Permite trabalhar com múltiplos documentos
5. **Área de Edição**: Onde o texto é digitado e editado
6. **Barra de Status**: Exibe informações como contagem de palavras e versão do aplicativo

### Barra de Menu

- **Arquivo**: Operações relacionadas a arquivos (Novo, Abrir, Salvar, Imprimir)
- **Editar**: Ferramentas de edição (Copiar, Colar, Desfazer, Localizar)
- **Formatar**: Opções de formatação de texto
- **Ferramentas**: Recursos adicionais (Calculadora, Calendário, Temas)
- **Ajuda**: Suporte e informações sobre o programa

## 📂 Gerenciamento de Arquivos

### Criando um Novo Documento
1. Clique em **Arquivo > Novo** no menu principal
2. Ou use o atalho **Ctrl+N**
3. Ou clique no botão **+** na barra de abas

Um novo documento em branco será aberto em uma nova aba.

### Abrindo um Arquivo Existente
1. Clique em **Arquivo > Abrir** no menu principal
2. Ou use o atalho **Ctrl+O**
3. Na caixa de diálogo que aparece, navegue até a localização do arquivo
4. Selecione o arquivo desejado e clique em "Abrir"

O Rabisco suporta a abertura dos seguintes formatos:
- Arquivos de texto (.txt)
- Documentos de texto formatado (.rtf)
- Documentos HTML (.html, .htm)

### Salvando um Documento
1. Para salvar pela primeira vez:
   - Clique em **Arquivo > Salvar** ou use **Ctrl+S**
   - Digite um nome para o arquivo
   - Escolha o local e o formato para salvar
   - Clique em "Salvar"
2. Para salvar alterações em um arquivo existente:
   - Clique em **Arquivo > Salvar** ou use **Ctrl+S**

### Salvando com Outro Nome
1. Clique em **Arquivo > Salvar Como** ou use **Ctrl+Shift+S**
2. Escolha um novo nome, local ou formato para o arquivo
3. Clique em "Salvar"

### Imprimindo um Documento
1. Clique em **Arquivo > Imprimir** ou use **Ctrl+P**
2. Na caixa de diálogo de impressão:
   - Selecione a impressora
   - Ajuste as configurações de impressão (intervalo, orientação, etc.)
   - Clique em "Imprimir"

### Pré-visualização de Impressão
1. Clique em **Arquivo > Visualizar Impressão**
2. Use os controles para navegar entre as páginas e ajustar a visualização
3. Clique em "Imprimir" para prosseguir ou "Fechar" para cancelar

### Trabalhando com Múltiplas Abas
- **Alternar entre documentos**: Clique na aba correspondente
- **Fechar uma aba**: Clique no X na aba ou use **Ctrl+W**
- **Reorganizar abas**: Arraste e solte para reposicionar
- **Mover para a próxima aba**: Use **Ctrl+Tab**
- **Mover para a aba anterior**: Use **Ctrl+Shift+Tab**

## ✏️ Edição de Texto

### Operações Básicas
- **Selecionar texto**: Clique e arraste sobre o texto desejado
- **Selecionar tudo**: Use **Ctrl+A**
- **Selecionar palavra**: Clique duas vezes na palavra
- **Selecionar parágrafo**: Clique três vezes no parágrafo

### Funções de Edição
- **Recortar**: Selecione o texto e use **Ctrl+X** ou **Editar > Recortar**
- **Copiar**: Selecione o texto e use **Ctrl+C** ou **Editar > Copiar**
- **Colar**: Posicione o cursor e use **Ctrl+V** ou **Editar > Colar**
- **Colar sem formatação**: Use **Ctrl+Shift+V**
- **Desfazer**: Use **Ctrl+Z** para reverter a última ação
- **Refazer**: Use **Ctrl+Y** para replicar a última ação desfeita

### Localizar e Substituir
1. Use **Ctrl+F** ou **Editar > Localizar** para abrir o painel de busca
2. Digite o texto que deseja localizar
3. Use as opções:
   - **Diferenciar maiúsculas/minúsculas**: Faz a busca considerar a capitalização exata
   - **Apenas palavras inteiras**: Localiza apenas ocorrências isoladas
   - **Usar expressão regular**: Permite busca avançada com padrões
4. Para substituir texto:
   - Clique em "Substituir" para expandir o painel
   - Digite o texto de substituição
   - Clique em "Substituir" para trocar a ocorrência atual
   - Clique em "Substituir Tudo" para trocar todas as ocorrências

## 🎨 Formatação

### Formatação de Caracteres
- **Negrito**: Selecione o texto e use **Ctrl+B** ou o botão **B** na barra de ferramentas
- **Itálico**: Selecione o texto e use **Ctrl+I** ou o botão *I* na barra de ferramentas
- **Sublinhado**: Selecione o texto e use **Ctrl+U** ou o botão correspondente
- **Tachado**: Selecione o texto e use **Ctrl+T** ou o botão correspondente
- **Sobrescrito**: Selecione o texto e use **Formatar > Sobrescrito**
- **Subscrito**: Selecione o texto e use **Formatar > Subscrito**

### Cor e Aparência
- **Cor do Texto**: Selecione o texto e clique em **Formatar > Cor do Texto**
- **Destacar Texto**: Selecione o texto e use **Formatar > Cor de Destaque**
- **Tamanho da Fonte**:
  - Aumentar: Use **Ctrl++** (tecla mais)
  - Diminuir: Use **Ctrl+-** (tecla menos)
  - Definir tamanho específico: Use **Formatar > Tamanho da Fonte**
- **Fonte**: Selecione **Formatar > Fonte** e escolha a família de fontes desejada

### Formatação de Parágrafos
- **Alinhamento**:
  - Esquerda: Use **Ctrl+L** ou o botão correspondente
  - Centro: Use **Ctrl+E** ou o botão correspondente
  - Direita: Use **Ctrl+R** ou o botão correspondente
  - Justificado: Use **Ctrl+J** ou o botão correspondente
- **Espaçamento de Linha**: Use **Formatar > Espaçamento de Linha**
- **Listas com Marcadores**: Posicione o cursor e use **Ctrl+Shift+L** ou **Formatar > Lista**
- **Recuo**:
  - Aumentar: Use **Tab** ou **Formatar > Aumentar Recuo**
  - Diminuir: Use **Shift+Tab** ou **Formatar > Diminuir Recuo**

### Estilos
- **Aplicar Estilo Predefinido**: Selecione **Formatar > Estilos** e escolha o estilo
- **Limpar Formatação**: Selecione o texto e use **Formatar > Limpar Formatação**

## 🛠️ Ferramentas

### Calculadora
1. Clique em **Ferramentas > Calculadora**
2. A calculadora do sistema será aberta em uma janela separada
3. Realize os cálculos necessários
4. Os resultados podem ser copiados e colados no documento

### Calendário
1. Clique em **Ferramentas > Calendário**
2. Navegue até o mês e ano desejados
3. Clique em uma data para selecioná-la
4. Clique em "Inserir Data" para adicionar a data formatada no cursor atual

### Contagem de Palavras
1. Para visualizar estatísticas do documento atual:
   - Clique em **Ferramentas > Contagem de Palavras**
   - Ou veja informações básicas na barra de status
2. Serão exibidas informações como:
   - Total de caracteres (com e sem espaços)
   - Número de palavras
   - Número de linhas e parágrafos

### Verificação Ortográfica
1. Para verificar a ortografia do documento:
   - Clique em **Ferramentas > Verificar Ortografia** ou use **F7**
2. O texto com possíveis erros será destacado
3. Para cada palavra detectada, você pode:
   - Selecionar uma sugestão de correção
   - Ignorar uma vez ou ignorar todas
   - Adicionar ao dicionário personalizado

## 🎭 Personalização

### Temas de Interface
1. Clique em **Ferramentas > Mudar Tema**
2. Escolha entre:
   - **Tema Claro**: Interface clara, ideal para ambientes bem iluminados
   - **Tema Escuro**: Reduz a fadiga ocular em ambientes com pouca luz

### Cores de Fundo
1. Clique em **Ferramentas > Mudar Cores**
2. Selecione uma das cores predefinidas ou escolha "Personalizada"
3. No seletor de cores, escolha a tonalidade desejada para o fundo do editor

### Configurações do Aplicativo
1. Clique em **Ferramentas > Opções**
2. Na janela de configurações, você pode personalizar:
   - **Geral**: Comportamento de inicialização, salvamento automático
   - **Editor**: Quebra de linha, indentação, tabulação
   - **Fonte**: Fonte padrão, tamanho e estilo
   - **Cores**: Esquemas de cores personalizados
   - **Atalhos**: Personalizar atalhos de teclado

## ⌨️ Atalhos de Teclado

### Arquivo
| Ação | Atalho |
|------|--------|
| Novo documento | <kbd>Ctrl</kbd>+<kbd>N</kbd> |
| Abrir arquivo | <kbd>Ctrl</kbd>+<kbd>O</kbd> |
| Salvar | <kbd>Ctrl</kbd>+<kbd>S</kbd> |
| Salvar como | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>S</kbd> |
| Imprimir | <kbd>Ctrl</kbd>+<kbd>P</kbd> |
| Fechar aba atual | <kbd>Ctrl</kbd>+<kbd>W</kbd> |
| Sair | <kbd>Alt</kbd>+<kbd>F4</kbd> |

### Edição
| Ação | Atalho |
|------|--------|
| Desfazer | <kbd>Ctrl</kbd>+<kbd>Z</kbd> |
| Refazer | <kbd>Ctrl</kbd>+<kbd>Y</kbd> |
| Recortar | <kbd>Ctrl</kbd>+<kbd>X</kbd> |
| Copiar | <kbd>Ctrl</kbd>+<kbd>C</kbd> |
| Colar | <kbd>Ctrl</kbd>+<kbd>V</kbd> |
| Selecionar tudo | <kbd>Ctrl</kbd>+<kbd>A</kbd> |
| Localizar | <kbd>Ctrl</kbd>+<kbd>F</kbd> |
| Substituir | <kbd>Ctrl</kbd>+<kbd>H</kbd> |
| Ir para linha | <kbd>Ctrl</kbd>+<kbd>G</kbd> |

### Formatação
| Ação | Atalho |
|------|--------|
| Negrito | <kbd>Ctrl</kbd>+<kbd>B</kbd> |
| Itálico | <kbd>Ctrl</kbd>+<kbd>I</kbd> |
| Sublinhado | <kbd>Ctrl</kbd>+<kbd>U</kbd> |
| Tachado | <kbd>Ctrl</kbd>+<kbd>T</kbd> |
| Aumentar tamanho da fonte | <kbd>Ctrl</kbd>+<kbd>+</kbd> |
| Diminuir tamanho da fonte | <kbd>Ctrl</kbd>+<kbd>-</kbd> |
| Alinhar à esquerda | <kbd>Ctrl</kbd>+<kbd>L</kbd> |
| Centralizar | <kbd>Ctrl</kbd>+<kbd>E</kbd> |
| Alinhar à direita | <kbd>Ctrl</kbd>+<kbd>R</kbd> |
| Justificar | <kbd>Ctrl</kbd>+<kbd>J</kbd> |
| Lista com marcadores | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>L</kbd> |

### Ferramentas e Visualização
| Ação | Atalho |
|------|--------|
| Verificar ortografia | <kbd>F7</kbd> |
| Contagem de palavras | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>W</kbd> |
| Modo de tela cheia | <kbd>F11</kbd> |
| Ampliar zoom | <kbd>Ctrl</kbd>+<kbd>Roda do mouse para cima</kbd> |
| Reduzir zoom | <kbd>Ctrl</kbd>+<kbd>Roda do mouse para baixo</kbd> |
| Sobre | <kbd>F1</kbd> |
| Ajuda | <kbd>Shift</kbd>+<kbd>F1</kbd> |

## 💡 Dicas e Truques

### Indicadores Visuais
- Um asterisco (*) junto ao nome do arquivo na aba indica que existem alterações não salvas
- A barra de status indica o número de palavras, a posição do cursor e o modo de edição atual

### Salvamento Automático
- O Rabisco pode salvar automaticamente seu trabalho a cada intervalo de tempo definido
- Configure esta função em **Ferramentas > Opções > Geral**

### Recursos Avançados
- **Arrastar e soltar**: Arraste arquivos diretamente para o Rabisco para abri-los
- **Listas numéricas**: Use **Formatar > Lista Numerada** para criar listas com numeração
- **Modo de foco**: Use **Visualizar > Modo de Foco** para uma experiência de escrita sem distrações
- **Histórico de arquivos recentes**: Acesse arquivos recentes em **Arquivo > Recentes**

### Plugins e Extensões
O Rabisco suporta extensão de funcionalidades através de plugins. Alguns plugins disponíveis:
- **Exportação para PDF**: Converte documentos para formato PDF
- **Verificação gramatical**: Análise gramatical avançada
- **Sincronização com nuvem**: Integração com serviços de armazenamento em nuvem

Para instalar plugins:
1. Baixe o plugin do repositório oficial
2. Coloque o arquivo na pasta "plugins" no diretório de instalação
3. Reinicie o Rabisco
4. Acesse **Ferramentas > Plugins** para configurar

## 🔧 Solução de Problemas

### O aplicativo não inicia
- **Solução 1**: Verifique se todas as dependências estão instaladas corretamente
- **Solução 2**: Execute como administrador
- **Solução 3**: Verifique se o Python está configurado corretamente no PATH (se usando o código-fonte)

### Arquivos não abrem corretamente
- **Solução 1**: Verifique se o formato do arquivo é suportado
- **Solução 2**: Certifique-se de que o arquivo não está corrompido
- **Solução 3**: Tente usar a opção "Arquivo > Abrir com Codificação" e selecione diferentes codificações

### Problemas ao salvar arquivos
- **Solução 1**: Verifique se você tem permissões de escrita no diretório
- **Solução 2**: Certifique-se de que o arquivo não está sendo usado por outro programa
- **Solução 3**: Tente "Salvar como" em uma localização diferente

### Lentidão ou travamentos
- **Solução 1**: Feche abas desnecessárias para liberar memória
- **Solução 2**: Reinicie o aplicativo
- **Solução 3**: Para documentos muito grandes, considere dividir em arquivos menores

### Problemas de formatação
- **Solução 1**: Para preservar toda a formatação, salve no formato RTF
- **Solução 2**: Alguns recursos de formatação podem não ser compatíveis com o formato TXT
- **Solução 3**: Use "Exportar como PDF" para preservar a formatação exata

## 📞 Suporte e Contato

### Recursos de Ajuda Integrados
- **Manual do Usuário**: Acessível pelo menu **Ajuda > Manual do Usuário**
- **Dicas Rápidas**: Passe o mouse sobre elementos da interface para ver dicas de uso
- **Tela de Boas-Vindas**: Exibe dicas e informações úteis no primeiro uso ou através de **Ajuda > Dicas**

### Contato com o Desenvolvedor
Se você tiver dúvidas, sugestões ou relatórios de bugs:
- **GitHub**: Abra uma issue em [github.com/danilodevsys/Rabisco---Bloco-de-Notas](https://github.com/danilodevsys/Rabisco---Bloco-de-Notas)
- **E-mail**: Entre em contato através do endereço disponível na página do GitHub
- **Redes Sociais**: Siga o desenvolvimento e contribua com ideias nas redes disponíveis na página do projeto

### Atualizações
- O Rabisco verifica automaticamente por atualizações ao iniciar (configurável nas opções)
- As atualizações podem ser verificadas manualmente em **Ajuda > Verificar Atualizações**
- O histórico de mudanças está disponível em **Ajuda > Notas de Versão**

---

<p align="center">
  <b>Rabisco</b> - Versão 1.0.0.1<br>
  Desenvolvido por <a href="https://github.com/danilodevsys">danilodevsys</a><br>
  Um editor de texto simples e prático com recursos avançados de edição
</p>