from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return "hello, version aplha 1.0"

if __name__ == "__main__":
    app.run(debug = True)