from pydantic import BaseModel
from datetime import datetime


class ProductTrackBaseSchema(BaseModel):
    user_id: int
    product_id: int

    class Config:
        from_attributes = True


class ProductTrackCreateSchema(ProductTrackBaseSchema):
    pass


class ProductTrackSchema(ProductTrackBaseSchema):
    id: int
    is_active: bool
    creation_date: datetime


