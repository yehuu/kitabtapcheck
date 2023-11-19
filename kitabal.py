import requests
import re
from bs4 import BeautifulSoup
from general_functions import GeneralFunctions

gf = GeneralFunctions()

SEARCH_URL = "http://kitabal.az/search.php?search="
MAX_SIMILARITY = 80



class Kitabal:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def axtar(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.book_parsed():
            return self.book_exists()



    def book_exists(self):
        all_books = self.parsed_html.find_all('div', {'class': 'col-sm-4 col-md-3'})
        collect_books = []
        for single_book in all_books:
            # bura seklini goturmek uchundur..
            all_links = single_book.find_all('a')
            book_url = f"//kitabal.az/{all_links[0].get('href')}"
            book_picture = all_links[0].find_all('img')[0].get('src')

            # bura kitab adini goturmek uchundur..
            all_h6 = single_book.find_all('h6')
            book_name = all_h6[0].find_all('a')[0].get('title')

            # bura similarity yoxlamaq uchundur..
            if self.similarity(self.axtarilan_soz, gf.filter_book_name(book_name)) > MAX_SIMILARITY:
                all_span = single_book.find_all('span', {'class': 'amount text-primary'})
                # burda qiymeti goturmek uchun..
                if len(all_span) == 2:
                    book_price = all_span[1].text.split(' ')[2]
                else:
                    book_price = all_span[0].text.split(' ')[0]
                # kitablari toplamaq uchun..
                collect_books.append({'book': book_name, 'picture': book_picture, 'price': book_price, 'url': book_url})
        return collect_books


    def book_parsed(self):
        search_url = f"{SEARCH_URL}{self.axtarilan_soz}"
        search_html = requests.get(search_url)
        search_html.encoding = 'utf-8'
        if search_html.ok:
            # decoded_html = search_html.text.encode('utf-8').decode('utf-8')
            soup = BeautifulSoup(search_html.text, 'html.parser')
            self.parsed_html = soup
            return True
        else:
            return False


    def similarity(self, sentence1, sentence2):

        set_a = set(sentence1.lower())
        set_b = set(sentence2.lower())

        similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        return similarity