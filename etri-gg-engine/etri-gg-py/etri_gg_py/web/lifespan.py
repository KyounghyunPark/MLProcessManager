from contextlib import asynccontextmanager
from os.path import dirname, realpath
from typing import AsyncGenerator

from fastapi import FastAPI

global_var = {}
DATA_INPUT = "data_input"
DATA_OUTPUT = "data_output"
DATA_MODEL = "data_model"
DATA_BIG_INPUT = "data_big_input"


@asynccontextmanager
async def lifespan_setup(
    app: FastAPI,
) -> AsyncGenerator[None, None]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """
    global_var[DATA_INPUT] = (
        dirname(dirname(dirname(realpath(__file__)))) + "/data_input"
    )
    global_var[DATA_OUTPUT] = (
        dirname(dirname(dirname(realpath(__file__)))) + "/data_output"
    )
    global_var[DATA_MODEL] = (
        dirname(dirname(dirname(realpath(__file__)))) + "/data_model"
    )
    global_var[DATA_BIG_INPUT] = (
        dirname(dirname(dirname(realpath(__file__)))) + "/data_big_input"
    )

    app.middleware_stack = None
    app.middleware_stack = app.build_middleware_stack()

    yield
