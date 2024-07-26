import googleapiclient.discovery
from textblob import TextBlob
import matplotlib.pyplot as plt
from urllib.parse import urlparse, parse_qs
import os

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]  # Extract ID from shortened URL
    elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]  # Extract ID from full URL
    return None

def get_comments(video_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()
    
    while request is not None:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment)
        
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            request = None

    return comments

def analyze_sentiment(comments):
    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
    for comment in comments:
        analysis = TextBlob(comment)
        if analysis.sentiment.polarity > 0:
            sentiments['positive'] += 1
        elif analysis.sentiment.polarity == 0:
            sentiments['neutral'] += 1
        else:
            sentiments['negative'] += 1
    return sentiments

def plot_sentiments(sentiments):
    labels = sentiments.keys()
    sizes = sentiments.values()
    colors = ['green', 'blue', 'red']
    explode = (0.1, 0, 0)
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Sentiment Analysis of YouTube Comments')
    plt.savefig('static/plot.png')  # Save the plot as a static image
    plt.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python analyze_youtube_video.py https://youtu.be/QELLdNrdYnU?si=QmUO951UzQGeze9e")
        sys.exit(1)
    
    video_url = sys.argv[1]
    video_id = extract_video_id(video_url)
    if not video_id:
        print("Invalid YouTube URL")
        sys.exit(1)
    
    api_key = 'AIzaSyDQZHgcESrX4vEdAzJjS7t2BGQhZSRduFw'  # Replace with your YouTube API key
    
    comments = get_comments(video_id, api_key)
    sentiments = analyze_sentiment(comments)
    plot_sentiments(sentiments)
