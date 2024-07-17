from pydantic import *
from typing import *


class Example(BaseModel):
    kind: Annotated[str, Field(max_length=32,)]
    name: Annotated[str, Field(max_length=128,)]
    description: Optional[Annotated[str, Field(max_length=4096,)]] = None
    version: Annotated[str, Field(pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",)]
    configuration: Annotated[Dict, Field()]

    