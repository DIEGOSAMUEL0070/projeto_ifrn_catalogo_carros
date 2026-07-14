import os
import subprocess
import psycopg2
import psycopg2.extras
from psycopg2 import sql

HOST = "localhost"
PORT = "5432"
DB_NAME = "banco_dados_carro"
USER = "postgres"
PASSWORD = "postgres"

def criar_banco():
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname="postgres",
        user=USER,
        password=PASSWORD
    )

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_NAME,)
    )

    if cur.fetchone() is None:
        cur.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_NAME)
            )
        )
        print("Banco criado com sucesso!")
    else:
        print("Banco já existe.")

    cur.close()
    conn.close()

def get_conn():
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD
    )

def criar_tabela():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS 

    """)

    if cur.fetchone()[0] == 0:
        cur.executemany()
    
    cur.execute("SELECT COUNT(*) FROM carro")


def restaurar_backup(arquivo="biblioteca_bck.sql"):
    if not os.path.exits(arquivo):
        print(f"Arquivo '{arquivo}' não encontrado.")
        return
    
    subprocess.run(
        [
            "psql",
            "-h", HOST,
            "-p", PORT,
            "-U", USER,
            "-d", DB_NAME,
            "-f", arquivo
        ],
        env={**os.environ, "PGPASSWORD": PASSWORD},
        check=True
    )

    print("Backup restaurado com sucesso.")

def banco_vazio():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'carro'
        )
    """)

    existe = cur.fetchone()[0]

    cur.close()
    conn.close()

    return not existe

def listar():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM carro ORDER BY id")
    carros = cur.fetchall()
    cur.close()
    conn.close()
    return carros

def buscar(id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM carro WHERE id = %s", (id,))
    carro = cur.fetchone()
    cur.close()
    conn.close()
    return carro

def inserir(ano, marca_id, preco, tipo_cambio_id, tipo_combustivel_id, cor_id, modelo, usuario_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO carro (ano, marca_id, preco, tipo_cambio_id, tipo_combustivel_id, cor_id, modelo, usuario_id) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (ano, marca_id, preco, tipo_cambio_id, tipo_combustivel_id, cor_id, modelo, usuario_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def atualizar(id, ano, marca_id, preco, tipo_cambio_id, tipo_combustivel_id, cor_id, modelo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """UPDATE carro SET ano = %s, marca_id = %s, preco = %s, tipo_cambio_id = %s,
            tipo_combustivel_id = %s, cor_id = %s, modelo = %s 
        WHERE id = %s""",
        (ano, marca_id, preco, tipo_cambio_id, tipo_combustivel_id, cor_id, modelo, id)
    )
    conn.commit()
    cur.close()
    conn.close()

def excluir(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM carro WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

def buscar_usuario_por_login(nome, senha):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM usuario WHERE nome = %s AND senha = %s", (nome, senha))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario

def buscar_usuario_por_nome(nome):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM usuario WHERE nome = %s", (nome,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario

def inserir_usuario(nome, senha, tipo_usuario="cliente"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO usuario (nome, senha, tipo_usuario) VALUES (%s, %s, %s)""",
        (nome, senha, tipo_usuario)
    )
    conn.commit()
    cur.close()
    conn.close()