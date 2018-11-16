from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image, AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import MDList, OneLineRightIconListItem
from kivymd.list import IRightBodyTouch
from kivymd.snackbar import Snackbar
# from kivymd.grid import GridLayout, SmartTile
from services import anilist_api
from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem

from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
import functools
from tinydb import TinyDB, Query
from async_gui.engine import Task
from async_gui.toolkits.kivy import KivyEngine
from models.anime import Anime
import requests
import Global
import shutil
import webbrowser


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
        self.dialog3 = MDDialog(title='Are you sure you want to remove ' + anime_to_remove + ' anime from your watchlist?',
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

    # def download_image(self, url):
    #     r = requests.get('https://s3.anilist.co/media/anime/cover/small/nx101359-X6psMqBfatdw.jpg', stream=True)
    #     if r.status_code == 200:
    #         with open("img.png", 'wb') as f:
    #             r.raw.decode_content = True
    #             shutil.copyfileobj(r.raw, f)

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
            self.ids.rating_slider_percentage.text = str(
                int(round(self.ids.rating_slider.value))) + '%'
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
        name = 'anime_lists/' + x.ids.list_name.text + '_' +Global.DB_FILE
        db = TinyDB(name)

        Anime = Query()
        seasonYear = Global.SEASON_NAME + Global.SEASON_YEAR

        for anime in anime_list:
            if anime.name not in Global.ANIME_CONFIRM_LIST:
                continue
            db_anime = db.search(Anime.anime == anime.name)
            if(len(db_anime) == 0):
                print('adding ' + anime.name + ' to database')
                db.insert({'romaji_name': anime.name, 'eng_name': anime.english_name,'id': anime.id, 'airing': anime.airing, 'episodes_out': anime.episodes_out})


        self.dismiss()
        x.manager.transition.direction = 'left'
        x.manager.current = 'home'

        accord_box = Global.MAIN_WIDGET.ids.home.ids.accord_box
        for child in accord_box.children:
            accord_box.remove_widget(child)

        accord = MDAccordion()
        accord.orientation = 'vertical'
        accord.id = 'ani_list'
        accord.md_bg_color = Global.SEASON_COLOR
        accord.specific_text_color = get_color_from_hex('#000000')

        accord_box.add_widget(accord)

        Global.HOME_CLASS.load_anime_list(name,accord)


    def show_desc(self, anime_model):
        # content = GridLayout(cols= 2)
        webbrowser.open('https://anilist.co/anime/'+str(anime_model.id)+'/', new=2)
        # content2 = MDLabel(font_style='Body1',
        #                   theme_text_color='Secondary',
        #                   text=anime_model.description)
        #
        # content3 = MDLabel(font_style='Body1',
        #                   theme_text_color='Secondary',
        #                   text=anime_model.description)
        #
        # self.download_image('https://s3.anilist.co/media/anime/cover/small/nx101359-X6psMqBfatdw.jpg')
        #
        # image = Image(source='thumbnails/img.png')
        # content = BoxLayout()
        # content.orientation = 'vertical'
        #
        # content2.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        #
        #
        # content.add_widget(content2)
        # content.add_widget(image)
        # # content.add_widget(SmartTile(mapmap=True,source='https://s3.anilist.co/media/anime/cover/small/nx101359-X6psMqBfatdw.jpg'))
        # #content.bind(texture_size=content.setter('size'))
        # self.dialog2 = MDDialog(title=anime_model.name,
        #                         content=content,
        #                         size_hint=(.8, None),
        #                         height=dp(500),
        #                         auto_dismiss=False)
        #
        # self.dialog2.add_action_button("Dismiss",
        #                                action=lambda *x: self.dialog2.dismiss())
        # self.dialog2.open()

    def anime_confirmation(self, anime_list):
        for anime in anime_list:
            Global.ANIME_CONFIRM_LIST.append(anime.name)

        ml = MDList()

        for anime in anime_list:
            item = OneLineRightIconListItem(
                text=anime.name
            )
            item.on_release = functools.partial(self.show_desc, anime)
            remove_button = RemoveButton(name=anime.name, icon='server-remove')
            item.add_widget(remove_button)
            ml.add_widget(item)


        self.dialog = MDDialog(title=str(len(anime_list)) + " Results! This is what we found for you. Click to open browser for more info!",
                               content=ml,
                               size_hint=(.8, None),
                               height=dp(650),
                               auto_dismiss=False)

        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())

        self.dialog.add_action_button("Confirm and + to watchlist",
                                      action=lambda *x: self.add_anime_to_db(self.dialog, anime_list))
        self.dialog.open()

    def filter_anime(self, anime_models):

        filtered_anime_models = []

        # Getting amount of popular anime specified by critera
        for amount in range(0, Global.POPULARITY):
            filtered_anime_models.append(anime_models[amount])
        del anime_models[:Global.POPULARITY]

        # Get anime thata re selcted in genre and over the req rating value
        for anime in anime_models:
            intersect = list(set(Global.GENRES) & set(anime.genres))
            if len(intersect) > 0:
                if anime.rating >= Global.RATING:
                    filtered_anime_models.append(anime)

            #Go through exclusions list
            for exclusion in Global.EXCLUSIONS:
                if exclusion is "exclude_long":
                    print(str(anime.episodes_out) + " " + anime.name)
                    if anime.episodes_out is None:
                        if anime in filtered_anime_models:
                            filtered_anime_models.remove(anime)
                    elif anime.episodes_out > 100:
                        print("anime "+ anime.name + " is larger than 100 eps")
                        if anime in filtered_anime_models:
                            filtered_anime_models.remove(anime)
                if exclusion is "exclude_adapt":
                    if str(anime.source) != "ORIGINAL" and str(anime.source) != "None":
                        if anime in filtered_anime_models:
                            filtered_anime_models.remove(anime)

        return filtered_anime_models

    def number_validation_sanitation(self):
        popularity_value = self.ids.pop_num.text

        if popularity_value.isdigit():
            Global.POPULARITY = int(popularity_value)
        elif popularity_value is "":
            Global.POPULARITY = 0
        else:
            Snackbar(
                text="Popularity value must be numeric or disabled", duration=2).show()
            return False

        if self.ids.rating_slider.disabled:
            Global.RATING = 0
        else:
            Global.RATING = int(round(self.ids.rating_slider.value))

        if len(Global.GENRES) < 1:
            Snackbar(text="You must select at least one Genre",
                     duration=2).show()
            return False

        if not self.ids.list_name.text:
            Snackbar(text="You must name this search",
                     duration=2).show()
            return False


        return True

    @engine.async
    def set_anime_from_criterea(self, *_):
        if not self.number_validation_sanitation():
            return

        self.ids.spinner.active = True
        current_releasing_anime = yield Task(anilist_api.get_releasing_anime)

        anime_models = []
        for anime in current_releasing_anime:
            anime_m = Anime(anime)
            anime_models.append(anime_m)

        filtered_anime_models = self.filter_anime(anime_models)
        self.anime_confirmation(filtered_anime_models)

        self.ids.spinner.active = False
