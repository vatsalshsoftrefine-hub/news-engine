import requests
from bs4 import BeautifulSoup
from datetime import datetime
import uuid
from models.dynamodb import DynamoDBClient

db_client = DynamoDBClient()


def fetch_news_from_rss(url):
    """
    Fetch news articles from RSS feed
    """

    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, features="xml")

    items = soup.findAll("item")

    articles = []

    for item in items:
        article = {
            "id": str(uuid.uuid4()),
            "title": item.title.text if item.title else "",
            "description": item.description.text if item.description else "",
            "link": item.link.text if item.link else "",
            "published_at": item.pubDate.text if item.pubDate else "",
            "source": url,
            "created_at": datetime.utcnow().isoformat()
        }

        articles.append(article)

    return articles


def save_articles(articles):
    """
    Save only new articles (deduplicated)
    """

    table = db_client.get_table("news_items")

    saved_count = 0

    for article in articles:

        # Skip duplicates
        if article_exists(article["link"]):
            continue

        table.put_item(Item=article)
        saved_count += 1

    return saved_count

def article_exists(link):
    """
    Check if article already exists using link
    """

    table = db_client.get_table("news_items")

    response = table.scan()

    for item in response.get("Items", []):
        if item.get("link") == link:
            return True

    return False