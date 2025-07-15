import os
import json
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# OAuth configuration
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Your email address for authentication
AUTHORIZED_EMAIL = os.environ.get('AUTHORIZED_EMAIL', 'your-email@gmail.com')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'google_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'google_token' in session:
        return redirect(url_for('countdown'))
    return render_template('login.html')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['google_token'] = (resp['access_token'], '')
    
    # Get user info
    user_info = google.get('userinfo')
    user_email = user_info.data.get('email', '')
    
    # Check if user is authorized
    if user_email.lower() == AUTHORIZED_EMAIL.lower():
        session['user_email'] = user_email
        return redirect(url_for('countdown'))
    else:
        session.pop('google_token', None)
        return render_template('unauthorized.html', email=user_email)

@app.route('/countdown')
@login_required
def countdown():
    return render_template('countdown.html')

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True, port=5001) 