from fastapi import APIRouter

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/demo")
async def demo_ticket():
    return {"ticket": "Aquí se mostrarán los tickets de prueba"}
