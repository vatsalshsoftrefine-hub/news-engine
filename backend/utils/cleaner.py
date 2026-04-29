from bs4 import BeautifulSoup


def clean_html(text):
    """
    Remove HTML tags from text
    """

    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")

    return soup.get_text().strip()