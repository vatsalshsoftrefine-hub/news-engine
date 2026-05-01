from celery_worker import celery
from services.news_services import fetch_news_from_rss, process_and_store_articles


RSS_URL = "https://feeds.bbci.co.uk/news/rss.xml"


@celery.task
def run_news_ingestion():
    print("🔥 Celery: Running news ingestion...")

    articles = fetch_news_from_rss(RSS_URL)
    saved_count = process_and_store_articles(articles)

    print(f"✅ Celery ingestion complete. Saved: {saved_count}")