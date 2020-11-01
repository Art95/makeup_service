import cv2
import numpy as np
from skimage.filters import gaussian
import enum


class HeadPart(enum.Enum):
    hair = 17
    upper_lip = 12
    lower_lip = 13


def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, multichannel=True)

    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255

    return np.array(img_out, dtype=np.uint8)


def color_bgr_to_hsv(color):
    pixel = np.zeros((1, 1, 3), np.uint8)
    pixel[0, 0, :] = color

    hsv_pixel = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)

    return hsv_pixel[0, 0]


def color_hsv_to_bgr(color):
    pixel = np.zeros((1, 1, 3), np.uint8)
    pixel[0, 0, :] = color

    bgr_pixel = cv2.cvtColor(pixel, cv2.COLOR_HSV2BGR)

    return bgr_pixel[0, 0]


def change_segment_color(image, segmentation, head_part, color):
    segment_indexes = np.where(segmentation == head_part.value)
    segment_pixels = list(zip(segment_indexes[0], segment_indexes[1]))

    new_hsv_color = color_bgr_to_hsv(color)

    for pixel_index in segment_pixels:
        orig_bgr_color = image[pixel_index[0], pixel_index[1]]
        hsv_color = color_bgr_to_hsv(orig_bgr_color)

        if head_part is HeadPart.upper_lip or head_part is HeadPart.lower_lip:
            hsv_color[0:2] = new_hsv_color[0:2]
        else:
            hsv_color[0:1] = new_hsv_color[0:1]

        image[pixel_index[0], pixel_index[1]] = color_hsv_to_bgr(hsv_color)

    if HeadPart.hair == head_part:
        sharpened_image = sharpen(image)
        sharpened_image[segmentation != HeadPart.hair.value] = image[segmentation != HeadPart.hair.value]

        return sharpened_image

    return image
