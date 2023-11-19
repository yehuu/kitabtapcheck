from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from search_book import SearchBook
from kivy.clock import Clock
from libraff import Libraff

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDLabel:
        text: "Libraff imported"
        halign: 'center'
        theme_text_color: 'Secondary'
'''

class HelloWorldApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    HelloWorldApp().run()


# from kivymd.app import MDApp
# from kivy.lang import Builder
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.menu import MDDropdownMenu
# from search_book import SearchBook
# from kivy.clock import Clock

# from libraff import Libraff
# from alinino import Alinino
# from kitabal import Kitabal
# from kitabevim import Kitabevim
# from novella import Novella
# from ovod import Ovod
# from kivymd.uix.imagelist import MDSmartTile
# from kivymd.uix.label import MDLabel
# import webbrowser
#
# Builder.load_file("dizaynim.kv")
#
# class MenimDizaynim(MDScreen):
#     def __init__(self, **kwargs):
#         super(MenimDizaynim, self).__init__(**kwargs)
#         self.dropdown_menu = ''
#
#     def axtar(self):
#         axtarilan_soz = self.ids.kitab_axtar.text
#         dizaynim_ids = self.ids
#
#         if len(axtarilan_soz) > 1:
#             search_book = SearchBook()
#             search_result = search_book.search_book(axtarilan_soz)
#             print(search_result)
#             if search_result:
#                 menu_items = [
#                     {
#                         "text": f"{single_data['text']}",
#                         "on_release": lambda x=f"{single_data['text']}": self.menu_callback(x),
#                         "viewclass": "OneLineListItem"
#                     } for single_data in search_result
#                 ]
#             else:
#                 menu_items = [{"text":"Tapılmadı", "viewclass":"OneLineListItem"}]
#
#             Clock.schedule_once(lambda dt: self.menu(dizaynim_ids, menu_items))
#
#
#     def menu_callback(self, text):
#         self.close_menu()
#         self.ids.cards.clear_widgets()
#         all_data = []
#
#         # Libraff klasindan neticeni goturur..
#         libraff = Libraff()
#         libraff_result = libraff.axtar(text)
#         if libraff_result:
#             all_data+= libraff_result
#
#         # Alininodan neticeni goturur..
#         alinino = Alinino()
#         alinino_result = alinino.axtar(text)
#         if alinino_result:
#             all_data += alinino_result
#
#         # kitabaldan neticeni goturur..
#         kitabal = Kitabal()
#         kitabal_result = kitabal.axtar(text)
#         if kitabal_result:
#             all_data += kitabal_result
#
#         # kitabevimdən neticeni goturur..
#         kitabevim = Kitabevim()
#         kitabevim_result = kitabevim.axtar(text)
#         if kitabevim_result:
#             all_data += kitabevim_result
#
#         # novelladan neticeni goturur..
#         novella = Novella()
#         novella_result = novella.axtar(text)
#         if novella_result:
#             all_data += novella_result
#
#         # ovoddan neticeni goturur..
#         ovod = Ovod()
#         ovod_result = ovod.axtar(text)
#         if ovod_result:
#             all_data += ovod_result
#
#
#         # butun kitablari toplayir..
#         if all_data:
#             for single_data in all_data:
#                 all_layout = MDSmartTile(
#                     source=f"{single_data['picture']}",
#                     box_color=(0, 0, 0, 0.9),
#                     size=(200, 200),
#                     size_hint_y=None
#                 )
#                 all_layout.bind(on_release=lambda x, url=single_data['url']: self.open_url(url))
#                 price_layout = MDLabel(text=f"{single_data['price']} azn", color=(1,1,1,1))
#                 all_layout.add_widget(price_layout)
#                 self.ids.cards.add_widget(all_layout)
#
#     def open_url(self, url):
#         webbrowser.open(url)
#
#     def menu(self, dizaynim_ids, menu_items):
#         if self.dropdown_menu:
#             self.dropdown_menu.dismiss()
#
#         self.dropdown_menu = MDDropdownMenu(
#             caller=dizaynim_ids.kitab_axtar,
#             items=menu_items,
#             width_mult = 4
#         )
#         self.dropdown_menu.open()
#
#     def close_menu(self):
#         if self.dropdown_menu:
#             Clock.schedule_once(lambda dt: self.dropdown_menu.dismiss())  # Schedule the menu method call in the main Kivy thread
#
# class MenimYeniAppim(MDApp):
#     def build(self):
#         self.theme_cls.primary_palette = "Orange"
#         self.theme_cls.theme_style = "Dark"
#         return MenimDizaynim()
#
# if __name__ == '__main__':
#     MenimYeniAppim().run()
