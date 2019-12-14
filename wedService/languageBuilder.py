import spacy
from spacy.pipeline import EntityRuler

class languageBuilder():
    def __init__(self):
        self.nlp = spacy.load("es_core_news_sm")
        pattern = [
                    {'POS': 'PROPN', 'OP': '+'},
                    {'TEXT': {'REGEX': 'de|del|-'}, 'OP': '?'},
                    {'POS': 'PROPN', 'OP': '?'}
                ]
        ruler = EntityRuler(self.nlp)
        patterns = [{"label": "PER", "pattern": pattern}]
        ruler.add_patterns(patterns)
        self.nlp.add_pipe(ruler)
        print("model load")
    
    def getlanguage(self):
        return self.nlp