import requests
from bs4 import BeautifulSoup


def get_website_html(
    url: str,
    params = None,
):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15'}

    pageTree = requests.get(url, headers=headers, params=params)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    return pageSoup
