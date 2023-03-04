import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()


async def text_diagnostic(
        session: aiohttp.ClientSession,
        text: str,
) -> dict:
    """
    Checks for anger and rudeness of the text

    :param session: session from aiohttp
    :param text: message or text what you want to check
    :return result: statistics of text
    """
    response = await session.post(
        f"https://api.sapling.ai/api/v1/tone",
        json={
            "key": os.getenv("SAPLING_KEY"),
            "text": text,
        },
    )

    result = await response.json()

    return result


async def comments_diagnostic(
        list_of_comments: list[str],
) -> list[int]:
    """
    Send a request for comment evaluation and return a new list diagnostics

    p.s: About sapling.ai:
    If you are using the trial version, then you will have restrictions!

    Something like that:
    Error: {'msg': 'Rate Limited. Visit https://sapling.ai/docs/api/api-access for details.'}

    :param list_of_comments: a list of comments
    :return diagnostic_list: a new list diagnostics
    """
    async with aiohttp.ClientSession() as session:
        diagnostics_list = []

        for index, comment in enumerate(list_of_comments, start=1):
            try:
                emotions = await text_diagnostic(session, comment)

                for emotion in emotions['overall']:
                    if emotion[1] == 'neutral':
                        # 0 - is neutral, 1 - angry
                        result = round(1 - emotion[0])
                        break
                else:
                    result = 0

                diagnostics_list.append(result)

                print(f"Diagnostic emotions №{index} completed!")
            except Exception as _ex:
                print(f"Exception №{index}! Error: {_ex}, {emotions}")

        return diagnostics_list
