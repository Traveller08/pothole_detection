from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

class DetectImageScreen(Screen):
    def __init__(self, **kwargs):
        super(DetectImageScreen, self).__init__(**kwargs)
        self.selected_file_label = None

    def on_enter(self, *args):
        # Create the layout for the Detect Image screen
        layout = BoxLayout(orientation="vertical")

        # Create the "Back to Select Image" button
        back_button = Button(text="Back to Select Image", on_press=self.switch_to_select_image)

        # Create a label to display the selected file name
        self.selected_file_label = Button(text="", size_hint_y=None, height=44)

        # Create the result image widget (replace this with your logic)
        result_image = Image(pos_hint={"center_x": 0.5, "center_y": 0.5})

        # Add widgets to the layout
        layout.add_widget(back_button)
        layout.add_widget(self.selected_file_label)
        layout.add_widget(result_image)

        # Add the layout to the screen
        self.add_widget(layout)

    def switch_to_select_image(self, *args):
        # Switch back to the Select Image screen
        self.manager.current = "select_image"

    def set_selected_file(self, selected_file):
        # Set the selected file name in the label
        self.selected_file_label = selected_file