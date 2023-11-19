import re

import requests
from bs4 import BeautifulSoup

from general_functions import GeneralFunctions

gf = GeneralFunctions()



SEARCH_URL = "https://ovod.az/search/"
MAX_SIMILARITY = 80

class Ovod:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def axtar(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.book_parsed():
            return self.book_exists()
        return False

    def book_exists(self):
        if not self.parsed_html:
            return False
        html_data = BeautifulSoup(self.parsed_html, 'html.parser')

        all_books = html_data.find_all('div',{'class':'item-inner product-layout product-grid col-lg-15'})

        # print(all_books)

        collect_books = []
        for single_book in all_books:
            book_name = single_book.find_all('a')[0].get('title')
            book_url = single_book.find_all('a')[0].get('href')
            book_picture = f"https://ovod.az{single_book.find_all('a')[0].find('img').get('src')}"
            book_price = single_book.find_all('span')[-1].text
            price_pattern = f"\d+\.\d+"
            book_price = re.findall(price_pattern, book_price)[0]

            # check similarity...
            similarity = self.similarity(gf.filter_book_name(book_name), self.axtarilan_soz)
            if similarity > MAX_SIMILARITY:
                collect_books.append({'book': book_name, 'price': book_price, 'picture': book_picture, 'url': book_url})

        return collect_books


    def book_parsed(self):
        search_url = f"{SEARCH_URL}{self.axtarilan_soz}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'referer': 'https://ovod.az'
        }
        search_html = requests.get(search_url, headers=headers)
        search_html.encoding = 'utf-8'
        if search_html.ok:
            self.parsed_html = search_html.text
            return True
        return False




    def similarity(self, sentence1, sentence2):
        if sentence1:
            set_a = set(sentence1.lower())
            set_b = set(sentence2.lower())

            similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        else:
            similarity = 0
        return similarity
