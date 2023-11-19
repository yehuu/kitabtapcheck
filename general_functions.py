

class GeneralFunctions:

    def filter_book_name(self, book_name):
        filtered_book_name = book_name.split('(')[0]
        return filtered_book_name

    def prepare_axtarilan_soz(self):
        # ancaq parsed funksiyasinda istifade olunur..URL uchun hazirlayir
        return quote(self.axtarilan_soz.lower()).replace("i%CC%87", "i")

"""
call_class = GeneralFunctions()

result = call_class.filter_book_name('Lorep ipsum (dolor sitamet)')

print(result)
"""