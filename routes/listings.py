from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from webapp.models import Listing, db

listings = Blueprint('listings', __name__)

@listings.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        duration = request.form.get('duration')
        category = request.form.get('category')
        new_listing = Listing(title=title, description=description, price=price, duration=duration, category=category, owner=current_user)
        db.session.add(new_listing)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_listing.html')

@listings.route('/listings')
def view_listings():
    all_listings = Listing.query.filter_by(status='available').all()
    return render_template('view_listings.html', listings=all_listings)
