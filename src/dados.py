#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rabisco - Um simples bloco de notas
Arquivo que gerencia o acesso aos dados e banco de dados SQLite
"""

import os
import sqlite3
import json
from datetime import datetime

class BancoDados:
    """Classe responsável por gerenciar o acesso ao banco de dados SQLite"""

    def __init__(self, arquivo_db="rabisco.db"):
        """Inicializa o banco de dados"""
        self.arquivo_db = arquivo_db
        self.conexao = None
        self.cursor = None

        # Criar pasta para o banco de dados se não existir
        diretorio = os.path.dirname(arquivo_db)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)

        # Inicializar banco de dados
        self._conectar()
        self._criar_tabelas()

    def _conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conexao = sqlite3.connect(self.arquivo_db)
            # Habilitar chaves estrangeiras (importante para ON DELETE CASCADE)
            self.conexao.execute('PRAGMA foreign_keys = ON;')
            self.conexao.row_factory = sqlite3.Row  # Para acessar colunas pelo nome
            self.cursor = self.conexao.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")

    def _desconectar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conexao:
            self.conexao.close()
            self.conexao = None
            self.cursor = None

    def close(self):
        """Alias para _desconectar"""
        self._desconectar()

    def _criar_tabelas(self):
        """Cria as tabelas necessárias se não existirem"""
        try:
            # Tabela de notas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    conteudo TEXT,
                    categoria TEXT,
                    data_criacao TEXT NOT NULL,
                    data_modificacao TEXT NOT NULL
                )
            ''')

            # Tabela de etiquetas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS etiquetas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL COLLATE NOCASE
                )
            ''')

            # Tabela de relação entre notas e etiquetas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS nota_etiqueta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nota_id INTEGER,
                    etiqueta_id INTEGER,
                    FOREIGN KEY (nota_id) REFERENCES notas (id)
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas (id)
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    UNIQUE (nota_id, etiqueta_id) -- Evita etiquetas duplicadas na mesma nota
                )
            ''')

            # Tabela para histórico de arquivos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_arquivos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_arquivo TEXT NOT NULL,
                    caminho TEXT NOT NULL,
                    tipo_acesso TEXT NOT NULL, -- Ex: 'leitura', 'escrita', 'leitura (latin-1)'
                    data_acesso TEXT NOT NULL
                )
            ''')

            # Tabela para configurações do aplicativo
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracoes (
                    chave TEXT PRIMARY KEY UNIQUE,
                    valor TEXT NOT NULL
                )
            ''')

            # Salvar alterações
            self.conexao.commit()
        except sqlite3.Error as e:
            self.conexao.rollback()
            raise Exception(f"Erro ao criar tabelas: {str(e)}")

    def criar_nota(self, titulo, conteudo="", data_criacao=None):
        """
        Cria uma nova nota no banco de dados

        Args:
            titulo: Título da nota
            conteudo: Conteúdo da nota (opcional)
            data_criacao: Data de criação no formato "YYYY-MM-DD HH:MM:SS" (opcional)

        Returns:
            int: ID da nota criada
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            # Usar data atual se não for fornecida
            if data_criacao is None:
                data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data_modificacao = data_criacao

            # Inserir a nota
            self.cursor.execute('''
                INSERT INTO notas (titulo, conteudo, data_criacao, data_modificacao)
                VALUES (?, ?, ?, ?)
            ''', (titulo, conteudo, data_criacao, data_modificacao))

            # Obter o ID da nota criada
            nota_id = self.cursor.lastrowid

            # Salvar alterações
            self.conexao.commit()

            return nota_id
        except sqlite3.Error as e:
            self.conexao.rollback()
            raise Exception(f"Erro ao criar nota: {str(e)}")

    def obter_nota(self, nota_id):
        """
        Obtém uma nota pelo seu ID

        Args:
            nota_id: ID da nota

        Returns:
            dict: Dados da nota ou None se não encontrada (inclui 'etiquetas')
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            # Buscar a nota
            self.cursor.execute('''
                SELECT id, titulo, conteudo, categoria, data_criacao, data_modificacao
                FROM notas WHERE id = ?
            ''', (nota_id,))

            # Obter o resultado
            resultado = self.cursor.fetchone()

            if resultado:
                # Converter para dicionário
                nota = dict(resultado)

                # Buscar etiquetas da nota
                self.cursor.execute('''
                    SELECT e.nome FROM etiquetas e
                    JOIN nota_etiqueta ne ON e.id = ne.etiqueta_id
                    WHERE ne.nota_id = ?
                ''', (nota_id,))

                etiquetas = [row_etiqueta['nome'] for row_etiqueta in self.cursor.fetchall()]
                nota['etiquetas'] = etiquetas

                return nota
            else:
                return None
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar nota {nota_id}: {str(e)}")

    def atualizar_nota(self, nota_id, dados):
        """
        Atualiza os dados de uma nota (título, conteúdo, categoria, data_modificacao).
        Etiquetas devem ser atualizadas separadamente com atualizar_etiquetas.

        Args:
            nota_id: ID da nota
            dados: Dicionário com os dados a serem atualizados
                   (chaves esperadas: 'titulo', 'conteudo', 'categoria', 'data_modificacao')

        Returns:
            bool: True se a atualização foi bem-sucedida (a nota existia)
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            # Verificar se a nota existe
            self.cursor.execute("SELECT id FROM notas WHERE id = ?", (nota_id,))
            if not self.cursor.fetchone():
                return False # Nota não encontrada

            # Construir a consulta de atualização
            campos = []
            valores = []

            # Adicionar data de modificação se não estiver nos dados
            if 'data_modificacao' not in dados:
                 dados['data_modificacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for campo, valor in dados.items():
                # Impedir atualização do ID e tratar 'etiquetas' separadamente
                if campo not in ['id', 'etiquetas']:
                    campos.append(f"{campo} = ?")
                    valores.append(valor)

            if not campos:
                return False  # Nada para atualizar além de possibly data_modificacao

            # Adicionar ID à lista de valores
            valores.append(nota_id)

            # Executar a consulta
            consulta = f"UPDATE notas SET {', '.join(campos)} WHERE id = ?"
            self.cursor.execute(consulta, valores)

            # Salvar alterações
            self.conexao.commit()

            return True # Atualização bem-sucedida
        except sqlite3.Error as e:
            self.conexao.rollback()
            raise Exception(f"Erro ao atualizar nota {nota_id}: {str(e)}")

    def atualizar_etiquetas(self, nota_id, etiquetas):
        """
        Atualiza a lista completa de etiquetas para uma nota.
        Remove etiquetas antigas e adiciona as novas.

        Args:
            nota_id: ID da nota
            etiquetas: Lista de strings com os nomes das etiquetas

        Returns:
            bool: True se a operação foi bem-sucedida (a nota existia)
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
             # Verificar se a nota existe
            self.cursor.execute("SELECT id FROM notas WHERE id = ?", (nota_id,))
            if not self.cursor.fetchone():
                return False # Nota não encontrada

            # Iniciar transação
            self.conexao.execute("BEGIN") # ou self.conexao.in_transaction = True em versões mais recentes

            # 1. Remover todas as associações de etiquetas existentes para esta nota
            self.cursor.execute("DELETE FROM nota_etiqueta WHERE nota_id = ?", (nota_id,))

            # 2. Adicionar as novas etiquetas e suas associações
            for nome_etiqueta in etiquetas:
                # Encontrar ou criar a etiqueta na tabela 'etiquetas'
                self.cursor.execute("SELECT id FROM etiquetas WHERE nome = ? COLLATE NOCASE", (nome_etiqueta,))
                etiqueta_row = self.cursor.fetchone()

                if etiqueta_row:
                    etiqueta_id = etiqueta_row['id']
                else:
                    # Etiqueta não existe, criar
                    self.cursor.execute("INSERT INTO etiquetas (nome) VALUES (?)", (nome_etiqueta,))
                    etiqueta_id = self.cursor.lastrowid

                # Criar a associação na tabela 'nota_etiqueta'
                # UNIQUE constraint (nota_id, etiqueta_id) na criação da tabela
                # garante que não haverá duplicatas acidentais.
                # Como limpamos antes, não deve haver erro aqui, mas é boa prática.
                self.cursor.execute("INSERT INTO nota_etiqueta (nota_id, etiqueta_id) VALUES (?, ?)",
                                    (nota_id, etiqueta_id))

            # Commit da transação
            self.conexao.commit()
            return True

        except sqlite3.Error as e:
            self.conexao.rollback() # Rollback em caso de erro
            raise Exception(f"Erro ao atualizar etiquetas para nota {nota_id}: {str(e)}")

    def excluir_nota(self, nota_id):
        """
        Exclui uma nota do banco de dados.
        As relações na tabela nota_etiqueta serão excluídas automaticamente
        devido à configuração ON DELETE CASCADE.

        Args:
            nota_id: ID da nota a ser excluída

        Returns:
            bool: True se a exclusão foi bem-sucedida (a nota existia)
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            # Verificar se a nota existe
            self.cursor.execute("SELECT id FROM notas WHERE id = ?", (nota_id,))
            if not self.cursor.fetchone():
                return False # Nota não encontrada

            # Excluir a nota (ON DELETE CASCADE cuida das relações nota_etiqueta)
            self.cursor.execute("DELETE FROM notas WHERE id = ?", (nota_id,))

            # Salvar alterações
            self.conexao.commit()

            # Verificar se a exclusão ocorreu (opcional, o commit já indica sucesso)
            # return self.cursor.rowcount > 0 # Melhor verificar antes
            return True
        except sqlite3.Error as e:
            self.conexao.rollback()
            raise Exception(f"Erro ao excluir nota {nota_id}: {str(e)}")

    def obter_todas_notas(self):
        """
        Obtém todas as notas do banco de dados, incluindo suas etiquetas.

        Returns:
            list: Lista de dicionários com os dados das notas
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            # Buscar todas as notas
            self.cursor.execute('''
                SELECT id, titulo, conteudo, categoria, data_criacao, data_modificacao
                FROM notas ORDER BY data_modificacao DESC
            ''')

            # Converter resultados para lista de dicionários e buscar etiquetas
            notas = []
            for row in self.cursor.fetchall():
                nota = dict(row)

                # Buscar etiquetas da nota individualmente
                self.cursor.execute('''
                    SELECT e.nome FROM etiquetas e
                    JOIN nota_etiqueta ne ON e.id = ne.etiqueta_id
                    WHERE ne.nota_id = ?
                ''', (nota['id'],))

                etiquetas = [row_etiqueta['nome'] for row_etiqueta in self.cursor.fetchall()]
                nota['etiquetas'] = etiquetas

                notas.append(nota)

            return notas
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar todas as notas: {str(e)}")

    def pesquisar_notas(self, termo_pesquisa, filtro=None):
        """
        Pesquisa notas por termo (no título ou conteúdo) e aplica filtros adicionais.

        Args:
            termo_pesquisa: Termo a ser pesquisado (string). Case-insensitive.
            filtro: Dicionário opcional com filtros (ex: {'categoria': 'Trabalho', 'etiqueta': 'importante'})

        Returns:
            list: Lista de dicionários com as notas encontradas (inclui 'etiquetas').
                  Retorna todas as notas se termo_pesquisa for vazio e sem filtros.
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            consulta = '''
                SELECT DISTINCT n.id, n.titulo, n.conteudo, n.categoria,
                         n.data_criacao, n.data_modificacao
                FROM notas n
            '''
            parametros = []
            condicoes = []
            join_etiquetas = False # Flag para adicionar o JOIN de etiquetas apenas se necessário

            # Adicionar pesquisa por termo (case-insensitive)
            if termo_pesquisa:
                termo = f"%{termo_pesquisa}%"
                condicoes.append("(n.titulo LIKE ? COLLATE NOCASE OR n.conteudo LIKE ? COLLATE NOCASE)")
                parametros.extend([termo, termo])

            # Adicionar filtros
            if filtro:
                if 'categoria' in filtro and filtro['categoria'] is not None:
                    condicoes.append("n.categoria LIKE ? COLLATE NOCASE") # Pesquisa por categoria exata ou parcial
                    parametros.append(f"%{filtro['categoria']}%") # Usando LIKE para flexibilidade

                if 'etiqueta' in filtro and filtro['etiqueta'] is not None:
                    join_etiquetas = True # Precisamos do JOIN
                    condicoes.append("e.nome LIKE ? COLLATE NOCASE") # Pesquisa por etiqueta exata ou parcial
                    parametros.append(f"%{filtro['etiqueta']}%") # Usando LIKE para flexibilidade


            # Adicionar JOIN para etiquetas se o filtro de etiqueta for usado
            if join_etiquetas:
                consulta += '''
                    JOIN nota_etiqueta ne ON n.id = ne.nota_id
                    JOIN etiquetas e ON ne.etiqueta_id = e.id
                '''

            # Adicionar cláusula WHERE se houver condições
            if condicoes:
                consulta += " WHERE " + " AND ".join(condicoes)

            # Adicionar ordenação
            consulta += " ORDER BY n.data_modificacao DESC" # Ou outra ordenação padrão

            # Executar a consulta principal
            self.cursor.execute(consulta, parametros)

            # Buscar resultados e adicionar etiquetas a cada nota encontrada
            resultados = []
            for row in self.cursor.fetchall():
                nota = dict(row)

                # Buscar etiquetas para esta nota específica (mesmo se não usou filtro de etiqueta)
                self.cursor.execute('''
                    SELECT e.nome FROM etiquetas e
                    JOIN nota_etiqueta ne ON e.id = ne.etiqueta_id
                    WHERE ne.nota_id = ?
                ''', (nota['id'],))
                etiquetas = [row_etiqueta['nome'] for row_etiqueta in self.cursor.fetchall()]
                nota['etiquetas'] = etiquetas

                resultados.append(nota)

            return resultados

        except sqlite3.Error as e:
            raise Exception(f"Erro ao pesquisar notas: {str(e)}")

    def registrar_historico(self, nome_arquivo, caminho, tipo_acesso, data_acesso=None):
        """
        Registra um evento de acesso a arquivo no histórico.

        Args:
            nome_arquivo: Nome do arquivo acessado.
            caminho: Caminho completo do arquivo.
            tipo_acesso: Tipo de acesso (ex: 'leitura', 'escrita', 'leitura (latin-1)').
            data_acesso: Data e hora do acesso no formato "YYYY-MM-DD HH:MM:SS" (opcional).
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            if data_acesso is None:
                data_acesso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute('''
                INSERT INTO historico_arquivos (nome_arquivo, caminho, tipo_acesso, data_acesso)
                VALUES (?, ?, ?, ?)
            ''', (nome_arquivo, caminho, tipo_acesso, data_acesso))

            self.conexao.commit()
            # Return True # O registro de histórico não precisa retornar sucesso normalmente
        except sqlite3.Error as e:
            self.conexao.rollback()
            # Nota: GerenciadorNotas ignora erros aqui, mas o BD levanta exceção.
            # Dependendo da robustez desejada, pode-se adicionar um log aqui
            # ao invés de re-levantar. Mantendo a consistência do BD por enquanto.
            raise Exception(f"Erro ao registrar histórico: {str(e)}")


    def atualizar_categoria_notas(self, categoria, nota_ids):
        """
        Define a categoria para uma lista de notas.

        Args:
            categoria: Nome da categoria (string). Pode ser None para remover a categoria.
            nota_ids: Lista de IDs de notas a serem atualizadas.

        Returns:
            bool: True se a operação foi executada (mesmo que nenhum ID exista).
                  Mais útil verificar self.cursor.rowcount após o execute.
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        if not nota_ids:
            return True # Nada para fazer

        try:
            # Use a sintaxe WHERE id IN (...) com marcadores de posição (?)
            marcadores = ','.join('?' for _ in nota_ids)
            consulta = f"UPDATE notas SET categoria = ? WHERE id IN ({marcadores})"

            # Os valores são a categoria seguida pelos IDs
            valores = [categoria] + nota_ids

            self.cursor.execute(consulta, valores)
            self.conexao.commit()

            # Opcional: retornar o número de linhas afetadas
            # return self.cursor.rowcount > 0
            return True # Indicando que a operação foi tentada
        except sqlite3.Error as e:
            self.conexao.rollback()
            raise Exception(f"Erro ao atualizar categoria das notas: {str(e)}")

    def restaurar_notas(self, notas_backup):
        """
        Restaura notas a partir de uma lista de dados de backup.
        Esta implementação LIMPA o banco de dados atual de notas e etiquetas
        e insere os dados do backup.

        Args:
            notas_backup: Lista de dicionários representando as notas a serem restauradas.
                          Cada dicionário deve ter 'id', 'titulo', 'conteudo', 'categoria',
                          'data_criacao', 'data_modificacao' e 'etiquetas' (lista de strings).

        Returns:
            bool: True se a restauração foi executada com sucesso.
        Raises:
             Exception: Se ocorrer um erro no banco de dados durante a restauração.
        """
        try:
            self.conexao.execute("BEGIN") # Iniciar transação

            # 1. Limpar tabelas relevantes (isso também reseta AUTOINCREMENT em SQLite)
            self.cursor.execute("DELETE FROM nota_etiqueta")
            self.cursor.execute("DELETE FROM notas")
            self.cursor.execute("DELETE FROM etiquetas")
            # Opcional: Resetar sequências AUTOINCREMENT para IDs começarem do 1 novamente
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('notas', 'etiquetas', 'nota_etiqueta')")


            # 2. Inserir notas e reconstruir relações de etiquetas
            for nota_data in notas_backup:
                # Inserir a nota (SQLite irá gerar um novo ID, ignorando o ID do backup)
                self.cursor.execute('''
                    INSERT INTO notas (titulo, conteudo, categoria, data_criacao, data_modificacao)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nota_data.get('titulo', ''),
                      nota_data.get('conteudo', ''),
                      nota_data.get('categoria'), # Categoria pode ser None
                      nota_data.get('data_criacao', datetime.now().strftime("%Y-%m-%d %H:%M:%S")), # Use data atual se faltar
                      nota_data.get('data_modificacao', datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Use data atual se faltar
                     ))
                new_nota_id = self.cursor.lastrowid # Novo ID atribuído pelo banco

                # Processar etiquetas para esta nota
                etiquetas_backup = nota_data.get('etiquetas', [])
                if etiquetas_backup:
                    for nome_etiqueta in etiquetas_backup:
                         # Encontrar ou criar a etiqueta na tabela 'etiquetas'
                        self.cursor.execute("SELECT id FROM etiquetas WHERE nome = ? COLLATE NOCASE", (nome_etiqueta,))
                        etiqueta_row = self.cursor.fetchone()

                        if etiqueta_row:
                            etiqueta_id = etiqueta_row['id']
                        else:
                            # Etiqueta não existe, criar
                            self.cursor.execute("INSERT INTO etiquetas (nome) VALUES (?)", (nome_etiqueta,))
                            etiqueta_id = self.cursor.lastrowid

                        # Criar a associação na tabela 'nota_etiqueta' usando o NOVO ID da nota
                        self.cursor.execute("INSERT INTO nota_etiqueta (nota_id, etiqueta_id) VALUES (?, ?)",
                                            (new_nota_id, etiqueta_id))


            self.conexao.commit() # Commit da transação
            return True

        except sqlite3.Error as e:
            self.conexao.rollback() # Rollback em caso de erro
            raise Exception(f"Erro ao restaurar notas do backup: {str(e)}")

    def obter_configuracao(self, chave, valor_default=None):
        """
        Obtém um valor de configuração pelo nome da chave.

        Args:
            chave: Chave da configuração (string).
            valor_default: Valor a retornar se a chave não for encontrada (opcional).

        Returns:
            str: O valor da configuração ou valor_default se não encontrado.
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            self.cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado['valor']
            else:
                return valor_default
        except sqlite3.Error as e:
            raise Exception(f"Erro ao obter configuração '{chave}': {str(e)}")

    def salvar_configuracao(self, chave, valor):
        """
        Salva ou atualiza um valor de configuração.

        Args:
            chave: Chave da configuração (string).
            valor: Valor da configuração (string).
        Returns:
            bool: True se a operação foi bem sucedida.
        Raises:
             Exception: Se ocorrer um erro no banco de dados.
        """
        try:
            # INSERT OR REPLACE irá inserir se a chave não existir, ou atualizar se já existir
            self.cursor.execute("INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)", (chave, valor))
            self.conexao.commit()
            return True
        except sqlite3.Error as e:
            self.conexao.rollback()
            raise Exception(f"Erro ao salvar configuração '{chave}': {str(e)}")


# --- Exemplo de Uso ---
if __name__ == "__main__":
    db_file = "dados/rabisco_teste.db" # Arquivo de banco de dados de teste
    # Crie o diretório se ele não existir
    os.makedirs(os.path.dirname(db_file), exist_ok=True)

    print(f"--- Testando a classe BancoDados em {db_file} ---")

    # Limpar arquivo de teste anterior, se existir
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Arquivo de banco de dados anterior '{db_file}' removido.")

    banco = None # Inicializar banco como None
    try:
        # 1. Inicializar o banco de dados (cria arquivo e tabelas se não existirem)
        banco = BancoDados(db_file)
        print("Banco de dados inicializado com sucesso.")

        # 2. Criar algumas notas
        print("\n--- Criando notas ---")
        nota1_id = banco.criar_nota("Reunião Projeto Alpha", "Discutir prazos e recursos.")
        nota2_id = banco.criar_nota("Ideias para Blog Post", "Tópicos: Python, SQLite, Notas.")
        nota3_id = banco.criar_nota("Lista de Compras", "Leite, Pão, Ovos.")
        nota4_id = banco.criar_nota("Nota Rascunho", "Apenas um teste.")

        print(f"Notas criadas: ID {nota1_id}, ID {nota2_id}, ID {nota3_id}, ID {nota4_id}")

        # 3. Obter uma nota
        print("\n--- Obtendo nota por ID ---")
        nota_obtida = banco.obter_nota(nota2_id)
        if nota_obtida:
            print(f"Nota obtida (ID {nota2_id}): {nota_obtida['titulo']}, Conteúdo: {nota_obtida['conteudo']}")
        else:
            print(f"Nota com ID {nota2_id} não encontrada.")

        # 4. Atualizar uma nota
        print("\n--- Atualizando nota ---")
        dados_atualizacao = {
            'titulo': 'Ideias para Blog Post (Revisado)',
            'conteudo': 'Tópicos: Python, SQLite, Banco de Dados, Notas em Python.',
            'data_modificacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Atualiza a data
        }
        sucesso_atualizacao = banco.atualizar_nota(nota2_id, dados_atualizacao)
        print(f"Atualização da nota ID {nota2_id} bem-sucedida: {sucesso_atualizacao}")
        nota_atualizada = banco.obter_nota(nota2_id)
        if nota_atualizada:
             print(f"Nota após atualização: {nota_atualizada['titulo']}, Conteúdo: {nota_atualizada['conteudo']}")


        # 5. Atualizar etiquetas
        print("\n--- Atualizando etiquetas ---")
        etiquetas_nota2 = ["python", "sqlite", "blog", "ideias"]
        sucesso_etiquetas = banco.atualizar_etiquetas(nota2_id, etiquetas_nota2)
        print(f"Atualização de etiquetas para nota ID {nota2_id} bem-sucedida: {sucesso_etiquetas}")
        nota_com_etiquetas = banco.obter_nota(nota2_id)
        if nota_com_etiquetas:
             print(f"Nota com etiquetas: {nota_com_etiquetas['titulo']}, Etiquetas: {nota_com_etiquetas['etiquetas']}")

        etiquetas_nota1 = ["projeto", "reuniao", "alpha"]
        banco.atualizar_etiquetas(nota1_id, etiquetas_nota1)
        nota_com_etiquetas_1 = banco.obter_nota(nota1_id)
        if nota_com_etiquetas_1:
             print(f"Nota com etiquetas: {nota_com_etiquetas_1['titulo']}, Etiquetas: {nota_com_etiquetas_1['etiquetas']}")


        # 6. Organizar por categoria
        print("\n--- Organizando notas por categoria ---")
        sucesso_categoria = banco.atualizar_categoria_notas("Trabalho", [nota1_id, nota2_id])
        print(f"Organização de notas {nota1_id}, {nota2_id} na categoria 'Trabalho' bem-sucedida: {sucesso_categoria}")
        nota_cat1 = banco.obter_nota(nota1_id)
        nota_cat2 = banco.obter_nota(nota2_id)
        if nota_cat1: print(f"Nota ID {nota1_id} Categoria: {nota_cat1['categoria']}")
        if nota_cat2: print(f"Nota ID {nota2_id} Categoria: {nota_cat2['categoria']}")


        # 7. Pesquisar notas
        print("\n--- Pesquisando notas ---")
        termo_pesquisa = "notas"
        resultados_termo = banco.pesquisar_notas(termo_pesquisa)
        print(f"Resultados para termo '{termo_pesquisa}': {len(resultados_termo)}")
        for r in resultados_termo:
            print(f"- ID: {r['id']}, Título: {r['titulo']}, Etiquetas: {r['etiquetas']}, Categoria: {r['categoria']}")

        print("\n--- Pesquisando com filtro de categoria ---")
        resultados_filtro_cat = banco.pesquisar_notas("", filtro={'categoria': 'Trabalho'}) # Pesquisa vazia, só filtro
        print(f"Resultados para categoria 'Trabalho': {len(resultados_filtro_cat)}")
        for r in resultados_filtro_cat:
            print(f"- ID: {r['id']}, Título: {r['titulo']}, Categoria: {r['categoria']}")

        print("\n--- Pesquisando com filtro de etiqueta ---")
        resultados_filtro_tag = banco.pesquisar_notas("", filtro={'etiqueta': 'python'}) # Pesquisa vazia, só filtro
        print(f"Resultados para etiqueta 'python': {len(resultados_filtro_tag)}")
        for r in resultados_filtro_tag:
            print(f"- ID: {r['id']}, Título: {r['titulo']}, Etiquetas: {r['etiquetas']}")

        print("\n--- Pesquisando termo + filtro de etiqueta ---")
        resultados_termo_tag = banco.pesquisar_notas("revisado", filtro={'etiqueta': 'blog'})
        print(f"Resultados para termo 'revisado' + etiqueta 'blog': {len(resultados_termo_tag)}")
        for r in resultados_termo_tag:
            print(f"- ID: {r['id']}, Título: {r['titulo']}, Etiquetas: {r['etiquetas']}")


        # 8. Obter todas as notas
        print("\n--- Obtendo todas as notas ---")
        todas_notas = banco.obter_todas_notas()
        print(f"Total de notas no banco: {len(todas_notas)}")
        for nota in todas_notas:
             print(f"- ID: {nota['id']}, Título: {nota['titulo']}, Etiquetas: {nota['etiquetas']}, Categoria: {nota['categoria']}")


        # 9. Registrar histórico de arquivo (simulado)
        print("\n--- Registrando histórico de arquivo ---")
        banco.registrar_historico("minha_nota.txt", "/caminho/qualquer/minha_nota.txt", "leitura")
        banco.registrar_historico("outro_arquivo.log", "/var/log/outro_arquivo.log", "escrita")
        print("Históricos registrados (verificar diretamente no DB se necessário).")


        # 10. Testar backup e restauração (simulado)
        print("\n--- Testando backup e restauração (apaga e recria) ---")
        backup_data = banco.obter_todas_notas() # Simula obter dados para backup
        print(f"Simulando dados de backup para {len(backup_data)} notas.")

        # Excluir algumas notas antes de restaurar
        banco.excluir_nota(nota3_id)
        print(f"Nota ID {nota3_id} excluída antes da restauração simulada.")
        print(f"Notas restantes antes da restauração: {len(banco.obter_todas_notas())}")

        print("Iniciando restauração...")
        sucesso_restauracao = banco.restaurar_notas(backup_data) # Restaura o estado original antes da exclusão
        print(f"Restauração bem-sucedida: {sucesso_restauracao}")

        print(f"Notas após restauração: {len(banco.obter_todas_notas())}")
        notas_restauradas = banco.obter_todas_notas()
        print("Notas restauradas:")
        for nota in notas_restauradas:
            print(f"- ID: {nota['id']}, Título: {nota['titulo']}, Etiquetas: {nota['etiquetas']}, Categoria: {nota['categoria']}")


        # 11. Gerenciar configurações
        print("\n--- Gerenciando configurações ---")
        banco.salvar_configuracao("tema", "dark")
        banco.salvar_configuracao("fonte_tamanho", "12")
        banco.salvar_configuracao("tema", "light") # Atualiza o tema

        tema = banco.obter_configuracao("tema")
        tamanho_fonte = banco.obter_configuracao("fonte_tamanho")
        cor_inexistente = banco.obter_configuracao("cor_tema", "blue")

        print(f"Configuração 'tema': {tema}")
        print(f"Configuração 'fonte_tamanho': {tamanho_fonte}")
        print(f"Configuração 'cor_tema' (default): {cor_inexistente}")


        # 12. Excluir uma nota
        print("\n--- Excluindo nota ---")
        id_para_excluir = nota4_id
        print(f"Tentando excluir nota com ID {id_para_excluir} (original).")
        sucesso_exclusao = banco.excluir_nota(id_para_excluir)
        print(f"Exclusão da nota ID {id_para_excluir} bem-sucedida: {sucesso_exclusao}")
        nota_excluida_check = banco.obter_nota(id_para_excluir)
        print(f"Nota ID {id_para_excluir} encontrada após exclusão: {nota_excluida_check is not None}")


    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {e}")

    finally:
        # 13. Fechar a conexão
        if banco:
            banco.close()
            print("\nConexão com o banco de dados fechada.")
        # Manter o arquivo .db para inspeção manual se desejar
        # os.remove(db_file) # Descomente para limpar o arquivo de teste
        # print(f"Arquivo de banco de dados de teste '{db_file}' removido.")