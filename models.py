class Projeto:
    def __init__(self, nome, categoria, descricao, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.descricao = descricao

class Funcionario:
    def __init__(self, id, nome, email, ra, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.ra = ra
        self.senha = senha