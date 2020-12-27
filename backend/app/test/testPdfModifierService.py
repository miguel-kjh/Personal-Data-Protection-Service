from app.test.base import BaseTestCase
from app.main.service.PdfModifierService import PdfModifierService
from app.test.fileVariables import pathDocuments,nameDocuments

import unittest
import os

@unittest.skip("for api credits")
class MyTestCase(BaseTestCase):

    def setUp(self):
        self.service = PdfModifierService()

    def test_upload_file(self):
        self.assertNotEqual(self.service._uploadFile(os.path.join(pathDocuments, nameDocuments + ".pdf")), '')

    def test_replace_string_in_a_pdf(self):
        self.assertTrue(self.service.modifiedPdf(
            os.path.join(pathDocuments, nameDocuments + ".pdf"),
            os.path.join(pathDocuments, "document_test_resul.pdf"),
            ["Miguel", "Ángel"],
            ["Borja", "Zarco"]
        ))


if __name__ == '__main__':
    unittest.main()
