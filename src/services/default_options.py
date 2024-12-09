# DefaultOpts = {
#     "ngram": (1,3),
#     "lang": "en"
# }

def Desc(endpoint):
    return {
        'About': f"Keyword extraction endpoint. Uses {endpoint} underneath.",
        'Usage' : 
f'''GET /{endpoint} -> this prompt 

POST /{endpoint} {{ text:str, <ngram:int> }} -> [str] 
    Extracts keywords from text

POST /{endpoint}/dataset {{ texts=[str], <ngram=3> }} -> {{taskId: UUID}}
    Asynchronous extraction of keywords from 
    Returns uuid of task.

GET /{endpoint}?uuid=UUID -> {{progress:float}} | {{results:[[str]]}}
    Returns progress or result of task of given uuid.
'''
}