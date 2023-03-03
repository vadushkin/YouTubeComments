from enum import Enum
import time

from help_functions import create_json_file_of_comments_with_user
from html_functions import get_html_for_video, get_dictionary_of_comments_from_div_block, \
    get_list_of_comments_from_div_block, get_div_of_all_comments_from_html
from translate_functions import translate_list, translate_dictionary


class QuantityOfComments(Enum):
    VERY_SMALL = 10
    SMALL = 30
    MEDIUM = 60
    LARGE = 120
    VERY_LARGE = 240


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
