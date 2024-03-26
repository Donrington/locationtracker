import json, os, requests
from os.path import basename
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
from flask_login import current_user, login_required
from flask import * 
from flask_socketio import SocketIO, emit, join_room, leave_room
from markupsafe import escape
import re 
from flask_wtf.csrf import CSRFProtect
from location import app,csrf,socketio
from location .forms import *
from flask_login import login_required
from location.models import db,User,Location
from sqlalchemy import func,desc  
from datetime import datetime





@app.route('/')
def index():
    user_id = session.get('userlogged')
    user = User.query.get(user_id)

    config_items = app.config
    return render_template('index.html', pagename="Home Page", user=user, config_items=config_items)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if not username or not password or not email:
            flash('All fields are required.')
            return render_template('Registration.html')
    
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            password_hash = generate_password_hash(password)
            new_user = User(username=username, password_hash=password_hash, email=email)
            db.session.add(new_user)
            db.session.commit()
            session['userlogged'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Username already exists')
            
    return render_template('Registration.html')
# Example login logic

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            # Proceed with your authentication logic...
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['userlogged'] = user.id  # Make sure this is the correct user attribute
                return redirect(url_for('dashboard'))
        except BadRequestKeyError:
            flash('Missing username or password', 'danger')
            return redirect(url_for('login'))
    # Render login template if method is GET or in case of error
    return render_template('login.html')



@app.route('/logout/')
def logout():
    user = None  # Initialize user as None

    if session.get('userlogged') is not None:
        user = session.get('userlogged')
        # Assuming you have a database model for users named MyUser
        user = User.query.get(user)

        session.pop('userlogged', None)
        flash('You have been logged out', category='success')

    return redirect(url_for('index'))
  

# Google Maps API URL
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

@app.route('/dashboard')
def dashboard():
    user_id = session.get('userlogged')
    if not user_id:
        flash('You must be logged in to view the dashboard.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    total_locations = Location.query.filter_by(user_id=user.id).count()
    last_location = Location.query.filter_by(user_id=user.id).order_by(Location.timestamp.desc()).first()
    
    # Extract the address from the last location if it exists
    last_address = "Not available"
    if last_location:
        # Make a request to the Google Maps API to get the address
        params = {
            'latlng': f"{last_location.latitude},{last_location.longitude}",
            'key': app.config['GOOGLE_MAPS_API_KEY']
        }
        response = requests.get(GOOGLE_MAPS_API_URL, params=params)
        if response.status_code == 200:
            results = response.json()
            last_address = results['results'][0]['formatted_address']
            
    return render_template('dashboard.html', 
                           user=user, 
                           pagename="Dashboard", 
                           total_locations=total_locations, 
                           last_address=last_address,
                           last_location=last_location)

@app.route('/location', methods=['POST'])
def location():
    if 'userlogged' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user = User.query.filter_by(id=session['userlogged']).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json(silent=True)  # silent=True will fail quietly if the data isn't JSON
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    latitude = data['latitude']
    longitude = data['longitude']

    # Check if the incoming data is from a search form or geolocation API
    if request.json:
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']
    else:
        latitude = request.form['latitude']
        longitude = request.form['longitude']

    api_key = app.config['GOOGLE_MAPS_API_KEY']
    params = {'latlng': f'{latitude},{longitude}', 'key': api_key}
    response = requests.get(GOOGLE_MAPS_API_URL, params=params)

    if response.status_code == 200:
        results = response.json()
        address = results['results'][0]['formatted_address']
        # Create and save a new location
        new_location = Location(user_id=user.id, latitude=latitude, longitude=longitude)
        db.session.add(new_location)
        db.session.commit()
        return jsonify({'address': address}), 200
    else:
        return jsonify({'error': 'Unable to get the address'}), response.status_code



@app.route('/location-history')
def location_history():
    # Directly check for 'userlogged' in session and retrieve its value
    user_id = session.get('userlogged', None)

    # If user_id is None (meaning 'userlogged' is not in session), redirect to login
    if not user_id:
        flash('You must be logged in to view the location history.', 'warning')
        return redirect(url_for('login'))

    # Fetch the user by ID. If not found, it will abort with a 404 error.
    user = User.query.get_or_404(user_id)

    # Query the locations for the current user, ordered by timestamp
    locations = Location.query.filter_by(user_id=user.id).order_by(Location.timestamp.desc()).all()

    # Pass both the locations and the user to the template
    return render_template('locationhistory.html', user=user, locations=locations)


@app.route('/delete-location/<int:location_id>', methods=['POST'])
def delete_location(location_id):
    if 'userlogged' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    location = Location.query.get_or_404(location_id)
    
    # Check if the current user owns the location to prevent unauthorized deletion
    if location.user.username != session['userlogged']:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(location)
    db.session.commit()

    return jsonify({'success': 'Location deleted successfully'})

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from flask import Flask, request, redirect, url_for, flash, render_template, session
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os

@app.route('/update-profile', methods=['POST', 'GET'])
def update_profile():
    # Assuming 'userlogged' contains the username of the currently logged-in user
    user_id = session.get('userlogged')
    if not user_id:
        flash('Please log in to update your profile.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    if not user:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('userprofile.html', user=user)

    elif request.method == 'POST':
        try:
            username = request.form.get('username')
            new_email = request.form.get('email')
            new_password = request.form.get('password')
            profile_picture = request.files.get('profile_picture')

            if username and username != user.username:
                # Check if the new username already exists to avoid duplicates
                if User.query.filter_by(username=username).first():
                    flash('Username already exists. Please choose a different one.', 'danger')
                    return redirect(url_for('update_profile'))
                
                user.username = username
                # Update the session with the new username
                session['userlogged'] = username

            if new_email:
                user.email = new_email

            if new_password:
                user.password_hash = generate_password_hash(new_password)

            if profile_picture and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                profile_picture.save(filepath)
                user.profile_picture = filename

            db.session.commit()
            flash('Profile information has been updated successfully.', 'success')
            return redirect(url_for('update_profile'))

        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')

    return render_template('userprofile.html', user=user)





@app.errorhandler(BadRequestKeyError)
def handle_bad_request(e):
    return 'Bad Request: {}'.format(e), 400


