import spacy
from spacy.pipeline import EntityRuler
from spacy.tokens import Token

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class LanguageBuilder(metaclass=Singleton):
    def __init__(self):
        self.nlp = spacy.load("es_core_news_md")
        print("model load")

    def defineNameEntity(self):
        pattern = [
                    {'POS': 'PROPN', 'OP': '+'},
                    {'TEXT': {'REGEX': 'de|del|-|el|los|todos'}, 'OP': '?'},
                    {'POS': 'PROPN', 'OP': '?'}
                ]
        ruler = EntityRuler(self.nlp)
        patterns = [{"label": "NAME", "pattern": pattern}]
        ruler.add_patterns(patterns)
        self.nlp.add_pipe(ruler,before='ner')
    
    def getlanguage(self):
        return self.nlp