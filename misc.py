# -*- coding: utf-8 -*-

import csv
import datetime

from credentials import WORDPRESS_ARTICLE_GUID


def transliterate(name):
    """
    Simple transliterator
    """
    dictionary = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                  'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                  'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                  'ю': 'u', 'я': 'ja', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'e',
                  'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'i', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
                  'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'Х', 'Х': 'h',
                  'Ц': 'c', 'Ч': 'cz', 'Ш': 'sh', 'Щ': 'scz', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e',
                  'Ю': 'u', 'Я': 'ja', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
                  '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
                  ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
                  '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
                  'Є': 'e'}

    # replacing all chars in a string following the cycle
    for key in dictionary:
        name = name.replace(key, dictionary[key])
    return name


def write_csv_headers():
    """
    Creates and saves a file for results, writes headers according to Wordpress specifications
    """
    with open('articles.csv', 'w') as csvfile:
        article_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        article_writer.writerow([
            "ID",  # 1
            "post_author",  # 2
            "post_date",  # 3
            "post_date_gmt",  # 4
            "post_content",  # 5
            "post_title",  # 6
            "post_excerpt",  # 7
            "post_status",  # 8
            "comment_status",  # 9
            "ping_status",  # 10
            "post_password",  # 11
            "post_name",  # 12
            "to_ping",  # 13
            "pinged",  # 14
            "post_modified",  # 15
            "post_modified_gmt",  # 16
            "post_content_filtered",  # 17
            "post_parent",  # 18
            "guid",  # 19
            "menu_order",  # 20
            "post_type",  # 21
            "post_mime_type",  # 22
            "comment_count"  # 23
        ])


def write_post_to_csv(page_title, page_text_for_csv, post_id, publish_day):
    """
    Saves result into CSV
    """

    print ' [>>] Writing CSV …',
    with open('articles.csv', 'a') as csvfile:
        # opening the file in altering mode
        article_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        article_writer.writerow([
            post_id,  # 1 counter
            "1",  # 2 author
            publish_day.strftime('%Y-%m-%d %H:%M:%S'),  # 3
            (publish_day + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),  # 4
            page_text_for_csv.encode('utf-8').strip(),  # 5
            page_title.encode('utf-8').strip(),  # 6
            "",  # 7
            "future",  # 8 future publication
            "open",  # 9
            "closed",  # 10
            "",  # 11
            transliterate(page_title.encode('utf-8').strip()),  # 12
            "",  # 13
            "",  # 14
            publish_day.strftime('%Y-%m-%d %H:%M:%S'),  # 15
            (publish_day + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),  # 16
            "",  # 17
            "0",  # 18
            WORDPRESS_ARTICLE_GUID + str(post_id),  # 19 article GUID, taken from id_counter
            "0",  # 20
            "post",  # 21
            "",  # 22
            "0",  # 23
        ])
        print '[Ok]'