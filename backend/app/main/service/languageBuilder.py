import spacy
from spacy.pipeline import EntityRuler

class LanguageBuilder():
    def __init__(self):
        self.nlp = spacy.load("es_core_news_sm")
        print("model load")

    def defineNameEntity(self):
        pattern = [
                    {'POS': 'PROPN', 'OP': '+'},
                    {'TEXT': {'REGEX': 'de|del|-'}, 'OP': '?'},
                    {'POS': 'PROPN', 'OP': '?'}
                ]
        ruler = EntityRuler(self.nlp)
        patterns = [{"label": "PER", "pattern": pattern}]
        ruler.add_patterns(patterns)
        self.nlp.add_pipe(ruler)
    
    def getlanguage(self):
        return self.nlp