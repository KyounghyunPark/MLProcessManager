from pydantic import BaseModel


class MapMatchingParams(BaseModel):
    input: str
    output: str


class MapMatchingRequest(BaseModel):
    id: str
    name: str
    value: str
    params: MapMatchingParams


class MapMatchingResponse(BaseModel):
    id: str
