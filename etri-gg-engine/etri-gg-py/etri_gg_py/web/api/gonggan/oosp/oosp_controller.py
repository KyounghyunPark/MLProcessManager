from fastapi import APIRouter

from etri_gg_py.web.api.gonggan.oosp.oosp_main import OopsMain
from etri_gg_py.web.api.gonggan.oosp.oosp_dto import OospRequest

oosp_router = APIRouter()

@oosp_router.post("/exec")
async def do_oosp(oosp_request: OospRequest) -> str:
    print("OOSP request: %s", oosp_request)

    input_file = oosp_request.params.input
    output_file = f"{oosp_request.id}@{oosp_request.params.output}"

    OopsMain.do_oosp(input_file, output_file)
    return output_file
