import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='mitech_user', passwd='mitech2014', host='localhost', port=3306)

# Descomente se quiser desfazer o banco...
conn.cursor().execute("DROP DATABASE `mitech`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `mitech` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `mitech`;
    CREATE TABLE `projeto` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `categoria` varchar(40) COLLATE utf8_bin NOT NULL,
      `descricao` varchar(500) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `funcionario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `email` varchar(50) COLLATE utf8_bin NOT NULL,
      `ra` varchar(8) COLLATE utf8_bin NOT NULL,
      `senha` varchar(20) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo funcionarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO mitech.funcionario (id, nome, email, ra, senha) VALUES (%s, %s, %s, %s, %s)',
      [
            ('hiro', 'Hiro', 'rhiroakidata@gmail.com', '11042714', 'mitech2014')
      ])

cursor.execute('select * from mitech.funcionario')
print(' -------------  Funcionarios:  -------------')
for funcionario in cursor.fetchall():
    print(funcionario[1])

# inserindo projetos
cursor.executemany(
      'INSERT INTO mitech.projeto (nome, categoria, descricao) VALUES (%s, %s, %s)',
      [
            ('TG', 'Pessoas', 'Detectar numero de pessoas')
      ])

cursor.execute('select * from mitech.projeto')
print(' -------------  Projetos:  -------------')
for projeto in cursor.fetchall():
    print(projeto[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()