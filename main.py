import datetime
from enum import Enum
import json
import time
from urllib.error import URLError

from bs4 import BeautifulSoup
from mtranslate import translate
from selenium import webdriver


class QuantityOfComments(Enum):
    VERY_SMALL = 10
    SMALL = 30
    MEDIUM = 60
    LARGE = 120
    VERY_LARGE = 240


def _scroll_to_bottom(
        driver: webdriver.Chrome.page_source,
        page_loading_time: [float, int],
        quantity: QuantityOfComments,
) -> None:
    """
    Function to scroll down

    :param driver: instance of webdriver
    :param page_loading_time: how long do we have to wait to see new comments
    :param quantity: instance of QuantityOfComments, how 'many' comments do we need
    """

    # Get scroll height
    last_height = driver.execute_script(
        "return document.body.scrollHeight || document.documentElement.scrollHeight;"
    )

    if not isinstance(quantity, QuantityOfComments):
        raise TypeError("Quantity must be instance of QuantityOfComments' class")

    for _ in range(1, quantity.value):
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);"
        )
        # Wait to load page
        time.sleep(page_loading_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(
            "return document.body.scrollHeight || document.documentElement.scrollHeight;"
        )
        if new_height == last_height:
            break

        last_height = new_height


def get_html_for_video(
        video_url: str,
        page_loading_time: float,
        quantity: QuantityOfComments
) -> webdriver.Chrome.page_source:
    """Return a html page with comments

    :param video_url: video url
    :param page_loading_time: how long do we have to wait to see new comments
    :param quantity: instance of QuantityOfComments, how 'many' comments do we need
    :return html: html for url
    """

    if not video_url:
        raise TypeError("Your url is empty")

    browser = webdriver.Chrome()
    # get page
    browser.get(video_url)

    # time.sleep(50)

    # download new comments
    _scroll_to_bottom(browser, page_loading_time, quantity)

    # get html and exit
    html = browser.page_source
    browser.quit()

    return html


def get_div_of_all_comments_from_html(html: webdriver.Chrome.page_source) -> list[BeautifulSoup]:
    """
    Return raw list of comments

    :param html: html of page
    :return all_comments: raw list of comments
    """

    soup = BeautifulSoup(html, "lxml")

    box_of_comments = soup.find(
        "ytd-comments",
        id="comments",
    ).find(
        "ytd-item-section-renderer",
        id="sections",
    ).find(
        "div",
        id="contents",
    )
    all_comments = box_of_comments.find_all(
        "ytd-comment-thread-renderer",
        class_="style-scope ytd-item-section-renderer",
    )

    return all_comments


def get_list_of_comments_from_div_block(list_of_div_blocks: list[BeautifulSoup]) -> list[str]:
    """
    Return all comments from list of divs after translating to string

    :param list_of_div_blocks: list of divs
    :return comments: list of comments
    """
    if not list_of_div_blocks:
        raise TypeError("List of comments is empty")

    comments = []

    for div_block in list_of_div_blocks:
        comment = div_block.find("yt-formatted-string", id="content-text").text
        comments.append(comment)

    return comments


def get_dictionary_of_comments_from_div_block(list_of_div_blocks: list[BeautifulSoup]) -> dict:
    """
    Return dictionary of comments from div block

    :param list_of_div_blocks: a list of divs
    :return comments: a dictionary of comments
    """
    if not list_of_div_blocks:
        raise TypeError("List of comments is empty")

    comments = {}

    for div_block in list_of_div_blocks:
        comment = div_block.find("yt-formatted-string", id="content-text").text
        user = div_block.find("a", id="author-text").find("span").text

        user = user.strip()

        comments[user] = comment

    return comments


def create_json_file_of_comments_with_user(dictionary_of_comments: dict) -> None:
    """
    Create a json file of comments with users from list of divs

    :param dictionary_of_comments: list of divs
    """
    if not isinstance(dictionary_of_comments, dict):
        raise TypeError("dictionary_of_comments must be a dict")

    # Change date from "2077-07-07 22:22:22.22222" to "2077-07-07_22-22-22"
    date_now = str(datetime.datetime.now()).replace(":", "-").replace(" ", "_").split(".")[0]

    with open(f'comments_{date_now}.json', 'w', encoding='utf-8') as f:
        json.dump(dictionary_of_comments, f, ensure_ascii=False, indent=4)


def translate_dictionary(
        dictionary: dict,
        is_rename_names: bool = False,
        to_language: str = "auto",
        from_language: str = "auto",
) -> dict:
    """
    Translate a dictionary and return a new translated dictionary

    :param dictionary: dictionary of comments
    :param is_rename_names: we want to translate names?
    :param to_language: to what language we will translate a text
    :param from_language: from what language we will translate a text
    :return new_dictionary: new translated dictionary
    """
    new_dictionary = {}

    for index, (name, comment) in enumerate(dictionary.items(), start=1):
        try:
            new_name = translate(name, to_language, from_language) if is_rename_names else name
            new_comment = translate(comment, to_language, from_language)

            new_dictionary[new_name] = new_comment
            print(f"Comment №{index} translated!")
        except URLError:
            print(f"Wrong url №{index}")

    return new_dictionary


def translate_list(
        list_of_comments: list[str],
        to_language: str = "auto",
        from_language: str = "auto",
) -> list[str]:
    """
    Translate a list and return a new translated list

    :param list_of_comments: a list of comments
    :param to_language: to what language we will translate a text
    :param from_language: from what language we will translate a text
    :return translated_list: new translated list
    """
    translated_list = []

    for index, comment in enumerate(list_of_comments, start=1):
        try:
            new_comment = translate(comment, to_language, from_language)

            translated_list.append(new_comment)
            print(f"Comment №{index} translated!")
        except URLError:
            print(f"Wrong url №{index}")

    return translated_list


def main():
    # <3
    html = get_html_for_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", 0.6, QuantityOfComments.VERY_SMALL)

    div_block = get_div_of_all_comments_from_html(html)
    list_of_comments = get_list_of_comments_from_div_block(div_block)
    dictionary_of_comments = get_dictionary_of_comments_from_div_block(div_block)

    translated_dictionary = translate_dictionary(dictionary_of_comments, is_rename_names=True, to_language="en")
    translated_list = translate_list(list_of_comments, to_language="en")

    create_json_file_of_comments_with_user(dictionary_of_comments)
    time.sleep(1)
    create_json_file_of_comments_with_user(translated_dictionary)

    print("Non-translated list:\n", list_of_comments)
    print("Translated list:\n", translated_list)

    print()
    print("#" * 30)
    print()

    print("Non-translated dict:\n", dictionary_of_comments)
    print("Translated dict:\n", translated_dictionary)


if __name__ == '__main__':
    main()
