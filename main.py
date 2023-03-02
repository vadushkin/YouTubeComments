from enum import Enum
import time

from selenium import webdriver


class QuantityOfComments(Enum):
    SMALL = 30
    MEDIUM = 60
    LARGE = 120


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
    """Return a html page with comments"""

    browser = webdriver.Chrome()
    # get page
    browser.get(video_url)

    # download new comments
    _scroll_to_bottom(browser, 0.6, QuantityOfComments.SMALL)

    # get html and exit
    html = browser.page_source
    browser.quit()

    return html


def main():
    print(get_html_for_video("https://www.youtube.com/watch?v=tgwc1Mw6jto"))


if __name__ == '__main__':
    main()
