from flask import Flask, request, render_template

version = "alpha 1.0"
app = Flask(__name__)

@app.route('/')
def main():
    return "hello, version aplha 1.0"

@app.route('/version')
def getVersion():
    return {
        "version":version
    }

@app.route('/file')
def getOperations():
    return {
        "operations":"encode,target,give list of names and give csv of names"
    }

@app.route('/file/encode', methods=['POST'])
def getFileEncode():
    return "encode does not have implementation yet"

@app.route('/file/listNames', methods=['POST'])
def getListOfNames():
    return "listNames does not have implementation yet"

@app.route('/file/target/htmlFile', methods=['POST'])
def getHtmlFilesWithNameMarked():
    return "target does not have implementation yet"

@app.route('/file/giveCsvFile', methods=['POST'])
def giveCsvFile():
    return "csv does not have implementation yet"

if __name__ == "__main__":
    app.run(debug = True)