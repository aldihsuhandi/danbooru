import urllib.parse

from module import Util
from module.Page import Page


def _create_link(filter, tags):
    s = "https://danbooru.donmai.us/posts?tags=%s" % tags
    if filter == "SFW Only":
        s = "https://safebooru.donmai.us/posts?tags=%s" % tags

    if filter == "NSFW Only":
        s = s + "+" + urllib.parse.quote("rating:explicit")

    return s


def _scrap_page_number(link):
    page = Page(link)
    return page.scrap_page_number()


class Danbooru:
    def __init__(self, filter, tags):
        self._pages = []
        self._filter = filter
        self._tags = Util.sanitize_tags(tags)
        self._link = _create_link(self._filter, self._tags)
        self._max_page = _scrap_page_number(self._link)

    def _scrap_page(self):
        pass

    def _generate_page(self, low, high):
        self._pages = []
        for i in range(low, high):
            pass

    def get_max_page(self):
        return self._max_page
