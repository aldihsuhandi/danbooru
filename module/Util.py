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
