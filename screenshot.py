from selenium import webdriver
from PIL import Image


def take_screenshot(url, path):
    """Take screenshot"""
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true',
                                               '--ssl-protocol=any'])
    driver.get(url)

    element = driver.find_elements_by_class_name('entryWrapper')[0]
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
