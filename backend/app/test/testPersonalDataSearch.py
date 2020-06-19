import unittest

from app.test.base import BaseTestCase
from app.main.service.personalDataSearchByEntities import PersonalDataSearchByEntities
from app.main.service.personalDataSearchByRules import PersonalDataSearchByRules
from app.main.service.personalDataSearch import PersonalData

personalDataSearchByEnt = PersonalDataSearchByEntities()
textForTest = {
    "simple": "Miguel estuvo aquí hace dos minutos",
    "normal": "El calendario gregoriano es debido a el papa Gregorio y el juliano por Julio Cesar",
    "hard": "Bien, soy el juez Cayo Medina de Lara, voy a nombrar a los representantes de la Asamblea, que son: "
            + " Laura Vega, "
            + "Juan Sebastian Ramírez y "
            + "Miguel Medina.",
    "twoSent": "Daniel está comiendo como si nada, mientras José intenta mantener la calma ante esta situción. ¿Dónde está Miguel?"
}


class TestSearchTextByEnt(BaseTestCase):

    def test_simple_look_for_names_by_searchNamesText(self):
        dictionatyOfNames,_ = personalDataSearchByEnt.searchPersonalData(textForTest["simple"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 1)
        self.assertEqual(dictionatyOfNames[0], "Miguel")

    def test_normal_look_for_names_by_searchNamesText(self):
        dictionatyOfNames,_ = personalDataSearchByEnt.searchPersonalData(textForTest["normal"])
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 2)
        self.assertEqual(dictionatyOfNames[0], "Gregorio")
        self.assertEqual(dictionatyOfNames[1], "Julio Cesar")

    def test_hard_look_for_names_by_searchNamesText(self):
        dictionatyOfNames,_ = personalDataSearchByEnt.searchPersonalData(textForTest["hard"])
        names = [
            "Cayo Medina de Lara", "Laura Vega", "Juan Sebastian Ramírez", "Miguel Medina"
        ]
        self.assertEqual(len(dictionatyOfNames), len(names))
        for index, name in enumerate(names):
            self.assertEqual(dictionatyOfNames[index], name)

    def test_diferents_data_personal(self):
        dictionatyOfNames,_ = personalDataSearchByEnt.searchPersonalData(textForTest["simple"], PersonalData.name)
        self.assertNotEqual(dictionatyOfNames, [])
        self.assertEqual(len(dictionatyOfNames), 1)
        self.assertEqual(dictionatyOfNames[0], "Miguel")
        dictionatyOfNames,_ = personalDataSearchByEnt.searchPersonalData(textForTest["simple"], PersonalData.idCards)
        self.assertEqual(dictionatyOfNames, [])
        dictionatyOfNames,idCards = personalDataSearchByEnt.searchPersonalData("43294881A", PersonalData.idCards)
        self.assertNotEqual(idCards, [])
        self.assertEqual(len(dictionatyOfNames), 0)
        self.assertEqual(len(idCards), 1)
        self.assertEqual(idCards[0], "43294881A")


    def test_isDni(self):
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54094110L"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54094110l"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54.09.41.10l"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54.09 41 10 L"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54 09 41 10L"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54.09-41 10 L"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54 09 41-10L"))
        self.assertEqual(personalDataSearchByEnt.giveIdCards("54 09 41-10L wde 54.09-41 10 L"), ["54 09 41-10L","54.09-41 10 L"])
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54094110 L"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54094110\tL"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54094110         L"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("43294881\t\tA"))
        self.assertFalse(personalDataSearchByEnt.giveIdCards("54094110 hola L"))
        self.assertFalse(personalDataSearchByEnt.giveIdCards("43294884A"))
        self.assertTrue(personalDataSearchByEnt.giveIdCards("54094110\nL"))
        self.assertFalse(personalDataSearchByEnt.giveIdCards("example"))
        self.assertFalse(personalDataSearchByEnt.giveIdCards(""))

    def test_isName(self):
        self.assertTrue(personalDataSearchByEnt.isName("Miguel"))
        self.assertTrue(personalDataSearchByEnt.isName("Miguel Ángel"))
        self.assertTrue(personalDataSearchByEnt.isName("Paco León Medina"))
        self.assertFalse(personalDataSearchByEnt.isName(""))
        self.assertFalse(personalDataSearchByEnt.isName("MIguel9 Medina"))
        self.assertFalse(personalDataSearchByEnt.isName("estoy aqui"))

    def test_check_data_in_DB_name(self):
        self.assertEqual(personalDataSearchByEnt.checkNamesInDB([""]), [])
        self.assertEqual(personalDataSearchByEnt.checkNamesInDB([]), [])
        self.assertEqual(personalDataSearchByEnt.checkNamesInDB(["Miguel"]), ["Miguel"])
        self.assertEqual(personalDataSearchByEnt.checkNamesInDB(["Miguel Ángel Medina Ramírez", 
        "Paco Flores"]), ["Miguel Ángel Medina Ramírez","Paco Flores"])
        self.assertEqual(personalDataSearchByEnt.checkNamesInDB(["Miguel Ángel Medina Ramírez", 
        "Pacccco Floreis"]), ["Miguel Ángel Medina Ramírez"])



if __name__ == '__main__':
    unittest.main()
