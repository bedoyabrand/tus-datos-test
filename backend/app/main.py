from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, events, sessions, registrations
from app.db import base as models_base  # noqa: F401


app = FastAPI(title="Mis Eventos API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(sessions.router)
app.include_router(registrations.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root():
    return {"message": "Mis Eventos API. Visita /docs para la documentación."}
