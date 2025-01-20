import os
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import APIRouter, UploadFile, Query
from pydantic import BaseModel
from starlette.responses import JSONResponse, FileResponse

from etri_gg_py.web.lifespan import DATA_INPUT, global_var, DATA_OUTPUT

router = APIRouter()


@router.get("/hello")
async def hello() -> str:
    """Hello to test route is working."""
    return "Welcome to Etri Gonggan!"


@router.post("/upload-file")
async def create_upload_file(file: UploadFile):
    cur_file_name = file.filename

    file_path = Path(global_var[DATA_INPUT]) / cur_file_name
    if os.path.isfile(file_path):
        os.remove(file_path)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return JSONResponse(content={
        "content": cur_file_name
    })




@router.get("/download-file/{filename}")
async def predict(filename) -> FileResponse:
    data_output_path = Path(global_var[DATA_OUTPUT])
    file = data_output_path / filename
    if "@" in filename:
        filename = filename.split("@")[1]

    return FileResponse(file, media_type="application/octet-stream", filename=filename)


class DownloadQueryParams(BaseModel):
    filename: str
    folder: str

@router.get("/download-file")
async def predict(params: Annotated[DownloadQueryParams, Query()]) -> FileResponse:
    data_output_path = Path(global_var[DATA_OUTPUT])
    data_input_path = Path(global_var[DATA_INPUT])
    filename = params.filename

    if params.folder == "input":
        file = data_input_path / filename
    else:
        file = data_output_path / filename
    if "@" in filename:
        filename = filename.split("@")[1]

    return FileResponse(file, media_type="application/octet-stream", filename=filename)
