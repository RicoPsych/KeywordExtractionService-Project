import time
import keybert

class keybertService :
    engine: keybert.KeyBERT
    asyncResults = {}

    def __init__(self):
        self.engine = keybert.KeyBERT() #lan="pl"

    def extract(self,text,ngram):
        self.engine = keybert.KeyBERT() 
        ext = self.engine.extract_keywords(text,keyphrase_ngram_range=(1,ngram))
        return [n[0].lower() for n in ext]

    def extractDataset(self, dataset, ngram, results, uuid):
        self.engine = keybert.KeyBERT() 
        results[uuid] = { "progress": 0.00, "results": [] }
        size = len(dataset)
        i = 0
        for text in dataset:
            i+=1
            # time.sleep(5)
            ext = self.engine.extract_keywords(text,keyphrase_ngram_range=(1,ngram))
            results[uuid]["progress"] = i/size 
            results[uuid]["results"].append([n[0].lower() for n in ext])
        
        time.sleep(300)
        del results[uuid]
        return 