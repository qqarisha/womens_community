from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from database import Database
import sys
import io

# Устанавливаем корректную кодировку для консоли
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = 'your_secret_key'

db = Database('database.db')

@app.route('/')
def main_page():
    return render_template("afisha.html")

@app.route('/meropriatie')
def meropriatie():
    events = db.get_all_events()
    return render_template("meropriatie.html", events=events)

@app.route('/lk')
def lk():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("lk.html")

# Добавьте этот маршрут в app.py
@app.route('/check_events')
def check_events():
    events = db.get_all_events()
    return jsonify({
        'status': 'success',
        'events': events,
        'count': len(events)
    })

@app.route("/admin_lk", methods=["GET", "POST"])
def admin_lk():
    if request.method == "POST":
        print("\n[REQUEST DATA]")
        print("Form data:", request.form)
        print("JSON data:", request.json)
        print("Headers:", request.headers)
        
        # Остальная обработка формы
        print("\n[FORM] Получены данные:", request.form)
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        
        if not all([title, description, date]):
            print("[VALIDATION] Не все поля заполнены")
            flash("Все поля должны быть заполнены", "error")
            return redirect(url_for("admin_lk"))

        print(f"[EVENT] Попытка добавления: {title} | {date}")
        if db.add_event(title, description, date, session.get("user_id")):
            flash("Событие успешно добавлено!", "success")
        else:
            flash("Ошибка при добавлении события", "error")
        
        return redirect(url_for("admin_lk"))

        # Добавляем отладочный вывод
        print(f"Данные для добавления: {title}, {description}, {date}")
        
        if db.add_event(title, description, date, session.get("user_id")):
            flash("Событие успешно добавлено!", "success")
        else:
            flash("Ошибка при добавлении события", "error")
        
        return redirect(url_for("admin_lk"))

    events = db.get_all_events()
    print(f"Получено событий из БД: {len(events)}")  # Отладочный вывод
    return render_template("admin_lk.html", events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.get_user_by_email(email)

        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('admin_lk' if user['is_admin'] else 'lk'))
        else:
            flash('Неверный email или пароль')
    
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Пароли не совпадают")
            return render_template("register.html")

        if db.get_user_by_email(email):
            flash("Email уже зарегистрирован")
            return render_template("register.html")
            
        db.add_user({
            "full_name": full_name,
            "email": email,
            "password": password,
            "is_admin": 0
        })
        flash("Регистрация успешна! Теперь войдите", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из системы", "success")
    return redirect(url_for('main_page'))

@app.route('/auth')
def auth():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)