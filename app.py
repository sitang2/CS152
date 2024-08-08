from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24).hex()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    expiry_date = db.Column(db.DateTime)
    review_code = db.Column(db.String(6), unique=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    business = db.relationship('Business', backref=db.backref('reviews', lazy=True))

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful.', 'success')
            return redirect(url_for('business_list'))
        flash('Login failed. Check your email and password.', 'error')
    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/business_list')
def business_list():
    businesses = Business.query.all()
    return render_template('business_list.html', businesses=businesses)

@app.route('/submit_review/<int:business_id>', methods=['GET', 'POST'])
@login_required
def submit_review(business_id):
    business = Business.query.get_or_404(business_id)
    error_message = None

    if request.method == 'POST':
        review_code = request.form['review_code']
        rating = request.form.get('rating')
        review_text = request.form['review']

        # Validate review code
        review = Review.query.filter_by(review_code=review_code, business_id=business_id).first()
        if review and review.expiry_date > datetime.now():
            # Insert or update the review
            if not review.rating and not review.review:
                review.rating = rating
                review.review = review_text
                db.session.commit()
                flash('Review submitted successfully!')
            else:
                flash('Review already submitted.')
            return redirect(url_for('view_business', business_id=business_id))
        else:
            error_message = 'Invalid or expired review code. Please try again.'
            print('Invalid or expired review code.')

    return render_template('submit_review.html', business_id=business_id, error_message=error_message)

@app.route('/business/<int:business_id>')
def view_business(business_id):
    business = Business.query.get_or_404(business_id)
    reviews = Review.query.filter_by(business_id=business_id).all()
    return render_template('view_business.html', business=business, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
