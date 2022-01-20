import multiprocessing
import os
import urllib.parse
import urllib.request

from module.Url import Url

image_list = multiprocessing.Manager().list()
danbooru = ""


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


def get_list_image(url, tags):
    links = url.find_all('a')
    res = []
    for link in links:
        if check_link(link['href'], tags):
            res.append(link['href'])

    return res


def get_max_page(url):
    max_page = 0
    paginator = url.find_class('a', 'paginator-page')
    for p in paginator:
        max_page = max(int(p.get_text()), max_page)

    return max_page


def sanitize_tags(tags):
    tags = tags.lower()
    tags = tags.rstrip()
    tags = tags.replace(" ", "_")
    return urllib.parse.quote(tags)


def generate_link(tags):
    global danbooru
    return danbooru + "/posts?tags=" + tags


def generate_post_link(post_id):
    global danbooru
    return danbooru + post_id
    # return "https://danbooru.donmai.us" + post_id


def get_image(link):
    url = Url(link)
    image_link = url.find_class('a', 'image-view-original-link')
    if image_link and image_link[0].has_attr('href'):
        return image_link[0]['href']

    image_link = url.find('img')
    if image_link:
        return image_link['src']

    return ""


def scrap_image_link(post_link):
    global image_list

    image_link = get_image(post_link)
    if image_link == "" or "original" not in image_link:
        return
    image_list.append(image_link)


def get_image_from_page(tags, link, page):
    url = Url(link)
    url.add_attribute("page", page)
    link_images = get_list_image(url, tags)
    jobs = []
    for link in link_images:
        post_link = generate_post_link(link)
        t = multiprocessing.Process(target=scrap_image_link, args=(post_link,))
        jobs.append(t)
        t.start()

    cont = True
    while cont:
        cont = False
        for job in jobs:
            if job.is_alive():
                cont = True


def create_directory(tags):
    parent = os.getcwd()

    path = os.path.join(parent, "image")
    if not os.path.isdir(path):
        os.mkdir(path)

    path = os.path.join(path, tags)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def download_image(directory, image_name, link):
    path = os.path.join(directory, image_name)
    if os.path.isfile(path):
        os.remove(path)

    try:
        urllib.request.urlretrieve(link, path)
        print("Finish downloading %s" % image_name)
    except:
        print("error: %s - %s" % (image_name, link))


def generate_image_name(tags, indx, url):
    dump, extension = os.path.splitext(url)
    image_name = tags + " " + str(indx) + extension
    return image_name


def convert_list_to_set():
    global image_list
    image_set = set()
    for image in image_list:
        if image == "" or "original" not in image:
            continue
        image_set.add(image)

    return image_set


def main():
    global image_list
    global danbooru

    print("Input tags: ", end="")
    tags = input()
    print("Input page: ", end="")
    pages = int(input())
    print("Only download sfw[y/n]: ", end="")
    sfw = input()

    if sfw == "y":
        danbooru = "https://safebooru.donmai.us"
    else:
        danbooru = "https://danbooru.donmai.us"

    tags = sanitize_tags(tags)
    directory = create_directory(tags)
    link = generate_link(tags)
    url = Url(link)
    pages = min(pages, get_max_page(url))

    print("Searching for image link...")
    for page in range(1, pages + 1):
        load = "Scraping page %d of %d" % (page, pages)
        print(load)
        get_image_from_page(tags, link, page)

    image_sets = convert_list_to_set()

    print("Found total of %d image(s)" % len(image_list))
    print("Downloading image...")
    indx = 1
    jobs = []
    for link in image_sets:
        image_name = generate_image_name(tags, indx, link)
        indx += 1
        t = multiprocessing.Process(target=download_image, args=(directory, image_name, link))
        jobs.append(t)
        t.start()


if __name__ == "__main__":
    main()
