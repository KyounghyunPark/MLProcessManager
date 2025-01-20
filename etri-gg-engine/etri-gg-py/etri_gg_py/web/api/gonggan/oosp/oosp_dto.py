from pydantic import BaseModel


class OospParams(BaseModel):
    input: str
    output: str


class OospRequest(BaseModel):
    id: str
    name: str
    value: str
    params: OospParams


class OospResponse(BaseModel):
    id: str
