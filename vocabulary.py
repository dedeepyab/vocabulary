# Author: Dedeepya Bonthu <dedeepya.bonthu@gmail.com>
# Date:  2017-04-27

"""
Shows the definition of a word from Oxford dictionary.
If no word is specified, it picks random words from the corpus and saves their
definitions

Requires:
Word: The word for which definition needs to be shown
Count: # word definitions to be saved
"""

import argparse
import os
import random
import time
from PIL import Image
from selenium import webdriver


def get_words(count):
    with open('words_list.csv', 'r') as f:
        lines = f.readlines()
        while count:
            count -= 1
            number = random.randint(1, len(lines))
            word = lines[number].split()[0]
            try:
                get_word(word, True)
            except Exception as exception:
                print exception
                count += 1


def get_word(word, save=False):
    url = 'https://en.oxforddictionaries.com/definition/{word}'.format(
        word=word)
    current_date = time.strftime("%d-%m-%Y")
    path = './words/{word}_{date}.png'.format(word=word, date=current_date)
    get_image(url, path, word, save)


def get_image(url, path, word, save):
    """Take screenshot"""
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true',
                                               '--ssl-protocol=any'])
    driver.get(url)

    no_matches = driver.find_elements_by_class_name('no-exact-matches')
    if len(no_matches):
        raise Exception('No matches found')

    derivatives = driver.find_elements_by_class_name('derivative_of')
    if derivatives:
        derivative = derivatives[0]
        root_word = derivative.find_elements_by_tag_name('a')[0].text
        url = url.replace(word, root_word)
        path = path.replace(word, root_word)
        driver.get(url)

    elements = driver.find_elements_by_class_name('entryWrapper')
    if not elements:
        raise Exception('No definition found')

    element = elements[0]
    location = element.location
    size = element.size
    driver.save_screenshot('temp.png')
    driver.quit()

    im = Image.open('temp.png')

    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x'] + size['width'])
    bottom = int(location['y'] + size['height'])

    im1 = im.crop((left, top, right, bottom))
    if save:
        im1.save(path)
    else:
        im1.show()

    os.remove('temp.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool to get the definition \
of words', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    default_count = 10
    parser.add_argument('--count', action='store', dest='count',
                        default=default_count)
    parser.add_argument('--word', action='store', dest='word', default=None)

    arguments = parser.parse_args()
    count = arguments.count
    word = arguments.word

    if word:
        get_word(word)
    else:
        get_words(count)
