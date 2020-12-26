from app.main.util.heuristicMeasures import MINIMAL_UPPER_CHAR_DENSITY

import spacy
from spacy.pipeline import EntityRuler
from spacy.matcher  import Matcher


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LanguageBuilder(metaclass=Singleton):
    def __init__(self):
        model = "es_core_news_md"
        self.nlp            = spacy.load(model)
        self.nlpRules       = spacy.load(model, disable=["parser","ner"])
        self.vectorialSpace = spacy.load(model, disable=["tagger","parser","ner"])
        print("models load")


        self.matcher = Matcher(self.nlp.vocab)
        patterNotContext = [
                {'POS'      : 'PROPN', 'OP': '+'}, 
                {"IS_PUNCT" : True}, 
                {'POS'      : 'PROPN', 'OP': '+'}
            ]
        self.matcher.add("withoutContext", None, patterNotContext)

    def defineRulesOfNames(self):
        """
        Create the patterns to search for names in the SpaCy search engine
        """
        names      = [
            {'POS' : 'PROPN', 'OP': '+'},
            {'TEXT': {'REGEX': 'de|del|-|el|los|de todos los'}, 'OP': '?'},
            {'POS' : 'PROPN', 'OP': '*'}
        ]
        ruler      = EntityRuler(self.nlpRules)
        self.label = "NAME"
        patterns = [
            {"label": self.label, "pattern":names}
        ]
        ruler.add_patterns(patterns)
        self.nlpRules.add_pipe(ruler, after='tagger')

    def semanticSimilarity(self, text: str, textToCompare: str) -> float:
        """
        Compares the range of semantic similarity between two texts
        Only use this funtion when used a md or lg models
        :param text: string
        :param textToCompare: string
        :retunr: semantic similarity of Float
        """
        if not text.strip(): 
            return 0.0

        doc = self.vectorialSpace(text)

        if not doc.vector_norm: 
            return False

        docToCompare = self.vectorialSpace(textToCompare)

        return doc.similarity(docToCompare)

    def getlanguage(self):
        return self.nlp

    def getlanguageByRules(self):
        return self.nlpRules
    
    def getLabelNameOfRules(self) -> str:
        try: 
            return self.label
        except NameError:
            return None

    def hasContex(self, text: str) -> bool:
        """
        Find out if a text has enough semantic load to consider if it has enough context
        :param text: string
        :return: boolean
        """
        if not text:
            return False
        doc = self.nlpRules(text)
        matches = self.matcher(doc)
        return not ((bool(matches) and matches[-1][2] == len(doc)) 
        or (sum(char.isupper() for char in text.replace(" ",''))+1)/len(text) > MINIMAL_UPPER_CHAR_DENSITY)
