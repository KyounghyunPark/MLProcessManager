from fastapi.routing import APIRouter

from etri_gg_py.web.api import echo, gonggan, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(gonggan.router, prefix="/gg", tags=["gg"])
api_router.include_router(gonggan.lstm_router, prefix="/lstm", tags=["lstm"])
api_router.include_router(gonggan.mm_router, prefix="/mm", tags=["mm"])
api_router.include_router(gonggan.oosp_router, prefix="/oosp", tags=["oosp"])
api_router.include_router(gonggan.svdd_router, prefix="/svdd", tags=["svdd"])
