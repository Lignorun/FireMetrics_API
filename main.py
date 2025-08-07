from fastapi import FastAPI
from routes.fireAlert import router as fire_router
from routes.desmatamento import router as desmatamento_router
from routes.homepage import router as homepage_router  # se quiser manter

app = FastAPI()

# routs

app.include_router(homepage_router)
app.include_router(fire_router)
app.include_router(desmatamento_router)
