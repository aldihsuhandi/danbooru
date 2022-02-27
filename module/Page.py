import urllib.parse

from module.Url import Url


def _sanitize_link(link):
    return urllib.parse.quote(link)


class Page:
    def __init__(self, link):
        self.url = Url(link)

    def scrap_page_number(self):
        page = 0
        paginator = self.url.find_class('a', 'paginator-page')
        for p in paginator:
            page = max(page, int(p.getText()))

        return page
