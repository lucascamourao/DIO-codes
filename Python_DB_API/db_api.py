import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

# extensão .db é melhor, mas o padrão do SQLite Viewer é a extensão .sqlite
conexao = sqlite3.connect(ROOT_PATH / "meu_banco.sqlite")
# print(conexao)
cursor = conexao.cursor()
# cursor.row_factory = sqlite3.Row
# deixar a row factory do sistema padrão: sempre vai retornar dicionário


def criar_tabela(conexao, cursor):
    cursor.execute(
        "CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))"
    )
    conexao.commit()  # não precisa (deixar padrão)


def inserir_registro(conexao, cursor, nome, email):
    # Para evitar inserção de SQL indesejado e insegurança, utiliza-se ? nos campos.
    data = (nome, email)
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?);", data)
    conexao.commit()  # não esquecer


def atualizar_registro(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute("UPDATE clientes SET nome=?, email=? WHERE id=?;", data)
    conexao.commit()


def excluir_registro(conexao, cursor, id):
    data = (id,)
    cursor.execute("DELETE FROM clientes WHERE id=?", data)
    conexao.commit()


def inserir_muitos(conexao, cursor, dados):
    cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?, ?);", dados)
    conexao.commit()
    # Faz um commit só, ao invés de vários (FOR)


def recuperar_cliente(cursor, id):
    cursor.row_factory = sqlite3.Row
    # retorna o objeto e pode transformar em dicionário
    cursor.execute("SELECT * FROM clientes WHERE id=?;", (id,))
    return cursor.fetchone()


def listar_clientes(cursor):
    return cursor.execute("SELECT * FROM clientes;")


# atualizar_registro(conexao, cursor, "Lucas20 gamer", "lucas20gamer@gmail.com", 1)
# excluir_registro(conexao, cursor, 1)
"""
dados = [
    ("Lucas", "lucas@gmail.com"),
    ("João", "joao@gmail.com"),
    ("Tony", "tony@gmail.com"),
] """

# inserir_muitos(conexao, cursor, dados)

clientes = listar_clientes(cursor)
for cliente in clientes:
    print(cliente)

cliente = recuperar_cliente(cursor, 2)
print(dict(cliente))
print(cliente["id"], cliente["nome"])

print(f"Seja bem vindo, {cliente["nome"]}")

try: 
    cursor.execute("DELETE FROM clientes WHERE id=10;")
    cursor.execute("INSERT INTO clientes (id, nome, email) VALUES (?, ?, ?);", (2, "Luke", "luke@gmail.com"))
    conexao.commit()
except Exception as e:
    print(f"Erro: {e}")
    conexao.rollback() 
