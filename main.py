import sys
import time

from help_classes import QuantityOfComments
from help_functions import create_json_file_of_comments_with_user
from html_functions import get_html_for_video, get_dictionary_of_comments_from_div_block, \
    get_list_of_comments_from_div_block, get_div_of_all_comments_from_html
from translate_functions import translate_list, translate_dictionary


def main():
    if sys.argv[1:]:
        url = sys.argv[1]
    else:
        # <3
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    html = get_html_for_video(url, 0.6, QuantityOfComments.VERY_SMALL)

    div_block = get_div_of_all_comments_from_html(html)

    print(f"--- Measurement start time ---")
    start_time = time.time()

    list_of_comments = get_list_of_comments_from_div_block(div_block)
    dictionary_of_comments = get_dictionary_of_comments_from_div_block(div_block)

    translated_list = translate_list(list_of_comments, to_language="en")
    translated_dictionary = translate_dictionary(dictionary_of_comments, is_rename_names=True, to_language="en")

    print(f"--- For {time.time() - start_time} seconds comments was translated ---")

    create_json_file_of_comments_with_user(dictionary_of_comments)
    time.sleep(1)
    create_json_file_of_comments_with_user(translated_dictionary)

    # print("Non-translated list:\n", list_of_comments)
    # print("Translated list:\n", translated_list)
    #
    # print()
    # print("#" * 30)
    # print()
    #
    # print("Non-translated dict:\n", dictionary_of_comments)
    # print("Translated dict:\n", translated_dictionary)


if __name__ == '__main__':
    main()
