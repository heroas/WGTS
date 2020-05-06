import kivy
kivy.require('1.10.0')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivymd.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
import Global
from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem
from kivymd.list import OneLineListItem, TwoLineListItem
from tinydb import TinyDB, Query
from NyaaPy import Nyaa
import home
import requests
import os
import sys
import subprocess
import shutil
from services import anilist_api
import functools
from kivymd.snackbar import Snackbar

from async_gui.engine import Task
from async_gui.toolkits.kivy import KivyEngine

engine = KivyEngine()

class Home(Screen):
    def navigate(self, route):
        if route is 'home':
            Global.HOME_CLASS.load_anime_list()
            self.ids.scr_mngr.transition.direction = 'left'
        else:
            self.ids.scr_mngr.transition.direction = 'right'

        self.ids.scr_mngr.current = route

    def download_image(self, url, anime_name):
        filename = "thumbnails/"+ anime_name + ".jpg"
        if os.path.isfile(filename):
            return

        print('starting dl')
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    @engine.async
    def open_episode_page_with_model(self, episode, anime, *_):
        print('aight lets go')
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = True
        Snackbar(
            text="Fetching torrents for: "+ anime["romaji_name"]+ " Ep " + str(episode), duration=2).show()
        filename = "thumbnails/"+ anime["romaji_name"] + ".jpg"
        print(filename + ' is the image')
        self.ids.home_spinner.active = True
        yield Task(functools.partial(Global.EPISODE_PAGE_CLASS.search_with_episode,anime,episode,filename))
        self.manager.transition.direction = 'left'
        self.manager.current = 'ep_page'
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = False

    @engine.async
    def open_episode_page_with_string(self, string, *_):
        print('aight lets go')
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = True
        Snackbar(
            text="Fetching torrents for: "+ string, duration=2).show()
        self.ids.home_spinner.active = True
        yield Task(functools.partial(Global.EPISODE_PAGE_CLASS.search,string))
        self.manager.transition.direction = 'left'
        self.manager.current = 'ep_page'
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = False

    @engine.async
    def load_anime_list(self, db_file, home_anime_list):

        db = TinyDB(db_file)
        anime_db = db.all()
        Anime = Query()

        print(home_anime_list)

        if len(anime_db) < 1 and len(home_anime_list.children) < 1:
            print('im here')
            get_started = MDAccordionItem()
            get_started.icon = 'help'
            get_started.title = "This is where you're watchlist will show."
            home_anime_list.add_widget(get_started)
            navigate_to_crit = MDAccordionSubItem(parent_item= get_started, text='Get started by going to the criterea selection screen!')
            # navigate_to_crit.on_release = functools.partial(self.navigate, 'criterea_selection')
            get_started.add_widget(navigate_to_crit)

        for anime in anime_db:
            print('processing ' + anime["romaji_name"])
            self.download_image(anime["image"], anime["romaji_name"])

            start_fetching_episodes_from =  0
            episodes_out = anime["episodes_out"]
            if(episodes_out is None):
                episodes_out = 0

            if anime["romaji_name"] not in Global.ANIME_LIST:
                print('Gonna start then')
                anime_item = MDAccordionItem()
                anime_item.icon = 'movie'
                anime_item.title = anime["romaji_name"]
                home_anime_list.add_widget(anime_item)
                #can skip if anime isnt airing (for future season expansions)

                if anime["airing"]:
                    current_episode = yield Task(functools.partial(anilist_api.get_next_airing_episode,anime["id"]))
                    print(current_episode)
                    if(current_episode is not None):
                        current_episode = current_episode - 1
                        print(anime["romaji_name"] + ' is on episode '+ str(current_episode) + ' | database shows '+ str(episodes_out))
                        if(current_episode != episodes_out):
                            print('changing db to match with eps')
                            db.update({'episodes_out': current_episode}, Anime.id == anime["id"])
                            episodes_out = current_episode

                if episodes_out > 50:
                    start_fetching_episodes_from = episodes_out - 50

                for episode in range(start_fetching_episodes_from, episodes_out):
                    anime_sub_item = MDAccordionSubItem(parent_item = anime_item, text = 'Episode ' + str(episode + 1))
                    anime_sub_item.on_release = functools.partial(self.open_episode_page_with_model, episode + 1, anime)
                    anime_item.add_widget(anime_sub_item)
                Global.ANIME_LIST.append(anime["romaji_name"])

        print(len(anime_db))


    def load_list(self):
        print("hello")
        self.manager.transition.direction = 'down'
        self.manager.current = 'file_chooser'

    def remove_accord_test(self):
        print(self.ids.accord_box.children)
        for child in self.ids.accord_box.children:
            print(child)
            self.ids.accord_box.remove_widget(child)


    def add_accord_test(self):
        accord = MDAccordion()
        accord.orientation = 'vertical'
        accord.id = 'ani_list'
        accord.md_bg_color = Global.SEASON_COLOR
        accord.specific_text_color = get_color_from_hex('#000000')

        self.ids.accord_box.add_widget(accord)

        home_anime_list = accord
        get_started = MDAccordionItem()
        get_started.icon = 'help'
        get_started.title = "This is where you're watchlist will show."
        home_anime_list.add_widget(get_started)
        navigate_to_crit = MDAccordionSubItem(parent_item= get_started, text='Get started by going to the criterea selection screen!')
        get_started.add_widget(navigate_to_crit)

    def add_item_accord_test(self):
        home_anime_list = Global.MAIN_WIDGET.ids.home.ids.home_anime_list
        print('im here')
        get_started = MDAccordionItem()
        get_started.icon = 'help'
        get_started.title = "This is where you're watchlist will show."
        home_anime_list.add_widget(get_started)
        navigate_to_crit = MDAccordionSubItem(parent_item= get_started, text='Get started by going to the criterea selection screen!')
        # navigate_to_crit.on_release = functools.partial(self.navigate, 'criterea_selection')
        get_started.add_widget(navigate_to_crit)


    def testin_nyaapy(self):
        animeList = Nyaa.search(keyword="Shoukoku no Altair", category=1, subcategory=2)
        Global.Test = animeList[0]["magnet"]

    pass
