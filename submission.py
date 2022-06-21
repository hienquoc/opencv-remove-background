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
cv2.createTrackbar("Lower Hue", "Panel", 0, 255, nothing)
cv2.createTrackbar("Upper Hue", "Panel", 0, 255, nothing)
cv2.createTrackbar("Lower Saturation", "Panel", 0, 255, nothing)
cv2.createTrackbar("Upper Saturation", "Panel", 255, 255, nothing)
cv2.createTrackbar("Lower Value", "Panel", 0, 255, nothing)
cv2.createTrackbar("Upper Value", "Panel", 255, 255, nothing)
cv2.createTrackbar("Gaussian Blurr Pixel Size", "Panel", 0, 25, nothing)
cv2.createTrackbar("Gaussian Blurr Sigma", "Panel", 0, 50, nothing)
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
        frame_counter = 0  # Or whatever as long as it is the same as nex8b,y7qwdwsuhqwuiasujw;ae'{9grut6y59tug ikldyl ;b ,t line
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Change the color of the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_pixel_of_mouse_click = hsv[0, frame_counter, callback.y, callback.x, 0]
    h_pixel = h_pixel_of_mouse_click.item(0, 0)
    h_pixel_of_mouse_click_shape = h_pixel_of_mouse_click.shape
    cv2.setTrackbarPos("Lower Hue", "Panel", int(h_pixel))
    cv2.setTrackbarPos("Upper Hue", "Panel", int(h_pixel))

    get_lower_hue_trackbar_position = cv2.getTrackbarPos("Lower Hue", "Panel")
    get_upper_hue_trackbar_position = cv2.getTrackbarPos("Upper Hue", "Panel")
    get_lower_saturation_trackbar_position = cv2.getTrackbarPos("Lower Saturation", "Panel")
    get_upper_saturation_trackbar_position = cv2.getTrackbarPos("Upper Saturation", "Panel")
    get_lower_value_trackbar_position = cv2.getTrackbarPos("Lower Value", "Panel")
    get_upper_value_trackbar_position = cv2.getTrackbarPos("Upper Value", "Panel")
    get_gaussian_blur_pixel_size_position = cv2.getTrackbarPos("Gaussian Blurr Pixel Size", "Panel")
    get_gaussian_blur_sigma_size_position = cv2.getTrackbarPos("Gaussian Blurr Sigma", "Panel", )

    #define lower range and upper range
    lower_green_range = np.array([get_lower_hue_trackbar_position, get_lower_saturation_trackbar_position, get_lower_value_trackbar_position])
    upper_green_range = np.array([get_upper_hue_trackbar_position, get_upper_saturation_trackbar_position, get_upper_value_trackbar_position])

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
    try:
        background_frame = cv2.resize(background_frame, (cap_width, cap_height), interpolation=cv2.INTER_AREA)
        foreground = cv2.GaussianBlur(foreground, (get_gaussian_blur_pixel_size_position, get_gaussian_blur_pixel_size_position),
                                           get_gaussian_blur_sigma_size_position, get_gaussian_blur_sigma_size_position)

        # Change the color of the frame
    #background_frame_hsv = cv2.cvtColor(background_frame, cv2.COLOR_BGR2HSV)
        background_frame[mask == 0] = 0
    except Exception as e:
        print(str(e))

    final_complete_frame = foreground + background_frame

    debug.title = 'class: main def: while cap.isOpened()'
    debug_path = {'callback.x': callback.x,
                  'callback.y': callback.y,
                  'video_window_name': video_window_name,
                  'cap_width': cap_width,
                  'cap_height:': cap_height,
                  'callback.y': callback.y,
                  'callback.x': callback.x,
                  'h_pixel_of_mouse_click': h_pixel_of_mouse_click,
                  'h_pixel_of_mouse_click_shape':  h_pixel_of_mouse_click_shape,
                  'h_pixel': h_pixel}
    debug.print_value_dictionary(debug_path)
    if ret == True:

        # cv2.imshow(video_window_name, frame)
        # cv2.imshow("Mask", mask)
        # cv2.imshow("Mask of Asteroid", mask_of_asteroid)
        # cv2.imshow("Background Frame Mask", background_frame)
        cv2.imshow("Foreground", foreground)
        # cv2.imshow("Background", background)
        cv2.imshow("Final Complete Video", final_complete_frame)
        cv2.imshow("Panel", panel)
        # Wait for 25 ms before moving on to the next frame
        # This will slow down the video
        cv2.waitKey(25)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()