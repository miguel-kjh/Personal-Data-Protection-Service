from flask import Flask, request,render_template

app = Flask(__name__)

@app.route('/')
def doc():
    return render_template('doc.html')

@app.route('/web')
def web():
    return render_template('web.html')

if __name__ == "__main__":
    app.run(port=5001, debug=False)