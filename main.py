from enum import Enum
import time

from bs4 import BeautifulSoup
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


def get_html_for_video(video_url: str) -> webdriver.Chrome.page_source:
    """Return a html page with comments

    :param video_url: video url
    :return html: html for url
    """

    if not video_url:
        raise TypeError("Your url is empty")

    browser = webdriver.Chrome()
    # get page
    browser.get(video_url)

    # time.sleep(50)

    # download new comments
    _scroll_to_bottom(browser, 0.6, QuantityOfComments.VERY_SMALL)

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


def get_list_of_comments_from_div(list_of_div_blocks: list[BeautifulSoup]) -> list[str]:
    """
    Return all comments from div after translating to string

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


def main():
    html = get_html_for_video("https://www.youtube.com/watch?v=tgwc1Mw6jto")

    div_block = get_div_of_all_comments_from_html(html)
    list_of_comments = get_list_of_comments_from_div(div_block)

    print(list_of_comments)


if __name__ == '__main__':
    main()
