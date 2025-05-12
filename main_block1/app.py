from flask import Flask, render_template
from flask_cors import CORS
from api import bp as api_bp  

app = Flask(__name__)
cors = CORS(app, resources=r'/api/*')

@app.route('/')
def main_page():
    return render_template("afisha.html")

@app.route('/meropriatie')
def meropriatie():
    return render_template("meropriatie.html")

@app.route('/lk')
def lk():
    return render_template("lk.html")

@app.route('/lk/register')
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.register_blueprint(api_bp)

    app.run(debug=True, port=5000)