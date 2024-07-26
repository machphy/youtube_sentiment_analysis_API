from flask import Flask, request, render_template
import googleapiclient.discovery
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from analyze_youtube_video import extract_video_id, get_comments, analyze_sentiment, plot_sentiments

app = Flask(__name__)


API_KEY = 'AIzaSyCuhpv4DkE8D8IgB8vLSFx1UVmwYkqHzm8'

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
            video_id = extract_video_id(video_url)
            if video_id:
                try:
                    video_details = get_video_details(video_id, API_KEY)
                    comments = get_comments(video_id, API_KEY)
                    sentiments = analyze_sentiment(comments) or {}  # Ensure it's a dictionary
                    img_path = 'static/plot.png'
                    plot_sentiments(sentiments)
                    with open(img_path, 'rb') as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                except Exception as e:
                    error = str(e)
            else:
                error = 'Invalid YouTube URL'
    
    return render_template('index.html', error=error, img_base64=img_base64, sentiments=sentiments, video_url=video_url, video_details=video_details)

if __name__ == '__main__':
    app.run(debug=True)
