import requests
from bs4 import BeautifulSoup

def fetch_reviews():

    url = "https://example.com"

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    r = requests.get(
        url,
        headers=headers
    )

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )

    reviews = []

    for review in soup.find_all("p")[:10]:

        reviews.append({

            "platform": "Reviews",

            "text": review.text
        })

    return reviews