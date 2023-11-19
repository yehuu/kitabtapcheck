import requests

from general_functions import GeneralFunctions

gf = GeneralFunctions()

ALININO_URL = "https://alinino.az/search.json?q="

class Alinino:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def axtar(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        is_parsed = self.parse_alinino()
        if is_parsed:
            return self.book_exists()

    def book_exists(self):
        collect_books = []
        # print(self.parsed_html)
        for single_book in self.parsed_html:
            similarity = self.similarity(self.axtarilan_soz, gf.filter_book_name(single_book['title']))
            if similarity > 79:
                if single_book['variants'][0]['quantity']  >   0:
                    book_price  =   single_book['variants'][0]['price']
                    book_name = single_book['title']
                    book_url = f"//alinino.az{single_book['url']}"
                    book_picture = single_book['images'][0]['compact_url']

                    collect_books.append({'book': book_name, 'price': book_price, 'picture': book_picture, 'url':book_url})
        return collect_books

    def parse_alinino(self):
        alinino_url = f"{ALININO_URL}{self.axtarilan_soz}"
        alinino_response = requests.get(alinino_url)

        if alinino_response.ok:
            json_data = alinino_response.json()  # Parse the JSON data
            self.parsed_html = json_data  # Store the parsed JSON data
            return True
        return False


    def similarity(self, sentence1, sentence2):
        set_a = set(sentence1.lower())
        set_b = set(sentence2.lower())
        similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        return similarity

    # def similarity(self, sentence1, sentence2):
    #     similarity_ratio = SequenceMatcher(None, sentence1, sentence2).ratio() * 100
    #     return similarity_ratio


"""
from difflib import SequenceMatcher

def similarity(sentence1, sentence2):
    similarity_ratio = SequenceMatcher(None, sentence1, sentence2).ratio() * 100
    return similarity_ratio

sentence1 = "Janna Dark"
sentence2 = "Janna Dark"
similarity_score = similarity(sentence1, sentence2)
print(f"Similarity between '{sentence1}' and '{sentence2}': {similarity_score}%")

"""
