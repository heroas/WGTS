import Global
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.snackbar import Snackbar
from kivymd.list import OneLineListItem, TwoLineListItem

class Criterea_Selection(Screen):

    def add_genre(self, genre_type):
        Snackbar(text='Added ' + genre_type).show()
        self.ids.ml.add_widget(TwoLineListItem(
            text=genre_type, secondary_text='Genre'))
        Global.GENRES.append(genre_type)

    def remove_genre(self, genre_type):
        Snackbar(text='Removed ' + genre_type).show()
        for c in self.ids.ml.children:
            if(c.text == genre_type):
                self.ids.ml.remove_widget(c)
        Global.GENRES.remove(genre_type)
