```makefile
.PHONY: up down logs api web db psql rebuild

up:
\tdocker compose up -d --build

down:
\tdocker compose down

logs:
\tdocker compose logs -f

api:
\tdocker compose logs -f api

web:
\tdocker compose logs -f web

db:
\tdocker compose logs -f db

psql:
\tdocker compose exec -it db psql -U $$POSTGRES_USER -d $$POSTGRES_DB

rebuild:
\tdocker compose down && docker compose build --no-cache && docker compose up -d
