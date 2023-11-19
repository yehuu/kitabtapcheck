from urllib.parse import quote
import requests

SEARCH_URL = 'https://kitabtap.com/pages/kitab_axtar.php?app=1&q='

class SearchBook:
    def __init__(self):
        pass

    def search_book(self, axtarilan_soz):
        axtarilan_soz = self.prepare_axtarilan_soz(axtarilan_soz)
        search_url = f"{SEARCH_URL}{axtarilan_soz}"
        url_get_response = requests.get(search_url)

        if url_get_response.ok:
            json_data = url_get_response.json()  # Parse the JSON data
        return json_data

    def prepare_axtarilan_soz(self, axtarilan_soz):
        # ancaq parsed funksiyasinda istifade olunur..URL uchun hazirlayir
        return quote(axtarilan_soz.lower()).replace("i%CC%87", "i")