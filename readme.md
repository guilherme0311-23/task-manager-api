# Task Manager API

API REST desenvolvida em Python utilizando FastAPI para gerenciamento de tarefas.  
O projeto implementa um CRUD completo com persistência em banco de dados SQLite utilizando SQLAlchemy.

Este projeto foi desenvolvido com o objetivo de praticar conceitos fundamentais de backend, como arquitetura de APIs, manipulação de banco de dados, validação de dados e versionamento com Git.

---

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Git / GitHub

---

## Funcionalidades

A API permite:

- Criar tarefas
- Listar tarefas
- Buscar tarefa por ID
- Atualizar tarefas
- Deletar tarefas
- Marcar tarefa como concluída

---

## Estrutura do projeto


task-manager-api
│
├── app
│ ├── main.py # rotas da API
│ ├── database.py # configuração do banco
│ ├── models.py # definição das tabelas
│ ├── schemas.py # validação de dados
│ └── storage.py # operações no banco
│
├── requirements.txt
└── app.db


---

## Instalação

Clone o repositório:


git clone https://github.com/guilherme0311-23/task-manager-api.git


Entre na pasta:


cd task-manager-api


Crie o ambiente virtual:


python -m venv .venv


Ative o ambiente virtual:

Windows:


.venv\Scripts\activate


Linux / Mac:


source .venv/bin/activate


Instale as dependências:


pip install -r requirements.txt


---

## Executando a API

Inicie o servidor:


uvicorn app.main:app --reload


A API estará disponível em:


http://127.0.0.1:8000


---

## Documentação automática

FastAPI gera automaticamente a documentação da API.

Swagger UI:


http://127.0.0.1:8000/docs


ReDoc:


http://127.0.0.1:8000/redoc


---

## Endpoints principais

### Criar tarefa

POST `/tasks`


{
"title": "Estudar FastAPI",
"description": "Aprender backend com Python"
}


---

### Listar tarefas

GET `/tasks`

---

### Buscar tarefa

GET `/tasks/{id}`

---

### Atualizar tarefa

PUT `/tasks/{id}`

---

### Deletar tarefa

DELETE `/tasks/{id}`

---

### Marcar como concluída

PATCH `/tasks/{id}/done`

---

## Autor

Guilherme Dias  
Estudante de Sistemas de Informação