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
from services import anilist_api
import functools
from kivymd.snackbar import Snackbar

from async_gui.engine import Task
from async_gui.toolkits.kivy import KivyEngine

class File_Chooser(Screen):

    def root():
        return self.root

    def selected(self, filename):
        print (filename)

        self.manager.transition.direction = 'up'
        self.manager.current = 'home'

        #get fresh accordian list
        accord_box = Global.MAIN_WIDGET.ids.home.ids.accord_box
        for child in accord_box.children:
            accord_box.remove_widget(child)

        accord = MDAccordion()
        accord.orientation = 'vertical'
        accord.id = 'ani_list'
        accord.md_bg_color = Global.SEASON_COLOR
        accord.specific_text_color = get_color_from_hex('#000000')

        accord_box.add_widget(accord)

        Global.HOME_CLASS.load_anime_list(filename[0], accord)
