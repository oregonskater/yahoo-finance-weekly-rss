import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

def fetch_latest_article():
    base_url = 'https://finance.yahoo.com/'
    page_url = 'https://finance.yahoo.com/news/'
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('a', {'class': 'Fw(b)'})
    for article in articles:
        title = article.text
        if "what to know this week" in title.lower():
            link = base_url + article['href']
            return title, link
    return None, None

def update_rss_feed():
    title, link = fetch_latest_article()
    if title and link:
        fg = FeedGenerator()
        fg.title('Yahoo Finance Weekly Article')
        fg.link(href=link)
        fg.description('RSS feed for Yahoo Finance weekly article.')

        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.description('Click to read the full article.')

        rss_feed = fg.rss_str(pretty=True)
        fg.rss_file('yahoo_finance_weekly_article.xml')

        print(f"RSS feed updated with article: {title}")
    else:
        print("No new article found.")
        open('yahoo_finance_weekly_article.xml', 'w').close()  # Create an empty file if no article found

if __name__ == "__main__":
    update_rss_feed()
