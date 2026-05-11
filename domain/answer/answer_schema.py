from datetime import datetime
from pydantic import BaseModel, field_validator, Field
from domain.user.user_schema import User


class AnswerCreate(BaseModel):
    content: str
#    created_date : datetime | None = None
#    created_date: datetime = Field(default_factory=datetime.now)
    @field_validator('content')
    def not_empty(cls, v):
#        if not v or not v.strip():
        if not isinstance(v, str) or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

class Answer(BaseModel):
    id : int
    content: str
    created_date : datetime
    user : User | None
    question_id : int
    modify_date: datetime | None = None
    voter:list[User] = []

#    class AnswerUpdate(AnswerCreate):
class AnswerUpdate(BaseModel):
    content: str
    answer_id : int


class AnswerDelete(BaseModel):
    answer_id : int

class AnswerVote(BaseModel):
    answer_id : int



