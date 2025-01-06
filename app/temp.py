from PIL import Image

# 创建一个新的RGB图像，指定宽度、高度以及颜色模式
img = Image.new('RGB', (720, 1280), (255, 0, 0))

# 保存图像为文件，这里保存为'red_image.jpg'，你也可以根据需求更换保存格式及文件名
img.save('720x1280.png')