import unittest

from app.test.base import BaseTestCase
from app.main.service.NameSearchByEntities import NameSearchByEntities
from app import api

searchNamesText = NameSearchByEntities()
textForTest = {
    "simple": "Miguel estuvo aquí hace dos minutos",
    "normal": "El calendario Gregoriano es debido a el papa Gregorio XIII y el juliano por Julio Cesar",
    "hard": "Bien, soy el juez Cayo Medina de Lara, voy a nombrar a los representantes de la Asamblea: "
            + "Laura Vega, "
            + "Juan Sebastian Ramírez y "
            + "Joseph Stetter."
}


class TestSearchText(BaseTestCase):

    def test_start_end_char_name(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(dictionatyOfNames[0]["star_char"], textForTest["simple"].find("Miguel"))
        self.assertEqual(dictionatyOfNames[0]["end_char"], textForTest["simple"].find("Miguel") + len("Miguel"))

    def test_simple_look_for_names_by_searchNamesText(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 1)
        self.assertEqual(dictionatyOfNames[0]["name"], "Miguel")

    def test_normal_look_for_names_by_searchNamesText(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["normal"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 2)
        self.assertEqual(dictionatyOfNames[0]["name"], "Gregorio XIII")
        self.assertEqual(dictionatyOfNames[1]["name"], "Julio Cesar")

    def test_hard_look_for_names_by_searchNamesText(self):
        dictionatyOfNames = searchNamesText.searchNames(textForTest["hard"])
        names = [
            "Cayo Medina de Lara", "Laura Vega", "Juan Sebastian Ramírez", "Joseph Stetter"
        ]
        self.assertEqual(len(dictionatyOfNames), len(names))
        for index, name in enumerate(names):
            self.assertEqual(dictionatyOfNames[index]["name"], names[index])


if __name__ == '__main__':
    unittest.main()
