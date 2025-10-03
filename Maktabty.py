# # Maktabty.py
# # -*- coding: utf-8 -*-
# from flask import (
#     Flask, render_template, request, redirect, url_for, session, flash, g
# )
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# import os

# # -------------------- App & Config --------------------
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///library.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # -------------------- Models --------------------
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)
#     is_admin = db.Column(db.Boolean, default=False)

#     def set_password(self, pw):
#         self.password_hash = generate_password_hash(pw)

#     def check_password(self, pw):
#         return check_password_hash(self.password_hash, pw)

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     author = db.Column(db.String(200))
#     copies = db.Column(db.Integer, default=1)

# class Booking(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
#     status = db.Column(db.String(20), default='reserved')  # reserved, returned
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     user = db.relationship('User', backref='bookings')
#     book = db.relationship('Book')

# # -------------------- Helpers --------------------
# def current_user():
#     uid = session.get('user_id')
#     if not uid:
#         return None
#     return User.query.get(uid)

# # --------- Language helpers (must be after app definition) ----------
# @app.before_request
# def set_lang():
#     # default language = English
#     lang = session.get('lang', 'en')
#     g.lang = lang

# def tpl(name):
#     """Return path to template based on selected language (en or ar)."""
#     lang = session.get('lang', 'en')
#     return f"{lang}/{name}"

# @app.route('/set_language/<lang>')
# def set_language(lang):
#     if lang not in ('en', 'ar'):
#         lang = 'en'
#     session['lang'] = lang
#     return redirect(request.referrer or url_for('home'))
# # -------------------------------------------------------------------

# # -------------------- Routes --------------------
# @app.route('/')
# def home():
#     return render_template(tpl('home.html'), user=current_user())

# @app.route('/register', methods=['GET','POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username','').strip()
#         password = request.form.get('password','')
#         if not username or not password:
#             flash('Please provide username and password.')
#             return redirect(url_for('register'))
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists' if session.get('lang','en')=='en' else 'اليوزر موجود بالفعل')
#             return redirect(url_for('register'))
#         u = User(username=username)
#         u.set_password(password)
#         db.session.add(u)
#         db.session.commit()
#         flash('Registered successfully. You can login now.' if session.get('lang','en')=='en' else 'تم التسجيل، دلوقتي تقدر تعمل تسجيل دخول')
#         return redirect(url_for('login'))
#     return render_template(tpl('register.html'))

# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username','').strip()
#         password = request.form.get('password','')
#         u = User.query.filter_by(username=username).first()
#         if not u or not u.check_password(password):
#             flash('Wrong username or password' if session.get('lang','en')=='en' else 'خطأ في اليوزر أو الباسورد')
#             return redirect(url_for('login'))
#         session['user_id'] = u.id
#         flash('Logged in' if session.get('lang','en')=='en' else 'تم تسجيل الدخول')
#         return redirect(url_for('home'))
#     return render_template(tpl('login.html'))

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('Logged out' if session.get('lang','en')=='en' else 'تم تسجيل الخروج')
#     return redirect(url_for('home'))

# @app.route('/books')
# def books():
#     books = Book.query.all()
#     return render_template(tpl('books.html'), books=books, user=current_user())

# @app.route('/book/<int:book_id>/reserve', methods=['POST'])
# def reserve(book_id):
#     if 'user_id' not in session:
#         flash('Please login to reserve' if session.get('lang','en')=='en' else 'اعمل تسجيل دخول عشان تحجز كتاب')
#         return redirect(url_for('login'))
#     book = Book.query.get_or_404(book_id)
#     if book.copies < 1:
#         flash('No copies available right now' if session.get('lang','en')=='en' else 'مافيش نسخ متاحة دلوقتي')
#         return redirect(url_for('books'))
#     book.copies -= 1
#     booking = Booking(user_id=session['user_id'], book_id=book.id)
#     db.session.add(booking)
#     db.session.commit()
#     flash('Book reserved' if session.get('lang','en')=='en' else 'تم حجز الكتاب')
#     return redirect(url_for('my_bookings'))

# @app.route('/my_bookings')
# def my_bookings():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.created_at.desc()).all()
#     # prepare simple view data
#     view_bookings = []
#     for b in bookings:
#         view_bookings.append({
#             "id": b.id,
#             "book_title": b.book.title if b.book else "Unknown",
#             "date": b.created_at.strftime("%Y-%m-%d %H:%M"),
#             "status": b.status
#         })
#     return render_template(tpl('my_bookings.html'), bookings=view_bookings, user=current_user())

# # -------------------- Admin routes --------------------
# @app.route('/admin')
# def admin_index():
#     u = current_user()
#     if not u or not u.is_admin:
#         flash('Not allowed' if session.get('lang','en')=='en' else 'ممنوع')
#         return redirect(url_for('home'))
#     books = Book.query.all()
#     return render_template(tpl('admin_index.html'), books=books, user=u)

# @app.route('/admin/add_book', methods=['GET','POST'])
# def admin_add_book():
#     u = current_user()
#     if not u or not u.is_admin:
#         flash('Not allowed' if session.get('lang','en')=='en' else 'ممنوع')
#         return redirect(url_for('home'))
#     if request.method == 'POST':
#         title = request.form.get('title','').strip()
#         author = request.form.get('author','').strip()
#         try:
#             copies = int(request.form.get('copies', 1))
#         except ValueError:
#             copies = 1
#         if not title:
#             flash('Title is required.')
#             return redirect(url_for('admin_add_book'))
#         b = Book(title=title, author=author, copies=copies)
#         db.session.add(b)
#         db.session.commit()
#         flash('Book added' if session.get('lang','en')=='en' else 'تم إضافة الكتاب')
#         return redirect(url_for('admin_index'))
#     return render_template(tpl('admin_add_book.html'), user=u)

# @app.route('/booking/<int:booking_id>/return', methods=['POST'])
# def return_booking(booking_id):
#     b = Booking.query.get_or_404(booking_id)
#     u = current_user()
#     if not u or (not u.is_admin and b.user_id != u.id):
#         flash('Not allowed' if session.get('lang','en')=='en' else 'غير مسموح')
#         return redirect(url_for('my_bookings'))
#     if b.status != 'returned':
#         b.status = 'returned'
#         if b.book:
#             b.book.copies += 1
#         db.session.commit()
#         flash('Booking returned' if session.get('lang','en')=='en' else 'تمت إعادة الكتاب')
#     return redirect(request.referrer or url_for('my_bookings'))

# # -------------------- Recommender placeholder route --------------------
# @app.route('/recs')
# def recs():
#     # simple placeholder: show latest books as "recommendations"
#     books = Book.query.order_by(Book.id.desc()).limit(5).all()
#     return render_template(tpl('recs.html'), recs=books, user=current_user())

# # -------------------- End routes --------------------

# # -------------------- Run & DB init --------------------
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         # create default admin only if not exists
#         if not User.query.filter_by(username='admin').first():
#             admin = User(username='admin')
#             admin.set_password('admin123')
#             admin.is_admin = True
#             db.session.add(admin)
#             db.session.commit()
#             print("Default admin added (admin/admin123).")
#         else:
#             print("Default admin already exists.")
#     # If console shows garbled text on Windows, run: chcp 65001
#     app.run(debug=True)
#**********************************
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "secret_key_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maktabty.db'
db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100))
    copies = db.Column(db.Integer, default=1)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default="Reserved")

# --- DATABASE INIT ---
def init_db():
    with app.app_context():
        db.create_all()
        # Add some initial books if not exist
        if not Book.query.first():
            sample_books = [
                Book(title="Python Programming", author="John Zelle", copies=5),
                Book(title="Flask Web Development", author="Miguel Grinberg", copies=3),
                Book(title="Data Science Handbook", author="Jake VanderPlas", copies=4)
            ]
            db.session.bulk_save_objects(sample_books)
            db.session.commit()
init_db()

# --- HELPER ---
def current_user():
    uid = session.get('user_id')
    if uid:
        return User.query.get(uid)
    return None

def get_language():
    return session.get('lang', 'en')

# --- ROUTES ---
@app.route("/set_language/<lang>")
def set_language(lang):
    if lang in ['en', 'ar']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

@app.route("/")
def home():
    lang = get_language()
    return render_template(f"{lang}/home.html", user=current_user())

@app.route("/login", methods=["GET","POST"])
def login():
    lang = get_language()
    if request.method=="POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['user_id'] = user.id
            flash("Logged in successfully!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!")
    return render_template(f"{lang}/login.html", user=current_user())

@app.route("/register", methods=["GET","POST"])
def register():
    lang = get_language()
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("User registered!")
            return redirect(url_for('login'))
    return render_template(f"{lang}/register.html", user=current_user())

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("Logged out!")
    return redirect(url_for('home'))

@app.route("/books")
def books():
    lang = get_language()
    books_list = Book.query.all()
    return render_template(f"{lang}/books.html", user=current_user(), books=books_list)

@app.route("/reserve/<int:book_id>", methods=["POST"])
def reserve(book_id):
    user = current_user()
    if not user:
        flash("Login first!")
        return redirect(url_for('login'))
    book = Book.query.get(book_id)
    if book and book.copies > 0:
        book.copies -= 1
        booking = Booking(user_id=user.id, book_id=book.id)
        db.session.add(booking)
        db.session.commit()
        flash("Book reserved successfully!")
    else:
        flash("Book not available!")
    return redirect(url_for('books'))

@app.route("/my_bookings")
def my_bookings():
    lang = get_language()
    user = current_user()
    if not user:
        flash("Login first!")
        return redirect(url_for('login'))
    bookings = Booking.query.filter_by(user_id=user.id).all()
    bookings_info = [{"book_title": Book.query.get(b.book_id).title, "date": b.date.strftime("%Y-%m-%d"), "status": b.status} for b in bookings]
    return render_template(f"{lang}/my_bookings.html", user=user, bookings=bookings_info)

# --- ADMIN ---
@app.route("/admin")
def admin_index():
    lang = get_language()
    u = current_user()
    if not u or u.username != "admin":
        flash("Admin only!")
        return redirect(url_for('home'))
    books_list = Book.query.all()
    return render_template(f"{lang}/admin_index.html", user=u, books=books_list)

@app.route("/admin/add_book", methods=["GET","POST"])
def admin_add_book():
    lang = get_language()
    u = current_user()
    if not u or u.username != "admin":
        flash("Admin only!")
        return redirect(url_for('home'))
    if request.method=="POST":
        title = request.form['title']
        author = request.form['author']
        copies = int(request.form['copies'])
        new_book = Book(title=title, author=author, copies=copies)
        db.session.add(new_book)
        db.session.commit()
        flash("Book added!")
        return redirect(url_for('admin_index'))
    return render_template(f"{lang}/admin_add_book.html", user=u)

@app.route("/recs")
def recs():
    lang = get_language()
    # Just return some books as recommendations
    books_list = Book.query.limit(5).all()
    return render_template(f"{lang}/recs.html", user=current_user(), recs=books_list)

# --- RUN APP ---
if __name__ == "__main__":
    app.run(debug=True)
###############################################################################################