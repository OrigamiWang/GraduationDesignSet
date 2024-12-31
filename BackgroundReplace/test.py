from PIL import Image
import cv2
import numpy as np

src_image = Image.open(r"D:\university\GraduationDesign\GraduationDesign\BackgroundReplace\input\20180526194553_burnl.jpg")
image = src_image.convert("RGB")
image = np.array(image.convert("RGBA"))

image = Image.fromarray(image)
print(image.mode)
image.show()