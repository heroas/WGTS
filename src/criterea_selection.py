from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import MDList, OneLineRightIconListItem
from kivymd.list import IRightBodyTouch
from kivymd.snackbar import Snackbar
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

    def add_genre(self, genre_type):
        Global.GENRES.append(genre_type)

    def remove_genre(self, genre_type):
        Global.GENRES.remove(genre_type)

    def toggle_all_genres(self, state):
        for genre in self.ids.genre_grid.children:
            genre.children[0].active = state

    def toggle_rating(self, state):
        self.ids.rating_slider.disabled = not state
        if not state:
            self.ids.rating_slider_percentage.text = "Doesn't Matter"
            self.ids.rating_slider_percentage.font_style = "Headline"
        else:
            self.ids.rating_slider_percentage.text = str(int(round(self.ids.rating_slider.value))) + '%'
            self.ids.rating_slider_percentage.font_style = "Display4"

    def toggle_popularity(self, state):
        self.ids.pop_num.disabled = not state
        if not state:
            self.ids.pop_num.hint_text = "Don't care"
            self.ids.pop_num.text = ""
            self.ids.pop_num.error = False
        else:
            self.ids.pop_num.hint_text = "Enter Numeric"

    def add_misc(self, misc):
        print('Adding' + misc)
        Global.EXCLUSIONS.append(misc)

    def remove_misc(self, misc):
        print('remove' + misc)
        Global.EXCLUSIONS.remove(misc)

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

        #Getting amount of popular anime specified by critera
        for amount in range(0, Global.POPULARITY):
            filtered_anime_models.append(anime_models[amount])
        del anime_models[:Global.POPULARITY]


        for anime in anime_models:
            intersect = list(set(Global.GENRES) & set(anime.genres))
            if len(intersect) > 0:
                if anime.rating >= Global.RATING:
                    filtered_anime_models.append(anime)
                    print(anime.name)
            # if not Global.RATING_IN_GENRE and anime.rating >= Global.RATING:
            #     filtered_anime_models.append(anime)
            #     print(anime.name)

        return filtered_anime_models

    def number_validation_sanitation(self):
        popularity_value = self.ids.pop_num.text

        if popularity_value.isdigit():
            Global.POPULARITY = int(popularity_value)
        elif popularity_value is "":
            Global.POPULARITY = 0
        else:
            Snackbar(text="Popularity value must be numeric or disabled",duration=2).show()
            return False

        if self.ids.rating_slider.disabled:
            Global.RATING = 0
        else:
            Global.RATING = int(round(self.ids.rating_slider.value))

        if len(Global.GENRES) < 1:
            Snackbar(text="You must select at least one Genre",duration=2).show()
            return False


        return True


    @engine.async
    def set_anime_from_criterea(self, *_):
        if not self.number_validation_sanitation():
            return

        self.ids.spinner.active = True
        print(Global.RATING)
        current_releasing_anime = yield Task(anilist_api.get_releasing_anime)

        anime_models = []
        for anime in current_releasing_anime:
            anime_m = Anime(anime)
            anime_models.append(anime_m)

        filtered_anime_models = self.filter_anime(anime_models)
        self.anime_confirmation(filtered_anime_models)

        self.ids.spinner.active = False
