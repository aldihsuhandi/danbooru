import os
import urllib.request

from controller import FileController as fc


class Image:
    def __init__(self, name, link):
        self._link = link
        self._name = name

    def get_link(self):
        return self._link

    def get_name(self):
        return self._name

    def download(self, directory):
        path = os.path.join(directory, self._name)
        fc.remove(path)

        res = True, "Success"

        try:
            urllib.request.urlretrieve(self._link, path)
            print("Finish download %s" % self._name)
        except:
            res = False, "Error download %s" % self._name

        return res
