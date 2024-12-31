from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import numpy as np
import cv2
import PIL.Image as Image
import os
from ultralytics import YOLO


def segany_mask_generate(seg_model, image):
    if isinstance(image, str):
        image = cv2.imread(image)
    if isinstance(image, Image.Image):
        image = np.array(image)
    # 生成mask
    original_image_size = image.shape[:2]
    # 如果图片太大，就resize到1920以下，最长边为1920
    if max(original_image_size) > 1920:
        scale = 1920 / max(original_image_size)
        image = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
    masks = seg_model.generate(image)
    return_masks = []
    for i, mask in enumerate(masks):
        #把masks给resize到原图大小
        return_masks.append(mask['segmentation'].astype(np.uint8))
    return np.array(return_masks)

# 2. yolov8的seg标注
def yolo_mask_generate(yolo_model, image):
    # 生成mask
    masks = yolo_model(image)
    if masks[0].masks is None:
        return None
    masks = masks[0].masks.data.data.cpu().numpy().sum(axis=0)
    #获取数量
    return masks

# 3. 投票机制，这里由于只有一类，所以直接融合所有YOLO_masks，然后和SAM_masks做投票，如果SAM_masks的重合率大于threshold就保留SAM_masks，否则扔掉，最后融合保留的SAM_masks并返回
def vote_mask_generate(SAM_masks,YOLO_masks,threshold=0.8,num = 1,erode_iter=3,erode_kernel_size=3):
    scores = []
    #把yolo_masks给resize到和SAM_masks一样的大小
    zeros = np.zeros_like(SAM_masks[0])
    #zeros与所有的SAM_masks进行或运算，得到一个和SAM_masks一样大小的mask 然后取反，得到所有的未标注区域，然后与YOLO_masks相与，得到所有的未标注区域的YOLO_masks
    full_mask = np.zeros_like(SAM_masks[0])
    for i, mask in enumerate(SAM_masks):
        full_mask = cv2.bitwise_or(full_mask,mask)
    #对YOLO_masks先进行一些腐蚀再膨胀
    kernel = np.ones((erode_kernel_size,erode_kernel_size),np.uint8)
    YOLO_masks = cv2.erode(YOLO_masks,kernel,iterations = erode_iter)
    if erode_iter > 1:
        YOLO_masks = cv2.dilate(YOLO_masks,kernel,iterations = erode_iter-1)
    YOLO_masks = cv2.resize(YOLO_masks, (SAM_masks[0].shape[1], SAM_masks[0].shape[0])).astype(np.uint8)
    not_labeled = cv2.bitwise_not(cv2.bitwise_or(zeros, full_mask))
    final_mask = np.zeros_like(SAM_masks[0])
    for i, mask in enumerate(SAM_masks):
        score = np.sum(YOLO_masks*mask/mask.sum())
        scores.append(score)
        if score > threshold:
            #或运算
            final_mask = cv2.bitwise_or(final_mask,mask)
        #print(score)
    not_labeled_yolo = cv2.bitwise_and(not_labeled, YOLO_masks)
    final_mask = cv2.bitwise_or(final_mask,not_labeled_yolo)
    final_mask = cv2.erode(final_mask,kernel,iterations = erode_iter)
    final_mask = cv2.dilate(final_mask,kernel,iterations = erode_iter)
    return final_mask.astype(np.uint8)
    
def plot_sam_mask(masks):
    color = np.random.randint(0, 255, (len(masks), 3), dtype=np.uint8)
    background = np.zeros((masks[0].shape[0],masks[0].shape[1],3),dtype=np.uint8)
    for i, mask in enumerate(masks):
        # 产生一个三通道的随机颜色 
        temp = np.concatenate((mask[:,:,np.newaxis],mask[:,:,np.newaxis],mask[:,:,np.newaxis]),axis=2)
        temp = temp*color[i]
        background = cv2.bitwise_or(background,temp)
    return background


def pipeline(seg_model, yolo_model, src_image, threshold=0.6):
    image = src_image.convert("RGB")
    yolo_masks= yolo_mask_generate(yolo_model,image)
    if yolo_masks is None:
        return None, None, None, None
    sam_masks = segany_mask_generate(seg_model,image)
    voted_mask = vote_mask_generate(sam_masks,yolo_masks,threshold=threshold)
    image = np.array(image.convert("RGBA"))
    voted_mask = np.array(voted_mask)
    #把mask给resize到和image一样的大小
    voted_mask = cv2.resize(voted_mask, (image.shape[1], image.shape[0])).astype(np.uint8)
    #mask大于0的地方，image的alpha通道为255，否则为0
    image[:,:,3] = voted_mask*255
    # image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)

    image = Image.fromarray(image)
    return voted_mask, image, sam_masks, yolo_masks


def replace_bg(src_img, bg_img):
    bg_img = bg_img.convert("RGBA")
    # 打开背景图片
    img_width, img_height = src_img.size
    bg_width, bg_height = bg_img.size
    
    # 计算宽高比
    img_ratio = img_width / img_height
    bg_ratio = bg_width / bg_height
    
    # 根据宽高比调整背景图的尺寸
    if img_ratio > bg_ratio:
        # 如果原图的宽高比大于背景图的宽高比，以宽度为准进行拉伸
        new_bg_width = img_width
        new_bg_height = int(new_bg_width / bg_ratio)
    else:
        # 如果原图的宽高比小于或等于背景图的宽高比，以高度为准进行拉伸
        new_bg_height = img_height
        new_bg_width = int(new_bg_height * bg_ratio)
    
    # 调整背景图片的尺寸
    bg_img = bg_img.resize((new_bg_width, new_bg_height))
    
    # 创建一个新的图片，将去除背景的图片粘贴到新的背景上
    # 计算粘贴位置，使前景图像居中
    paste_x = (new_bg_width - img_width) // 2
    paste_y = (new_bg_height - img_height) // 2
    new_image = Image.new("RGBA", (new_bg_width, new_bg_height))
    new_image.paste(bg_img, (0, 0), bg_img)
    new_image.paste(src_img, (paste_x, paste_y), src_img)
    
    return new_image


def get_mask(src_image, sam_model_path="./segany/sam_vit_h_4b8939.pth", yolo_model_path="./yolo/ver3.pt"):
    sam = sam_model_registry["vit_h"](checkpoint=sam_model_path)
    sam = sam.cuda()

    sam_model_generator = SamAutomaticMaskGenerator(sam,
                                                pred_iou_thresh=0.6,
                                                stability_score_thresh=0.8,
                                                crop_n_points_downscale_factor=1,
                                                crop_n_layers=1)
    yolo_model = YOLO(yolo_model_path)
    output_mask, output_image, sam_mask, yolo_mask = pipeline( sam_model_generator, yolo_model, src_image)
    return output_image