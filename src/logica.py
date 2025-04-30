#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rabisco - Um simples bloco de notas
Arquivo que contém a lógica de negócio da aplicação
"""
import os
import json
from datetime import datetime

# --- Mock para a classe BancoDados (necessária para rodar este script de forma independente) ---
# Em um aplicativo real, esta classe seria substituída por uma implementação
# que interage com um banco de dados real (SQL, NoSQL, etc.)
class MockBancoDados:
    """
    Classe mock para simular as interações com um banco de dados.
    Usada apenas para permitir que a classe GerenciadorNotas seja testada/demonstrada.
    """
    def __init__(self):
        print("MockBancoDados inicializado.")
        self._notas = [] # Lista para armazenar notas simuladas
        self._historico = [] # Lista para armazenar histórico simulado
        self._next_note_id = 1 # Contador para IDs de notas

    def criar_nota(self, titulo, conteudo, data_criacao):
        """Simula a criação de uma nota."""
        nota = {
            "id": self._next_note_id,
            "titulo": titulo,
            "conteudo": conteudo,
            "data_criacao": data_criacao,
            "data_modificacao": data_criacao,
            "etiquetas": [],
            "categoria": None
        }
        self._notas.append(nota)
        note_id = self._next_note_id
        self._next_note_id += 1
        print(f"MockBancoDados: Nota '{titulo}' criada com ID {note_id}.")
        return note_id

    def atualizar_nota(self, nota_id, dados):
        """Simula a atualização de uma nota."""
        for nota in self._notas:
            if nota["id"] == nota_id:
                nota.update(dados)
                print(f"MockBancoDados: Nota ID {nota_id} atualizada.")
                return True
        print(f"MockBancoDados: Nota ID {nota_id} não encontrada para atualização.")
        return False

    def atualizar_etiquetas(self, nota_id, etiquetas):
        """Simula a atualização das etiquetas de uma nota."""
        for nota in self._notas:
            if nota["id"] == nota_id:
                nota["etiquetas"] = etiquetas
                print(f"MockBancoDados: Etiquetas da nota ID {nota_id} atualizadas: {etiquetas}")
                return True
        print(f"MockBancoDados: Nota ID {nota_id} não encontrada para atualizar etiquetas.")
        return False

    def excluir_nota(self, nota_id):
        """Simula a exclusão de uma nota."""
        initial_count = len(self._notas)
        self._notas = [nota for nota in self._notas if nota["id"] != nota_id]
        if len(self._notas) < initial_count:
            print(f"MockBancoDados: Nota ID {nota_id} excluída.")
            return True
        print(f"MockBancoDados: Nota ID {nota_id} não encontrada para exclusão.")
        return False

    def pesquisar_notas(self, termo_pesquisa, filtro=None):
        """Simula a pesquisa de notas."""
        termo = termo_pesquisa.lower()
        resultados = []
        print(f"MockBancoDados: Pesquisando por '{termo}' com filtro '{filtro}'.")
        for nota in self._notas:
            match = False
            if termo in nota.get("titulo", "").lower() or termo in nota.get("conteudo", "").lower():
                 match = True

            # Implementação simples de filtro (ex: por categoria ou etiqueta)
            if filtro and match:
                # Exemplo de filtro por categoria ou se termo está em etiquetas
                if 'categoria' in filtro and nota.get('categoria') != filtro['categoria']:
                    match = False
                elif 'etiqueta' in filtro and filtro['etiqueta'].lower() not in [e.lower() for e in nota.get('etiquetas', [])]:
                     match = False # Simplificado: verifica se *qualquer* etiqueta contém o termo do filtro

            if match:
                resultados.append(nota)
        print(f"MockBancoDados: Encontrados {len(resultados)} resultados.")
        return resultados

    def obter_todas_notas(self):
        """Simula a obtenção de todas as notas."""
        print(f"MockBancoDados: Obtendo todas as {len(self._notas)} notas.")
        return self._notas[:] # Retorna uma cópia para evitar modificação externa

    def restaurar_notas(self, notas):
        """Simula a restauração de notas a partir de um backup."""
        print(f"MockBancoDados: Restaurando {len(notas)} notas.")
        self._notas = notas
        # Resetar o contador de ID pode ser necessário, dependendo da lógica de backup
        # Para este mock, vamos apenas substituir a lista.
        if notas:
             self._next_note_id = max([n['id'] for n in notas]) + 1 if notas else 1
        else:
             self._next_note_id = 1

        print("MockBancoDados: Restauração concluída.")
        return True

    def registrar_historico(self, nome_arquivo, caminho, tipo_acesso, data_acesso):
        """Simula o registro de histórico de acesso a arquivo."""
        self._historico.append({
            "nome_arquivo": nome_arquivo,
            "caminho": caminho,
            "tipo_acesso": tipo_acesso,
            "data_acesso": data_acesso
        })
        print(f"MockBancoDados: Histórico registrado - {tipo_acesso} em {nome_arquivo}.")
        return True

    def atualizar_categoria_notas(self, categoria, nota_ids):
        """Simula a atualização da categoria de notas."""
        count = 0
        for nota in self._notas:
            if nota["id"] in nota_ids:
                nota["categoria"] = categoria
                count += 1
        print(f"MockBancoDados: Categoria '{categoria}' definida para {count} notas.")
        return True

# --- Classe GerenciadorNotas Original (Corrigida e Completa) ---

class GerenciadorNotas:
    """Classe responsável por gerenciar as notas e arquivos"""

    def __init__(self, banco_dados):
        """Inicializa o gerenciador de notas"""
        self.db = banco_dados
        self.notas_abertas = {} # Atributo presente, mas não utilizado na lógica fornecida

    def ler_arquivo(self, caminho):
        """
        Lê o conteúdo de um arquivo

        Args:
            caminho: Caminho do arquivo a ser lido

        Returns:
            str: Conteúdo do arquivo

        Raises:
            FileNotFoundError: Se o arquivo não existir
            PermissionError: Se não houver permissão para ler o arquivo
            Exception: Para outros erros
        """
        try:
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"O arquivo {caminho} não existe")

            with open(caminho, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()

            # Registrar acesso ao arquivo no histórico
            self._registrar_acesso(caminho, "leitura")

            return conteudo
        except UnicodeDecodeError:
            # Tentar ler com codificação alternativa
            try:
                 with open(caminho, 'r', encoding='latin-1') as arquivo:
                    conteudo = arquivo.read()
                 self._registrar_acesso(caminho, "leitura (latin-1)") # Registrar tentativa alternativa
                 return conteudo
            except Exception as e:
                 # Se latim-1 também falhar, re-raise a exceção original ou a nova
                 raise Exception(f"Erro de decodificação (UTF-8 e Latin-1 falharam) ao ler o arquivo {caminho}: {str(e)}")
        except Exception as e:
            # Repassar a exceção para ser tratada no nível superior
            raise e

    def salvar_arquivo(self, caminho, conteudo):
        """
        Salva conteúdo em um arquivo

        Args:
            caminho: Caminho onde o arquivo será salvo
            conteudo: Conteúdo a ser salvo

        Raises:
            PermissionError: Se não houver permissão para escrever no arquivo
            IOError: Se ocorrer um erro de I/O durante a escrita
            Exception: Para outros erros
        """
        try:
            # Garantir que o diretório exista, se o caminho inclui diretórios
            diretorio = os.path.dirname(caminho)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio, exist_ok=True) # Cria diretórios intermediários se necessário

            with open(caminho, 'w', encoding='utf-8') as arquivo:
                arquivo.write(conteudo)

            # Registrar acesso ao arquivo no histórico
            self._registrar_acesso(caminho, "escrita")

            return True
        except PermissionError:
             raise PermissionError(f"Permissão negada para escrever no arquivo {caminho}")
        except IOError as e:
             raise IOError(f"Erro de I/O ao salvar o arquivo {caminho}: {str(e)}")
        except Exception as e:
            # Repassar a exceção para ser tratada no nível superior
            raise e

    def criar_nova_nota(self, titulo, conteudo=""):
        """
        Cria uma nova nota no banco de dados

        Args:
            titulo: Título da nota
            conteudo: Conteúdo da nota (opcional)

        Returns:
            int: ID da nota criada

        Raises:
            Exception: Se ocorrer um erro durante a criação da nota no banco de dados.
        """
        try:
            data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Criar nota no banco de dados
            nota_id = self.db.criar_nota(titulo, conteudo, data_criacao)

            return nota_id
        except Exception as e:
            raise Exception(f"Erro ao criar nota: {str(e)}")

    def atualizar_nota(self, nota_id, titulo=None, conteudo=None, etiquetas=None, categoria=None):
        """
        Atualiza uma nota existente

        Args:
            nota_id: ID da nota a ser atualizada
            titulo: Novo título (opcional)
            conteudo: Novo conteúdo (opcional)
            etiquetas: Novas etiquetas (lista de strings, opcional)
            categoria: Nova categoria (string, opcional)

        Returns:
            bool: True se a atualização foi bem-sucedida

        Raises:
            Exception: Se ocorrer um erro durante a atualização da nota no banco de dados.
        """
        try:
            data_modificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Preparar os dados para atualização
            dados = {"data_modificacao": data_modificacao}

            if titulo is not None:
                dados["titulo"] = titulo

            if conteudo is not None:
                dados["conteudo"] = conteudo

            if categoria is not None:
                 dados["categoria"] = categoria

            # Atualizar a nota no banco de dados (dados básicos)
            resultado_nota = self.db.atualizar_nota(nota_id, dados)

            # Atualizar etiquetas separadamente, se fornecidas
            resultado_etiquetas = True # Assume sucesso se etiquetas não forem fornecidas
            if etiquetas is not None:
                 resultado_etiquetas = self.db.atualizar_etiquetas(nota_id, etiquetas)


            # A atualização geral só é bem sucedida se ambas as partes (nota e etiquetas) funcionarem
            return resultado_nota and resultado_etiquetas
        except Exception as e:
            raise Exception(f"Erro ao atualizar nota {nota_id}: {str(e)}")

    def excluir_nota(self, nota_id):
        """
        Exclui uma nota do banco de dados

        Args:
            nota_id: ID da nota a ser excluída

        Returns:
            bool: True se a exclusão foi bem-sucedida

        Raises:
            Exception: Se ocorrer um erro durante a exclusão da nota no banco de dados.
        """
        try:
            resultado = self.db.excluir_nota(nota_id)
            return resultado
        except Exception as e:
            raise Exception(f"Erro ao excluir nota {nota_id}: {str(e)}")

    def pesquisar_notas(self, termo_pesquisa, filtro=None):
        """
        Pesquisa notas por termo e filtros

        Args:
            termo_pesquisa: Termo a ser pesquisado (string)
            filtro: Dicionário de filtros (ex: {'categoria': 'Trabalho', 'etiqueta': 'importante'}) (opcional)

        Returns:
            list: Lista de notas encontradas (dicionários)

        Raises:
            Exception: Se ocorrer um erro durante a pesquisa no banco de dados.
        """
        try:
            resultado = self.db.pesquisar_notas(termo_pesquisa, filtro)
            return resultado
        except Exception as e:
            raise Exception(f"Erro ao pesquisar notas: {str(e)}")

    def criar_backup(self, caminho_destino):
        """
        Cria um backup de todas as notas em formato JSON.

        Args:
            caminho_destino: Caminho completo onde o arquivo de backup será salvo (ex: '/caminho/para/backup.json')

        Returns:
            bool: True se o backup foi bem-sucedido

        Raises:
            Exception: Se ocorrer um erro durante a criação ou escrita do arquivo de backup.
        """
        try:
            # Obter todas as notas
            notas = self.db.obter_todas_notas()

            # Criar estrutura de dados para o backup
            dados_backup = {
                "data_backup": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "notas": notas
            }

            # Garantir que o diretório de destino exista
            diretorio = os.path.dirname(caminho_destino)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio, exist_ok=True)

            # Salvar o backup como JSON
            with open(caminho_destino, 'w', encoding='utf-8') as arquivo:
                json.dump(dados_backup, arquivo, ensure_ascii=False, indent=4)

            print(f"Backup criado com sucesso em {caminho_destino}")
            return True
        except Exception as e:
            raise Exception(f"Erro ao criar backup em {caminho_destino}: {str(e)}")

    def restaurar_backup(self, caminho_origem):
        """
        Restaura notas a partir de um arquivo de backup JSON.
        NOTA: Esta operação pode substituir as notas existentes, dependendo da
        implementação do método restaurar_notas no MockBancoDados.

        Args:
            caminho_origem: Caminho do arquivo de backup JSON a ser restaurado.

        Returns:
            bool: True se a restauração foi bem-sucedida

        Raises:
            FileNotFoundError: Se o arquivo de backup não existir.
            json.JSONDecodeError: Se o arquivo não for um JSON válido.
            KeyError: Se a estrutura do JSON de backup estiver incorreta (faltando 'notas').
            Exception: Para outros erros durante a leitura ou restauração no banco de dados.
        """
        try:
            if not os.path.exists(caminho_origem):
                 raise FileNotFoundError(f"O arquivo de backup {caminho_origem} não foi encontrado.")

            # Ler o arquivo de backup
            with open(caminho_origem, 'r', encoding='utf-8') as arquivo:
                dados_backup = json.load(arquivo)

            # Verificar se a estrutura do backup está correta
            if "notas" not in dados_backup:
                 raise KeyError("Estrutura de backup inválida: 'notas' não encontrado no arquivo JSON.")

            # Restaurar as notas no banco de dados
            resultado = self.db.restaurar_notas(dados_backup["notas"])

            print(f"Restauração a partir de {caminho_origem} concluída.")
            return resultado
        except FileNotFoundError:
             raise # Re-raise a exceção FileNotFoundError
        except json.JSONDecodeError:
             raise json.JSONDecodeError(f"Erro ao decodificar o arquivo JSON de backup {caminho_origem}. Verifique se é um arquivo JSON válido.", doc="", pos=0)
        except KeyError as e:
             raise KeyError(f"Erro na estrutura do arquivo de backup: {e}. Arquivo inválido.")
        except Exception as e:
            raise Exception(f"Erro ao restaurar backup a partir de {caminho_origem}: {str(e)}")

    def _registrar_acesso(self, caminho, tipo_acesso):
        """
        Registra o acesso a um arquivo no histórico (via banco de dados).
        Erros neste processo são ignorados para não interromper a operação principal.

        Args:
            caminho: Caminho do arquivo acessado
            tipo_acesso: Tipo de acesso (leitura/escrita)
        """
        try:
            data_acesso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Usar abspath para garantir caminho completo no histórico
            caminho_completo = os.path.abspath(caminho)
            nome_arquivo = os.path.basename(caminho_completo)

            # Registrar no banco de dados
            self.db.registrar_historico(nome_arquivo, caminho_completo, tipo_acesso, data_acesso)
        except Exception as e:
            # Ignorar erros no registro de histórico, mas opcionalmente logar para debug
            print(f"AVISO: Falha ao registrar histórico de acesso ao arquivo {caminho}: {e}")
            pass

    def organizar_notas(self, categoria, nota_ids):
        """
        Organiza notas atribuindo-lhes uma categoria.

        Args:
            categoria: Nome da categoria (string)
            nota_ids: Lista de IDs de notas a serem organizadas (lista de int)

        Returns:
            bool: True se a organização foi bem-sucedida

        Raises:
            Exception: Se ocorrer um erro durante a atualização das categorias no banco de dados.
        """
        try:
            resultado = self.db.atualizar_categoria_notas(categoria, nota_ids)
            return resultado
        except Exception as e:
            raise Exception(f"Erro ao organizar notas nas categoria '{categoria}': {str(e)}")


# --- Exemplo de Uso ---
if __name__ == "__main__":
    # 1. Crie uma instância do banco de dados (aqui usamos o mock)
    banco_dados_mock = MockBancoDados()

    # 2. Crie uma instância do gerenciador de notas, passando o banco de dados
    gerenciador = GerenciadorNotas(banco_dados_mock)

    print("\n--- Testando a criação de notas ---")
    try:
        nota1_id = gerenciador.criar_nova_nota("Minha Primeira Nota", "Conteúdo inicial desta nota.")
        nota2_id = gerenciador.criar_nova_nota("Ideias para o Projeto X")
        nota3_id = gerenciador.criar_nova_nota("Lembretes Rápidos", "Comprar pão\nPagar conta de luz")
        print(f"Notas criadas com IDs: {nota1_id}, {nota2_id}, {nota3_id}")
    except Exception as e:
        print(f"Erro ao criar notas: {e}")

    print("\n--- Testando a pesquisa de notas ---")
    try:
        termo = "nota"
        resultados_nota = gerenciador.pesquisar_notas(termo)
        print(f"Notas encontradas com o termo '{termo}':")
        for nota in resultados_nota:
            print(f"- ID: {nota['id']}, Título: {nota['titulo']}")

        termo = "Projeto X"
        resultados_projeto = gerenciador.pesquisar_notas(termo)
        print(f"\nNotas encontradas com o termo '{termo}':")
        for nota in resultados_projeto:
            print(f"- ID: {nota['id']}, Título: {nota['titulo']}")

    except Exception as e:
        print(f"Erro ao pesquisar notas: {e}")

    print("\n--- Testando a atualização de nota ---")
    try:
        if nota2_id: # Verifica se a nota foi criada
             sucesso_atualizacao = gerenciador.atualizar_nota(
                 nota2_id,
                 titulo="Ideias Projeto X - V2",
                 conteudo="Conteúdo atualizado com mais detalhes.",
                 etiquetas=["projeto", "ideias", "trabalho"]
             )
             print(f"Atualização da nota ID {nota2_id} bem-sucedida: {sucesso_atualizacao}")

             # Pesquisar novamente para ver a atualização
             termo = "V2"
             resultados_atualizados = gerenciador.pesquisar_notas(termo)
             print(f"\nNotas encontradas com o termo '{termo}' após atualização:")
             for nota in resultados_atualizados:
                 print(f"- ID: {nota['id']}, Título: {nota['titulo']}, Etiquetas: {nota['etiquetas']}")

    except Exception as e:
         print(f"Erro ao atualizar nota: {e}")


    print("\n--- Testando organização por categoria ---")
    try:
        if nota2_id and nota1_id:
            sucesso_organizar = gerenciador.organizar_notas("Trabalho", [nota2_id])
            print(f"Organização da nota ID {nota2_id} na categoria 'Trabalho' bem-sucedida: {sucesso_organizar}")

            # Pesquisar por categoria
            resultados_categoria = gerenciador.pesquisar_notas("", filtro={'categoria': 'Trabalho'})
            print("\nNotas na categoria 'Trabalho':")
            for nota in resultados_categoria:
                 print(f"- ID: {nota['id']}, Título: {nota['titulo']}, Categoria: {nota['categoria']}")

    except Exception as e:
         print(f"Erro ao organizar notas: {e}")


    print("\n--- Testando salvar e ler arquivo ---")
    arquivo_teste_caminho = "rabisco_teste.txt"
    conteudo_teste = "Este é um conteúdo de teste para o arquivo.\nCom acentos: áéíóúãõç."
    try:
        sucesso_salvar = gerenciador.salvar_arquivo(arquivo_teste_caminho, conteudo_teste)
        print(f"Arquivo salvo com sucesso: {sucesso_salvar}")

        conteudo_lido = gerenciador.ler_arquivo(arquivo_teste_caminho)
        print(f"Conteúdo lido do arquivo:\n{conteudo_lido}")

    except Exception as e:
        print(f"Erro ao salvar/ler arquivo: {e}")
    finally:
        # Limpar o arquivo de teste
        if os.path.exists(arquivo_teste_caminho):
            os.remove(arquivo_teste_caminho)
            print(f"Arquivo de teste {arquivo_teste_caminho} removido.")


    print("\n--- Testando backup e restauração ---")
    backup_teste_caminho = "rabisco_backup_teste.json"
    try:
        sucesso_backup = gerenciador.criar_backup(backup_teste_caminho)
        print(f"Backup criado com sucesso: {sucesso_backup}")

        # Excluir notas existentes para simular um estado inicial vazio ou diferente
        if nota1_id: gerenciador.excluir_nota(nota1_id)
        if nota2_id: gerenciador.excluir_nota(nota2_id)
        if nota3_id: gerenciador.excluir_nota(nota3_id)
        print("Notas simuladas excluídas antes da restauração.")
        print(f"Notas após exclusão: {banco_dados_mock.obter_todas_notas()}")

        # Restaurar a partir do backup
        sucesso_restauracao = gerenciador.restaurar_backup(backup_teste_caminho)
        print(f"Restauração a partir de backup bem-sucedida: {sucesso_restauracao}")

        # Verificar as notas após a restauração
        notas_restauradas = banco_dados_mock.obter_todas_notas()
        print("\nNotas após restauração:")
        for nota in notas_restauradas:
            print(f"- ID: {nota['id']}, Título: {nota['titulo']}, Conteúdo: {nota['conteudo'][:30]}...") # Exibe parte do conteúdo


    except Exception as e:
        print(f"Erro durante backup/restauração: {e}")
    finally:
         # Limpar o arquivo de backup
        if os.path.exists(backup_teste_caminho):
            os.remove(backup_teste_caminho)
            print(f"Arquivo de backup de teste {backup_teste_caminho} removido.")


    print("\n--- Testando exclusão de nota ---")
    try:
        # Pegar o ID de uma nota restaurada (assumindo que a restauração funcionou)
        if notas_restauradas:
            id_para_excluir = notas_restauradas[0]['id']
            print(f"Tentando excluir a nota com ID {id_para_excluir}.")
            sucesso_exclusao = gerenciador.excluir_nota(id_para_excluir)
            print(f"Exclusão da nota ID {id_para_excluir} bem-sucedida: {sucesso_exclusao}")

            # Verificar se a nota foi realmente excluída
            notas_apos_exclusao = banco_dados_mock.obter_todas_notas()
            encontrada = any(nota['id'] == id_para_excluir for nota in notas_apos_exclusao)
            print(f"Nota ID {id_para_excluir} encontrada após exclusão: {encontrada}")
        else:
            print("Não há notas restauradas para testar a exclusão.")

    except Exception as e:
        print(f"Erro ao excluir nota: {e}")

    print("\n--- Fim do exemplo ---")
    print("\nHistórico de Acessos Simulados:")
    for entry in banco_dados_mock._historico:
        print(f"  - {entry['data_acesso']} | {entry['tipo_acesso'].ljust(15)} | {entry['nome_arquivo']}")