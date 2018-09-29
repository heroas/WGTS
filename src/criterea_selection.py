from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import MDList, OneLineRightIconListItem
from kivymd.list import IRightBodyTouch
from kivy.metrics import dp
from kivy.uix.image import Image
from services import anilist_api

import functools
from tinydb import TinyDB, Query
from async_gui.engine import Task
from async_gui.toolkits.kivy import KivyEngine
from models.anime import Anime

import Global


engine = KivyEngine()

class RemoveButton(IRightBodyTouch, MDIconButton):
    name = StringProperty()

    def remove_anime_from_list(x, self, anime_to_remove):
        x.parent.parent.parent.remove_widget(x.parent.parent)
        if anime_to_remove in Global.ANIME_CONFIRM_LIST:
            Global.ANIME_CONFIRM_LIST.remove(anime_to_remove)

        self.dismiss()

    def on_release(self):
        anime_to_remove = self.parent.parent.text
        self.dialog3 = MDDialog(title='Are you sure you want to remove '+ anime_to_remove +' anime from your watchlist?',
                               size_hint=(.8, None),
                               height=dp(150),
                               auto_dismiss=False)

        self.dialog3.add_action_button("Actually....",
                                      action=lambda *x: self.dialog3.dismiss())
        self.dialog3.add_action_button("Im Sure!",
                                      action=lambda *x: self.remove_anime_from_list(self.dialog3, anime_to_remove))
        self.dialog3.open()

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
            Global.POPULARITY = 0
            self.ids.pop_verbatim.text = 'also I dont care about whats popular.'

    def add_anime_to_db(x, self, anime_list):
        db = TinyDB(Global.DB_FILE)

        Anime = Query()
        seasonYear = Global.SEASON_NAME + Global.SEASON_YEAR

        for anime in anime_list:
            if anime.name not in Global.ANIME_CONFIRM_LIST: continue
            db_anime = db.search(Anime.anime == anime.name)
            if(len(db_anime) == 0):
                print('adding ' + anime.name+ ' to database')
                db.insert({'anime_name': anime.name, 'season': seasonYear, 'episodes_out': anime.episodes_out })


        self.dismiss()

    def show_desc(self, anime_model):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=anime_model.description,
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog2 = MDDialog(title=anime_model.name,
                               content=content,
                               size_hint=(.8, None),
                               height=dp(400),
                               auto_dismiss=False)

        self.dialog2.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog2.dismiss())
        self.dialog2.open()

    def anime_confirmation(self, anime_list):
        for anime in anime_list:
            Global.ANIME_CONFIRM_LIST.append(anime.name)


        ml = MDList()

        for anime in anime_list:
            item = OneLineRightIconListItem(
                text = anime.name
            )
            item.on_release = functools.partial(self.show_desc, anime)
            remove_button = RemoveButton(name= anime.name, icon='server-remove')
            item.add_widget(remove_button)
            ml.add_widget(item)

        self.dialog = MDDialog(title="This is what we found for you.",
                               content=ml,
                               size_hint=(.8, None),
                               height=dp(650),
                               auto_dismiss=False)

        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())

        self.dialog.add_action_button("Confirm and + to watchlist",
                                      action=lambda *x : self.add_anime_to_db(self.dialog, anime_list))
        self.dialog.open()

    def filter_anime(self, anime_models):

        filtered_anime_models = []

        for amount in range(0, Global.POPULARITY):
            filtered_anime_models.append(anime_models[amount])

        del anime_models[:Global.POPULARITY]

        for anime in anime_models:
            intersect = list(set(Global.GENRES) & set(anime.genres))
            if len(intersect) > 0:
                if Global.RATING_IN_GENRE:
                    if anime.rating >= Global.RATING:
                        filtered_anime_models.append(anime)
                        print(anime.name)
                else:
                    filtered_anime_models.append(anime)
                    print(anime.name)

            if not Global.RATING_IN_GENRE and anime.rating >= Global.RATING:
                filtered_anime_models.append(anime)
                print(anime.name)

        return filtered_anime_models



    @engine.async
    def set_anime_from_criterea(self, *_):
        self.ids.spinner.active = True

        Global.RATING = int(round(self.ids.rating_slider.value))

        current_releasing_anime = yield Task(anilist_api.get_releasing_anime)
        anime_models = []
        for anime in current_releasing_anime:
            anime_m = Anime(anime)
            anime_models.append(anime_m)

        filtered_anime_models = self.filter_anime(anime_models)
        self.anime_confirmation(filtered_anime_models)

        self.ids.spinner.active = False
