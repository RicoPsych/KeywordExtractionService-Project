import time
import yake

class yakeService :
    engine: yake.KeywordExtractor
    asyncResults = {}

    def __init__(self):
        self.engine = yake.KeywordExtractor() #lan="pl"

    def getLanguageCode(self, lang):
        match lang:
            case "en":
                return "en"
            case "pl":
                return "pl"
            case _ : 
                return "en"
            
    def extract(self,text,ngram,lang):
        lan = self.getLanguageCode(lang)
        self.engine = yake.KeywordExtractor(n=ngram, lan=lan) 
        ext = self.engine.extract_keywords(text)
        return [n[0].lower() for n in ext]

    def extractDataset(self, dataset, ngram, lang, results, uuid):
        lan = self.getLanguageCode(lang)
        self.engine = yake.KeywordExtractor(n=ngram, lan=lan) 
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