import os
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.video import Video
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.toolbar import MDTopAppBar


class SelectVideoScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectVideoScreen, self).__init__(**kwargs)      
        self.selected_video = None

    def on_enter(self, *args):
        # Create the layout
        MDApp.get_running_app().root.get_screen("home").set_current_screen('select_video')
        self.layout = BoxLayout(orientation="vertical")

         # Create the "Select Image" button
        self.toolbar = MDTopAppBar(title="Select Video", elevation=10)
        self.toolbar.left_action_items = [['arrow-left', lambda x: setattr(MDApp.get_running_app().root,'current', MDApp.get_running_app().root.get_screen("home").goto_prev_screen())]]

        self.buttons_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=44)

        # Create the "Select Image" button
        self.select_video_button = Button(text="Select Video", on_press=self.open_file_selector)   
        self.detect_button = Button(text="Detect in Selected Video", on_press=self.detect_in_selected_image)

        # Add buttons to the buttons layout
        self.buttons_layout.add_widget(self.select_video_button)
        self.buttons_layout.add_widget(self.detect_button)     
        
        self.layout.add_widget(self.toolbar)
        
        self.video_widget = Video(pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.layout.add_widget(self.video_widget)
       
        self.layout.add_widget(self.buttons_layout)  
        # Add the layout to the screen
        self.add_widget(self.layout)

    def open_file_selector(self, *args):
        app = MDApp.get_running_app()
        app.root.current='file_select'
        
    def detect_in_selected_image(self, *args):
        # Get the selected file name
        selected_file = self.file_chooser.selection and self.file_chooser.selection[0]
        if selected_file:
            # Call the function to detect in the selected image and pass the file name
            app = MDApp.get_running_app()
            detect_image_screen = app.root.get_screen("detect_video")
            detect_image_screen.set_selected_file(selected_file)
            app.root.current = "detect_video"
    def selected(self,value, *args):
        # This method is called when a file is selected
        file_path = os.path.join(value)
        toast(f"Selected Video: {file_path}")
        self.show_selected_video(file_path)

    def show_selected_video(self, video_path):
        # Set the source of the Video widget to the selected video
        self.video_widget.source = video_path
        # Change the state of the Video widget to play
        self.video_widget.state = 'play'

   
   
   
   

