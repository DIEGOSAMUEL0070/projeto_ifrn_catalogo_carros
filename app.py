from flask import Flask, render_template, request, redirect, url_for, session
import uuid
import re
import model

app = Flask(__name__)
app.secret_key = "fc_company"
    
model.criar_banco()
model.criar_tabela()

# model.criar_banco()
# if model.banco_vazio():
#     model.restaurar_backup("banco_dados_carro_bck.sql") --- Restauração pelo backup

def usuario_logado():
    return session.get("logado", False) and "usuario_id" in session

def gerar_id():
    return str(uuid.uuid4())

def email_valido(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if usuario_logado():
        return redirect(url_for("carros_page"))
    
    erro = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not email_valido(email):
            erro = "Digite um e-mail válido."        
        elif len(senha) < 4 or len(senha) > 20:
            erro = "Senha inválida. A senha deve ter entre 4 e 20 caracteres."
        else:
            usuario = model.buscar_usuario_por_login(email, senha)  

            if usuario:
                session["logado"] = True
                session["usuario_id"] = usuario["id"]
                session["nome"] = usuario["nome"]
                return redirect(url_for("carros_page"))
            else:
                erro = "E-mail ou senha incorretos."             
    return render_template("login.html", erro=erro)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    
    if usuario_logado():
        return redirect(url_for("carros_page"))

    erro = None

    if request.method == "POST":
        nome =  request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not nome or not email or not senha:
            erro = "Nome, e-mail e senha são obrigatórios."
            return render_template("cadastro.html", erro=erro)

        if not email_valido(email):
            erro = "Digite um e-mail válido para o cadastro."
            return render_template("cadastro.html", erro=erro)

        if len(senha) < 4 or len(senha) > 20:
            erro = "Senha inválida. A senha deve ter entre 4 e 20 caracteres."
            return render_template("cadastro.html", erro=erro)

        if model.buscar_usuario_por_email(email):
            erro = "Este e-mail já está cadastrado."
            return render_template("cadastro.html", erro=erro)
        
        model.inserir_usuario(email, senha, nome)
        return redirect(url_for("login"))

    return render_template("cadastro.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home")) 

@app.route("/carros", methods=["GET", "POST"])
def carros_page():

    if not usuario_logado():
        return redirect(url_for("login"))
    
    ano_id = request.args.get("ano")
    marca_id = request.args.get("marca")
    cor_id = request.args.get("cor")
    tipo_cambio_id = request.args.get("tipo_cambio")
    tipo_combustivel_id = request.args.get("tipo_combustivel")

    carros = model.listar(ano_id, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id)
   
    return render_template(
        "carros.html",
        carros = carros,
        anos = model.listar_anos(),
        marcas = model.listar_marcas(),
        cores = model.listar_cores(),
        cambios = model.listar_cambios(),
        combustiveis = model.listar_combustiveis()
    )

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
   
    if not usuario_logado():
        return redirect(url_for("login"))
   
    modelo = request.form.get("modelo", "").strip()
    ano_id = request.form.get("ano")
    preco = request.form.get("preco")
    marca_id = request.form.get("marca")
    cor_id = request.form.get("cor")
    tipo_cambio_id = request.form.get("tipo_cambio")
    tipo_combustivel_id = request.form.get("tipo_combustivel")

    erro_modelo = None
    erro_preco = None
    erro_ano = None
    erro_marca = None
    erro_cor = None
    erro_tipo_cambio = None
    erro_tipo_combustivel = None

    if not modelo or len(modelo) < 2 or len(modelo) >= 100:
        erro_modelo = "Modelo inválido. Deve ter pelo entre 2 e 100 caracteres. Tente novamente!"

    if not preco:
        erro_preco = "O preço é um campo obrigatório."
    else:
        try:
            preco_digitado = float(preco)
            if preco_digitado <= 5000:
                erro_preco = "O preço digitado é inválido. O valor mínimo é de R$ 5.000,00"

            elif preco_digitado > 1000000:
                erro_preco = "O preço digitado é inválido. O valor máximo é de R$ 1.000.000,00"

        except ValueError:
            erro_preco = "O valor digitado é inválido. O preço deve ser um número. Tente novamente!"

    if not ano_id:
        erro_ano = "O ano de fabricação é obrigatório"
    if not marca_id:
        erro_marca = "A marca é obrigatória"
    if not cor_id:
        erro_cor = "A cor do carro é obrigatória"
    if not tipo_cambio_id:
        erro_tipo_cambio = "O tipo de câmbio é obrigatório"
    if not tipo_combustivel_id:
        erro_tipo_combustivel = "O tipo de combustível é obrigatório"
    
    sem_erros = not any(
        [
            erro_modelo, erro_preco, erro_ano, erro_marca, erro_cor, erro_tipo_cambio, erro_tipo_combustivel
        ]
    )

    if sem_erros:
        model.inserir(
            gerar_id(), modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id, session["usuario_id"]
        )
        return redirect(url_for("carros_page"))
   
    return render_template(
        "carros.html",
        carros = model.listar(), 
        anos = model.listar_anos(),
        marcas = model.listar_marcas(),
        cores = model.listar_cores(),
        cambios = model.listar_cambios(),
        combustiveis = model.listar_combustiveis(),

        erro_modelo=erro_modelo,
        erro_preco=erro_preco,
        erro_ano=erro_ano,
        erro_marca=erro_marca,
        erro_cor=erro_cor,
        erro_tipo_cambio=erro_tipo_cambio,
        erro_tipo_combustivel=erro_tipo_combustivel,

        valor_modelo=modelo,
        valor_ano=ano_id,
        valor_preco=preco,
        valor_marca=marca_id,
        valor_cor=cor_id,
        valor_tipo_cambio=tipo_cambio_id,
        valor_tipo_combustivel=tipo_combustivel_id
    )

@app.route("/editar/<string:id>", methods=["GET", "POST"])
def editar(id):

    if not usuario_logado():
        return redirect(url_for("login"))

    carro = model.buscar(id)

    if not carro:
        return redirect(url_for("carros_page"))

    erro_modelo = None
    erro_preco = None
    erro_ano = None
    erro_marca = None
    erro_cor = None
    erro_tipo_cambio = None
    erro_tipo_combustivel = None

    if request.method == "POST":

        modelo = request.form.get("modelo", "").strip()
        ano_id = request.form.get("ano")
        preco = request.form.get("preco")
        marca_id = request.form.get("marca")
        cor_id = request.form.get("cor")
        tipo_cambio_id = request.form.get("tipo_cambio")
        tipo_combustivel_id = request.form.get("tipo_combustivel")
       
        if not modelo or len(modelo) < 2 or len(modelo) >= 100:
            erro_modelo = "Modelo inválido. Deve ter entre 2 e 100 caracteres. Tente novamente!"

        if not preco:
            erro_preco = "O preço é obrigatório"
        else:
            try:
                preco_digitado = float(preco)
                if preco_digitado <= 5000:
                    erro_preco = "O preço digitado é inválido. O valor mínimo é de R$ 5.000,00."

                elif preco_digitado > 1000000:
                    erro_preco = "O preço digitado é inválido. O valor máximo é de R$ 1.000.000,00"

            except ValueError:
                erro_preco = "O valor digitado é inválido. O preço deve ser um número. Tente novamente!"
            
        if not ano_id:
            erro_ano = "O ano de fabricação é obrigatório"
        if not marca_id:
            erro_marca = "A marca é obrigatória"
        if not cor_id:
            erro_cor = "A cor do carro é obrigatória"
        if not tipo_cambio_id:
            erro_tipo_cambio = "O tipo de câmbio é obrigatório"
        if not tipo_combustivel_id:
            erro_tipo_combustivel = "O tipo de combustível é obrigatório"
        
        sem_erros = not any(
            [
                erro_modelo, erro_preco, erro_ano, erro_marca, erro_cor, erro_tipo_cambio, erro_tipo_combustivel
            ]
        )

        if sem_erros:
            model.atualizar(
                id, modelo, ano_id, preco, marca_id, cor_id, tipo_cambio_id, tipo_combustivel_id
            )
            return redirect(url_for("carros_page"))

    return render_template(
        "editar.html",
        carro = carro,
        anos = model.listar_anos(),
        marcas = model.listar_marcas(),
        cores = model.listar_cores(),
        cambios = model.listar_cambios(),
        combustiveis = model.listar_combustiveis(),

        erro_modelo = erro_modelo,
        erro_preco = erro_preco,
        erro_ano = erro_ano,
        erro_marca = erro_marca,
        erro_cor = erro_cor,
        erro_tipo_cambio = erro_tipo_cambio,
        erro_tipo_combustivel = erro_tipo_combustivel
    )

@app.route("/excluir/<string:id>")
def deletar(id):

    if not usuario_logado():
        return redirect(url_for("login"))
    
    model.excluir(id)
    return redirect(url_for("carros_page"))


@app.route("/gerenciar")
def gerenciar():
   
    if not usuario_logado():
        return redirect(url_for("login"))

    return render_template(
        "gerenciar.html",
        anos = model.listar_anos(),
        cores = model.listar_cores(),
        cambios = model.listar_cambios(),
        marcas = model.listar_marcas(),
        combustiveis = model.listar_combustiveis()
    )

if __name__ == "__main__":
    app.run(debug=True)