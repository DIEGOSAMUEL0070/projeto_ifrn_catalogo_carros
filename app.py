from flask import Flask, render_template, request, redirect, url_for, session
import uuid
import json
from datetime import datetime
import os
import re
import model

app = Flask(__name__)

model.criar_banco()
model.criar_tabela()

@app.route("/")
def index():
    carros = model.listar()
    return render_template("carros.html", carros=carros)

# @app.route("/novo")
# def novo():
#     return render_template("editar.html", carros=None) --- Não vai ser usado, pois é criado dentro de uma mesma página

@app.route("/editar/<int:id>")
def editar(id):
    carro = model.buscar(id)
    return render_template("editar.html", carro=carro)

@app.route("/inserir", methods=["POST"])
def inserir():
    ano = request.form["ano"]
    marca_id = request.form["marca_id"]
    preco = request.form["preco"].strip()
    tipo_cambio_id = request.form
    tipo_combustivel_id = request.form["tipo_combustivel_id"]
    cor_id = request.form["cor_id"]
    modelo = request.form["modelo"].strip()
    usuario_id = request.form["usuario_id"]

    model.inserir(ano, marca_id, preco, tipo_cambio_id, tipo_combustivel_id, cor_id, modelo, usuario_id)
    return redirect("/")

@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    ano = request.form["ano"]
    marca_id = request.form["marca_id"]
    preco = request.form["preco"].strip()
    tipo_cambio_id = request.form
    tipo_combustivel_id = request.form["tipo_combustivel_id"]
    cor_id = request.form["cor_id"]
    modelo = request.form["modelo"].strip()
    usuario_id = request.form["usuario_id"]

    model.atualizar(id, ano, marca_id, preco, tipo_cambio_id, tipo_combustivel_id, cor_id, modelo, usuario_id)
    return redirect("/")

@app.route("/excluir/<int:id>")
def excluir(id):
    model.excluir(id)
    return redirect("/")

app.secret_key = "fc_company"

CARROS_FILE = "database/carros_cadastrados.json"
CAMBIOS_FILE = "database/cambio.json"
MARCAS_FILE = "database/marca.json"
TIPO_COMBUSTIVEL_FILE = "database/tipo_combustivel.json"
CORES_FILE = "database/cor.json"
ANOS_FILE = "database/anos.json"
USUARIOS_FILE = "database/usuarios.json"

def carregar_json(arquivo):
    if not os.path.exists(arquivo):
        return []
   
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)
   
def salvar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
        
ano_atual = datetime.now().year

anos = list(range(ano_atual, 1900, -1))
carros = carregar_json(CARROS_FILE)
cambios = carregar_json(CAMBIOS_FILE)
marcas = carregar_json(MARCAS_FILE)
combustiveis = carregar_json(TIPO_COMBUSTIVEL_FILE)
cores = carregar_json(CORES_FILE)
usuarios = carregar_json(USUARIOS_FILE)

if not cambios:
    cambios = [
        "Automático",
        "Manual"
    ]

    salvar_json(CAMBIOS_FILE, cambios)

if not marcas:
    marcas = [
        "Chevrolet",
        "Fiat",
        "Ford",
        "Hyundai",
        "Toyota",
        "Volkswagen",
        "Ferrari"
    ]

    salvar_json(MARCAS_FILE, marcas)

if not combustiveis:
    combustiveis = [
        "Gasolina",
        "Etanol",
        "Diesel",
        "Híbrido",
        "Elétrico"
    ]

    salvar_json(TIPO_COMBUSTIVEL_FILE, combustiveis)

if not cores:
    cores = [
        "Branco",
        "Preto",
        "Prata",
        "Cinza",
        "Vermelho"
    ]

    salvar_json(CORES_FILE, cores)

if not anos:
    anos = [
        str(ano) for ano in range(2001, 2020)
    ]

    salvar_json(ANOS_FILE, anos)

def usuario_logado():
    return session.get("logado", False) and "email" in session

def gerar_id():
    return str(uuid.uuid4())

def buscar_carro(id):
    return next((carro for carro in carros if carro["id"] == id), None)

def autenticar_usuario(email, senha):
    for user in usuarios:
        if user.get("email") == email and user.get("senha") == senha:
            return True
    return False

@app.route("/")
def home():
    return render_template("home.html")
   
@app.route("/login", methods=["GET", "POST"])
def login():

    def email_valido(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    email = request.form.get("email", "")
    senha = request.form.get("senha", "")
    erro = None

    if not email_valido(email):
        erro = "Digite um e-mail válido."
        
    elif len(senha) < 4 or len(senha) > 20:
        erro = "Senha inválida. A senha deve ter entre 4 e 20 caracteres."
        
    else:
        if autenticar_usuario(email, senha):
            session["logado"] = True
            session["email"] = email
            return redirect(url_for("carros_page"))
        else:
            erro = "Usuário ou senha incorretos."
            
    return render_template("login.html", erro=erro)@app.route("/login", methods=["GET", "POST"])

def login():
    if usuario_logado():
        return redirect(url_for("carros_page"))

    def email_valido(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    erro = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not email_valido(email):
            erro = "Digite um e-mail válido."
        elif len(senha) < 4 or len(senha) > 20:
            erro = "Senha inválida. A senha deve ter entre 4 e 20 caracteres."
        else:
            if autenticar_usuario(email, senha):
                session["logado"] = True
                session["email"] = email 
                return redirect(url_for("carros_page"))
            else:
                erro = "E-mail ou senha incorretos."

    return render_template("login.html", erro=erro)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if usuario_logado():
        return redirect(url_for("carros_page"))

    def email_valido(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    erro = None

    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        senha = (request.form.get("senha") or "").strip()

        if not email or not senha:
            erro = "E-mail e senha são obrigatórios."
            return render_template("cadastro.html", erro=erro)

        if not email_valido(email):
            erro = "Digite um e-mail válido para o cadastro."
            return render_template("cadastro.html", erro=erro)

        if len(senha) < 4 or len(senha) > 20:
            erro = "Senha inválida. A senha deve ter entre 4 e 20 caracteres."
            return render_template("cadastro.html", erro=erro)

        for user in usuarios:
            if user.get("email") == email:
                erro = "Este e-mail já está cadastrado."
                return render_template("cadastro.html", erro=erro)

        usuarios.append({
            "email": email,
            "senha": senha
        })
        salvar_json(USUARIOS_FILE, usuarios)
        return redirect(url_for("login"))

    return render_template("cadastro.html", erro=erro)

@app.route("/carros", methods=["GET"])
def carros_page():

    if not usuario_logado():
        return redirect(url_for("login"))
    
    cor_id = request.form.get("cor")
    tipo_cambio_id = request.form.get("tipo_cambio")
    marca_id = request.form.get("marca")
    tipo_combustivel_id = request.form.get("tipo_combustivel")

    carros_filtrados = carros

    if tipo_cambio_id:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["tipo_cambio"] == tipo_cambio_id
        ]
   
    if marca_id:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["marca"] == marca_id
        ]
   
    if tipo_combustivel_id:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["tipo_combustivel"] == tipo_combustivel_id
        ]
   
    if cor_id:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["cor"] == cor_id
        ]
   
    return render_template(
        "carros.html",
        anos = anos,
        cores = cores,
        carros = carros_filtrados,
        cambios = cambios,
        marcas = marcas,
        combustiveis = combustiveis
    )

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
   
    if not usuario_logado():
        return redirect(url_for("login"))
   
    modelo = request.form.get("modelo")
    ano = request.form.get("ano")
    preco = request.form.get("preco")
    cor = request.form.get("cor")
    tipo_cambio = request.form.get("tipo_cambio")
    marca = request.form.get("marca")
    tipo_combustivel = request.form.get("tipo_combustivel")
    erro_modelo = None
    erro_preco = None

    if modelo:
        nome = modelo.strip()
        if len(nome) < 2 or len(nome) >= 100:
            erro_modelo = "Modelo inválido. Deve ter pelo entre 2 e 100 caracteres. Tente novamente!"
            nome = None

    if preco:
        try:
            preco_digitado = float(preco)
            if preco_digitado <= 5000:
                erro_preco = "O preço digitado é inválido. O valor mínimo é de R$ 5.000,00."
                preco = None

            elif preco_digitado > 1000000:
                erro_preco = "O preço digitado é inválido. O valor máximo é de R$ 1.000.000,00"
                preco = None

        except ValueError:
            erro_preco = "O valor digitado é inválido. O preço deve ser um número. Tente novamente!"
            preco = None

    if modelo and preco:
        if not ano:
            ano = "Não informado"
        if not cor_id:
            cor_id = "Não informada"
        if not tipo_cambio_id:
            tipo_cambio_id = "Não informado"
        if not marca_id:
            marca_id = "Não informada"
        if not tipo_combustivel_id:
            tipo_combustivel_id = "Não informado"
           
        carros.append({
            "id": gerar_id(),
            "modelo": modelo,
            "ano": ano if ano else "Não informado",
            "preco": preco,
            "cor_id": int(cor_id) if cor_id else None,
            "tipo_cambio_id": int(tipo_cambio_id) if tipo_cambio_id else None,
            "marca_id": int(marca_id) if marca_id else None,
            "tipo_combustivel_id": int(tipo_combustivel_id) if tipo_combustivel_id else None,
        })

        salvar_json(CARROS_FILE, carros)
        return redirect(url_for("carros_page"))
   
    return render_template(
        "carros.html",
        anos=anos,
        cores=cores,
        cambios=cambios,
        marcas=marcas,
        combustiveis=combustiveis,
        carros=carros,
        erro_modelo=erro_modelo,
        erro_preco=erro_preco,
        valor_modelo=modelo,
        valor_ano=ano,
        valor_preco=preco,
        valor_cor=cor,
        valor_tipo_cambio=tipo_cambio,
        valor_marca=marca,
        valor_tipo_combustivel=tipo_combustivel
    )

@app.route("/deletar/<string:id>")
def deletar(id):
   
    if not usuario_logado():
        return redirect(url_for("login"))
   
    carro = buscar_carro(id)
    if carro:
        carros.remove(carro)

        salvar_json(CARROS_FILE, carros)
    return redirect(url_for("carros_page"))

@app.route("/editar/<string:id>", methods=["GET", "POST"])
def editar(id):

    carro = buscar_carro(id)

    if not carro:
        return redirect(url_for("carros_page"))

    erro_modelo = None
    erro_preco = None

    if request.method == "POST":

        modelo = request.form.get("modelo")
        ano = request.form.get("ano")
        preco = request.form.get("preco")
        cor = request.form.get("cor")
        tipo_cambio = request.form.get("tipo_cambio")
        marca = request.form.get("marca")
        tipo_combustivel = request.form.get("tipo_combustivel")

        if modelo:
            modelo = modelo.strip()
       
        if not modelo or len(modelo) < 2 or len(modelo) >= 100:
            erro_modelo = "Modelo inválido. Deve ter entre 2 e 100 caracteres. Tente novamente!"
            modelo = None

        if preco:
            try:
                preco_digitado = float(preco)
                if preco_digitado <= 5000:
                    erro_preco = "O preço digitado é inválido. O valor mínimo é de R$ 5.000,00."
                    preco = None

                elif preco_digitado > 1000000:
                    erro_preco = "O preço digitado é inválido. O valor máximo é de R$ 1.000.000,00"
                    preco = None

            except ValueError:
                erro_preco = "O valor digitado é inválido. O preço deve ser um número. Tente novamente!"
                preco = None
        else:
            erro_preco = "O Preço é obrigatório."

        if not erro_modelo and not erro_preco:

            carro["modelo"] = modelo
            carro["ano"] = ano if ano else "Não informado"
            carro["preco"] = preco
            carro["cor_id"] = int(cor) if cor else None
            carro["tipo_cambio_id"] = int(tipo_cambio) if tipo_cambio else None
            carro["marca_id"] = int(marca) if marca else None
            carro["tipo_combustivel_id"] = int(tipo_combustivel) if tipo_combustivel else None

            salvar_json(CARROS_FILE, carros)

            return redirect(url_for("carros_page"))

    return render_template(
        "editar.html",
        carro=carro,
        anos=anos,
        cores=cores,
        cambios=cambios,
        marcas=marcas,
        combustiveis=combustiveis,
        erro_modelo=erro_modelo,
        erro_preco=erro_preco
    )

@app.route("/gerenciar")
def gerenciar():
   
    if not usuario_logado():
        return redirect(url_for("login"))

    return render_template(
        "gerenciar.html",
        cores=cores,
        cambios=cambios,
        marcas=marcas,
        combustiveis=combustiveis
    )

@app.route("/logout")
def logout():
    session.pop("logado", None)
    session.pop("email", None)
    return redirect(url_for("home")) 

if __name__ == "__main__":
    app.run(debug=True)
