import unittest
from app.test.base import BaseTestCase
from app.main.service.personalDataSearchByRules import PersonalDataSearchByRules

textForTest = {
    "simple": "Miguel estuvo aquí hace dos minutos",
    "normal": "El calendario gregoriano es debido a el papa Gregorio y el juliano por Julio Cesar",
    "hard": "Bien, soy el juez Cayo Medina de Lara, voy a nombrar a los representantes de la Asamblea, que son: "
            + " Laura Vega, "
            + "Juan Sebastian Ramírez y "
            + "Miguel Medina.",
    "twoSent": "Daniel está comiendo como si nada, mientras José intenta mantener la calma ante esta situción. ¿Dónde está Miguel?"
}

personalDataSearchByRul = PersonalDataSearchByRules()
class TestSearchTextByRul(BaseTestCase):

    def test_start_end_char_name_rules(self):
        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(dictionatyOfNames[0]["star_char"], textForTest["simple"].find("Miguel"))
        self.assertEqual(dictionatyOfNames[0]["end_char"], textForTest["simple"].find("Miguel") + len("Miguel"))

        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["twoSent"])
        self.assertNotEqual(dictionatyOfNames, [])
        
        self.assertEqual(dictionatyOfNames[0]["star_char"], textForTest["twoSent"].find("Daniel"))
        self.assertEqual(dictionatyOfNames[0]["end_char"], textForTest["twoSent"].find("Daniel") + len("Daniel"))
        
        self.assertEqual(dictionatyOfNames[1]["star_char"], textForTest["twoSent"].find("José"))
        self.assertEqual(dictionatyOfNames[1]["end_char"], textForTest["twoSent"].find("José") + len("José"))

        self.assertEqual(dictionatyOfNames[2]["star_char"], textForTest["twoSent"].find("Miguel"))
        self.assertEqual(dictionatyOfNames[2]["end_char"], textForTest["twoSent"].find("Miguel") + len("Miguel"))
        

    def test_simple_look_for_names_by_searchNamesText_rules(self):
        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 1)
        self.assertEqual(dictionatyOfNames[0]["name"], "Miguel")

    def test_normal_look_for_names_by_searchNamesText_rules(self):
        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["normal"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 2)
        self.assertEqual(dictionatyOfNames[0]["name"], "Gregorio")
        self.assertEqual(dictionatyOfNames[1]["name"], "Julio Cesar")

    def test_hard_look_for_names_by_searchNamesText_rules(self):
        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["hard"])
        names = [
            "Cayo Medina de Lara", "Laura Vega", "Juan Sebastian Ramírez", "Miguel Medina"
        ]
        self.assertEqual(len(dictionatyOfNames), len(names))
        for index, name in enumerate(names):
            self.assertEqual(dictionatyOfNames[index]["name"], name)


if __name__ == '__main__':
    unittest.main()
