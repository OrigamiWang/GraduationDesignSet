# main.py
# Usage: %python main.py

# Import the FaceDetect class
from biz.face_detect.FaceDetect.facedetect import FaceDetect
# from FaceDetect.facedetect import FaceDetect


# Initialize FaceDetect
# Params:
# - settings (optional): Dictionary with settings to be passed to the FaceDetector
#   * mode:  image or video (default)
#   * custom: False (default). If you wish to extend the FaceDetect class, specify the method that it needs to execute
#   * method: call native callback methods during detection or bypass with a custom method
#   * draw: draws the detection on the canvas if set to True (default)
#   * print: prints the face locations and labels on the console
#   * face-extraction: extracts captures of the faces into their own images. Applicable only to mode image
#   * face-features: Draws the specified face features. Off by default. Pass the list ['face'] to draw the whole face
#   * known-faces: Setting need for facial recognition when 'method' is set to 'recognize'
#                  It is a dictionary of face labels and image paths associated.
#                  For example: {'John': 'person1.png', 'Jane': 'person2.png'}
#


facedetector = FaceDetect({'mode': 'image', 'draw': False, 'print': False})

def human_face_detect(img_data):
    return facedetector.start(img_data)