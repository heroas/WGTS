import Global
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.snackbar import Snackbar
from kivymd.list import OneLineListItem, TwoLineListItem
from services import anilist_api
import requests
import main
import NyaaPy

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

    def get_animes_from_genres(self):

        self.ids.season.text = 'summer-2018'
        if self.parse_season(self.ids.season.text):
            Snackbar(text="Please insert a season!").show()
            return

        for genre in Global.GENRES:
            anilist_api.get_anime_from_genre(genre)

        print(Global.ANIME_LIST)


    def testin_nyaapy(self):
        print (Nyaa.search(keyword="Shoukoku no Altair", category=1, subcategory=2))

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



    def testin_verbatim(self):
        Global.RATING = int(round(self.ids.rating_slider.value))

        print(Global.GENRES)
        print (Global.POPULARITY)
        print (Global.RATING)
        print (Global.RATING_IN_GENRE)
        print (Global.QUALITY)

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
