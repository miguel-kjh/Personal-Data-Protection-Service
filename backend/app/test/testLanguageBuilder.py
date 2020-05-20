from app.test.base import BaseTestCase
from app.main.service.languageBuilder import LanguageBuilder

import unittest

class TestLanguageBuilder(BaseTestCase):
    def test_semanticSimilarity(self):
        self.assertTrue(LanguageBuilder().semanticSimilarity("papa", "patata") > 0.5)
        self.assertTrue(LanguageBuilder().semanticSimilarity("", "patata") < 0.5)
        self.assertTrue(LanguageBuilder().semanticSimilarity("hormigon", "patata") < 0.5)

    def test_hasContex(self):
        self.assertTrue(LanguageBuilder().hasContex("Hola, que tal?"))
        self.assertFalse(LanguageBuilder().hasContex("MIGUEL"))
        self.assertFalse(LanguageBuilder().hasContex("MIGUEL ÁNGEL"))
        self.assertFalse(LanguageBuilder().hasContex(""))

if __name__ == '__main__':
    unittest.main()