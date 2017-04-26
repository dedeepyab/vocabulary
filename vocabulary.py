import os
import random
import sys
import time
from PIL import Image
from selenium import webdriver


def get_words(count):
    with open('words_list.csv', 'r') as f:
        lines = f.readlines()
        while count:
            count -= 1
            number = random.randint(10000, 50000)
            word = lines[number].split()[0]
            try:
                url = 'https://en.oxforddictionaries.com/definition/{word}'.\
                    format(word=word)
                current_date = time.strftime("%d-%m-%Y")
                path = './words/{word}_{date}.png'.format(word=word,
                                                          date=current_date)
                save_image(url, path, word)
            except Exception as exception:
                print exception
                count += 1


def save_image(url, path, word):
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
    im1.save(path)

    os.remove('temp.png')


if __name__ == '__main__':
    count = int(sys.argv[1])
    get_words(count)
