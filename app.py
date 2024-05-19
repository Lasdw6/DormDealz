from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exchange.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    insta = db.Column(db.String(150), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    listing = db.relationship('Listing')

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=True)
    duration = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "userName": self.user_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "duration": self.duration,
            "category": self.category
            }

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
        if user and check_password(user.password, password):
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

@app.route('/listings', methods=['GET'])
def listings():
    try:
        listings = Listing.query.all()
        json_listings = list(map(lambda x: x.to_json(), listings))
        #return jsonify({"listings": json_listings})
        return render_template('listings.html', listings=listings)
    except Exception as e:
        app.logger.error(f"Error fetching listings: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


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

@app.route('/send_message/<int:listing_id>', methods=['POST'])
def send_message(listing_id):
    if 'user_id' not in session:
        flash('You need to be logged in to express interest.', 'warning')
        return redirect(url_for('login'))

    sender_id = session['user_id']
    listing = Listing.query.get_or_404(listing_id)
    receiver_id = listing.user_id

    new_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        listing_id=listing_id,
        content="I'm interested in your listing."
    )

    db.session.add(new_message)
    db.session.commit()
    flash('Your interest has been expressed to the listing owner.', 'success')
    return redirect(url_for('listing_detail', id=listing_id))

@app.route('/inbox')
def inbox():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    messages = Message.query.filter_by(receiver_id=user_id).all()
    return render_template('inbox.html', user=user, messages=messages)

@app.route('/profile_home')
def profile_home():
    if 'user_id' not in session:
        flash('You need to be logged in to view your profile.', 'warning')
        return redirect(url_for('login'))
    return render_template('profile_home.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('You need to be logged in to view your profile.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        flash('You need to be logged in to view your profile.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        insta = request.form['insta']
        user.username= username
        user.email= email
        user.phone = phone
        user.insta = insta
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

@app.route('/wishlist', methods=['GET'])
def wishlist():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    messages = Message.query.filter_by(sender_id= user_id).all()
    for message in messages:
        listings=[]
        listing_id= message.listing_id
        listing= Listing.query.get(listing_id)
        if listing:
            listings.append(listing)
    return render_template('wishlist.html', user=user, listings=listings)

@app.route('/search_go')
def search_go():
        return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if query:
        results = Listing.query.filter(Listing.title.contains(query) | Listing.description.contains(query)).all()
        return render_template('search_results.html', listings=results, query=query)
    else:
        return redirect(url_for('search_go'))
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)