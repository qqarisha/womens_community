from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from database import Database
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = 'your_secret_key'

# Настройки загрузки файлов
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Проверка допустимого формата файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Инициализация базы данных
db = Database('database.db')


@app.route('/')
def main_page():
    events = db.get_all_events()  # Получаем события из базы
    return render_template("afisha.html", events=events)

@app.route('/meropriatie')
def meropriatie():
    events = db.get_all_events()
    return render_template("meropriatie.html", events=events)


@app.route('/lk', methods=['GET', 'POST'])
def lk():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.get_user_by_id(session['user_id'])
    if not user:
        flash("Пользователь не найден. Пожалуйста, войдите заново.")
        session.clear()
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                db.update_user_avatar(user['id'], filename)
                user['avatar'] = filename
                flash('Аватар обновлён!')

    favorites = db.get_user_favorites(user['id'])
    events = db.get_user_events(user['id'])

    return render_template("lk.html", user=user, favorites=favorites, events=events)


@app.route('/my_events')
def my_events():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    events = db.get_user_events(session['user_id'])
    return render_template("my_events.html", events=events)


@app.route("/admin/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    db.delete_event(event_id)
    flash("Событие удалено", "success")
    return redirect(url_for("admin_lk"))


@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    favorites = db.get_user_favorites(session['user_id'])
    return render_template("favorites.html", favorites=favorites)


@app.route("/admin_lk", methods=["GET", "POST"])
def admin_lk():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        image_file = request.files.get("image")
        image_filename = None
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        db.add_event_with_image(title, description, date, image_filename)

    events = db.get_all_events()
    return render_template("admin_lk.html", events=events)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.get_user_by_email(email)

        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('admin_lk' if user['is_admin'] else 'lk'))
        else:
            flash('Неверный email или пароль')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/lk/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        avatar_file = request.files.get("avatar")

        if password != confirm_password:
            return render_template("register.html", error="Пароли не совпадают")

        if db.get_user_by_email(email):
            return render_template("register.html", error="Email уже зарегистрирован")

        avatar_filename = None
        if avatar_file and allowed_file(avatar_file.filename):
            filename = secure_filename(avatar_file.filename)
            avatar_filename = f"{email}_{filename}"
            avatar_file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

        db.add_user({
            "full_name": full_name,
            "email": email,
            "password": password,
            "is_admin": 0,
            "avatar": avatar_filename
        })

        user = db.get_user_by_email(email)
        session['user_id'] = user['id']
        session['is_admin'] = 0

        flash("Регистрация успешна!", "success")
        return redirect(url_for("lk"))

    return render_template("register.html")


@app.route('/admin/add_event', methods=['GET', 'POST'])
def add_event():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        db.add_event({'title': title, 'description': description, 'date': date})
        flash("Событие добавлено!", "success")
        return redirect('/meropriatie')

    return render_template("add_event.html")

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = db.get_event_by_id(event_id)
    if not event:
        flash("Событие не найдено.")
        return redirect(url_for('main_page'))
    return render_template("event_detail.html", event=event)


@app.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('main_page'))


@app.route('/auth')
def auth():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin_lk'))
        else:
            return redirect(url_for('lk'))
    return redirect(url_for('login'))


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    file = request.files.get('avatar')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        db.update_user_avatar(session['user_id'], filename)

    return redirect(url_for('lk'))


if __name__ == "__main__":
    app.run(debug=True)
