import cv2
import numpy as np
import os
from callback_function import CallBackFunction
from utility.utility import Utility


# Declare variables
file_path = os.path.abspath(os.getcwd()) + '\greenscreen-asteroid.mp4'
video_window_name = 'Video Output'
cap = cv2.VideoCapture(file_path)
cap_width = int(cap.get(3))      # Get width of video
cap_height = int(cap.get(4))     # Get height of video

# Initialize class objects
debug = Utility(custom_ident_number=1, custom_turn_on_debug=True)
callback = CallBackFunction(file_path, custom_name_of_window=video_window_name)


# Check if camera opened successfully
debug.def_name = 'Before If Loop'
if cap.isOpened() == False:
    print("Error opening video stream or file")



# Run call back function
cv2.namedWindow(video_window_name)
cv2.setMouseCallback(video_window_name, callback.press_left_mouse_button_get_x_y_coordinates)

# Create a def that does nothing when trackbar changes
def nothing(x):
    pass

# Create a panel with track bar
panel = np.zeros([100, 700, 3], np.uint8)       # Creation 100 pixel x 700 pixel 3 dimension of zeros for a black screen
cv2.namedWindow("Panel")
cv2.createTrackbar("Lower Hue", "Panel", 0, 179, nothing)
cv2.createTrackbar("Upper Hue", "Panel", 179, 179, nothing)
cv2.createTrackbar("Lower Saturation", "Panel", 0, 255, nothing)
cv2.createTrackbar("Upper Saturation", "Panel", 255, 255, nothing)
cv2.createTrackbar("Lower Value", "Panel", 0, 255, nothing)
cv2.createTrackbar("Upper Value", "Panel", 255, 255, nothing)
cv2.createTrackbar("Gaussian Pixel", "Panel", 1, 25, nothing)
cv2.createTrackbar("Gaussian Sigma", "Panel", 1, 25, nothing)

# Background Video
background_video_filepath = os.path.abspath(os.getcwd()) + '\\Nebula - 25168.mp4'
background_video_capture = cv2.VideoCapture(background_video_filepath)

debug.title = 'class: main def: after if statement'
debug_path = {'cap.isOpened': cap.isOpened(),
              'file_path': file_path,
              'video_window_name': video_window_name,
              'cap_width': cap_width,
              'cap_height': cap_height,
              'background_video_filepath': background_video_filepath,
              'background_video_capture.isOpened': background_video_capture.isOpened()}
debug.print_value_dictionary(debug_path)
frame_counter = 0       # Initialize frame counter for infinite playback
while True:
    frame_counter += 1      # Increment frame count
    # If the last frame is reached, reset the capture and the frame_counter
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0  # Or whatever as long as it is the same as next line
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # Capture frame-by-frame
    ret, frame = cap.read()

    get_lower_hue_trackbar_position = cv2.getTrackbarPos("Lower Hue", "Panel")
    getl_upper_hue_trackbar_position = cv2.getTrackbarPos("Upper Hue", "Panel")
    get_lower_saturation_trackbar_position = cv2.getTrackbarPos("Lower Saturation", "Panel")
    getl_upper_saturation_trackbar_position = cv2.getTrackbarPos("Upper Saturation", "Panel")
    get_lower_value_trackbar_position = cv2.getTrackbarPos("Lower Value", "Panel")
    getl_upper_value_trackbar_position = cv2.getTrackbarPos("Upper Value", "Panel")
    get_gaussian_pixel = cv2.getTrackbarPos("Gaussian Pixel", "Panel")
    get_gaussian_sigma = cv2.getTrackbarPos("Gaussian Sigma", "Panel")

    frame = cv2.GaussianBlur(frame, (get_gaussian_pixel, get_gaussian_pixel), get_gaussian_sigma, get_gaussian_sigma)
    # Change the color of the frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define lower range and upper range
    lower_green_range = np.array([get_lower_hue_trackbar_position, get_lower_saturation_trackbar_position, get_lower_value_trackbar_position])
    upper_green_range = np.array([getl_upper_hue_trackbar_position, getl_upper_saturation_trackbar_position, getl_upper_value_trackbar_position])

    # Create a Mask

    mask = cv2.inRange(hsv, lower_green_range, upper_green_range)
    mask_inverse = cv2.bitwise_not(mask)

    # Get the background of image
    background = cv2.bitwise_and(frame, frame, mask=mask)
    foreground = cv2.bitwise_and(frame, frame, mask=mask_inverse)

    # Black Out Mask Area and let background show through
    mask_of_asteroid = cv2.inRange(frame, lower_green_range, upper_green_range)
    mask_of_asteroid_show_asteroid = np.copy(frame)
    mask_of_asteroid_show_asteroid[mask_of_asteroid != 0] = 0

    # Read background video
    background_return, background_frame = background_video_capture.read()
    background_frame = cv2.resize(background_frame, (cap_width, cap_height), interpolation=cv2.INTER_AREA)

    # Change the color of the frame
    #background_frame_hsv = cv2.cvtColor(background_frame, cv2.COLOR_BGR2HSV)
    background_frame[mask == 0] = 0
    final_complete_frame = background_frame + foreground

    debug.title = 'class: main def: while cap.isOpened()'
    debug_path = {'callback.x': callback.x,
                  'callback.y': callback.y,
                  'video_window_name': video_window_name}
    debug.print_value_dictionary(debug_path)
    if ret == True:

        # cv2.imshow(video_window_name, frame)
        # cv2.imshow("Mask", mask)
        # cv2.imshow("Mask of Asteroid", mask_of_asteroid)
        # cv2.imshow("Background Frame Mask", background_frame)
        # cv2.imshow("Foreground", foreground)
        # cv2.imshow("Background", background)
        cv2.imshow("Final Complete Video", final_complete_frame)
        cv2.imshow("Panel", panel)
        # Wait for 25 ms before moving on to the next frame
        # This will slow down the video
        cv2.waitKey(25)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()