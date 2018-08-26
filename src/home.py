import kivy
kivy.require('1.10.0')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
import Global



class Home(Screen):
    Global.SEASON_COLOR = get_color_from_hex(colors['Yellow']['200'])
    season_color = Global.SEASON_COLOR
