import unittest

from app.test.base import BaseTestCase
from app.main.service.personalDataSearchByEntities import PersonalDataSearchByEntities

personalDataSearch = PersonalDataSearchByEntities()
textForTest = {
    "simple": "Miguel estuvo aquí hace dos minutos",
    "normal": "El calendario Gregoriano es debido a el papa Gregorio XIII y el juliano por Julio Cesar",
    "hard": "Bien, soy el juez Cayo Medina de Lara, voy a nombrar a los representantes de la Asamblea, que son: "
            + " Laura Vega, "
            + "Juan Sebastian Ramírez y "
            + "Miguel Medina."
}


class TestSearchText(BaseTestCase):

    def test_start_end_char_name(self):
        dictionatyOfNames,_ = personalDataSearch.searchPersonalData(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(dictionatyOfNames[0]["star_char"], textForTest["simple"].find("Miguel"))
        self.assertEqual(dictionatyOfNames[0]["end_char"], textForTest["simple"].find("Miguel") + len("Miguel"))

    def test_simple_look_for_names_by_searchNamesText(self):
        dictionatyOfNames,_ = personalDataSearch.searchPersonalData(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 1)
        self.assertEqual(dictionatyOfNames[0]["name"], "Miguel")

    def test_normal_look_for_names_by_searchNamesText(self):
        dictionatyOfNames,_ = personalDataSearch.searchPersonalData(textForTest["normal"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 2)
        self.assertEqual(dictionatyOfNames[0]["name"], "Gregorio XIII")
        self.assertEqual(dictionatyOfNames[1]["name"], "Julio Cesar")

    def test_hard_look_for_names_by_searchNamesText(self):
        dictionatyOfNames,_ = personalDataSearch.searchPersonalData(textForTest["hard"])
        names = [
            "Cayo Medina de Lara", "Laura Vega", "Juan Sebastian Ramírez", "Miguel Medina"
        ]
        self.assertEqual(len(dictionatyOfNames), len(names))
        for index, name in enumerate(names):
            self.assertEqual(dictionatyOfNames[index]["name"], name)

    def test_isDni(self):
        self.assertTrue(personalDataSearch.isDni("54094110L"))
        self.assertTrue(personalDataSearch.isDni("54094110l"))
        self.assertTrue(personalDataSearch.isDni("54094110 L"))
        self.assertTrue(personalDataSearch.isDni("54094110\tL"))
        self.assertTrue(personalDataSearch.isDni("54094110         L"))
        self.assertTrue(personalDataSearch.isDni("43294881\t\tA"))
        self.assertFalse(personalDataSearch.isDni("54094110 hola L"))
        self.assertFalse(personalDataSearch.isDni("43294884A"))
        self.assertTrue(personalDataSearch.isDni("54094110\nL"))
        self.assertFalse(personalDataSearch.isDni("example"))
        self.assertFalse(personalDataSearch.isDni(""))

    def test_isName(self):
        self.assertTrue(personalDataSearch.isName("Miguel"))
        self.assertTrue(personalDataSearch.isName("Miguel Ángel"))
        self.assertTrue(personalDataSearch.isName("Paco León Medina"))
        self.assertFalse(personalDataSearch.isName(""))
        self.assertFalse(personalDataSearch.isName("MIguel9 Medina"))
        self.assertFalse(personalDataSearch.isName("estoy aqui"))

    def test_selectedName(self):
        self.assertEqual(personalDataSearch.selectNames([{"name": "", "star_char": 0, "end_char": 0}]), [])
        self.assertEqual(personalDataSearch.selectNames([]), [])
        self.assertEqual(personalDataSearch.selectNames(
            [{"name": "Miguel", "star_char": 0, "end_char": 0}]),
            [{"name": "Miguel", "star_char": 0, "end_char": 0}])
        self.assertEqual(personalDataSearch.selectNames(
            [{"name": "Miguel Ángel Medina Ramírez", "star_char": 0, "end_char": 0}, 
            {"name": "Paco Guerra", "star_char": 0, "end_char": 0}]), 
            [{"name": "Miguel Ángel Medina Ramírez", "star_char": 0, "end_char": 0}, 
            {"name": "Paco Guerra", "star_char": 0, "end_char": 0}])
        self.assertEqual(personalDataSearch.selectNames(
            [{"name": "Miguel Ángel Medina Ramírez", "star_char": 0, "end_char": 0}, 
            {"name": "ff Guefffrra", "star_char": 0, "end_char": 0}]), 
            [{"name": "Miguel Ángel Medina Ramírez", "star_char": 0, "end_char": 0}])

    def test_check_data_in_DB_name(self):
        self.assertEqual(personalDataSearch.checkNamesInDB([""]), [])
        self.assertEqual(personalDataSearch.checkNamesInDB([]), [])
        self.assertEqual(personalDataSearch.checkNamesInDB(["Miguel"]), ["Miguel"])
        self.assertEqual(personalDataSearch.checkNamesInDB(["Miguel Ángel Medina Ramírez", 
        "Paco Flores"]), ["Miguel Ángel Medina Ramírez","Paco Flores"])
        self.assertEqual(personalDataSearch.checkNamesInDB(["Miguel Ángel Medina Ramírez", 
        "Pacccco Floreis"]), ["Miguel Ángel Medina Ramírez"])


if __name__ == '__main__':
    unittest.main()
