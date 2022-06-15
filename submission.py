import cv2
import numpy as np
import os
from callback_function import CallBackFunction
from utility.utility import Utility


# Declare variables
file_path = os.path.abspath(os.getcwd()) + '\greenscreen-asteroid.mp4'
video_window_name = 'Video Output'
cap = cv2.VideoCapture(file_path)

# Initialize class objects
debug = Utility(custom_ident_number=1, custom_turn_on_debug=True)
callback = CallBackFunction(file_path, custom_name_of_window=video_window_name)


# Check if camera opened successfully
debug.def_name = 'Before If Loop'
if cap.isOpened() == False:
    print("Error opening video stream or file")

debug.title = 'class: main def: after if statement'
debug_path = {'cap.isOpened': cap.isOpened(),
              'file_path': file_path,
              'video_window_name': video_window_name}
debug.print_value_dictionary(debug_path)

# Run call back function
cv2.namedWindow(video_window_name)
cv2.setMouseCallback(video_window_name, callback.press_left_mouse_button_get_x_y_coordinates)


while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    debug.title = 'class: main def: while cap.isOpened()'
    debug_path = {'callback.x': callback.x,
                  'callback.y': callback.y,
                  'video_window_name': video_window_name}
    debug.print_value_dictionary(debug_path)
    if ret == True:

        cv2.imshow(video_window_name, frame)

        # Wait for 25 ms before moving on to the next frame
        # This will slow down the video
        cv2.waitKey(25)

    # Break the loop
    else:
        break
cv2.destroyAllWindows()