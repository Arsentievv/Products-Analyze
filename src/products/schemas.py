from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    title: str
    price: float
    url: str

    class Config:
        from_attributes = True


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductSchema(ProductBaseSchema):
    id: int
