# DefaultOpts = {
#     "ngram": (1,3),
#     "lang": "en"
# }

def Desc(endpoint):
    return {
        'About': f"Keyword extraction endpoint. Uses {endpoint} underneath.",
        'Usage' : {
            f'''GET /{endpoint}''' : 
                " -> this prompt" ,
            f'''POST /{endpoint} {{ text:str, <ngram:int> , <lang:str = "en"> }}''':
                ''' -> [str],   Extracts keywords from text''',
            f'''POST /{endpoint}/dataset {{ texts=[str], <ngram=3> , <lang:str = "en"> }} ''':
                ''' -> {{taskId: UUID}},    Asynchronous extraction of keywords from text, Returns uuid of task.''',
            f'''GET /{endpoint}?uuid=UUID''' :
                ''' -> {{progress:float}} | {{results:[[str]]}},    Returns progress or result of task of given uuid.'''
        }
}