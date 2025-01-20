from fastapi import APIRouter

from etri_gg_py.web.api.gonggan.mapmatching.map_matching_dto import MapMatchingRequest
from etri_gg_py.web.api.gonggan.mapmatching.map_matching_main import MapMatching

mm_router = APIRouter()


@mm_router.get("/mapmatching")
async def test_func() -> str:
    return "Welcome to Map Matching!"


@mm_router.post("/mapmatching")
async def do_map_matching(map_mapching_request: MapMatchingRequest) -> str:
    """Hello to test route is working."""
    print("Map Matching request: %s", map_mapching_request)

    input_file = map_mapching_request.params.input
    output_file = f"{map_mapching_request.id}@{map_mapching_request.params.output}"

    MapMatching.map_matching_func(input_file, output_file)
    return output_file
