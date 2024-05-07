# shortener_fastapi
Simple URL shortener service. Python 3 + FastAPI

## Changelog (31.01.2024)
- Extended OpenApi documentation, added requets examples, fields descriptions & response examples
- Automatic migrations on startup
- Extended logging

## Requirements
- Docker

## Installation
- Clone repository
- Go into `infra` directory
- Create `.env` file
```
git clone https://github.com/firepanda70/shortener_fastapi
cd shortener_fastapi/infra
touch .env
```
- Fill `.env` file like below
```
DB_URL=docker:docker@pg
COMPOSE_PROJECT_NAME=shorcuter_fastapi
POSTGRES_USER=docker
POSTGRES_PASSWORD=docker
POSTGRES_DB=docker
HOST=http://localhost/
SHORTCUT_AUTO_LENGTH=6
LOG_LEVEL=INFO
```
- Build docker containers
```
docker compose up -d --build
```
- Done!

## Usage
Docs will be avaliable [here](http://localhost/docs#/)

To run tests execute:
```
docker exec <WEB_CONTAINER_ID> python -m pytest
```

To access logs execute:
```
docker logs -f <WEB_CONTAINER_ID>
```

## Technologies
- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- Poetry
- Docker
- Nginx
- Pytest
