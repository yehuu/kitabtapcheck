import requests
from bs4 import BeautifulSoup
from general_functions import GeneralFunctions

gf = GeneralFunctions()

LIBRAFF_URL = "https://www.libraff.az/?match=all&subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&dispatch=products.search&sl=az&q="
MAX_SIMILARITY = 80

class Libraff:
    def __init__(self):
        self.axtarilan_soz = ""
        self.parsed_html = ""
        self.price = ""

    def axtar(self, axtarilan_soz):
        self.axtarilan_soz = axtarilan_soz
        if self.libraff_parsed():
            result = self.book_exists()
            return result



    def book_exists(self):
        axtarishda = self.parsed_html.find('div', {'class': 'ty-no-items cm-pagination-container'})
        if axtarishda != None:
            return False
        stokda = self.parsed_html.find_all("div", {'class': 'ty-column4'})
        collect_books = []
        for element in stokda:
            stock_is_empty = element.find_all('span', {'class': 'ty-qty-out-of-stock ty-control-group__item'})
            if not stock_is_empty:
                print(f"kitab: {stock_is_empty}")
                find_book_name = element.find_all('a', {'class': 'product-title'})
                find_book_price = element.find_all('span', {'class': 'ty-price-num'})
                find_book_picture = element.find_all('img', {'class':'ty-pict cm-image'})
                find_book_url = element.find_all('a')
                # print(find_book_url[0].get('href'))
                if find_book_name:
                    book_name = find_book_name[0].text.lower()
                    if find_book_price:
                        book_price = find_book_price[0].text
                    if find_book_picture:
                        book_picture = find_book_picture[0].get('data-src')
                    book_url = find_book_url[0].get('href')
                    similarity = self.similarity(gf.filter_book_name(book_name), self.axtarilan_soz)
                    if similarity > MAX_SIMILARITY:
                        collect_books.append({'book':book_name, 'price': book_price, 'picture':book_picture, 'url': book_url})
        print(f"halbuki burda: {collect_books}")
        return collect_books


    def libraff_parsed(self):
        libraff_url = f"{LIBRAFF_URL}{self.axtarilan_soz}"
        libraff_html = requests.get(libraff_url)
        libraff_html.encoding = 'utf-8'
        if libraff_html.ok:
            soup = BeautifulSoup(libraff_html.text, 'html.parser')
            self.parsed_html = soup
            return True
        else:
            return False



    def similarity(self, sentence1, sentence2):
        set_a = set(sentence1.lower())
        set_b = set(sentence2.lower())

        similarity = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) * 100
        return similarity


# https://alinino.az/search.json?q=kimyag%C9%99r