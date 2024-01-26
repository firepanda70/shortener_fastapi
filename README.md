# shortener_fastapi
Simple URL shortener service. Python 3 + FastAPI

## Requirements
- Docker
- Python 3.12

## Installation
- Clone repository
- Go into `infra` directory
- Create and fill `.env` file. Template in `.env.example`
- Build docker containers
```
git clone https://github.com/firepanda70/shortener_fastapi
cd shortener_fastapi/infra
docker compose up -d --build
```
- Inside web container, run alembic migrations
```
web-1 # alembic upgrade head
```
- Done!

## Usage
Docs will be avaliable [here](http://localhost/docs#/)

## Technologies
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Poetry
- Docker
- Nginx
- Pytest
