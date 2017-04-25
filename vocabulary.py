import random
import screenshot
import time


def get_words(count):
    with open('words_list.csv', 'r') as f:
        lines = f.readlines()
        total_lines = len(lines)
        for i in range(count):
            number = random.randint(10000, total_lines)
            word = lines[number].split()[0]
            try:
                url = 'https://en.oxforddictionaries.com/definition/{word}'.\
                    format(word=word)
                current_date = time.strftime("%d-%m-%Y")
                path = './words/{word}_{date}.png'.format(word=word,
                                                      date=current_date)
                screenshot.take_screenshot(url, path)
            except Exception as exception:
                print exception
                count += 1


if __name__ == '__main__':
    count = 10
    get_words(count)
