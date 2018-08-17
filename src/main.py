# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.list import OneLineListItem, TwoLineListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
import requests
import os
import sys


class Criterea():
    Genres = []

critereas = Criterea()

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class WGTS(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "What's Good This Season?"

    def root():
        return self.root

    def build(self):
        kv_file = resource_path(os.path.join('templates', 'main.kv'))
        main_widget = Builder.load_file(kv_file)
        return main_widget

    def show_example_snackbar(self, snack_type):

        query = '''
             query ($season: MediaSeason, $seasonYear: Int, $page: Int, $perPage: Int, $genre: [String]) {
                Page (page: $page, perPage: $perPage){
                    pageInfo{
                        total
                        currentPage
                        lastPage
                        hasNextPage
                        perPage
                    }
                    media (season: $season, seasonYear: $seasonYear type: ANIME, genre_in: $genre) {
                        genres
                        title {
                            english
                        }
                    }
                }
             }
             '''
        variables = {
            'season': 'WINTER',
            'seasonYear': 2016,
            'page': 1,
            'perPage': 5,
            'genre': critereas.Genres
        }
        url = 'https://graphql.anilist.co'
        response = requests.post(
            url, json={'query': query, 'variables': variables})

        text = str(response.content)
        data = response.json()

        self.root.ids.rsLbl.text = text

        Snackbar(text=text).show()

    def add_genre(self, genre_type):
        Snackbar(text='Added ' + genre_type).show()
        self.root.ids.ml.add_widget(TwoLineListItem(
            text=genre_type, secondary_text='Genre'))
        critereas.Genres.append(genre_type)

    def remove_genre(self, genre_type):
        Snackbar(text='Removed ' + genre_type).show()
        for c in self.root.ids.ml.children:
            if(c.text == genre_type):
                self.root.ids.ml.remove_widget(c)
        critereas.Genres.remove(genre_type)


    def print_crit(self):
        self.root.ids.rsLbl.text = ''
        for x in critereas.Genres:
            self.root.ids.rsLbl.text += ' ' + x

if __name__ == '__main__':
    WGTS().run()
