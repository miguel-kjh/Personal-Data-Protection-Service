from app.test.base import BaseTestCase
from app.main.service.PdfModifierService import PdfModifierService

import unittest




class MyTestCase(BaseTestCase):

    def setUp(self):
        self.service = PdfModifierService()

    def test_upload_file(self):
        self.assertTrue(self.service._uploadFile("ddd"))


if __name__ == '__main__':
    unittest.main()
