from pydantic import BaseModel


class ArticleTitleSchema(BaseModel):
    id: int
    title: str

class ArticleCreateSchema(BaseModel):
    title: str
    content: str

class ArticleUpdateSchema(BaseModel):
    title: str | None = None
    content: str | None = None

class ArticleFullResponseSchema(BaseModel):
    id: int
    title: str
    content: str