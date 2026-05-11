from datetime import datetime
from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


#class Question(BaseModel):
class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str
    create_date:datetime
    answers: list[Answer]
    user: User | None
    modify_date: datetime | None = None
    voter:list[User] = []


class QuestionList(BaseModel):
    total : int = 0
    question_list : list[QuestionSchema] = []


class QuestionCreateSchema(BaseModel):
    subject: str
    content: str
    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise  ValueError('빈 값은 허용되지 않습니다.')
        return v

class QuestionUpdateSchema(QuestionCreateSchema):
    question_id: int

class QuestionDeleteSchema(BaseModel):
    question_id: int

class QuestionVoteSchema(BaseModel):
    question_id: int