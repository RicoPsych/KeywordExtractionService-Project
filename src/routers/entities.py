from uuid import UUID
from pydantic import BaseModel

class Request(BaseModel):
    text: str
    ngram: int | None = 3
    lang: str | None = "en"

class Response(BaseModel):
    output: list[str]

class AsyncTaskID(BaseModel):
    taskId: UUID

class ResponseDataset(BaseModel):
    progress: float | None = None
    results: list[list[str]] | None = None
    
class RequestDataset(BaseModel):
    texts: list[str]
    ngram: int | None = 3
    lang: str | None = "en"