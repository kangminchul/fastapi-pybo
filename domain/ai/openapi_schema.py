from pydantic import BaseModel, field_validator

class OpenAPISchema(BaseModel):
    openapi: str

class OpenAPIParamSchema(BaseModel):
    type : str
    content: str
    @field_validator('type', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise  ValueError('빈 값은 허용되지 않습니다.')
        return v

