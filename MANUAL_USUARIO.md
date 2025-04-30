# Manual do Usuário - Rabisco

## Introdução

Bem-vindo ao **Rabisco**, um editor de texto simples e prático desenvolvido para facilitar a criação e edição de notas e documentos de texto. Este manual fornece instruções detalhadas sobre como utilizar todas as funcionalidades do aplicativo.

## Instalação

### A partir do código-fonte:
1. Certifique-se de ter o Python 3.6 ou superior instalado
2. Instale as dependências executando: `pip install -r requirements.txt`
3. Execute o aplicativo com: `python main.py`

### A partir do executável:
1. Execute o arquivo `Rabisco.exe` localizado na pasta de instalação
2. Não é necessário instalar - o aplicativo é portátil e pode ser executado de qualquer local

## Interface do Usuário

A interface do Rabisco é composta por:
- **Barra de Menu**: Contém todos os comandos organizados em categorias
- **Barra de Ferramentas**: Acesso rápido às funcionalidades mais utilizadas
- **Área de Edição**: Onde você digita e edita o texto
- **Barra de Status**: Exibe informações sobre a versão do aplicativo

## Funcionalidades

### Gerenciamento de Arquivos

#### Criar um Novo Documento
- Clique em **Arquivo > Novo** ou use o atalho **Ctrl+N**
- Você também pode clicar no botão **+** na barra de abas

#### Abrir um Arquivo Existente
- Clique em **Arquivo > Abrir** ou use o atalho **Ctrl+O**
- Navegue até o arquivo desejado e clique em "Abrir"

#### Salvar um Documento
- Clique em **Arquivo > Salvar** ou use o atalho **Ctrl+S**
- Se for a primeira vez que está salvando, será solicitado um nome e local

#### Salvar com Outro Nome
- Clique em **Arquivo > Salvar Como** ou use o atalho **Ctrl+Shift+S**
- Escolha um novo nome e local para o arquivo

#### Imprimir um Documento
- Clique em **Arquivo > Imprimir** ou use o atalho **Ctrl+P**
- Configure as opções de impressão e clique em "Imprimir"

### Edição de Texto

#### Operações Básicas
- **Cortar**: Selecione o texto e use **Ctrl+X** ou clique em **Editar > Cortar**
- **Copiar**: Selecione o texto e use **Ctrl+C** ou clique em **Editar > Copiar**
- **Colar**: Posicione o cursor e use **Ctrl+V** ou clique em **Editar > Colar**
- **Desfazer**: Use **Ctrl+Z** para desfazer a última ação
- **Refazer**: Use **Ctrl+Y** para refazer a última ação desfeita

#### Localizar e Substituir
1. Clique em **Editar > Localizar** ou use o atalho **Ctrl+F**
2. Digite o texto a ser localizado
3. Opcionalmente, digite o texto substituto
4. Use os botões "Localizar", "Substituir" ou "Substituir Tudo"

### Formatação de Texto

#### Estilos de Texto
- **Negrito**: Selecione o texto e use **Ctrl+B**
- **Itálico**: Selecione o texto e use **Ctrl+I**
- **Sublinhado**: Selecione o texto e use **Ctrl+U**
- **Tachado**: Selecione o texto e use **Ctrl+T**

#### Listas
- Posicione o cursor onde deseja iniciar a lista
- Use **Ctrl+L** para inserir uma lista com marcadores

#### Cor do Texto
1. Selecione o texto que deseja colorir
2. Clique em **Formatar > Cor do Texto**
3. Escolha a cor desejada no seletor de cores

#### Tamanho da Fonte
- Para aumentar: Use **Ctrl++** (Ctrl e tecla de adição)
- Para diminuir: Use **Ctrl+-** (Ctrl e tecla de subtração)

#### Alinhamento de Texto
1. Posicione o cursor no parágrafo ou selecione o texto
2. Clique no botão de formatação ou use **Ctrl+Shift+F**
3. Escolha o tipo de alinhamento desejado:
   - Alinhar à Esquerda
   - Centralizar
   - Alinhar à Direita
   - Justificar

### Ferramentas

#### Calculadora
- Clique em **Ferramentas > Calculadora** para abrir a calculadora do sistema

#### Calendário
1. Clique em **Ferramentas > Calendário**
2. Selecione a data desejada
3. Clique em "Inserir" para adicionar a data no cursor atual

#### Personalização de Cores
1. Clique em **Ferramentas > Mudar Cores**
2. Escolha uma das cores predefinidas ou selecione "Personalizada"
3. A cor de fundo do editor será alterada

#### Alternar Tema
- Clique em **Ferramentas > Mudar Tema** para alternar entre os temas claro e escuro

### Ajuda

#### Visualizar Ajuda
- Clique em **Ajuda > Ajuda** ou use o atalho **Shift+F1**
- Uma janela com instruções detalhadas será exibida

#### Sobre o Rabisco
- Clique em **Ajuda > Sobre** ou use o atalho **F1**
- Serão exibidas informações sobre o aplicativo e seus desenvolvedores

## Dicas e Truques

- Um asterisco (*) ao lado do nome do arquivo indica que há alterações não salvas
- Use múltiplas abas para trabalhar com vários documentos simultaneamente
- O tema escuro pode reduzir o cansaço visual em ambientes com pouca luz
- Utilize os atalhos de teclado para aumentar sua produtividade
- O aplicativo salva automaticamente o estado das abas ao ser fechado

## Solução de Problemas

### O aplicativo não inicia
- Verifique se todas as dependências estão instaladas
- Certifique-se de que o Python está corretamente configurado (se executando do código-fonte)
- Tente executar o aplicativo como administrador

### Problemas ao salvar arquivos
- Verifique se você tem permissões de escrita no diretório de destino
- Certifique-se de que o arquivo não está aberto em outro programa

### Problemas de formatação
- Algumas formatações avançadas podem não ser preservadas ao salvar como arquivo de texto simples
- Para preservar todas as formatações, considere usar o recurso de impressão para PDF

## Contato e Suporte

Para suporte técnico ou sugestões, entre em contato com o desenvolvedor:
- **Autor**: Danilo (danilodevsys)

---

Obrigado por escolher o Rabisco para suas necessidades de edição de texto!
