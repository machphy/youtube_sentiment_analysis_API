# YouTube Sentiment Analysis 😊😐😔😡

![YouTube Sentiment Analysis](https://media.sproutsocial.com/uploads/2023/07/Sentiment-analysis-HUB-Final.jpg)
<br>

## About
**A web application that performs sentiment analysis on YouTube video comments. The application uses the YouTube Data API to fetch comments and then analyzes their sentiment using a pre-trained model. Results are visualized and displayed on a web interface.**

Sentiment Analysis is a popular application of Natural Language Processing (NLP). This project focuses on analyzing YouTube comments to understand the sentiments expressed by viewers.

<br>

## Live Link
**Hosted on GitHub Pages**

### 🔗 [Live Demo Link](https://github.com/machphy/youtube_sentiment_analysis_API)

<br>

## Project Specifications

**Below are the libraries and frameworks used to create the project:**
- **Web Framework:** Flask
- **Visualization:** Matplotlib
- **Sentiment Analysis Libraries:** TensorFlow/Keras
- **API Requests:** `requests`

<br>

## Project Components

**The project currently includes:**
1. **Comment Analysis** - Fetches comments from a YouTube video using the YouTube Data API and analyzes their sentiment.
2. **Visualization** - Displays sentiment distribution and insights using charts.

<br>

## Screenshots

**Application Interface**

![Screenshot 2024-07-26 185950](doc/Screenshot%202024-07-26%20185950.png)

**Sentiment Analysis Results**

![Screenshot 2024-07-26 190011](doc/Screenshot%202024-07-26%20190011.png)

<br>




<br>

## Important Information

### **YouTube Data API**

API documentation link - [YouTube Data API Documentation](https://developers.google.com/youtube/v3/docs)

<br>

To work with the API, you need to **create an API key**.
To create an API key, **register** on the Google Cloud Console and a unique key will be generated for you. Use this key to make successful API requests.

**Note:** Ensure your API key is kept secure and adhere to usage limits.

<br>

### **API Specifications**
To fetch comments, the application performs the following API calls:
1. **Fetch Comments** - Retrieve comments for a YouTube video using the YouTube Data API.
2. **Analyze Sentiment** - Process the comments and analyze their sentiment.

**API Endpoint for Comments** - `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={videoId}&key={apiKey}`

<br>

## Models Used
The project uses pre-trained models for sentiment analysis. Here’s a brief overview of the tools used:

- **TensorFlow/Keras** - Libraries for building and using machine learning models for sentiment analysis.

<br>

*__Note:__*
1. The sentiment analysis model classifies comments into sentiment categories (POSITIVE🙂, NEGATIVE☹️, NEUTRAL😐).

<br>

## Project Development Ideas

**Future enhancements may include:**
- Analyzing comments in different languages.
- Integrating with other social media platforms.
- Enhancing visualizations with interactive charts.

<br>
# rajeev@2024 

<br> 
## Thank You!
Thank you for exploring the project. **I hope you find it useful**. 

If you did, please consider **giving a star**⭐ to this repository. It would mean a lot!
