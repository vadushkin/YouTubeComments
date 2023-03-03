import datetime
import json


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
