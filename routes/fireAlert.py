from fastapi import APIRouter, Query
from services.alertas import get_alertas_incendio

router = APIRouter(prefix="/incendios", tags=["Incêndios"])

@router.get("/")
def incendios(
    uf: str = Query(..., description="UF do estado, ex: 'PA'"),
    ano_inicial: int = Query(2020),
    ano_final: int = Query(2025)
):
    return get_alertas_incendio(uf, ano_inicial, ano_final)
