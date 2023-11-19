import urllib.parse
import requests
from bs4 import BeautifulSoup
import json
import re

from general_functions import GeneralFunctions

gf = GeneralFunctions()



SEARCH_URL = "https://kitabevim.az/wp-admin/admin-ajax.php"
MAX_SIMILARITY = 80

class Kitabevim:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def axtar(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.book_parsed():
            return self.book_exists()

    def book_exists(self):
        not_found = self.parsed_html.find('p')
        if not_found:
            if "tapılmadı" in not_found.text:
                print("Not found")
                return False
        all_books = self.parsed_html.find_all('li')
        collect_books = []
        for single_book in all_books:
            if single_book.find('span', {'class':'hightlight'}):
                book_picture = single_book.find_all('img')[0].get('src').encode('utf-8')
                book_picture = urllib.parse.quote(book_picture, safe=':/')
                book_url = single_book.find_all('a')[0].get('href')
                print(f"Huhu{book_picture}")
                book_name = single_book.find('span', {'class':'hightlight'}).text
                similarity = self.similarity(gf.filter_book_name(book_name), self.axtarilan_soz)
                if similarity > MAX_SIMILARITY:
                    all_prices = single_book.find_all('span', {'class':'woocommerce-Price-amount amount'})
                    cheap_price = ''
                    for single_price in all_prices:
                        single_price_pattern = f"\d+\.\d+"
                        filtered_price = re.findall(single_price_pattern, single_price.text)
                        if cheap_price:
                            if float(filtered_price[0]) < cheap_price:
                                book_price = filtered_price[0]
                            else:
                                book_price = cheap_price
                        else:
                            book_price = filtered_price[0]
                    collect_books.append({'book': book_name, 'price': book_price, 'picture': book_picture, 'url': book_url})

        return collect_books


    def book_parsed(self):
        search_url = f"{SEARCH_URL}"
        data = {'action': 'mymedi_ajax_search', 'category': '', 'search_string': f'{self.axtarilan_soz}'}
        search_html = requests.post(search_url, data=data)
        search_html.encoding = 'utf-8'
        if search_html.ok:
            json_data = json.loads(search_html.text)
            pretty_json = json.dumps(json_data, indent=4)
            soup = BeautifulSoup(json_data["html"], 'html.parser')
            self.parsed_html = soup
            return True
        else:
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


# kitabevim = Kitabevim()
# result = kitabevim.axtar('kimyagər')
#
# print(result)