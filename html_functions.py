import time

from bs4 import BeautifulSoup
from selenium import webdriver

from help_classes import QuantityOfComments


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
