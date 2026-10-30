
import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


NEWS_SOURCE = "MIT Technology Review"
RSS_URL = "https://www.technologyreview.com/feed/"


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--window-size=1280,800")

    return webdriver.Chrome(options=options)


def search_article(keyword):
    driver = create_driver()

    try:
        driver.set_page_load_timeout(40)

        # Open MIT Technology Review RSS feed
        driver.get(RSS_URL)

        # Extract RSS XML displayed inside Chrome
        page_soup = BeautifulSoup(
            driver.page_source,
            "html.parser"
        )

        pre_tag = page_soup.find("pre")

        if pre_tag:
            feed_xml = html.unescape(pre_tag.get_text())
        else:
            feed_xml = driver.page_source

        # Parse RSS XML
        feed_soup = BeautifulSoup(feed_xml, "xml")
        articles = feed_soup.find_all("item")

        print("RSS articles found:", len(articles))

        # Search for the requested keyword
        for item in articles:
            title_tag = item.find("title")
            description_tag = item.find("description")
            link_tag = item.find("link")

            title = (
                title_tag.get_text(" ", strip=True)
                if title_tag else ""
            )

            description = (
                description_tag.get_text(" ", strip=True)
                if description_tag else ""
            )

            url = (
                link_tag.get_text(strip=True)
                if link_tag else ""
            )

            searchable_text = (
                title + " " + description
            ).lower()

            if (
                keyword.lower() in searchable_text
                and url.startswith("https://")
            ):

                # Open matching article
                driver.get(url)

                article_soup = BeautifulSoup(
                    driver.page_source,
                    "html.parser"
                )

                # Extract paragraphs from the main page
                paragraphs = article_soup.select("main p")

                paragraph_texts = [
                    p.get_text(" ", strip=True)
                    for p in paragraphs
                    if p.get_text(strip=True)
                ]

                # Find first paragraph containing keyword
                match_index = next(
                    (
                        i
                        for i, paragraph in enumerate(
                            paragraph_texts
                        )
                        if (
                           keyword.lower() in paragraph.lower()
                           and not paragraph.startswith(("-", "-"))
                        )
                    ),
                    None
                )

                if match_index is None:
                    raise Exception(
                        "Keyword was found in RSS but not "
                        "in the article body."
                    )

                # Select matching paragraph and next two
                selected_paragraphs = paragraph_texts[
                    match_index:match_index + 3
                ]

                # Remove newsletter and promotional text
                selected_paragraphs = [
                    p for p in selected_paragraphs
                    if not p.lower().startswith((
                        "read more",
                        "this is today's edition",
                        "this article is from",
                        "sign up"
                    ))
                ]

                article_text = " ".join(
                    selected_paragraphs
                )

                if len(article_text) < 100:
                    raise Exception(
                        "Not enough relevant article content extracted."
                    )

                return {
                    "title": title,
                    "url": url,
                    "content": article_text
                }

        raise Exception(
            f"No article found for keyword: {keyword}"
        )

    finally:
        driver.quit()

