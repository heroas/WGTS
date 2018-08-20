# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
Config.set('graphics', 'width', '1080')
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
from kivymd.menu import MDDropdownMenu
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
import requests
import os
import sys
import NyaaPy

class Criterea():
    Genres = []
    Names = []
    Quality = '720'

critereas = Criterea()

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class Criterea_Selection(Screen):
    pass

class Home(Screen):
    pass

class WGTS(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "What's Good This Season?"
    quality_items = [{'viewclass': 'MDMenuItem','text': 'Example item'}]
    quality_dropDown = MDDropdownMenu(items=[{'viewclass': 'MDMenuItem','text': 'Example item'}], width_mult = 4)

    def on_touch(touch):
        Snackbar(text=str(touch.pos)).show()

    quality_dropDown.on_touch_down = on_touch

    def root():
        return self.root

    def build(self):
        kv_file = resource_path(os.path.join('templates', 'nav.kv'))
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

        self.root.idscrits.ids.rsLbl.text = text

        Snackbar(text=text).show()

    def add_genre(self, genre_type):
        Snackbar(text='Added ' + genre_type).show()
        self.root.ids.crits.ids.ml.add_widget(TwoLineListItem(
            text=genre_type, secondary_text='Genre'))
        critereas.Genres.append(genre_type)

    def remove_genre(self, genre_type):
        Snackbar(text='Removed ' + genre_type).show()
        for c in self.root.ids.crits.ids.ml.children:
            if(c.text == genre_type):
                self.root.ids.crits.ids.ml.remove_widget(c)
        critereas.Genres.remove(genre_type)

    def set_quality(self, quality):
        critereas.Quality = quality


    def print_crit(self):
        url = "https://nyaa.pantsu.cat/api/search/?samuraichamploo"
        response = requests.get(url)
        data = response.json()


        Snackbar(text=str(response.content)).show()
        self.root.ids.crits.ids.rsLbl.text = ''
        for x in critereas.Genres:
            self.root.ids.crits.ids.rsLbl.text += ', ' + x

        self.root.ids.crits.ids.rsLbl.text += ', ' + critereas.Quality

        for x in critereas.Names:
            self.root.ids.crits.ids.rsLbl.text += ', ' + x

        #self.root.ids.crits.ids.rsLbl.text = str(response.content)


    def add_malid(self, mal_id):
        if mal_id.isdigit():
            query = '''
                 query ($malId: Int) {
                        Media (idMal: $malId,type: ANIME) {
                            id
                            idMal
                            title {
                                english
                                romaji
                            }
                        }
                 }
                 '''
            variables = {
                'malId':mal_id
            }
            url = 'https://graphql.anilist.co'
            response = requests.post(
                url, json={'query': query, 'variables': variables})

            data = response.json()
            title_obj = data["data"]["Media"]["title"]
            english_title = str(title_obj["english"])
            romaji_title = str(title_obj["romaji"])

            if title_obj["english"] is None:
                title = romaji_title
            else:
                title = english_title

            self.root.ids.crits.ids.rsLbl.text = title
            critereas.Names.append(title);
            self.root.ids.crits.ids.ml.add_widget(TwoLineListItem(text=title, secondary_text='From M.A.L Id'))
            self.root.ids.crits.ids.mal_id.text = ""



if __name__ == '__main__':
    WGTS().run()
