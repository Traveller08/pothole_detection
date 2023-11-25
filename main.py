from kivy.lang import Builder
import cv2 as cv
import time
import geocoder
import os
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

from image import detect_from_image
from camera_video import detect_from_video

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
        self.class_name = []
        

    def on_enter(self, *args):
        # This method is called when the screen is entered
        with open(os.path.join("project_files",'obj.names'), 'r') as f:
            self.class_name = [cname.strip() for cname in f.readlines()]
        self.net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
        self.net1.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.net1.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
        self.model1 = cv.dnn_DetectionModel(self.net1)
        self.model1.setInputParams(size=(640, 480), scale=1/255, swapRB=True)
        
        self.capture = cv.VideoCapture(0)
        self.width  = self.capture.get(3)
        self.height = self.capture.get(4)
        
        self.result = cv.VideoWriter('result.avi', cv.VideoWriter_fourcc(*'MJPG'),10,(int(self.width),int(self.height)))
        _, self.frame = self.capture.read()
        self.image = Image()

        # Schedule the update method to be called every 1/30 seconds (30 fps)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        self.add_widget(self.image)
        
        #defining parameters for result saving and get coordinates
        #defining initial values for some parameters in the script
        self.g = geocoder.ip('me')
        self.result_path = "pothole_coordinates"
        self.starting_time = time.time()
        self.Conf_threshold = 0.5
        self.NMS_threshold = 0.4
        self.frame_counter = 0
        self.i = 0
        self.b = 0

    def on_leave(self, *args):
        # This method is called when the screen is left
        if self.capture:
            self.capture.release()

    def update(self, dt):
        # Read a frame from the camera
        ret, frame = self.capture.read()
        self.frame_counter += 1
        if ret == False:
            self.on_leave()
        
            #analysis the stream with detection model
        classes, scores, boxes = self.model1.detect(frame, self.Conf_threshold, self.NMS_threshold)
        for (classid, score, box) in zip(classes, scores, boxes):
            label = "pothole"
            x, y, w, h = box
            recarea = w*h
            area = self.width*self.height
                #drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
            if(len(scores)!=0 and scores[0]>=0.7):
                if((recarea/area)<=0.1 and box[1]<600):
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 1)
                    cv.putText(frame, "%" + str(round(scores[0]*100,2)) + " " + label, (box[0], box[1]-10),cv.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 1)
                    if(self.i==0):
                        cv.imwrite(os.path.join(self.result_path,'pothole'+str(self.i)+'.jpg'), frame)
                        with open(os.path.join(self.result_path,'pothole'+str(self.i)+'.txt'), 'w') as f:
                            f.write(str(self.g.latlng))
                            self.i=self.i+1
                    if(self.i!=0):
                        if((time.time()-self.b)>=2):
                            cv.imwrite(os.path.join(self.result_path,'pothole'+str(self.i)+'.jpg'), frame)
                            with open(os.path.join(self.result_path,'pothole'+str(self.i)+'.txt'), 'w') as f:
                                f.write(str(self.g.latlng))
                                b = time.time()
                                self.i = self.i+1
            #writing fps on frame
        endingTime = time.time() - self.starting_time
        fps = self.frame_counter/endingTime
        cv.putText(frame, f'FPS: {fps}', (20, 50),cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
        #     #showing and saving result
        #     cv.imshow('frame', frame)
        self.result.write(frame)
        #     key = cv.waitKey(1)
        #     if key == ord('q'):
        #         break

        # # Convert the frame to texture
        buf1 = cv.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # # Update the Image widget with the new texture
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

        # Check the current screen and call the appropriate method
        current_screen = self.screen_manager.current
        if current_screen == 'select_image':
            self.openFileImage(path)
        elif current_screen == 'select_video':
            self.openFileVideo(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def imageToTexture(image):
        buf1 = cv.flip(image, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        
        return image_texture
        
    def openFileImage(self, image_path: str):
      
        print("Opening Selected Image File:", image_path)
        # Add your code to open or process the selected image file

    def openFileVideo(self, video_path: str):
        # Implement your logic to open or process the selected video file here
        detect_from_video(is_live=False, filename=video_path)
        print("Opening Selected Video File:", video_path)
        # Add your code to open or process the selected video file

    def open_live_camera_screen(self):
        self.screen_manager.current = 'live_camera'

    def open_camera(self):
        # Add your camera opening logic here
        pass

if __name__ == '__main__':
    ExampleApp().run()
