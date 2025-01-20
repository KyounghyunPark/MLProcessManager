from pydantic import BaseModel


class SvddParams(BaseModel):
    input: str
    output: str
    cValue: float
    hour: int


class SvddRequest(BaseModel):
    id: str
    name: str
    value: str
    params: SvddParams


class SvddResponse(BaseModel):
    id: str
