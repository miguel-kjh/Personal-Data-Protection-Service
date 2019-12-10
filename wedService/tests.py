import unittest
from SearcherNamesTexts import SearcherNamesTexts
from time import time
import numpy as np
import spacy
from spacy.pipeline import EntityRuler

nlp = spacy.load("es_core_news_md")
pattern = [
            {'POS': 'PROPN', 'OP': '+'},
            {'TEXT': {'REGEX': 'de|el|del|-'}, 'OP': '?'},
            {'POS': 'PROPN', 'OP': '?'}
        ]
ruler = EntityRuler(nlp)
patterns = [{"label": "PER", "pattern": pattern}]
ruler.add_patterns(patterns)
nlp.add_pipe(ruler)
print("model load")
#Variable Test
searchNamesText = SearcherNamesTexts(nlp)
textForTest = {
        "simple":"Miguel estuvo aquí hace dos minutos",
        "normal":"El calendario Gregoriano es debido a el papa Gregorio XIII y el juliano por Julio Cesar",
        "hard": "Bien, soy el juez Cayo Medina de Lara, voy a nombrar a los representantes de la Asamblea: "
                + "Laura Vega, "
                + "Juan Sebastian Ramírez y "
                + "Joseph Stetter."
}

class TestSearchText(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def test_start_end_char_name(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["simple"])
        try:
            self.assertEqual(dictionatyOfNames[0]["star_char"], textForTest["simple"].find("Miguel"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(dictionatyOfNames[0]["end_char"], textForTest["simple"].find("Miguel") + len("Miguel"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_simple_look_for_names_by_searchNamesText(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["simple"])
        try:
            self.assertEqual(len(dictionatyOfNames), 1)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(dictionatyOfNames[0]["name"], "Miguel")
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_normal_look_for_names_by_searchNamesText(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["normal"])
        try:
            self.assertEqual(len(dictionatyOfNames), 2)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(dictionatyOfNames[0]["name"], "Gregorio XIII")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(dictionatyOfNames[1]["name"], "Julio Cesar")
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_hard_look_for_names_by_searchNamesText(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["hard"])
        names = [
            "Cayo Medina de Lara","Laura Vega","Juan Sebastian Ramírez","Joseph Stetter"
        ]
        try:
            self.assertEqual(len(dictionatyOfNames), len(names))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        for index,name in enumerate(names):
            try:
                self.assertEqual(dictionatyOfNames[index]["name"], names[index])
            except AssertionError as e:
                self.verificationErrors.append(str(e))
class TestPerformance(unittest.TestCase):
    def test_performance(self):
        LIMIT = 0.1  # 0.1 S
        sampleTime = []
        with open("file_test/el_quijote.txt",'r', encoding="utf8") as f:
            for line in f:
                st = time()
                searchNamesText.searchNames(line)
                sampleTime.append(time()-st)
        res = np.mean(sampleTime)
        print(res)
        self.assertTrue(res < LIMIT)



if __name__ == '__main__':
    unittest.main()
