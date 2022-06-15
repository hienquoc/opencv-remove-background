import cv2
import math
from utility.utility import Utility


class CallBackFunction:

    def __init__(self, custom_file_path, custom_name_of_window='Window'):

        self.file_path = custom_file_path
        self.name_of_window = custom_name_of_window
        self.x = None
        self.y = None
        cv2.namedWindow(self.name_of_window)

        self.debug = Utility(custom_turn_on_debug=True)
        self.debug.title = 'class: CallBackFunction def: __init__'
        print("callback function")
        self.debug_variable_dictionary = {
            'self.name_of_window': self.name_of_window,
            'self.file_path': self.file_path}
        self.debug.print_value_dictionary(self.debug_variable_dictionary)

    def press_left_mouse_button_get_x_y_coordinates(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x = x
            self.y = y
            self.debug.title = 'class: CallBackFunction def: press_left_mouse_button_get_x_y_coordinates'
            self.debug_variable_dictionary = {
                'event': event,
                'x': x,
                'y': y,
                'self.x': self.x,
                'self.y': self.y
            }
            self.debug.print_value_dictionary(self.debug_variable_dictionary)


    def callback(self):
        #   Setup debug object attribute
        self.debug.title = 'class: CallBackFunction def: press_left_mouse_button_get_x_y_coordinates'
        self.debug_variable_dictionary = {
            'self.name_of_window': self.name_of_window,
            'self.file_path': self.file_path
        }
        self.debug.print_value_dictionary(self.debug_variable_dictionary)

        cv2.setMouseCallback(self.name_of_window, self.press_left_mouse_button_get_x_y_coordinates)
        cv2.imshow(self.name_of_window, self.file_path)

