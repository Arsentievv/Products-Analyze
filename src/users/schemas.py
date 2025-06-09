from pydantic import BaseModel, model_validator


class UserBaseSchema(BaseModel):
    email: str
    password: str
    telegram: str | None = None

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def validate_email(self):
        if "." not in self.email or "@" not in self.email:
            raise ValueError("Email is not correct")
        return self


class UserCreateSchema(UserBaseSchema):
    pass


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool


class UserLoginSchema(BaseModel):
    id: int
    access_token: str
