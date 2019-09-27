from models import Projeto, Funcionario

SQL_DELETA_PROJETO = 'delete from projeto where id = %s'
SQL_PROJETO_POR_ID = 'SELECT id, nome, categoria, descricao from projeto where id = %s'
SQL_FUNCIONARIO_POR_EMAIL = 'SELECT id, nome, email, ra, senha from funcionario where email = %s'
SQL_ATUALIZA_PROJETO = 'UPDATE projeto SET nome=%s, categoria=%s, descricao=%s where id = %s'
SQL_ATUALIZA_FUNCIONARIO = 'UPDATE projeto SET nome=%s, email=%s, ra=%d where id = %s'
SQL_BUSCA_PROJETOS = 'SELECT id, nome, categoria, descricao from projeto'
SQL_REGISTRA_FUNCIONARIO = 'INSERT into funcionario (nome, email, ra) values (%s, %s, %s)'
SQL_REGISTRA_PROJETO = 'INSERT into projeto (nome, categoria, descricao) values (%s, %s, %s)'


class ProjetoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, projeto):
        cursor = self.__db.connection.cursor()

        if (projeto.id):
            cursor.execute(SQL_ATUALIZA_PROJETO, (projeto.nome, projeto.categoria, projeto.descricao, projeto.id))
        else:
            cursor.execute(SQL_REGISTRA_FUNCIONARIO, (projeto.nome, projeto.categoria, projeto.descricao))
            projeto.id = cursor.lastrowid
        self.__db.connection.commit()
        return projeto

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_PROJETOS)
        projetos = traduz_projetos(cursor.fetchall())
        return projetos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PROJETO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Projeto(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_PROJETO, (id, ))
        self.__db.connection.commit()


class FuncionarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_email(self, email):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_FUNCIONARIO_POR_EMAIL, (email,))
        dados = cursor.fetchone()
        funcionario = traduz_funcionario(dados) if dados else None
        return funcionario


def traduz_projetos(projetos):
    def cria_projeto_com_tupla(tupla):
        return Projeto(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_projeto_com_tupla, projetos))


def traduz_funcionario(tupla):
    return Funcionario(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4])
