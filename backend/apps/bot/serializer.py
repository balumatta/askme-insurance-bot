from pydantic import BaseModel


class GenerateAnswerInputSerializer(BaseModel):
    query: str


class AnswerResponseSerializer(BaseModel):
    query: str
    answer: str
