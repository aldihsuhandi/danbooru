import urllib.parse


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


def check_tags(tags):
    if tags == "" or len(tags) == 0:
        print("Tags Cannot Be Empty")

    return tags != ""


def sanitize_tags(tags):
    tags = tags.lower()
    tags = tags.rstrip()
    tags = tags.replace(" ", "_")
    return urllib.parse.quote(tags)
