from fastapi import FastAPI

from .routers import yake_router
from .routers import keybert_router
from .routers import multirake_router

app = FastAPI(
    title='KeywordExtractionService',
    description='Service providing 3 engines for keyword extraction from text',
    version='0.1',
)

app.include_router(yake_router.router)
app.include_router(keybert_router.router)
app.include_router(multirake_router.router)
