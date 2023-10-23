from typing import  Optional

from pydantic import Field

from .rwschema import RWSchema

#these are schemas (interfaces) used for typization of parameters and arguments
class RunInResponseInComputing(RWSchema):
    id: str = Field(..., alias="id")
    title: str
    description: Optional[str] = ""
    method: str
    msg: str


