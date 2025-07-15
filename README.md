# Birthday Countdown Tracker

A private birthday countdown tracker with Google OAuth authentication. Only you can access your personal productivity tracker.

## Features

- Visual countdown to your 28th birthday (January 6, 2026)
- Daily progress tracking with visual dots
- Filter weekends and holidays
- Secure Google OAuth login
- Private access (only your email can login)

## Setup Instructions

### 1. Set up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add authorized redirect URI: 
     - For local testing: `http://localhost:5000/authorized`
     - For production: `https://your-app-name.onrender.com/authorized`
   - Save your Client ID and Client Secret

### 2. Local Development

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file (copy from `env.example`):
   ```bash
   cp env.example .env
   ```
5. Edit `.env` with your values:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
   - `AUTHORIZED_EMAIL`: Your email address (only this email can login)
   - `SECRET_KEY`: Generate a random string for Flask sessions
6. Run the application:
   ```bash
   python app.py
   ```
7. Visit http://localhost:5000

### 3. Deploy to Render (Free Hosting)

1. Create a [Render](https://render.com) account
2. Fork or push this code to your GitHub repository
3. In Render dashboard:
   - Click "New +" > "Web Service"
   - Connect your GitHub account and select your repository
   - Configure:
     - Name: Choose a unique name (e.g., `birthday-tracker-yourname`)
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Add environment variables (same as your `.env` file):
     - `GOOGLE_CLIENT_ID`
     - `GOOGLE_CLIENT_SECRET`
     - `AUTHORIZED_EMAIL`
     - `SECRET_KEY`
   - Click "Create Web Service"

4. Update Google OAuth:
   - Go back to Google Cloud Console
   - Add your Render URL to authorized redirect URIs:
     `https://your-app-name.onrender.com/authorized`

5. Your app will be live at: `https://your-app-name.onrender.com`

## Alternative Free Hosting Options

- **Vercel**: Requires converting to a serverless function
- **Railway**: Easy deployment with GitHub integration
- **Google Cloud Run**: Has a generous free tier
- **Fly.io**: Good for small apps

## Security Notes

- Only the email specified in `AUTHORIZED_EMAIL` can access the tracker
- Never commit your `.env` file to version control
- Generate a strong `SECRET_KEY` for production
- Keep your Google OAuth credentials secure

## Customization

To change the target date (currently Jan 6, 2026), edit line 264 in `templates/countdown.html`:
```javascript
const endDate = new Date('2026-01-06');
``` 