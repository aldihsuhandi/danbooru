import requests
from bs4 import BeautifulSoup


class Url:
    def __init__(self, url):
        self._url = url
        print(self._url)
        response = requests.get(url)
        self._soup = BeautifulSoup(response.content, 'html.parser')

    def find_all(self, tags):
        return self._soup.findAll(tags)

    def find(self, tags):
        return self._soup.find(tags)

    def find_class(self, tags, identifier):
        res = self._soup.findAll(tags, {"class": identifier})
        return res

    def add_attribute(self, attribute, value):
        self._url = self._url + "&" + attribute + "=" + str(value)
        self._update_soup()

    def _update_soup(self):
        response = requests.get(self._url)
        self._soup = BeautifulSoup(response.content, 'html.parser')

    def get_url(self):
        return self._url
