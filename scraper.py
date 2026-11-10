import requests
from bs4 import BeautifulSoup

def extract_article(url):

    try:

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        article = " ".join([p.text for p in paragraphs])

        return article

    except:
        return ""