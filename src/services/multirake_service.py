import time
import multi_rake

class multirakeService :
    engine: multi_rake.Rake
    asyncResults = {}

    def __init__(self):
        self.engine = multi_rake.Rake() #lan="pl"

    def extract(self,text,ngram):
        self.engine = multi_rake.Rake( max_words=ngram) 
        ext = self.engine.apply(text)
        return [n[0].lower() for n in ext]

    def extractDataset(self, dataset, ngram, results, uuid):
        self.engine = multi_rake.Rake( max_words=ngram) 
        results[uuid] = { "progress": 0.00, "results": [] }
        size = len(dataset)
        i = 0
        for text in dataset:
            i+=1
            # time.sleep(5)
            ext = self.engine.apply(text)
            results[uuid]["progress"] = i/size 
            results[uuid]["results"].append([n[0].lower() for n in ext])
        
        time.sleep(300)
        del results[uuid]
        return 