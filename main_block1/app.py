from flask import Flask, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from database import Database
import database_requests as reqs 
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

@app.route('/lk/izbr/<token>')
def izbr(token):
    db = Database('database.db')
    user = db.cursor.execute(reqs.data_by_token, (token,)).fetchone()
    if user:
        return render_template("izbr.html", user_name=user[0], user_email=user[1])
    return redirect(url_for('lk'))

'''
@app.route('/lk/admin')
def izbr():
    return render_template("izbr.html")
'''

if __name__ == "__main__":
    app.register_blueprint(api_bp)

    app.run(debug=True, port=5000)