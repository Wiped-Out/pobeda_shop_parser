from pydantic import BaseModel


class Good(BaseModel):
    title: str
    price: int
    barcode: int
    url: str
