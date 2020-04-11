import spacy
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher

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
        self.matcher = Matcher(self.nlp.vocab)
        patterNotContext = [
                {'POS': 'PROPN', 'OP': '+'}, {"IS_PUNCT": True}, {'POS': 'PROPN', 'OP': '+'}
            ]
        self.matcher.add("withoutContext", None, patterNotContext)

    def defineNameEntity(self):
        names = [
            {'POS': 'PROPN', 'OP': '+'},
            {'TEXT': {'REGEX': 'de|del|-|el|los|todos'}, 'OP': '?'},
            {'POS': 'PROPN', 'OP': '?'}
        ]
        ruler = EntityRuler(self.nlp)
        patterns = [
            {"label": "NAME", "pattern":names}
        ]
        ruler.add_patterns(patterns)
        self.nlp.add_pipe(ruler, before='ner')
        print("defined datas as entity")

    def semanticSimilarity(self, text: str, textToCompare: str) -> float:
        """
        Only use this funtion when used a md or lg models
        """
        if not text.strip(): return 0.0
        with self.nlp.disable_pipes("tagger","parser","ner"):
            doc = self.nlp(text)
            if not doc.vector_norm: return False
            docToCompare = self.nlp(textToCompare)
        return doc.similarity(docToCompare)

    def getlanguage(self):
        return self.nlp

    def hasContex(self, text: str) -> bool:
        if not text:
            return False
        with self.nlp.disable_pipes("parser","ner"):
            doc = self.nlp(text)
        matches = self.matcher(doc)
        return not ((bool(matches) and matches[-1][2] == len(doc)) 
        or (sum(char.isupper() for char in text)+1)/len(text) > 0.8)
