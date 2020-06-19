from app.test.base                        import BaseTestCase
from app.main.util.anonymizationFunctions import encode,dataObfuscation,disintegration

class TestAnonymization(BaseTestCase):
    def test_funtion(self):
        self.assertEqual(disintegration(''),'')
        self.assertEqual(disintegration('Miguel'),'******')
        self.assertEqual(disintegration('M'),'*')
        self.assertEqual(disintegration('43294881A'),'***9488**')
        self.assertEqual(disintegration('42610341N'),'***1034**')
        self.assertEqual(disintegration('42610341'),'********')

        self.assertNotEqual(dataObfuscation('43294881A'),disintegration('4*******A'))
        self.assertEqual(dataObfuscation('Miguel Ángel'),'M***** Á****')

        self.assertEqual(encode(''),'')
        self.assertEqual(encode('ddd'),'***')