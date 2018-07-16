import urllib.request as request
from bs4 import BeautifulSoup


def get_vid(search):
    query = request.quote(search)
    url = f'https://www.youtube.com/results?search_query={query}'
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    attributes = {'class': 'yt-uix-tile-link'}
    url = soup.findAll(attrs=attributes)[0]["href"]
    return f'https://www.youtube.com{url}'
