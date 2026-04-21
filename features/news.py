import os
import requests
from core.speaker import speak
from dotenv import load_dotenv

load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")

def handle_news_fetch(command):
    """Generates sequential audio summaries representing live headlines by category."""
    if not news_api_key:
        speak("News API key is missing. Please configure it in the environment.")
        return
        
    category_pattern = ""
    categories = ["business", "entertainment", "health", "science", "sports", "technology", "tech"]
    
    for cat in categories:
        if cat in command:
            category_pattern = "&category=technology" if cat == "tech" else f"&category={cat}"
            break
            
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in{category_pattern}&apiKey={news_api_key}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if not articles:
                speak("I couldn't find any news articles right now.")
            else:
                for article in articles[:5]:
                    speak(article['title'])
        else:
            speak("Failed to fetch news from the provider.")
    except Exception as e:
        print(f"News API Error: {e}")
        speak("I encountered an error while trying to fetch the news.")

def process(command, is_offline=False):
    if "news" in command:
        if is_offline:
            speak("Offline mode active. I cannot fetch the news right now.")
            return True
        handle_news_fetch(command)
        return True
    return False
