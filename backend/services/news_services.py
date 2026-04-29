import requests
from bs4 import BeautifulSoup
from datetime import datetime
import uuid
from models.dynamodb import DynamoDBClient
from utils.cleaner import clean_html

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
           "description": clean_html(item.description.text if item.description else ""),
           "link": item.link.text if item.link else "",
           "published_at": item.pubDate.text if item.pubDate else "",
           "source": url,
           "category": categorize_article(               
               item.title.text if item.title else "",
               item.description.text if item.description else ""
               ),
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

def categorize_article(title, description):
    """
    Basic keyword-based categorization
    """

    text = f"{title} {description}".lower()

    if "ai" in text or "technology" in text or "software" in text:
        return "technology"

    elif "football" in text or "cricket" in text or "sports" in text:
        return "sports"

    elif "market" in text or "stock" in text or "business" in text:
        return "business"

    elif "election" in text or "government" in text or "politics" in text:
        return "politics"

    return "general"

def get_news(category=None, limit=10):
    """
    Fetch news from DB with optional category filter
    """

    table = db_client.get_table("news_items")

    response = table.scan()
    items = response.get("Items", [])

    # Filter by category if provided
    if category:
        items = [item for item in items if item.get("category") == category]

    # Sort by latest (optional improvement)
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return items[:limit]

def calculate_relevance(article, interests):
    """
    Improved relevance scoring using keyword mapping
    """

    text = f"{article.get('title', '')} {article.get('description', '')}".lower()

    score = 0

    keyword_map = {
        "ai": ["ai", "artificial intelligence", "machine learning"],
        "technology": ["technology", "tech", "software", "startup"],
        "cricket": ["cricket", "ipl"],
        "sports": ["sports", "football", "tennis"],
        "business": ["business", "market", "stock", "economy"]
    }

    for interest in interests:
        words = keyword_map.get(interest.lower(), [interest.lower()])

        for word in words:
            if word in text:
                score += 1
                break  # avoid double counting

    return score


def get_relevant_news_for_user(user_id, interests, limit=10):
    """
    Get news relevant to user interests
    """

    table = db_client.get_table("news_items")

    response = table.scan()
    items = response.get("Items", [])

    scored_articles = []

    for article in items:
        score = calculate_relevance(article, interests)

        if score > 0:
            article["relevance_score"] = score
            scored_articles.append(article)

    # Sort by highest relevance
    scored_articles.sort(key=lambda x: x["relevance_score"], reverse=True)

    return scored_articles[:limit]

def filter_triggered_news(articles, threshold=1):
    """
    Filter only high relevance articles
    """

    triggered = []

    for article in articles:
        if article.get("relevance_score", 0) >= threshold:
            article["triggered"] = True
            triggered.append(article)

    return triggered