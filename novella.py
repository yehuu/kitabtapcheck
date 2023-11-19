import requests
from bs4 import BeautifulSoup

from general_functions import GeneralFunctions

gf = GeneralFunctions()

SEARCH_URL = "https://novella.az/?wc-ajax=aws_action"
MAX_SIMILARITY = 80

class Novella:
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
        all_books = self.parsed_html

        collect_books = []
        for single_book in all_books:
            book_name = BeautifulSoup(single_book['title'], 'html.parser').text
            book_url = single_book['link']
            book_picture = single_book['image']
            book_price = single_book['f_price']

            # check similarity...
            similarity = self.similarity(gf.filter_book_name(book_name), self.axtarilan_soz)
            if similarity > MAX_SIMILARITY:
                collect_books.append({'book': book_name, 'price': book_price, 'picture': book_picture, 'url': book_url})

        return collect_books


    def book_parsed(self):
        search_url = f"{SEARCH_URL}"
        data = {
            'keyword': self.axtarilan_soz,
            'aws_page': '2',
            'aws_tax': '',
            'lang':'',
            'page_url':'https://novella.az',
            'typedata':'json'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'referer': 'https://novella.az'
        }
        search_html = requests.post(search_url, data=data, headers=headers)
        search_html.encoding = 'utf-8'

        if search_html.ok:
            self.parsed_html = search_html.json()['products']
            return search_html.json()['products']
        return False




    def similarity(self, sentence1, sentence2):
        print(sentence1)
        print(sentence2)
        if sentence1:
            set_a = set(sentence1.lower())
            set_b = set(sentence2.lower())

            similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        else:
            similarity = 0
        return similarity
