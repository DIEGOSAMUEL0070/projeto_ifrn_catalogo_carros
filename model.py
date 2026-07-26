import os
import subprocess
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from datetime import datetime

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
        CREATE TABLE IF NOT EXISTS anos (
            id SERIAL PRIMARY KEY,
            ano INTEGER NOT NULL UNIQUE
        );
    """) 

    cur.execute("""
        CREATE TABLE IF NOT EXISTS marcas (
            id SERIAL PRIMARY KEY, 
            nome VARCHAR(100) NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cores (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cambios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS combustiveis (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            email VARCHAR(150) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL,
            nome VARCHAR(100) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS carros (
            id VARCHAR(36) PRIMARY KEY,
            modelo VARCHAR(100) NOT NULL,
            ano_id INTEGER,
            preco DECIMAL(10, 2) NOT NULL,
            marca_id INTEGER,
            cor_id INTEGER,
            tipo_cambio_id INTEGER,
            tipo_combustivel_id INTEGER,
            usuario_id INTEGER,
            
            FOREIGN KEY (ano_id) REFERENCES anos(id) ON DELETE SET NULL,
            FOREIGN KEY (marca_id) REFERENCES marcas(id) ON DELETE SET NULL,
            FOREIGN KEY (cor_id) REFERENCES cores(id) ON DELETE SET NULL,
            FOREIGN KEY (tipo_cambio_id) REFERENCES cambios(id) ON DELETE SET NULL,
            FOREIGN KEY (tipo_combustivel_id) REFERENCES combustiveis(id) ON DELETE SET NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
        );
    """)

    ano_atual = datetime.now().year
    anos_para_inserir = [(ano,) for ano in range(2001, ano_atual+1)]

    cur.executemany(
        "INSERT INTO anos (ano) VALUES (%s) ON CONFLICT (ano) DO NOTHING",
        anos_para_inserir
    )

    cur.execute("SELECT COUNT(*) FROM marcas")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO marcas (nome) VALUES (%s)",
            [
                ("Chevrolet",),
                ("Fiat",),
                ("Ford",), 
                ("Hyundai",),
                ("Toyota",), 
                ("Volkswagen",), 
                ("Ferrari",)
            ]
        )
    
    cur.execute("SELECT COUNT(*) FROM cores")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO cores (nome) VALUES (%s)",
            [
                ("Branco",),
                ("Preto",),
                ("Prata",),
                ("Cinza",),
                ("Vermelho",)
            ]
        )

    cur.execute("SELECT COUNT(*) FROM cambios")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO cambios (nome) VALUES (%s)",
            [
                ("Manual",),
                ("Automático",)
            ]
        )
   
    
    cur.execute("SELECT COUNT(*) FROM combustiveis")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO combustiveis (nome) VALUES (%s)",
            [
                ("Gasolina",),
                ("Etanol",),
                ("Diesel",),
                ("Híbrido",),
                ("Elétrico",)
            ]
        )
    
    conn.commit()
    cur.close()
    conn.close()

    print("Tabelas criadas e dados iniciais inseridos")


def restaurar_backup(arquivo="banco_dados_carro_bck.sql"):
    if not os.path.exists(arquivo):
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
              AND table_name = 'carros'
        )
    """)

    existe = cur.fetchone()[0]

    cur.close()
    conn.close()

    return not existe

def listar_anos():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM anos ORDER BY id")
    anos = cur.fetchall()
    cur.close()
    conn.close()
    return anos

def listar_marcas():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM marcas ORDER BY id")
    marcas = cur.fetchall()
    cur.close()
    conn.close()
    return marcas

def listar_cores():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM cores ORDER BY id")
    cores = cur.fetchall()
    cur.close()
    conn.close()
    return cores

def listar_cambios():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM cambios ORDER BY id")
    cambios = cur.fetchall()
    cur.close()
    conn.close()
    return cambios

def listar_combustiveis():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM combustiveis ORDER BY id")
    combustiveis = cur.fetchall()
    cur.close()
    conn.close()
    return combustiveis

def listar(ano_id=None, marca_id=None, cor_id=None, tipo_cambio_id=None, tipo_combustivel_id=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """
        SELECT
            carros.id,
            carros.modelo,
            carros.preco,
            anos.ano,
            marcas.nome AS marca,
            cores.nome AS cor,
            cambios.nome AS cambio,
            combustiveis.nome AS combustivel
        FROM carros
        LEFT JOIN anos ON carros.ano_id = anos.id
        LEFT JOIN marcas ON carros.marca_id = marcas.id
        LEFT JOIN cores ON carros.cor_id = cores.id
        LEFT JOIN cambios ON carros.tipo_cambio_id = cambios.id
        LEFT JOIN combustiveis ON carros.tipo_combustivel_id = combustiveis.id
        WHERE TRUE
    """
    valores = []

    if ano_id:
        query += " AND carros.ano_id = %s"
        valores.append(ano_id)
    if marca_id:
        query += " AND carros.marca_id = %s"
        valores.append(marca_id)
    if cor_id:
        query += " AND carros.cor_id = %s"
        valores.append(cor_id)
    if tipo_cambio_id:
        query += " AND carros.tipo_cambio_id = %s"
        valores.append(tipo_cambio_id)
    if tipo_combustivel_id:
        query += " AND carros.tipo_combustivel_id = %s"
        valores.append(tipo_combustivel_id)
    query += " ORDER BY modelo"

    cur.execute(query, valores)
    carros = cur.fetchall()
    cur.close()
    conn.close()
    return carros

def buscar(id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM carros WHERE id = %s", (id,))
    carro = cur.fetchone()
    cur.close()
    conn.close()
    return carro

def inserir(id, modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id, usuario_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO carros (id, modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id, usuario_id) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (id, modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id, usuario_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def atualizar(id, modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """UPDATE carros SET modelo = %s, ano_id = %s, preco = %s, marca_id = %s,
            cor_id = %s, tipo_cambio_id = %s, tipo_combustivel_id = %s 
        WHERE id = %s""",
        (modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id, id)
    )
    conn.commit()
    cur.close()
    conn.close()

def excluir(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM carros WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

def buscar_usuario_por_login(email, senha):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario

def buscar_usuario_por_email(email):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario

def inserir_usuario(email, senha, nome):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO usuarios (email, senha, nome) VALUES (%s, %s, %s)""",
        (email, senha, nome)
    )
    conn.commit()
    cur.close()
    conn.close()