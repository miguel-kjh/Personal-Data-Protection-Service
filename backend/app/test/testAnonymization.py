from app.test.base                        import BaseTestCase
from app.main.util.anonymizationFunctions import encode,dataObfuscation,disintegration

class TestAnonymization(BaseTestCase):
    def test_funtion(self):
        self.assertEqual(dataObfuscation(''),'')
        self.assertEqual(dataObfuscation('Miguel'),'M*****')
        self.assertEqual(dataObfuscation('M'),'M')
        self.assertEqual(dataObfuscation('Miguel Ángel'),'M***** Á****')
        self.assertEqual(dataObfuscation('43294881A'),'***9488**')
        self.assertEqual(dataObfuscation('42610341N'),'***1034**')
        self.assertEqual(dataObfuscation('42610341'),'4*******')
        self.assertNotEqual(disintegration('42610341'),disintegration('42610341'))
        self.assertEqual(encode(''),'')
        self.assertEqual(encode('ddd'),'***')