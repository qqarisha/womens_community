from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template("afisha.html")

@app.route('/afisha')
def about():
    return render_template("meropriatie.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)