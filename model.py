# Arquivo para o BD posterior
# import os
# import subprocess
import psycopg2
import psycopg2.extras
from psycopg2 import sql

HOST = "localhost"
PORT = "5432"
DB_NAME = "banco_dados_carro"
USER = "postgres"
PASSWORD = "postgres"

def get_conn():
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD
    )

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

    cur.execute(
        "SELECT * FROM carro WHERE id = %s",
        (id,)
    )

    carro = cur.fetchone()

    cur.close()
    conn.close()

    return carro

def inserir(ano, marca, preco, tipo_cambio, tipo_combustivel, modelo, usuario_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO carro (ano, marca, preco, tipo_cambio, tipo_combustivel, modelo, usuario_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (ano, marca, preco, tipo_cambio, tipo_combustivel, modelo, usuario_id)
    )

    conn.commit()
    cur.close()
    conn.close()

def atualizar(id, ano, marca, preco, tipo_cambio, tipo_combustivel, modelo):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """UPDATE carro SET ano = %s, marca = %s, preco = %s, tipo_cambio = %s,
            tipo_combustivel = %s, modelo = %s 
        WHERE id = %s""",
        (ano, marca, preco, tipo_cambio, tipo_combustivel, modelo, id)
    )

    conn.commit()
    cur.close()
    conn.close()

def excluir(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM carro WHERE id = %s",
        (id,)
    )

    conn.commit()
    cur.close()
    conn.close()


def buscar_usuario_por_login(nome, senha):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT * FROM usuario WHERE nome = %s AND senha = %s",
        (nome, senha)
    )

    usuario = cur.fetchone()

    cur.close()
    conn.close()

    return usuario

def buscar_usuario_por_nome(nome):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT * FROM usuario WHERE nome = %s",
        (nome,)
    )

    usuario = cur.fetchone()

    cur.close()
    conn.close()

    return usuario

def inserir_usuario(nome, senha, tipo_usuario="cliente"):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO usuario (nome, senha, tipo_usuario)
            VALUES (%s, %s, %s)""",
        (nome, senha, tipo_usuario)
    )

    conn.commit()
    cur.close()
    conn.close()