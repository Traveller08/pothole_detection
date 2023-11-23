# # # # from kivy.lang import Builder
# # # # import os

# # # # from kivy.core.window import Window
# # # # from kivy.lang import Builder

# # # # from kivymd.app import MDApp
# # # # from kivymd.uix.filemanager import MDFileManager
# # # # from kivymd.toast import toast


# # # # KV = '''
# # # # MDBoxLayout:
# # # #     orientation: "vertical"

# # # #     MDTopAppBar:
# # # #         title: "MDTopAppBar"
# # # #         left_action_items: [["menu", lambda x: app.callback()]]
# # # #         right_action_items: [["dots-vertical", lambda x: app.callback_1()]]

# # # #     MDLabel:
# # # #         text: "Content"
# # # #         halign: "center"
# # # # '''

# # # # homescreen = '''
# # # # MDBoxLayout:
# # # #     adaptive_height: True
# # # #     adaptive_width: True
# # # #     adaptive_size: True
# # # #     md_bg_color: app.theme_cls.primary_color
# # # #     orientation: "vertical"
    
# # # #     MDRaisedButton:
# # # #         text: "Select Image"
# # # #         md_bg_color: "red"
        
# # # #     MDRaisedButton:
# # # #         text: "Select Video"
# # # #         md_bg_color: "red"
        
# # # #     MDRaisedButton:
# # # #         text: "Detect Live"
# # # #         md_bg_color: "red"
    
# # # # '''

# # # # select_image_screen='''
# # # # MDBoxLayout:
# # # #     orientation: "vertical"

# # # #     MDTopAppBar:
# # # #         title: "MDFileManager"
# # # #         left_action_items: [["menu", lambda x: None]]
# # # #         elevation: 3

# # # #     MDFloatLayout:

# # # #         MDRoundFlatIconButton:
# # # #             text: "Open manager"
# # # #             icon: "folder"
# # # #             pos_hint: {"center_x": .5, "center_y": .5}
# # # #             on_release: app.file_manager_open()
# # # # '''

# # # # class Example(MDApp):
# # # #     def __init__(self, **kwargs):
# # # #         super().__init__(**kwargs)
# # # #         Window.bind(on_keyboard=self.events)
# # # #         self.manager_open = False
# # # #         self.file_manager = MDFileManager(
# # # #             exit_manager=self.exit_manager, select_path=self.select_path
# # # #         )

# # # #     def build(self):
# # # #         self.theme_cls.theme_style = "Dark"
# # # #         self.theme_cls.primary_palette = "Orange"
# # # #         return Builder.load_string(select_image_screen)

# # # #     def file_manager_open(self):
# # # #         self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
# # # #         self.manager_open = True

# # # #     def select_path(self, path: str):
# # # #         '''
# # # #         It will be called when you click on the file name
# # # #         or the catalog selection button.

# # # #         :param path: path to the selected directory or file;
# # # #         '''

# # # #         self.exit_manager()
# # # #         toast(path)

# # # #     def exit_manager(self, *args):
# # # #         '''Called when the user reaches the root of the directory tree.'''

# # # #         self.manager_open = False
# # # #         self.file_manager.close()

# # # #     def events(self, instance, keyboard, keycode, text, modifiers):
# # # #         '''Called when buttons are pressed on the mobile device.'''

# # # #         if keyboard in (1001, 27):
# # # #             if self.manager_open:
# # # #                 self.file_manager.back()
# # # #         return True
  
# # # # class Test(MDApp):
# # # #     def build(self):
# # # #         return Builder.load_string(live_camera_screen)


# # # # # Test().run()

# # # # Example().run()

# # # # import cv2
# # # # from kivy.app import App
# # # # from kivy.uix.image import Image
# # # # from kivy.clock import Clock
# # # # from kivy.graphics.texture import Texture


# # # # class CameraApp(App):
# # # #     def build(self):
# # # #         self.capture = cv2.VideoCapture(0)
# # # #         _, self.frame = self.capture.read()

# # # #         # Create Kivy Image widget
# # # #         self.image = Image()

# # # #         # Schedule the update method to be called every 1/30 seconds (30 fps)
# # # #         Clock.schedule_interval(self.update, 1.0 / 30.0)

# # # #         return self.image

# # # #     def update(self, dt):
# # # #         # Read a frame from the camera
# # # #         ret, frame = self.capture.read()

# # # #         # Convert the frame to texture
# # # #         buf1 = cv2.flip(frame, 0)
# # # #         buf = buf1.tostring()
# # # #         image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
# # # #         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

# # # #         # Update the Image widget with the new texture
# # # #         self.image.texture = image_texture

# # # #     def on_stop(self):
# # # #         # Release the camera when the app is closed
# # # #         self.capture.release()


# # # # if __name__ == '__main__':
# # # #     CameraApp().run()

# # # from kivy.lang import Builder
# # # import os
# # # import cv2
# # # from kivy.app import App
# # # from kivy.uix.image import Image
# # # from kivy.uix.screenmanager import ScreenManager, Screen
# # # from kivy.core.window import Window
# # # from kivymd.app import MDApp
# # # from kivymd.uix.filemanager import MDFileManager
# # # from kivymd.toast import toast
# # # from kivymd.uix.button import MDRaisedButton
# # # from kivymd.uix.boxlayout import MDBoxLayout

# # # from kivymd.uix.floatlayout import MDFloatLayout

# # # from kivy.graphics.texture import Texture
# # # from kivy.clock import Clock

# # # Builder.load_string('''
# # # #:import NoTransition kivy.uix.screenmanager.NoTransition

# # # <HomeScreen>:
# # #     MDBoxLayout:
# # #         orientation: "vertical"

# # #         MDTopAppBar:
# # #             title: "MDTopAppBar"
# # #             left_action_items: [["menu", lambda x: app.callback()]]
# # #             right_action_items: [["dots-vertical", lambda x: app.callback_1()]]

# # #         MDLabel:
# # #             text: "Content"
# # #             halign: "center"

# # # <SelectImageScreen>:
# # #     MDBoxLayout:
# # #         orientation: "vertical"

# # #         MDTopAppBar:
# # #             title: "MDFileManager"
# # #             left_action_items: [["menu", lambda x: None]]
# # #             elevation: 3

# # #         MDFloatLayout:

# # #             MDRoundFlatIconButton:
# # #                 text: "Open manager"
# # #                 icon: "folder"
# # #                 pos_hint: {"center_x": .5, "center_y": .5}
# # #                 on_release: app.file_manager_open()
# # # ''')

# # # class HomeScreen(Screen):
# # #     pass

# # # class SelectImageScreen(Screen):
# # #     pass

# # # class SelectVideoScreen(Screen):
# # #     pass

# # # class LiveCameraScreen(Screen):
# # #     def build(self):
# # #         self.capture = cv2.VideoCapture(0)
# # #         _, self.frame = self.capture.read()

# # #         # Create Kivy Image widget
# # #         self.image = Image()

# # #         # Schedule the update method to be called every 1/30 seconds (30 fps)
# # #         Clock.schedule_interval(self.update, 1.0 / 30.0)

# # #         return self.image

# # #     def update(self, dt):
# # #         # Read a frame from the camera
# # #         ret, frame = self.capture.read()

# # #         # Convert the frame to texture
# # #         buf1 = cv2.flip(frame, 0)
# # #         buf = buf1.tostring()
# # #         image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
# # #         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

# # #         # Update the Image widget with the new texture
# # #         self.image.texture = image_texture

# # #     def on_stop(self):
# # #         # Release the camera when the app is closed
# # #         self.capture.release()

# # # class ExampleApp(MDApp):
# # #     def __init__(self, **kwargs):
# # #         super().__init__(**kwargs)
# # #         Window.bind(on_keyboard=self.events)
# # #         self.manager_open = False
# # #         self.file_manager = MDFileManager(
# # #             exit_manager=self.exit_manager, select_path=self.select_path
# # #         )
# # #         self.screen_manager = ScreenManager()
# # #         self.home_screen = HomeScreen(name='home')
# # #         self.select_image_screen = SelectImageScreen(name='select_image')
# # #         self.select_video_screen = SelectVideoScreen(name='select_video')
# # #         self.live_camera_screen = LiveCameraScreen(name='live_camera')
# # #         self.screen_manager.add_widget(self.home_screen)
# # #         self.screen_manager.add_widget(self.select_image_screen)
# # #         self.screen_manager.add_widget(self.select_video_screen)
# # #         self.screen_manager.add_widget(self.live_camera_screen)

# # #     def build(self):
# # #         self.theme_cls.theme_style = "Dark"
# # #         self.theme_cls.primary_palette = "Orange"
# # #         return self.screen_manager

# # #     def file_manager_open(self):
# # #         self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
# # #         self.manager_open = True

# # #     def select_path(self, path: str):
# # #         self.exit_manager()
# # #         toast(path)

# # #     def exit_manager(self, *args):
# # #         self.manager_open = False
# # #         self.file_manager.close()

# # #     def events(self, instance, keyboard, keycode, text, modifiers):
# # #         if keyboard in (1001, 27):
# # #             if self.manager_open:
# # #                 self.file_manager.back()
# # #         return True

# # # if __name__ == '__main__':
# # #     ExampleApp().run()

# # from kivy.lang import Builder
# # import os
# # import cv2
# # from kivy.app import App
# # from kivy.uix.image import Image
# # from kivy.uix.screenmanager import ScreenManager, Screen
# # from kivy.core.window import Window
# # from kivymd.app import MDApp
# # from kivymd.uix.filemanager import MDFileManager
# # from kivymd.toast import toast
# # from kivymd.uix.button import MDRaisedButton
# # from kivymd.uix.boxlayout import MDBoxLayout
# # from kivymd.uix.floatlayout import MDFloatLayout
# # from kivy.graphics.texture import Texture
# # from kivy.clock import Clock

# # Builder.load_string('''
# # #:import NoTransition kivy.uix.screenmanager.NoTransition

# # <HomeScreen>:
# #     MDBoxLayout:
# #         orientation: "vertical"

# #         MDTopAppBar:
# #             title: "MDTopAppBar"
# #             left_action_items: [["menu", lambda x: app.callback()]]
# #             right_action_items: [["dots-vertical", lambda x: app.callback_1()]]

# #         MDLabel:
# #             text: "Content"
# #             halign: "center"

# #         MDRaisedButton:
# #             text: "Select Image"
# #             md_bg_color: "red"
# #             on_release: app.root.current = 'select_image'

# #         MDRaisedButton:
# #             text: "Select Video"
# #             md_bg_color: "red"
# #             on_release: app.root.current = 'select_video'

# #         MDRaisedButton:
# #             text: "Detect Live"
# #             md_bg_color: "red"
# #             on_release: app.root.current = 'live_camera'

# # <SelectImageScreen>:
# #     MDBoxLayout:
# #         orientation: "vertical"

# #         MDTopAppBar:
# #             title: "MDFileManager"
# #             left_action_items: [["menu", lambda x: app.callback()]]
# #             elevation: 3

# #         MDFloatLayout:

# #             MDRoundFlatIconButton:
# #                 text: "Open manager"
# #                 icon: "folder"
# #                 pos_hint: {"center_x": .5, "center_y": .5}
# #                 on_release: app.file_manager_open()

# # <SelectVideoScreen>:
# #     MDBoxLayout:
# #         orientation: "vertical"

# #         MDTopAppBar:
# #             title: "Select Video"
# #             left_action_items: [["arrow-left", lambda x: app.callback()]]
# #             elevation: 3

# #         MDFloatLayout:
# #             # Add your UI elements for selecting video here

# # <LiveCameraScreen>:
# #     MDBoxLayout:
# #         orientation: "vertical"

# #         MDTopAppBar:
# #             title: "Live Camera"
# #             left_action_items: [["arrow-left", lambda x: app.callback()]]
# #             elevation: 3

# #         MDFloatLayout:
# #             # Add your UI elements for live camera here
# # ''')

# # class HomeScreen(Screen):
# #     pass

# # class SelectImageScreen(Screen):
# #     pass

# # class SelectVideoScreen(Screen):
# #     pass

# # class LiveCameraScreen(Screen):
# #     def build(self):
# #         self.capture = cv2.VideoCapture(0)
# #         _, self.frame = self.capture.read()

# #         # Create Kivy Image widget
# #         self.image = Image()

# #         # Schedule the update method to be called every 1/30 seconds (30 fps)
# #         Clock.schedule_interval(self.update, 1.0 / 30.0)

# #         return self.image

# #     def update(self, dt):
# #         # Read a frame from the camera
# #         ret, frame = self.capture.read()

# #         # Convert the frame to texture
# #         buf1 = cv2.flip(frame, 0)
# #         buf = buf1.tostring()
# #         image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
# #         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

# #         # Update the Image widget with the new texture
# #         self.image.texture = image_texture

# #     def on_stop(self):
# #         # Release the camera when the app is closed
# #         self.capture.release()

# # class ExampleApp(MDApp):
# #     def __init__(self, **kwargs):
# #         super().__init__(**kwargs)
# #         Window.bind(on_keyboard=self.events)
# #         self.manager_open = False
# #         self.file_manager = MDFileManager(
# #             exit_manager=self.exit_manager, select_path=self.select_path
# #         )
# #         self.screen_manager = ScreenManager()
# #         self.home_screen = HomeScreen(name='home')
# #         self.select_image_screen = SelectImageScreen(name='select_image')
# #         self.select_video_screen = SelectVideoScreen(name='select_video')
# #         self.live_camera_screen = LiveCameraScreen(name='live_camera')
# #         self.screen_manager.add_widget(self.home_screen)
# #         self.screen_manager.add_widget(self.select_image_screen)
# #         self.screen_manager.add_widget(self.select_video_screen)
# #         self.screen_manager.add_widget(self.live_camera_screen)

# #     def build(self):
# #         self.theme_cls.theme_style = "Dark"
# #         self.theme_cls.primary_palette = "Orange"
# #         return self.screen_manager

# #     def file_manager_open(self):
# #         self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
# #         self.manager_open = True

# #     def select_path(self, path: str):
# #         self.exit_manager()
# #         toast(path)

# #     def exit_manager(self, *args):
# #         self.manager_open = False
# #         self.file_manager.close()

# #     def events(self, instance, keyboard, keycode, text, modifiers):
# #         if keyboard in (1001, 27):
# #             if self.manager_open:
# #                 self.file_manager.back()
# #         return True

# # if __name__ == '__main__':
# #     ExampleApp().run()




# from kivy.lang import Builder
# import os
# import cv2
# from kivy.app import App
# from kivy.uix.image import Image
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.core.window import Window
# from kivymd.app import MDApp
# from kivymd.uix.filemanager import MDFileManager
# from kivymd.toast import toast
# from kivymd.uix.button import MDRaisedButton
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.floatlayout import MDFloatLayout
# from kivy.graphics.texture import Texture
# from kivy.clock import Clock

# Builder.load_string('''
# #:import NoTransition kivy.uix.screenmanager.NoTransition

# <HomeScreen>:
#     MDBoxLayout:
#         orientation: "vertical"

#         MDTopAppBar:
#             title: "MDTopAppBar"
#             right_action_items: [["dots-vertical", lambda x: app.callback_1()]]

#         MDLabel:
#             halign: "center"
#         MDBoxLayout:
#             orientation: "vertical"
#             pos_hint: {"center_x": .5, "center_y": .5}
#             MDRaisedButton:
#                 text: "Select Image"
#                 md_bg_color: "red"
#                 on_release: app.root.current = 'select_image'

#             MDRaisedButton:
#                 text: "Select Video"
#                 md_bg_color: "red"
#                 on_release: app.root.current = 'select_video'

#             MDRaisedButton:
#                 text: "Detect Live"
#                 md_bg_color: "red"
#                 on_release: app.root.current = 'live_camera'


# <SelectImageScreen>:
#     MDBoxLayout:
#         orientation: "vertical"

#         MDTopAppBar:
#             title: "MDFileManager"
#             left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'home')]]
#             elevation: 3

#         MDFloatLayout:

#             MDRoundFlatIconButton:
#                 text: "Open manager"
#                 icon: "folder"
#                 pos_hint: {"center_x": .5, "center_y": .5}
#                 on_release: app.file_manager_open()

# <SelectVideoScreen>:
#     MDBoxLayout:
#         orientation: "vertical"

#         MDTopAppBar:
#             title: "Select Video"
#             left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'home')]]
#             elevation: 3

#         MDFloatLayout:

#             MDRoundFlatIconButton:
#                 text: "Open manager"
#                 icon: "folder"
#                 pos_hint: {"center_x": .5, "center_y": .5}
#                 on_release: app.file_manager_open()

# <LiveCameraScreen>:
#     MDBoxLayout:
#         orientation: "vertical"

#         MDTopAppBar:
#             title: "Live Camera"
#             left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'home')]]
#             elevation: 3

#         MDFloatLayout:
#             MDRaisedButton:
#                 text: "Open Camera"
#                 md_bg_color: "blue"
#                 pos_hint: {"center_x": .5, "center_y": .5}
#                 on_release: app.open_camera()
# ''')

# class HomeScreen(Screen):
#     pass

# class SelectImageScreen(Screen):
#     pass

# class SelectVideoScreen(Screen):
#     pass

# class LiveCameraScreen(Screen):
#     def build(self):
#         self.capture = cv2.VideoCapture(0)
#         _, self.frame = self.capture.read()

#         # Create Kivy Image widget
#         self.image = Image()

#         # Schedule the update method to be called every 1/30 seconds (30 fps)
#         Clock.schedule_interval(self.update, 1.0 / 30.0)

#         return self.image

#     def update(self, dt):
#         # Read a frame from the camera
#         ret, frame = self.capture.read()

#         # Convert the frame to texture
#         buf1 = cv2.flip(frame, 0)
#         buf = buf1.tostring()
#         image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
#         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

#         # Update the Image widget with the new texture
#         self.image.texture = image_texture

#     def on_stop(self):
#         # Release the camera when the app is closed
#         self.capture.release()

# class ExampleApp(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         Window.bind(on_keyboard=self.events)
#         self.manager_open = False
#         self.file_manager = MDFileManager(
#             exit_manager=self.exit_manager, select_path=self.select_path
#         )
#         self.screen_manager = ScreenManager()
#         self.home_screen = HomeScreen(name='home')
#         self.select_image_screen = SelectImageScreen(name='select_image')
#         self.select_video_screen = SelectVideoScreen(name='select_video')
#         self.live_camera_screen = LiveCameraScreen(name='live_camera')
#         self.screen_manager.add_widget(self.home_screen)
#         self.screen_manager.add_widget(self.select_image_screen)
#         self.screen_manager.add_widget(self.select_video_screen)
#         self.screen_manager.add_widget(self.live_camera_screen)

#     def build(self):
#         self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = "Orange"
#         return self.screen_manager

#     def file_manager_open(self):
#         self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
#         self.manager_open = True

#     def select_path(self, path: str):
#         self.exit_manager()
#         toast(path)

#     def exit_manager(self, *args):
#         self.manager_open = False
#         self.file_manager.close()

#     def events(self, instance, keyboard, keycode, text, modifiers):
#         if keyboard in (1001, 27):
#             if self.manager_open:
#                 self.file_manager.back()
#         return True

# if __name__ == '__main__':
#     ExampleApp().run()

# from kivy.lang import Builder
# import os
# import cv2
# from kivy.app import App
# from kivy.uix.image import Image
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.core.window import Window
# from kivymd.app import MDApp
# from kivymd.uix.filemanager import MDFileManager
# from kivymd.toast import toast



from kivy.lang import Builder
import os
import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock



Builder.load_string('''
#:import NoTransition kivy.uix.screenmanager.NoTransition
<HomeScreen>:
    
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Pothole Detection"
            right_action_items: [["dots-vertical", lambda x: app.callback_1()]]
            elevation: 10
        
        MDBoxLayout:
            spacing: "10dp"  # Adjust the spacing between buttons
            padding: "10dp"  # Add padding to the layout
            
            orientation: "vertical"
           
            MDRaisedButton:
                text: "Select Image"
                md_bg_color: app.theme_cls.primary_color  # Use the primary color
                pos_hint: {'center_x':0.5,'center_y':0.4}
                on_release: app.root.current = 'select_image'

            MDRaisedButton:
                text: "Select Video"
                md_bg_color: app.theme_cls.primary_color  # Use the primary color
                on_release: app.root.current = 'select_video'
                pos_hint: {'center_x':0.5,'center_y':0.5}

            MDRaisedButton:
                text: "Detect Live"
                md_bg_color: app.theme_cls.primary_color  # Use the primary color
                on_release: app.open_live_camera_screen()  # Call the method to open the live camera screen
                pos_hint: {'center_x':0.5,'center_y':0.6}

<SelectImageScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "MDFileManager"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'home')]]
            elevation: 3

        MDFloatLayout:

            MDRoundFlatIconButton:
                text: "Open manager"
                icon: "folder"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: app.file_manager_open()

<SelectVideoScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Select Video"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'home')]]
            elevation: 3

        MDFloatLayout:

            MDRoundFlatIconButton:
                text: "Open manager"
                icon: "folder"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: app.file_manager_open()

<LiveCameraScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Live Camera"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'home')]]
            elevation: 3

        MDFloatLayout:

            MDRoundFlatButton:
                text: "Open Camera"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: app.open_camera()

            Image:
                id: live_camera_image
''')

class HomeScreen(Screen):
    pass

class SelectImageScreen(Screen):
    pass

class SelectVideoScreen(Screen):
    pass

class LiveCameraScreen(Screen):
    def __init__(self, **kwargs):
        super(LiveCameraScreen, self).__init__(**kwargs)
        self.capture = None
        self.image = None

    def on_enter(self, *args):
        # This method is called when the screen is entered
        self.capture = cv2.VideoCapture(0)
        _, self.frame = self.capture.read()
        self.image = Image()

        # Schedule the update method to be called every 1/30 seconds (30 fps)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        self.add_widget(self.image)

    def on_leave(self, *args):
        # This method is called when the screen is left
        if self.capture:
            self.capture.release()

    def update(self, dt):
        # Read a frame from the camera
        ret, frame = self.capture.read()

        # Convert the frame to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # Update the Image widget with the new texture
        self.image.texture = image_texture
class ExampleApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.screen_manager = ScreenManager()
        self.home_screen = HomeScreen(name='home')
        self.select_image_screen = SelectImageScreen(name='select_image')
        self.select_video_screen = SelectVideoScreen(name='select_video')
        self.live_camera_screen = LiveCameraScreen(name='live_camera')
        self.screen_manager.add_widget(self.home_screen)
        self.screen_manager.add_widget(self.select_image_screen)
        self.screen_manager.add_widget(self.select_video_screen)
        self.screen_manager.add_widget(self.live_camera_screen)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return self.screen_manager

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def open_live_camera_screen(self):
        self.screen_manager.current = 'live_camera'

    def open_camera(self):
        # Add your camera opening logic here
        pass

if __name__ == '__main__':
    ExampleApp().run()
