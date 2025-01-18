import time
import multi_rake

class multirakeService :
    engine: multi_rake.Rake
    asyncResults = {}

    def __init__(self):
        self.engine = multi_rake.Rake() #lan="pl"

    def getLanguageCode(self, lang):
        match lang:
            case "en":
                return "en"
            case "pl":
                return "pl"
            case _ : 
                return "en" # Could be also None, for automatic detection


    def extract(self, text, ngram, lang):
        languageCode= self.getLanguageCode(lang)
        self.engine = multi_rake.Rake( max_words=ngram, language_code=languageCode) 
        ext = self.engine.apply(text)
        return [n[0].lower() for n in ext]

    def extractDataset(self, dataset, ngram, lang, results, uuid):
        languageCode= self.getLanguageCode(lang)
        self.engine = multi_rake.Rake( max_words=ngram, language_code=languageCode) 
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