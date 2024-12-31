from flask import Flask, request
import cv2
import numpy as np
from face_detect import human_face_detect

app = Flask(__name__)


@app.route("/face_detection", methods=["POST"])
def face_detection():
    file = request.files['face']
    img_data = file.read()
    return human_face_detect(img_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1145)