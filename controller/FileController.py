import os


def _mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def remove(path):
    if os.path.isfile(path):
        os.remove(path)


def create_directory(danbooru):
    parent = os.getcwd()
    path = os.path.join(parent, "image")
    _mkdir(path)

    tags = danbooru.get_tags()
    path = os.path.join(path, tags)
    _mkdir(path)

    return path
