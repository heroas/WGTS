import Global
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.snackbar import Snackbar
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivy.properties import ObjectProperty, StringProperty
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import OneLineListItem, TwoLineListItem, MDList, OneLineRightIconListItem
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from services import anilist_api
import requests
import main
import NyaaPy
from tinydb import TinyDB, Query
from async_gui.engine import Task, MultiProcessTask
from async_gui.toolkits.kivy import KivyEngine

engine = KivyEngine()

class MessageButton(IRightBodyTouch, MDIconButton):
    phone_number = StringProperty()

    def on_release(self):
        # sample code:
        print(phone_number)
        pass

class Criterea_Selection(Screen):
    genre_verbatim = 'Anything '
    first_switch_verbatim = 'as well as anything with a rating of '

    def add_genre(self, genre_type):
        Global.GENRES.append(genre_type)
        self.ids.genre_verbatim.text = ''
        for genre in Global.GENRES:
            self.ids.genre_verbatim.text += genre + '  '

    def remove_genre(self, genre_type):
        Global.GENRES.remove(genre_type)
        if len(Global.GENRES) == 0:
            self.ids.genre_verbatim.text = 'Anything '
        else:
            self.ids.genre_verbatim.text = ''
            for genre in Global.GENRES:
                self.ids.genre_verbatim.text += genre + '  '

    def add_malid(self, mal_id):
        title = anilist_api.get_anime_from_mal_id(mal_id)

        Global.ANIME_LIST.append(title)
        self.ids.rsLbl.text = title
        self.ids.ml.add_widget(TwoLineListItem(text=title, secondary_text='From M.A.L Id'))
        self.ids.mal_id.text = ""

    def set_quality(self, quality):
        Global.QUALITY = quality

    def parse_season(self, season):
        seasonArr = season.split('-')
        if(len(seasonArr) == 2 and seasonArr[1].isdigit() and seasonArr[0].upper() in Global.SEASON_LIST):
            Global.SEASON = seasonArr[0].upper()
            Global.SEASON_YEAR = seasonArr[1]
            return 0
        return 1

    def first_switch_toggle(self,switch):
        if switch == 'AND':
            self.ids.first_and.font_style = 'Display1'
            self.ids.first_and.text_color = Global.SEASON_COLOR_DARK
            self.ids.first_or.font_style = 'Body1'
            self.ids.first_or.text_color =[0, 0, 0, 1]
            self.ids.first_verbatim.text = 'as long as the rating is '
            Global.RATING_IN_GENRE = 1

        else:
            self.ids.first_or.font_style = 'Display1'
            self.ids.first_or.text_color = Global.SEASON_COLOR_DARK
            self.ids.first_and.font_style = 'Body1'
            self.ids.first_and.text_color =[0, 0, 0, 1]
            self.ids.first_verbatim.text  = 'as well as anything with a rating of '
            Global.RATING_IN_GENRE = 0

    def set_popularity(self, popularity):

        if popularity == 'Most':
            Global.POPULARITY = 1
            self.ids.pop_verbatim.text = 'also give me the most popular anime this season.'
        elif popularity == '3':
            Global.POPULARITY = 3
            self.ids.pop_verbatim.text = 'also give me the 3 most popular anime this season.'
        elif popularity == '5':
            Global.POPULARITY = 5
            self.ids.pop_verbatim.text = 'also give me the 5 most popular anime this season.'
        else:
            Global.POPULARITY = None
            self.ids.pop_verbatim.text = 'also I dont care about whats popular.'

    def anime_confirmation(self, anime_list):
        print('hello')
        ml = MDList()

        for anime in anime_list:
            print(anime)
            item = OneLineRightIconListItem(
                text = str(anime)
            )
            item.add_widget(MessageButton(phone_number='3334444'))
            ml.add_widget(item)

        self.dialog = MDDialog(title="This is a long test dialog",
                               content=ml,
                               size_hint=(.8, None),
                               height=dp(500),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    @engine.async
    def set_anime_from_criterea(self):
        self.ids.spinner.active = 'True'
        Global.RATING = int(round(self.ids.rating_slider.value))

        Global.ANIME_LIST = anilist_api.get_releasing_anime()

        self.ids.spinner.active = 'False'
        seasonYear = Global.SEASON_NAME + Global.SEASON_YEAR
        #self.anime_confirmation(Global.ANIME_LIST)
        #for anime in Global.ANIME_LIST:
            #db = TinyDB(Global.DB_FILE)
            #db.insert({'anime': str(anime), 'season': seasonYear, 'episodes_retrieved': 3, 'magnet_links': ['asdhjfasudtvhb','asdasfsdgfdbdf','ashdgvsuv'] })
