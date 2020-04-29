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

    
    def test_simple_look_for_names_by_searchNamesText_rules(self):
        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 1)
        self.assertEqual(dictionatyOfNames[0], "Miguel")

    def test_normal_look_for_names_by_searchNamesText_rules(self):
        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["normal"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 2)
        self.assertEqual(dictionatyOfNames[0], "Gregorio")
        self.assertEqual(dictionatyOfNames[1], "Julio Cesar")

    def test_hard_look_for_names_by_searchNamesText_rules(self):
        dictionatyOfNames,_ = personalDataSearchByRul.searchPersonalData(textForTest["hard"])
        names = [
            "Cayo Medina de Lara", "Laura Vega", "Juan Sebastian Ramírez", "Miguel Medina"
        ]
        self.assertEqual(len(dictionatyOfNames), len(names))
        for index, name in enumerate(names):
            self.assertEqual(dictionatyOfNames[index], name)


if __name__ == '__main__':
    unittest.main()
