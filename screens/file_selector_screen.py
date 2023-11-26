from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.toast import toast
from kivymd.app import MDApp


class FileSelectorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.bind(on_keyboard=self.events)
        
    def on_enter(self, *args):
        
        MDApp.get_running_app().root.get_screen("home").set_current_screen('file_select')
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.previous_screen = MDApp.get_running_app().root.get_screen("home").get_prev_screen()
        # self.prev_screen_name = super().get_screen_name()

        # Build the layout
        self.orientation = 'vertical'

        toolbar = MDTopAppBar(title="MDFileManager", elevation=10)
        
        layout = FloatLayout()

     
      
        self.add_widget(toolbar)
        self.add_widget(layout)
        
        self.file_manager_open()
                

    def file_manager_open(self, *args):
        self.file_manager.show('/Users\\ankit\\OneDrive\\Desktop')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        MDApp.get_running_app().root.get_screen(self.previous_screen).selected(value=path)
        self.exit_manager()
        

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        
        self.manager_open = False
        self.file_manager.close()
        
        next_screen = MDApp.get_running_app().root.get_screen("home").goto_prev_screen()
        
        MDApp.get_running_app().root.current=next_screen

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
