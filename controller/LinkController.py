import urllib.parse

from module.Url import Url


def check_link(link, tags):
    if "posts" not in link:
        return False
    if tags not in link:
        return False
    if "z" in link:
        return False
    if "deleted" in link:
        return False
    if "vote" in link:
        return False
    if "page" in link:
        return False
    if "search" in link:
        return False
    if "login" in link:
        return False
    if "tags" in link:
        return False
    return True


def _get_link(filter):
    s = "https://danbooru.donmai.us"
    if filter == "SFW Only":
        s = "https://safebooru.donmai.us"

    return s


def create_link(filter, tags):
    s = "https://danbooru.donmai.us/posts?tags=%s" % tags
    if filter == "SFW Only":
        s = "https://safebooru.donmai.us/posts?tags=%s" % tags

    if filter == "NSFW Only":
        s = s + "+" + urllib.parse.quote("rating:explicit")

    return s


def create_post_link(filter, image_id):
    return _get_link(filter) + image_id


def get_image(link):
    url = Url(link)
    image_link = url.find_class('a', 'image-view-original-link')
    if image_link and image_link[0].has_attr('href'):
        return image_link[0]['href']

    image_link = url.find('img')
    if image_link:
        return image_link['src']

    return ""
