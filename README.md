# FC Company

Sistema de Catálogo de Carros desenvolvido como projeto da disciplina de Programação de Aplicação Web.

## Objetivo

O sistema permite o cadastro, edição, exclusão, filtragem e gerenciamento de carros utilizando o banco de dados PostgreSQL.

Além disso, possui um sistema de login e cadastro de usuários.

## Algumas Tecnologias utilizadas

- Python
- Flask
- HTML5
- CSS3
- PostgreSQL
- psycopg2

---

## Funcionalidades
- Cadastro de usuários
- Login
- Cadastro de carros
- Edição das informações dos carros
- Exclusão de carros
- Filtros por:
    - Ano
    - Marca
    - Cor
    - Câmbio
    - Combustível

---

## Estrutura do Projeto

```Projeto/
│
├── app.py
├── model.py
├── templates/
│ ├── login.html
│ ├── cadastro.html
│ ├── carros.html
│ ├── gerenciar.html
│ ├── header.html
│ ├── cadastrar_carro.html
│ └── editar.html
│
├── static/
│ ├── style.css
│ ├── FC Company - Planejamento de Banco de Dados.md
│ └── fundo.png
│
└── README.md
```

## Como Executar

1. Instale o Pythnon.

2. Instale as dependências:

```bash
pip install flask psycopg2
```

3. Configure o PostgreSQL.

4. Ajuste as credenciais no arquivo model.py.

5. Execute:

```
python app.py
```

6. Abra o navegador em: 

```
http://127.0.0.1:5000
```

## Banco de Dados

O projeto cria automaticamente o banco de dados e as tabelas quando executado pela primeira vez.

## Autores

Diego José Araújo Santos, Diego Samuel Soares Pereira de Araújo, Paulo Henrique Ferreira Marques e Thalys Rafael de Brito Batalha