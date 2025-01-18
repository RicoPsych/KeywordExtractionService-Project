from fastapi import BackgroundTasks,APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4

from src.routers.entities import Response
from src.routers.entities import Request
from src.routers.entities import RequestDataset
from src.routers.entities import ResponseDataset

from src.services.default_options import Desc
from src.services.multirake_service import multirakeService

router = APIRouter(
    prefix='/multirake',
    tags=['multirake'],
    responses={404: {'description': 'Not found'}},
)

service = multirakeService()
asyncResults = {}

@router.get('/', summary='Usage info Endpoint', description='Returns a manual for endpoint usage.')
def info():
    """Returns information about endpoint."""
    return Desc("multirake")


@router.post(
    '/',
    summary='Keyword Extraction',
    description='Returns a list of keywords form provided Text',
    response_model=Response,
)
def extract(req: Request):
    """Extract keywords from text
    """
    return {"output":service.extract(req.text, req.ngram, req.lang)}
 

@router.post(
    '/dataset',
    summary='Keyword Extraction',
    description='Starts extraction from dataset',
    # response_model=AsyncTaskID,
)
async def extractDataset(req: RequestDataset, background_tasks: BackgroundTasks):
    """Extract keywords from texts in dataset"""
    uuid = uuid4()
    background_tasks.add_task( service.extractDataset, req.texts, req.ngram, req.lang, asyncResults, uuid)
    return {"taskId":uuid}

@router.get(
    '/tasks',
    summary='Existing tasks',
    description='Returns a list of ids of scheduled tasks',
)
def extractDataset():
    return {"tasksIds":list(asyncResults.keys())}

@router.get(
    '/dataset',
    summary='Keyword Extraction',
    description='Returns a list of keywords form provided Text',
    response_model=ResponseDataset,
)
def extractDataset(uuid:UUID):
    if uuid in asyncResults:
        res = asyncResults[uuid]
        if (res["progress"] != 1):
            return {"progress":res["progress"]}
        else:
            return {"results":res["results"]}
    else:
        raise HTTPException(status_code=404, detail="Not Found")