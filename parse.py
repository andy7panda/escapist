# -*- coding: utf-8 -*-

import urllib2
import re
import urllib
import os
import datetime
import simplejson
from bs4 import BeautifulSoup
from misc import transliterate, write_csv_headers, write_post_to_csv

from credentials import BLOGER_BY_URL, WORDPRESS_IMG_URL


def scrap_url_list(blogger_url, pages, reversed_order=False, url_list_filename='url_list.json'):
    """
    Extracts 'More…' URLs from the blog 'blogger_url' for 'pages' pages back, saves JSON into 'url_list_filename'
    """
    urls_to_posts = []
    print '[>>>] Extracting a list of {} first pages in blog with URL {}'.format(pages, blogger_url)

    for page_number in range(1, pages + 1):
        url_to_check = '{}/p{}/'.format(blogger_url, page_number)
        print ' [>>] Checking ', url_to_check, '…',
        page_with_urls = urllib2.urlopen(url_to_check)
        page_as_html = page_with_urls.read()
        page = BeautifulSoup(page_as_html)
        print '[ok]'

        page_urls = page.find_all('a', 'topic-more-a')
        print '  [>] Found {}'.format(page_urls)

        for url in page_urls:
            urls_to_posts.append(url.get('href'))

    # print urls_to_posts

    if reversed_order:
        urls_to_posts.reverse()

    url_list_file = open(url_list_filename, 'w+')
    simplejson.dump(urls_to_posts, url_list_file)
    url_list_file.close()
    print '[>>>] URL list saved to file {}'.format(url_list_filename)
    return url_list_file


def save_post_as_html(page_title, page_text, filename):
    """
    Saves header and text as HTML
    """
    file_full_name = '{}.html'.format(filename)
    print ' [>>] Saving {} …'.format(file_full_name),
    html_file = open(file_full_name, 'w')
    html_body = u'''<html>
    <head>
        <title>{0}</title>
        <link rel="stylesheet" type="text/css" href="custom.css" media="screen" />
    </head>
    <body>
        <h1>{0}</h1>
        <div class='article_text'>{1}</div>
    </body>
</html>'''.format(page_title, page_text)
    html_file.write(html_body.encode('utf8'))
    html_file.close()
    print '[Ok]'
    return html_file


def get_filename_from_url(image_url):
    """
    Extracts filename from image URL
    """
    image_filename = re.search('[\w]+\.jpg', image_url).group(0)
    return image_filename


def save_images(image_urls, image_path):
    """
    Saves images from 'image_urls' into 'image_path' folder and creates it if necessary
    """
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    for image_url in image_urls:
        image_filename = get_filename_from_url(image_url)
        image_full_path = image_path + '/' + image_filename
        print '  [>>] Downloading image {} в {} …'.format(image_url, image_path),
        urllib.urlretrieve(image_url, image_full_path)
        print '[Ok]'


def strip_div(html_string, prefix, suffix):
    """
    Cuts 'prefix' and 'suffix' from the sting
    """
    html_string = html_string[len(prefix):]
    html_string = html_string[:len(html_string) - len(suffix) + 1]
    return unicode(html_string)


def change_img_urls(page_text, old_url_regex, new_url):
    """
    Replaces old image URLs in 'page_text' post with new 'img_folder_name'
    """
    more_matches_left = True
    while more_matches_left:
        url_match = re.search(old_url_regex, page_text)
        if url_match:
            page_text = page_text[:url_match.start()] + new_url + '/' + page_text[url_match.end():]
        else:
            more_matches_left = False
    return page_text


def scrap_page(page_url, img_root_folder, img_root_url, post_id, publish_day):
    """
    Parses a page, replaces image URLs with 'img_root_url' and saves the images themselves into 'img_root_folder'
    """

    print '[>>>] {} Downloading page {} …'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), page_url),
    blog_page = urllib2.urlopen(page_url)
    page_as_html = blog_page.read()
    print '[Ok]'

    # parsing the page obtained
    page_as_soup_obj = BeautifulSoup(page_as_html)

    # extracting parts
    page_title = unicode(page_as_soup_obj.title.string)
    page_text = unicode(page_as_soup_obj.find('div', 'topic-txt clear'))
    page_text = strip_div(page_text, '<div class="topic-txt clear">', ' </div>')
    page_images = page_as_soup_obj.find_all('img')

    # getting image URL list as ['http://disney.com/img/little_maremaid.jpg', …]
    image_urls = []
    for image in page_images:
        image_src = image.get('src')
        re_match = re.search('http://media\.bloger\.by/source/photos/\d{4}/\d{2}/\d{2}/[\w]+\.jpg', image_src)
        if re_match:
            image_urls.append(image_src)

    # replacing article body URLs with local ones for HTML, saving HTML
    html_file_name = re.search('\d+', page_url).group(0)  # extracting post number from the URL as in '23452'
    page_text_for_html = change_img_urls(page_text, 'http://media\.bloger\.by/source/photos/\d{4}/\d{2}/\d{2}/.*?',
                                         '{}/{}'.format(img_root_folder, html_file_name))
    save_post_as_html(page_title, page_text_for_html, html_file_name)

    #  replacing article body URLs for CSV > Wordpress
    img_folder_name = '{}/{}'.format(img_root_folder, html_file_name)  # making path as in 'images/23452'
    page_text_for_csv = change_img_urls(page_text, 'http://media\.bloger\.by/source/photos/\d{4}/\d{2}/\d{2}/.*?',
                                        '{}/{}'.format(img_root_url, html_file_name))
    write_post_to_csv(page_title, page_text_for_csv, post_id, publish_day)

    #  downloading article pictures
    save_images(image_urls, img_folder_name)

    print '[>>>] Done'
    print ''


def scrap_articles():
    post_id = 2000
    publish_day = datetime.datetime.strptime('2014-02-02 08:00:00', '%Y-%m-%d %H:%M:%S')
    # setting current date-time and +2 hours shift for every blog post
    time_shift = datetime.timedelta(days=2)
    # root folder for HTML
    img_root_folder = 'images'
    # root folder for CSV
    img_root_url = WORDPRESS_IMG_URL
    # article URL list
    url_list_file_name = 'url_list.json'

    write_csv_headers()

    with open(url_list_file_name) as url_list_file:
        url_list = simplejson.load(url_list_file)
        for url in url_list:
            scrap_page(url, img_root_folder, img_root_url, post_id, publish_day)
            post_id += 1
            publish_day += time_shift


if __name__ == "__main__":
    # Uncomment to scrap URL list
    # scrap_url_list(BLOGGER_BY_URL, 17, reversed_order=True)

    # Uncomment to scrap pages according to URL list
    scrap_articles()
else:
    print 'scrap_url_list(blogger_url, pages, reversed_order=False, url_list_filename="url_list.json")'
    print 'scrap_articles()'
