# importing the required packages

import pyautogui
import cv2
import numpy as np
import os
from PIL import ImageGrab


# Specify resolution
Size = (ImageGrab.grab()).size

# Specify video codec
codec = cv2.VideoWriter_fourcc(*"XVID")

# Specify name of Output file
filename = "Record.mp4"

# Specify frames rate. We can choose any
# value and experiment with it
fps = 5.0

# Creating a VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, Size)

# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

# Resize this window
cv2.resizeWindow("Live", 480, 270)

while True:
	# Take screenshot using PyAutoGUI
	#img = pyautogui.screenshot()

	# Convert the screenshot to a numpy array
	img = np.array(ImageGrab.grab())

	# Convert it from BGR(Blue, Green, Red) to
	# RGB(Red, Green, Blue)
	frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	# Write it to the output file
	out.write(img)

	# Optional: Display the recording screen
	cv2.imshow('Live', frame)

	# Stop recording when we press 'q'
	if cv2.waitKey(1) == ord('q'):
		break


# Release the Video writer
out.release()

# Destroy all windows
cv2.destroyAllWindows()

