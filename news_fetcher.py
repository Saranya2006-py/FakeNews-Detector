import feedparser

def get_trending_news():

    url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

    feed = feedparser.parse(url)

    headlines = []

    for entry in feed.entries[:10]:
        headlines.append({
            "title": entry.title,
            "link": entry.link
        })

    return headlines