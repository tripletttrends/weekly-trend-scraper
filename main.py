import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import datetime

def get_google_trends(keyword):
    url = f"https://trends.google.com/trends/explore?q={keyword}"
    return f"Trend for {keyword}: [Check manually] - Trends site blocks scraping often."

def get_etsy_trends(keyword):
    return f"Etsy trend for {keyword}: Use their search bar autocomplete."

def get_reddit_keywords(subreddit):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        posts = r.json()["data"]["children"]
        titles = [post["data"]["title"] for post in posts]
        return titles[:5]
    return [f"Failed to pull from r/{subreddit}"]

def send_email(report):
    msg = MIMEText(report)
    msg["Subject"] = f"Weekly Trend Report – {datetime.date.today()}"
    msg["From"] = "yourbot@email.com"
    msg["To"] = "tripletttrends@gmail.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("yourbot@email.com", "your-app-password")
        server.send_message(msg)

if __name__ == "__main__":
    categories = ["apparel", "shirts", "hats", "clothing", "mugs", "tumblers", "cups"]
    reddit_subs = ["streetwear", "fashionreps", "mugs", "tumblers"]

    results = ["📈 Weekly Trend Report:
"]
    for cat in categories:
        results.append(f"\n🔍 {cat.title()}")
        results.append(get_google_trends(cat))
        results.append(get_etsy_trends(cat))

    for sub in reddit_subs:
        results.append(f"\n📡 Reddit /r/{sub}")
        results += get_reddit_keywords(sub)

    send_email("\n".join(results))
