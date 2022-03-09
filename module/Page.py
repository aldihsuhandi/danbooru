import multiprocessing
import urllib.parse

from controller import LinkController as lc
from module.Url import Url


def _sanitize_link(link):
    return urllib.parse.quote(link)


class Page:
    def __init__(self, link, filter):
        self.url = Url(link)
        self.filter = filter
        self.image_list = None

    def scrap_page_number(self):
        page = 0
        paginator = self.url.find_class('a', 'paginator-page')
        for p in paginator:
            page = max(page, int(p.getText()))

        return page

    def _get_list_image(self, tags):
        links = self.url.find_all('a')
        res = []
        for link in links:
            if lc.check_link(link['href'], tags):
                res.append(link['href'])

        return res

    def _scrap_image_link(self, image_link):
        image_link = lc.get_image(image_link)
        if image_link == "" or "original" not in image_link:
            return

        self.image_list.append(image_link)

    def scrap_page(self, tags):
        self.image_list = multiprocessing.Manager().list()
        images = self._get_list_image(tags)
        jobs = []
        for image in images:
            post_link = lc.create_post_link(self.filter, image)
            t = multiprocessing.Process(target=self._scrap_image_link, args=(post_link,))
            jobs.append(t)
            t.start()

        cont = True
        while cont:
            cont = False
            for job in jobs:
                if job.is_alive():
                    cont = True

        return self.image_list
