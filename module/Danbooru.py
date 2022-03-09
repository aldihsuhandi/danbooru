from controller import LinkController as lc
from module import Util
from module.Page import Page


def _scrap_page_number(link, filter):
    page = Page(link, filter)
    return page.scrap_page_number()


class Danbooru:
    def __init__(self, filter, tags):
        self._image_set = []
        self._filter = filter
        self._tags = Util.sanitize_tags(tags)
        self._link = lc.create_link(self._filter, self._tags)
        self._max_page = _scrap_page_number(self._link, self._filter)

    def get_tags(self):
        return self._tags

    def get_max_page(self):
        return self._max_page

    def set_image_set(self, image_set):
        self._image_set = image_set

    def get_page_link(self, page):
        s = "&page=%d" % page
        return self._link + s

    def get_filter(self):
        return self._filter
