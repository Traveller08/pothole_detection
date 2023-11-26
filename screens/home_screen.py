import cv2 as cv
import time
import geocoder
import os
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.is_camera_open = False
        self.capture = None
        self.image = None
        self.class_name = []
        with open(os.path.join("project_files", 'obj.names'), 'r') as f:
            self.class_name = [cname.strip() for cname in f.readlines()]
        self.net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
        self.net1.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.net1.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
        self.model1 = cv.dnn_DetectionModel(self.net1)
        self.model1.setInputParams(size=(640, 480), scale=1 / 255, swapRB=True)
        self.Conf_threshold = 0.5
        self.NMS_threshold = 0.4
        self.g = geocoder.ip('me')
        self.result_path = "pothole_coordinates"
    def on_enter(self, *args):
        super().on_enter(*args)

        # Create the top app bar
        self.top_app_bar = MDTopAppBar(
            title="Roadguard",
            pos_hint={"top": 1},
        )

        # Create the image widget
        self.image_layout=MDBoxLayout(
             padding=[dp(5), dp(0), dp(5), dp(0)],
        )
        self.image = Image()
        self.image_layout.add_widget(self.image)

        # Create the "Start Camera" button
        self.start_camera_button = MDRaisedButton(
            text="Open Camera",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.toggle_camera,
        )

        # Create the main layout
        self.main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(0), dp(0), dp(0), dp(10)],
            md_bg_color=(1, 1, 1, 1),  # White background color
        )

        # Add widgets to the main layout
        self.main_layout.add_widget(self.top_app_bar)
        self.main_layout.add_widget(self.image_layout)
        self.main_layout.add_widget(self.start_camera_button)

        self.add_widget(self.main_layout)

    def toggle_camera(self, *args):
        self.is_camera_open = not self.is_camera_open

        if self.is_camera_open:
            self.start_camera_button.text = "Stop Camera"
            self.start_camera()
        else:
            self.start_camera_button.text = "Start Camera"
            self.stop_camera()

    def start_camera(self):
      

        self.capture = cv.VideoCapture(0)
        self.width = self.capture.get(3)
        self.height = self.capture.get(4)

        self.result = cv.VideoWriter('result.avi', cv.VideoWriter_fourcc(*'MJPG'), 10,
                                     (int(self.width), int(self.height)))
        _, self.frame = self.capture.read()

        # Schedule the update method to be called every 1/30 seconds (30 fps)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        
        self.starting_time = time.time()
       
        self.frame_counter = 0
        self.i = 0
        self.b = 0
    def stop_camera(self):
        if self.capture:
            self.capture.release()

    def update(self, dt):
        ret, frame = self.capture.read()
        # Rest of the camera logic from the original code...
        if ret:
            self.frame_counter += 1
            classes, scores, boxes = self.model1.detect(frame, self.Conf_threshold, self.NMS_threshold)
            for (classid, score, box) in zip(classes, scores, boxes):
                label = "pothole"
                x, y, w, h = box
                recarea = w * h
                area = self.width * self.height
                # drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
                if (len(scores) != 0 and scores[0] >= 0.7):
                    if ((recarea / area) <= 0.1 and box[1] < 600):
                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                        cv.putText(frame, "%" + str(round(scores[0] * 100, 2)) + " " + label,
                                (box[0], box[1] - 10), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                        if (self.i == 0):
                            cv.imwrite(os.path.join(self.result_path, 'pothole' + str(self.i) + '.jpg'), frame)
                            with open(os.path.join(self.result_path, 'pothole' + str(self.i) + '.txt'), 'w') as f:
                                f.write(str(self.g.latlng))
                                self.i = self.i + 1
                        if (self.i != 0):
                            if ((time.time() - self.b) >= 2):
                                cv.imwrite(os.path.join(self.result_path, 'pothole' + str(self.i) + '.jpg'), frame)
                                with open(os.path.join(self.result_path, 'pothole' + str(self.i) + '.txt'), 'w') as f:
                                    f.write(str(self.g.latlng))
                                    b = time.time()
                                    self.i = self.i + 1

            # writing fps on frame
            endingTime = time.time() - self.starting_time
            fps = self.frame_counter / endingTime
            cv.putText(frame, f'FPS: {fps}', (20, 50), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

            # Convert the frame to texture
            buf1 = cv.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            # Update the Image widget with the new texture
            self.image.texture = image_texture

    def on_leave(self, *args):
        if self.is_camera_open:
            self.stop_camera()

# Instantiate and run the app
class MyApp(MDApp):
    def build(self):
        return HomeScreen()

if __name__ == "__main__":
    MyApp().run()
