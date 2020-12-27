import requests

class PdfModifierService:
    def __init__(self):
        self.apikey = "***"
        self.apiUrl = "https://api.pdf.co/v1"

    def _uploadFile(self, sourceFile: str) -> str:
        return ""

    def replaceStringFromPdf(self, uploadFileUrl: str, destinationFile: str, data: list, replace: list) -> bool:
        return True
