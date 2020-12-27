import requests
import os

from config import API_KEY

class PdfModifierService:
    def __init__(self):
        self.apikey = API_KEY
        self.apiUrl = "https://api.pdf.co/v1"

    def _uploadFile(self, sourceFile: str) -> str:
        """
        Uploads file to the cloud
        :param: sourceFile: string
        :return: uploadedFileUrl: string
        """
        url = "{}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={}".format(
        self.apiUrl, os.path.basename(sourceFile))

        response = requests.get(url, headers={ "x-api-key": self.apikey })
        if (response.status_code == 200):
            json = response.json()

            if json["error"] == False:
                uploadUrl = json["presignedUrl"]
                uploadedFileUrl = json["url"]
                with open(sourceFile, 'rb') as file:
                    requests.put(uploadUrl, data=file, headers={ "x-api-key": API_KEY, "content-type": "application/octet-stream" })

                return uploadedFileUrl
            else:
                raise RuntimeError(json["message"])
        else:
            raise RuntimeError(f"Request error: {response.status_code} {response.reason}")

    def _replaceStringFromPdf(self, uploadedFileUrl: str, destinationFile: str, data: list, replace: list):
        """
        Replace Text FROM UPLOADED PDF FILE using PDF.co Web API
        :param: uploadedFileUrl: string
        :param: destinationFile: string
        :param: data: list
        :param: replace: list
        :return: None
        """

        parameters = {
            "url":uploadedFileUrl,
            "searchStrings": data,
            "replaceStrings": replace,
            "password": "",
            "name": os.path.basename(destinationFile)
        }

        url = "{}/pdf/edit/replace-text".format(self.apiUrl)

        response = requests.post(url, json=parameters,
                                 headers={ "x-api-key": self.apikey,  "Content-Type": "application/json"})
        if (response.status_code == 200):
            json = response.json()

            if json["error"] == False:
                resultFileUrl = json["url"]
                r = requests.get(resultFileUrl, stream=True)
                if (r.status_code == 200):
                    with open(destinationFile, 'wb') as file:
                        for chunk in r:
                            file.write(chunk)
                    print(f"Result file saved as \"{destinationFile}\" file.")
                else:
                    raise RuntimeError(f"Request error: {response.status_code} {response.reason}")
            else:
                raise RuntimeError(json["message"])
        else:
            raise RuntimeError(f"Request error: {response.status_code} {response.reason}")

    def modifiedPdf(self, sourceFile: str, destinationFile: str, data: list, replace: list) -> bool:
        try:
            uploadedFileUrl = self._uploadFile(sourceFile)
            self._replaceStringFromPdf(uploadedFileUrl, destinationFile, data, replace)
            return True
        except Exception as e:
            print(e)
            return False
