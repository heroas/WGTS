import kivy
kivy.require('1.10.0')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
import Global
from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem
from tinydb import TinyDB, Query


class Home(Screen):
    def load_db(self):
        db = TinyDB(Global.DB_FILE)
        for anime in db:
            anime_item = MDAccordionItem();
            anime_item.icon = 'movie'
            anime_item.title = anime["anime"]
            self.ids.ani_list.add_widget(anime_item)
    pass
