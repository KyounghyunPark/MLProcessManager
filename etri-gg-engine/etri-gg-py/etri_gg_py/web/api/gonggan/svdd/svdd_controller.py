from fastapi import APIRouter

from etri_gg_py.web.api.gonggan.svdd import svdd_main
from etri_gg_py.web.api.gonggan.svdd.svdd_dto import SvddRequest


svdd_router =  APIRouter()

@svdd_router.post("/exec")
async def do_svdd(svdd_request: SvddRequest) -> str:
    print(f"SVDD request: {svdd_request}")

    input_file = svdd_request.params.input
    output_file = f"{svdd_request.id}@{svdd_request.params.output}"
    hour = svdd_request.params.hour
    c_value = svdd_request.params.cValue


    svdd_main.do_svdd(input_file, output_file, hour, c_value)

    return output_file
