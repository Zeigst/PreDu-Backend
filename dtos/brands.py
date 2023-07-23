from pydantic import BaseModel

class BrandInput(BaseModel):
    name: str
    description: str