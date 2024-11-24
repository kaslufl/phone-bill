# Phone Bill
Phone Bill é uma aplicação web que recebe eventos de início e término de chamadas telefônicas para calcular a fatura mensal de um assinante (identificada pelo seu respectivo número de telefone).

A aplicação está disponível via [Fly.io](https://fly.io) no endereço: https://corps.fly.dev/

|!["programando"](docs/deception.gif)|
|:-:|
| *Gif 1. Ilustração do processo de desenvolvimento.* |

Este software foi desenvolvido em um MacBook Pro Apple M2 2022 com macOS Sequoia 15.0.1 (24A348) utilizando o Visual Studio Code 2 1.95.3

## Índice

- [Como utilizar](#como-utilizar)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)


## Como utilizar
A documentação do projeto está no endpoint "/docs", disponível após iniciar a aplicação.

Os registros serão enviados para a aplicação na endpoint "/call"
```bash
curl -X 'POST' \
  'https://corps.fly.dev/call' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 70,
  "type": "end",
  "timestamp": "2016-02-29T14:00:00Z",
  "call_id": 70
}'
```

A conta telefônica é gerada no endpoint "/call/report"
```bash
curl -X 'GET' \
  'https://corps.fly.dev/call/report?subscriber=99988526423&billing_period=12%2F2017' \
  -H 'accept: application/json'
```

## Tecnologias

O ambiente de desenvolvimento emprega múltiplas bibliotecas que visam otimizar a produtividade e garantir a qualidade do código. Entre elas, destacam-se:

- [FastAPI](https://fastapi.tiangolo.com/): Framework rápido e moderno para criação de APIs RESTful baseadas em padrões OpenAPI.
- [SQLAlchemy](https://www.sqlalchemy.org/): Ferramenta robusta para mapeamento de objetos e gerenciamento de banco de dados.

Outras bibliotecas:

- [FastAPI-CLI](https://github.com/fastapi-cli/fastapi-cli): Simplifica a interação com projetos FastAPI.
- [Pydantic-Settings](https://pydantic-docs.helpmanual.io/): Usada para validação e configuração de ambientes.
- [Alembic](https://alembic.sqlalchemy.org/): Controle de versões de banco de dados integrado ao SQLAlchemy.
- [Psycopg](https://www.psycopg.org/): Biblioteca eficiente para interação com PostgreSQL.

Ferramentas auxiliares para garantir qualidade de código incluem:

- [Black](https://black.readthedocs.io/en/stable/): Formatação automática de código.
- [isort](https://pycqa.github.io/isort/): Organiza as importações.
- [Flake8](https://flake8.pycqa.org/en/latest/): Linter que combina PEP 8, PyFlakes e McCabe Complexity.

No contexto de testes:
- [pytest](https://docs.pytest.org/en/stable/): Framework de testes flexível e poderoso.
- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/): Mede a cobertura de código.
- [Factory-Boy](https://factoryboy.readthedocs.io/en/stable/): Criação de objetos de teste.
- [Testcontainers](https://testcontainers-python.readthedocs.io/): Utiliza containers Docker para testes integrados.
- [HTTPX](https://www.python-httpx.org/) oferece suporte avançado a requisições
- [Babel](https://babel.pocoo.org/en/latest/) gerencia internacionalização e localização.

## Instalação

Abaixo será descritos o passos de como instalar e configurar o projeto localmente.

### Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- Python
- Docker

### Passos

Na raiz do diretório do projeto executar os comandos abaixo.

```shell
#Crie um ambiente virtual
python -m venv env

#Ative o ambiente
source env/bin/activate

#Instale as dependências
pip install poetry
poetry install
```

Para executar este projeto localmente, você precisará de um banco de dados postgres. Neste exemplo usaremos uma imagem Docker.


```shell
#Baixar a imagem postgres
docker pull postgres

#Executar o container com as credenciais de teste
docker run --name phonedb -e POSTGRES_USER=corp -e POSTGRES_PASSWORD=corp -e POSTGRES_DB=phonebill -p 5432:5432 -d postgres
```

Posteriormente, você precisará criar um arquivo .env com uma conexão de banco de dados.

```shell
DATABASE_URL="postgresql+psycopg://corp:corp@localhost:5432/phonebill"
```

Após configurar a conexão, aplicar as migrations e iniciar a aplicação.

```shell
#Para aplicar as migrations.
alembic upgrade head

#Comando para executar.
fastapi dev phone_bill/app.py
```

|!["database diagram"](docs/db_diagram.png)|
|:-:|
| *Imagem 1. Tabelas do banco de dados.* |


```sql
#Para que o calculo de preço funcione é preciso preencher a tabela de billing

INSERT INTO public.billing (id, type, base_price, minute_fee, start_time, end_time) VALUES (1, 'peak', 36, 9, '06:00:00', '22:00:00');
INSERT INTO public.billing (id, type, base_price, minute_fee, start_time, end_time) VALUES (2, 'off_peak', 36, 0, '22:00:00', '06:00:00');
```

#### Docker

Para executar a aplicação via docker compose, siga os passos:

```shell
#Subir container.
docker compose up -d

#Para aplicar as migrations.
docker compose exec web alembic upgrade head
```


### Testes

Para efetuar os testes, executar o comando abaixo:

```shell
# --cov para mostrar a cobertura
# -v para mostrar mais detalhes
pytest --cov -v
```
