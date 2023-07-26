from pydantic import BaseModel

class ProductInput(BaseModel):
    name: str
    description: str
    brand_id: int
    category_id: int
    image: str
    cost_per_unit: float
    stock_quantity: int