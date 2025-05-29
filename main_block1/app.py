from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database
import os
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
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


@app.route('/lk')
def lk():
    if 'user_token' not in session:
        return redirect(url_for('login'))

    user = db.get_user_by_token(session['user_token'])
    if not user:
        flash("Пользователь не найден. Пожалуйста, войдите заново.")
        session.clear()
        return redirect(url_for('login'))

    events = db.get_user_events(user['token'])
    return render_template("lk.html", user=user, events=events)


@app.route('/my_events')
def my_events():
    if 'user_token' not in session:
        return redirect(url_for('login'))
    
    events = db.get_user_events(session['user_token'])
    return render_template("my_events.html", events=events)


@app.route("/admin/delete_event/<int:event_token>", methods=["POST"])
def delete_event(event_id):
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    db.delete_event(event_id)
    flash("Событие удалено", "success")
    return redirect(url_for("admin_lk"))


@app.route("/admin_lk", methods=["GET", "POST"])
def admin_lk():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        full_description = request.form["full_description"]
        event_format = request.form["event_format"]
        organizer = request.form["organizer"]
        location = request.form["location"]
        date = request.form["date"]

        image_file = request.files.get("image")
        image_filename = None
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        db.add_event_with_image(title, description, full_description, event_format, organizer, location, date, image_filename)

    events = db.get_all_events()
    return render_template("admin_lk.html", events=events)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        password_hash = hash_object.hexdigest()

        user = db.get_user_by_email(email)

        if user and user['password_hash'] == password_hash:
            session['user_token'] = user['token']
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

        if password != confirm_password:
            return render_template("register.html", error="Пароли не совпадают")

        if db.get_user_by_email(email):
            return render_template("register.html", error="Email уже зарегистрирован")
        
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        password_hash = hash_object.hexdigest()

        db.add_user({
            "full_name": full_name,
            "email": email,
            "password_hash": password_hash,
            "is_admin": 0,
        })

        user = db.get_user_by_email(email)
        session['user_token'] = user['token']
        session['is_admin'] = 0

        flash("Регистрация успешна!", "success")
        return redirect(url_for("lk"))

    return render_template("register.html")


@app.route('/admin/add_event', methods=['GET', 'POST'])
def add_event():
    if 'user_token' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        full_description = request.form['full_description']
        event_format = request.form['event_format']
        organizer = request.form['organizer']
        location = request.form['location']
        date = request.form['date']
        db.add_event({
            'title': title, 
            'description': description, 
            'full_description': full_description,
            'event_format': event_format,
            'organizer': organizer,
            'location': location,
            'date': date})
        flash("Событие добавлено!", "success")
        return redirect('/meropriatie')

    return render_template("add_event.html")

@app.route('/event/<int:event_token>')
def event_detail(event_token):
    event = db.get_event_by_token(event_token)
    if not event:
        flash("Событие не найдено.")
        return redirect(url_for('main_page'))
    return render_template("meropriatie.html", event=event)


@app.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('main_page'))


@app.route('/auth')
def auth():
    if 'user_token' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin_lk'))
        else:
            return redirect(url_for('lk'))
    return redirect(url_for('login'))

@app.route('/lk/mero_register/<event_token>')
def mero_register(event_token):
    # Проверка авторизации пользователя
    if 'user_token' not in session:
        flash('Для регистрации на мероприятие необходимо войти в систему', 'warning')
        return redirect(url_for('login'))
    
    user_token = session['user_token']
    
    # Проверка существования пользователя
    user = db.get_user_by_token(user_token)
    if not user:
        flash('Пользователь не найден. Пожалуйста, войдите заново.', 'error')
        session.clear()
        return redirect(url_for('login'))
    
    # Проверка существования мероприятия
    event = db.get_event_by_token(event_token)
    if not event:
        flash('Мероприятие не найдено', 'error')
        return redirect(url_for('main_page'))
    
    if db.is_user_registered(user_token, event_token):
        flash('Вы уже зарегистрированы на это мероприятие', 'info')
        return redirect(url_for('my_events'))

    try:
        # Регистрация пользователя на мероприятие
        db.register_for_event(user_token, event_token)
        flash('Регистрация на мероприятие прошла успешно!', 'success')
        return redirect(url_for('my_events'))
    
    except Exception as e:
        flash(f'Произошла ошибка при регистрации: {str(e)}', 'error')
        return redirect(url_for('event_detail', event_token=event_token))

# Будет удалено
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

# Будет удалено
@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    favorites = db.get_user_favorites(session['user_id'])
    return render_template("favorites.html", favorites=favorites)

if __name__ == "__main__":
    app.run(debug=True)
