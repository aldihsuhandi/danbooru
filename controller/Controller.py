import time

from module.Page import Page


def scrap_validate(danbooru, mini, maxi):
    if danbooru is None:
        return False, "Input tags first!"
    elif mini is None or maxi is None:
        return False, "Min page and Max page must be filled"
    elif not mini.isnumeric() or not maxi.isnumeric():
        return False, "Min page and Max page must be a number"

    mini = int(mini)
    maxi = int(maxi)

    if mini > danbooru.get_max_page() or maxi > danbooru.get_max_page():
        return False, "Min / Max Page cannot exceed the maximum page found!"
    elif mini > maxi:
        return False, "Min Page cannot exceed Max Page"

    return True, "Success"


def insert_log(log_box, text, tag):
    if tag == 'warning':
        text = "Warning: " + text + '\n'
    else:
        text = "Info: " + text + '\n'
    log_box.config(state="normal")
    log_box.insert('end', text, tag)
    log_box.config(state="disabled")


def scrap_page(danbooru, min_page_field, max_page_field, log_box):
    mini = min_page_field.get()
    maxi = max_page_field.get()

    res = scrap_validate(danbooru, mini, maxi)

    if not res[0]:
        insert_log(log_box, res[1], 'warning')
        return

    mini = int(mini)
    maxi = int(maxi)

    generate_page(mini, maxi, danbooru, log_box)


def _remove_duplicate(image_list, danbooru):
    pass


def generate_page(low, high, danbooru, log_box):
    image_list = []
    for page in range(low, high + 1):
        load = "Scraping page %d" % page
        insert_log(log_box, load, 'normal')
        time.sleep(1)
        link = danbooru.get_page_link(page)
        p = Page(link, danbooru.get_filter())
        image_list.extend(p.scrap_page(danbooru.get_tags()))

    print(image_list)
