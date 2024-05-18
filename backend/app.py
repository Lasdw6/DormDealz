from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exchange.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=True)
    duration = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hash, password):
    return hash == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        new_user = User(username=username, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            db.session.commit()
            return redirect(url_for('login'))
        except:
            flash('Registration failed. Email or username already exists.', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/listings')
def listings():
    listings = Listing.query.all()
    return render_template('listings.html', listings=listings)

@app.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    if 'user_id' not in session:
        flash('Please log in to create a listing.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        duration = request.form['duration']
        category = request.form['category']
        new_listing = Listing(user_id=session['user_id'], title=title, description=description, price=price, duration=duration, category=category)
        db.session.add(new_listing)
        db.session.commit()
        flash('Listing created successfully!', 'success')
        return redirect(url_for('listings'))
    return render_template('create_listing.html')

@app.route('/listing/<int:id>')
def listing_detail(id):
    listing = Listing.query.get_or_404(id)
    return render_template('listing_detail.html', listing=listing)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = Listing.query.filter(Listing.title.contains(query) | Listing.description.contains(query)).all()
    return render_template('search_results.html', listings=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
