import bs4
import urllib.request


def num_there(s):
    return any(i.isdigit() for i in s)


def get_talents(name):
    talents = []
    soup = bs4.BeautifulSoup(urllib.request.urlopen
                             (f'https://www.hotslogs.com/Sitewide/HeroDetails?Hero={name}'), "html.parser")
    for i in soup.find_all('tr'):
        if i.get('id') == "ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__0":
            for j in i.find_all('td'):
                if j.string is not None and not num_there(j.string):
                    talents.append(j.string)

    return talents
