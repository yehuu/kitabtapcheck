from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from search_book import SearchBook
from kivy.clock import Clock
from libraff import Libraff
from alinino import Alinino
from kitabal import Kitabal
from kitabevim import Kitabevim
from novella import Novella
from ovod import Ovod
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.label import MDLabel
import webbrowser

Builder.load_file("dizaynim.kv")

class Interface(MDBoxLayout):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.dropdown_menu = ''
        self.dialog = None

    def axtarilir_pop(self, call_func):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Axtarılır.."
            )
        self.dialog.open()
        if call_func == 'axtar589':
            Clock.schedule_once(lambda dt: self.axtar())
        else:
            Clock.schedule_once(lambda dt: self.search_bookshops(call_func))

    def update_dialog(self, book_count):
        self.dialog.dismiss()
        self.dialog = MDDialog(
            text=f"Axtarılır..({book_count})"
        )
        self.dialog.open()


    def axtar(self):
        self.dialog.dismiss()
        axtarilan_soz = self.ids.kitab_axtar.text
        dizaynim_ids = self.ids
        if len(axtarilan_soz) > 1:
            search_book = SearchBook()
            search_result = search_book.search_book(axtarilan_soz)
            print(search_result)
            if search_result:
                menu_items = [
                    {
                        "text": f"{single_data['text']}",
                        "on_release": lambda x=f"{single_data['text']}": self.menu_callback(x),
                        "viewclass": "OneLineListItem"
                    } for single_data in search_result
                ]
            else:
                menu_items = [{"text":"Tapılmadı", "viewclass":"OneLineListItem"}]

            Clock.schedule_once(lambda dt: self.menu(dizaynim_ids, menu_items))


    def menu_callback(self, text):
        self.close_menu()
        self.ids.cards.clear_widgets()
        Clock.schedule_once(lambda dt: self.axtarilir_pop(text))


    def search_bookshops(self, text):
        all_data = []

        # Libraff klasindan neticeni goturur..
        libraff = Libraff()
        libraff_result = libraff.axtar(text)
        if libraff_result:
            all_data+= libraff_result

        self.update_dialog(len(all_data))
        Clock.schedule_once(lambda dt: self.ali_nino(text, all_data))

    def ali_nino(self, text, all_data):
        # Alininodan neticeni goturur..
        alinino = Alinino()
        alinino_result = alinino.axtar(text)
        if alinino_result:
            all_data += alinino_result

        self.update_dialog(len(all_data))
        Clock.schedule_once(lambda dt: self.kitab_al(text, all_data))

    def kitab_al(self, text, all_data):
        # kitabaldan neticeni goturur..
        kitabal = Kitabal()
        kitabal_result = kitabal.axtar(text)
        if kitabal_result:
            all_data += kitabal_result

        self.update_dialog(len(all_data))
        Clock.schedule_once(lambda dt: self.kitab_evim(text, all_data))

    def kitab_evim(self, text, all_data):
        # kitabevimdən neticeni goturur..
        kitabevim = Kitabevim()
        kitabevim_result = kitabevim.axtar(text)
        if kitabevim_result:
            all_data += kitabevim_result

        self.update_dialog(len(all_data))
        Clock.schedule_once(lambda dt: self.novella(text, all_data))


    def novella(self, text, all_data):
        # novelladan neticeni goturur..
        novella = Novella()
        novella_result = novella.axtar(text)
        if novella_result:
            all_data += novella_result

        self.update_dialog(len(all_data))
        Clock.schedule_once(lambda dt: self.ovod(text, all_data))

    def ovod(self, text, all_data):
        # ovoddan neticeni goturur..
        ovod = Ovod()
        ovod_result = ovod.axtar(text)
        if ovod_result:
            all_data += ovod_result

        self.update_dialog(len(all_data))
        Clock.schedule_once(lambda dt: self.search_result(text, all_data))

    def search_result(self, text, all_data):
        # butun kitablari toplayir..
        if all_data:
            for single_data in all_data:
                all_layout = MDSmartTile(
                    source=f"{single_data['picture']}",
                    box_color=(0, 0, 0, 0.9)
                )
                all_layout.bind(on_release=lambda x, url=single_data['url']: self.open_url(url))
                price_layout = MDLabel(text=f"{single_data['price']} azn", color=(1,1,1,1))
                all_layout.add_widget(price_layout)
                self.ids.cards.add_widget(all_layout)
        Clock.schedule_once(lambda dt: self.dialog.dismiss())

    def open_url(self, url):
        webbrowser.open(url)

    def menu(self, dizaynim_ids, menu_items):
        if self.dropdown_menu:
            self.dropdown_menu.dismiss()

        self.dropdown_menu = MDDropdownMenu(
            caller=dizaynim_ids.kitab_axtar,
            items=menu_items,
            width_mult = 4
        )
        self.dropdown_menu.open()

    def close_menu(self):
        if self.dropdown_menu:
            Clock.schedule_once(lambda dt: self.dropdown_menu.dismiss())  # Schedule the menu method call in the main Kivy thread


class MenimYeniAppim(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Interface()

if __name__ == '__main__':
    MenimYeniAppim().run()
