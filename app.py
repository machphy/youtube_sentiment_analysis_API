from flask import Flask, request, render_template, after_this_request
import googleapiclient.discovery
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from analyze_youtube_video import extract_video_id, get_comments, analyze_sentiment, plot_sentiments
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from werkzeug.utils import secure_filename
import logging

# Initialize Flask app
app = Flask(__name__)

# Add HTTPS enforcement and content security policy using Flask-Talisman
talisman = Talisman(app, force_https=True, content_security_policy={
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'"],
    'object-src': ["'none'"]
})

# Enable CSRF protection
app.config['SECRET_KEY'] = 'your-secret-key'
csrf = CSRFProtect(app)

# Rate limiting setup (for the entire application)
limiter = Limiter(app)

# Set up logging for error tracking
logging.basicConfig(level=logging.ERROR)

# API key for YouTube API
API_KEY = 'AIzaSyCuhpv4DkE8D8IgB8vLSFx1UVmwYkqHzm8'

# Initialize the limiter for the rate limit on POST requests
@limiter.limit("5 per minute")  # 5 requests per minute

def get_video_details(video_id, api_key):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    video_details = response.get('items', [])[0].get('snippet', {}) if response.get('items') else {}
    return {
        'title': video_details.get('title', 'Unknown Title'),
        'description': video_details.get('description', 'No Description'),
        'thumbnail': video_details.get('thumbnails', {}).get('high', {}).get('url', '')
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    img_base64 = None
    sentiments = {}
    video_url = None
    video_details = {}
    
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if video_url:
            # Sanitize video URL
            video_url = secure_filename(video_url)
            
            video_id = extract_video_id(video_url)
            if video_id:
                try:
                    # Fetch video details
                    video_details = get_video_details(video_id, API_KEY)
                    
                    # Get comments and analyze sentiment
                    comments = get_comments(video_id, API_KEY)
                    sentiments = analyze_sentiment(comments) or {}  # Ensure it's a dictionary
                    
                    # Save and display sentiment chart
                    img_path = 'static/plot.png'
                    plot_sentiments(sentiments)
                    
                    with open(img_path, 'rb') as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                except Exception as e:
                    error = "An error occurred while processing the video."
                    app.logger.error(f"Error: {str(e)}")  # Log error for debugging
            else:
                error = 'Invalid YouTube URL'
    
    return render_template('index.html', error=error, img_base64=img_base64, sentiments=sentiments, video_url=video_url, video_details=video_details)

# After request hook for security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True)
