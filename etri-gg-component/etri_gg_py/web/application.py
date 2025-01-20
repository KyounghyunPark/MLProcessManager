from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware

from etri_gg_py.web.api.router import api_router
from etri_gg_py.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="etri_gg_py",
        version=metadata.version("etri_gg_py"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
