# SABER 

### Sistema de Assistência de Biblioteca e de Empréstimo Regional

Sistema de Empréstimo de livros desenvolvido como projeto da disciplina de Tópicos Específicos II.

## Objetivo

O sistema permite o cadastro, edição, exclusão, filtragem e gerenciamento de livros utilizando o banco de dados PostgreSQL.

Além disso, possui um sistema de login e cadastro de usuários, possibilitando o 

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
- Cadastro de livros
- Edição das informações dos livros
- Exclusão de livros
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
├── banco_dados_carro_bck.sql
├── templates/
│ ├── login.html
│ ├── cadastro.html
│ ├── carros.html
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