
import cv2 as cv
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex

from screens.home_screen import HomeScreen



class App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
      
        
        # self.file_manager = MDFileManager(
        #     exit_manager=self.exit_manager, select_path=self.select_path
        # )
        self.screen_manager = ScreenManager()
        self.home_screen = HomeScreen(name="home")
        self.screen_manager.add_widget(self.home_screen)
       
        

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.screen_manager.background_color = get_color_from_hex("#FFFFFF")
        return self.screen_manager

   


if __name__ == "__main__":
    App().run()
