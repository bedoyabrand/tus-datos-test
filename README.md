# Mis Eventos – Monorepo

Aplicación demo para gestión de eventos con **FastAPI + PostgreSQL** (backend) y **React** (frontend).  
Este repositorio contiene dos proyectos: `backend/` y `frontend/`.

## Requisitos
- Docker y Docker Compose
- Make (opcional)

## Primeros pasos
1. Clonar el repo y crear `.env` en la raíz (ver `.env.example`).
2. Levantar los servicios:
   ```bash
   docker compose up -d --build
