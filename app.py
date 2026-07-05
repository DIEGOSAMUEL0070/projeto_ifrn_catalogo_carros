from flask import Flask, render_template, request, redirect, url_for, session
import uuid
import json
import os
# import model (Para a conexão do BD posteriormente)

app = Flask(__name__)

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

carros = carregar_json(CARROS_FILE)
cambios = carregar_json(CAMBIOS_FILE)
marcas = carregar_json(MARCAS_FILE)
combustiveis = carregar_json(TIPO_COMBUSTIVEL_FILE)
cores = carregar_json(CORES_FILE)
anos = carregar_json(ANOS_FILE)
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
    return session.get("usuario")

def gerar_id():
    return str(uuid.uuid4())

def buscar_carro(id):
    return next((carro for carro in carros if carro["id"] == id), None)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():

    erro = None

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario:
            usuario = usuario.strip()
        if senha:
            senha = senha.strip()
        if usuario and (len(usuario) < 3 or len(usuario) > 40):
            erro = "Usuário inválido. O nome deve ter entre 3 e 40 caracteres."

        elif senha and (len(senha) < 4 or len(senha) > 20):
            erro = "Senha inválida. A senha deve ter entre 4 e 20 caracteres."
        else:
            for user in usuarios:

                if (
                    user["usuario"] == usuario
                    and
                    user["senha"] == senha
                ):

                    session["usuario"] = usuario

                    return redirect(url_for("carros_page"))

            erro = "Usuário ou senha inválidos"

    return render_template(
        "login.html",
        erro=erro
    )
    
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    erro = None

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario:
            usuario = usuario.strip()
        if senha:
            senha = senha.strip()

        if usuario and (len(usuario) < 3 or len(usuario) > 40):
            erro = "Usuário inválido. O nome deve ter entre 3 e 40 caracteres."
            return render_template(
                "cadastro.html",
                erro=erro
            )
        
        if senha and (len(senha) < 4 or len(senha) > 20):
            erro = "Senha inválida. A senha deve ter entre 4 e 20 caracteres."
            return render_template(
                "cadastro.html",
                erro=erro
            )

        for user in usuarios:

            if user["usuario"] == usuario:

                erro = "Usuário já existe"

                return render_template(
                    "cadastro.html",
                    erro=erro
                )

        usuarios.append({
            "usuario": usuario,
            "senha": senha
        })

        salvar_json(
            USUARIOS_FILE,
            usuarios
        )

        return redirect(url_for("home"))

    return render_template(
        "cadastro.html",
        erro=erro
    )

@app.route("/carros", methods=["GET"])
def carros_page():

    if not usuario_logado():
        return redirect(url_for("login"))
    ano = request.args.get("ano")
    tipo_cambio = request.args.get("tipo_cambio")
    marca = request.args.get("marca")
    tipo_combustivel = request.args.get("tipo_combustivel")
    cor = request.args.get("cor")

    carros_filtrados = carros

    if ano:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["ano"] == ano
        ]

    if tipo_cambio:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["tipo_cambio"] == tipo_cambio
        ]
    
    if marca:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["marca"] == marca
        ]
    
    if tipo_combustivel:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["tipo_combustivel"] == tipo_combustivel
        ]
    
    if cor:
        carros_filtrados = [
            carro for carro in carros_filtrados
            if carro["cor"] == cor
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
        if len(nome) < 10 or len(nome) >= 100:
            erro_modelo = "Modelo inválido. Deve ter pelo entre 10 e 100 caracteres. Tente novamente!"
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
        if not cor:
            cor = "Não informada"
        if not tipo_cambio:
            tipo_cambio = "Não informado"
        if not marca:
            marca = "Não informada"
        if not tipo_combustivel:
            tipo_combustivel = "Não informado"
            
        carros.append({
            "id": gerar_id(),
            "modelo": modelo,
            "ano": ano,
            "preco": preco,
            "cor": cor,
            "tipo_cambio": tipo_cambio,
            "marca": marca,
            "tipo_combustivel": tipo_combustivel,
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
        
        if not modelo or len(modelo) < 10 or len(modelo) >= 100:
            erro_modelo = "Modelo inválido. Deve ter entre 10 e 100 caracteres. Tente novamente!"
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
            carro["ano"] = ano
            carro["preco"] = preco
            carro["cor"] = cor
            carro["tipo_cambio"] = tipo_cambio
            carro["marca"] = marca
            carro["tipo_combustivel"] = tipo_combustivel

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

    return render_template(
        "gerenciar.html",
        cores=cores,
        cambios=cambios,
        marcas=marcas,
        combustiveis=combustiveis
    )
    
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)