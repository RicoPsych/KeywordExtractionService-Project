import time
import yake

class yakeService :
    engine: yake.KeywordExtractor
    asyncResults = {}

    def __init__(self):
        self.engine = yake.KeywordExtractor() #lan="pl"

    def extract(self,text,ngram):
        self.engine = yake.KeywordExtractor(n=ngram) 
        ext = self.engine.extract_keywords(text)
        return [n[0].lower() for n in ext]

    def extractDataset(self, dataset, ngram, results, uuid):
        self.engine = yake.KeywordExtractor(n=ngram) 
        results[uuid] = { "progress": 0.00, "results": [] }
        size = len(dataset)
        i = 0
        for text in dataset:
            i+=1
            # time.sleep(5)
            ext = self.engine.extract_keywords(text)
            results[uuid]["progress"] = i/size 
            results[uuid]["results"].append([n[0].lower() for n in ext])
        
        time.sleep(300)
        del results[uuid]
        return 