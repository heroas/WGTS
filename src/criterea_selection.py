import Global
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.snackbar import Snackbar
from kivymd.list import OneLineListItem, TwoLineListItem
from services import anilist_api
import requests
import main

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

    def add_malid(self, mal_id):
        title = anilist_api.get_anime_from_mal_id(mal_id)

        Global.ANIME_LIST.append(title)
        self.ids.rsLbl.text = title
        self.ids.ml.add_widget(TwoLineListItem(text=title, secondary_text='From M.A.L Id'))
        self.ids.mal_id.text = ""
        
    def print_crit(self):

        for anime in Global.ANIME_LIST:

            print('looking for ' + anime)
            url = "https://nyaa.pantsu.cat/api/search?c=3_5&sort=5&q=" + anime + "&page=" + str(1)
            response = requests.get(url)
            data = response.json()

            torrents = data["torrents"]

            for torrent in torrents:
                name = str(torrent["name"])
                if anime in name and Global.QUALITY in name and torrent["seeders"] > 0:
                    self.ids.rsLbl.text += name + ', '
                    main.open_magnet(torrent["magnet"])
                    break
            continue
