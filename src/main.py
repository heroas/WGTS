# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '700')
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.list import OneLineListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
import requests


class WGTS(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "What's Good This Season?"

    def root():
        return self.root

    def build(self):
        main_widget = Builder.load_file('./main.kv')
        return main_widget

    def show_example_snackbar(self, snack_type):


         query = '''
             query ($id: Int) { # Define which variables will be used in the query (id)
             Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
                 id
                 title {
                 romaji
                 english
                 native
                 }
                 }
             }
             '''
         variables = {
             'id': 15125
         }
         url = 'https://graphql.anilist.co'
         response = requests.post(url, json={'query': query, 'variables': variables})

         text = str(response.content)
         data = response.json()

         self.root.ids.rsLbl.text = str(data["data"]["Media"]["title"]["english"])

         Snackbar(text=text).show()

    def add_genre(self, genre_type):
        Snackbar(text='Added '+ genre_type).show()
        self.root.ids.ml.add_widget(OneLineListItem(text=genre_type))

if __name__ == '__main__':
    WGTS().run()
