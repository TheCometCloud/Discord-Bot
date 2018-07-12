import urllib.request as request
from bs4 import BeautifulSoup


def get_vid(search):
    query = request.quote(search)
    url = f'https://www.youtube.com/results?search_query{query}'
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    soup.find()
    attributes = {'class': 'yt-uix-tile-link'}
    return f'https://www.youtube.com{soup.findAll(attributes)[0]["href"]}'
