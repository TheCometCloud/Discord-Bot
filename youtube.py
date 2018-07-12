import urllib.request
from bs4 import BeautifulSoup


def get_vid(search):
    query = urllib.request.quote(search)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    soup.find()
    return "https://www.youtube.com" + soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]['href']
