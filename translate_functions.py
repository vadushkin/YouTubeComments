import html
import re
from urllib.error import URLError

import aiohttp


async def translate(session, to_language, from_language, name):
    response = await session.get(
        f"https://translate.google.com/m?tl={to_language}&sl={from_language}&q={name}"
    )

    raw_data = await response.read()

    data = raw_data.decode("utf-8")
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)

    if len(re_result) == 0:
        result = ""
    else:
        result = html.unescape(re_result[0])

    return result


async def translate_dictionary(
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
    async with aiohttp.ClientSession() as session:
        new_dictionary = {}

        for index, (name, comment) in enumerate(dictionary.items(), start=1):
            try:
                new_name = await translate(session, to_language, from_language, name) if is_rename_names else name
                new_comment = await translate(session, to_language, from_language, name)

                new_dictionary[new_name] = new_comment

                print(f"Comment №{index} translated!")
            except URLError:
                print(f"Wrong url №{index}")

        return new_dictionary


async def translate_list(
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
    async with aiohttp.ClientSession() as session:
        translated_list = []

        for index, comment in enumerate(list_of_comments, start=1):
            try:
                new_comment = await translate(session, comment, to_language, from_language)

                translated_list.append(new_comment)

                print(f"Comment №{index} translated!")
            except URLError:
                print(f"Wrong url №{index}")

        return translated_list
