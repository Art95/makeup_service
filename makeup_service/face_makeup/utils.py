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


def change_segment_color(image, segmentation, head_part, color):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if head_part is HeadPart.upper_lip or head_part is HeadPart.lower_lip:
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    else:
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    if head_part is HeadPart.hair:
        changed = sharpen(changed)

    changed[segmentation != head_part.value] = image[segmentation != head_part.value]
    return changed


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


def sharpen_my(pixel, pixel_gauss):
    alpha = 1.5
    pixel_out = (pixel - pixel_gauss) * alpha + pixel

    pixel_out = pixel_out / 255.0

    mask_1 = pixel_out < 0
    mask_2 = pixel_out > 1

    pixel_out = pixel_out * (1 - mask_1)
    pixel_out = pixel_out * (1 - mask_2) + mask_2
    pixel_out = np.clip(pixel_out, 0, 1)
    pixel_out = pixel_out * 255

    return pixel_out


def change_lip_color(image, segmentation, lip_type, color):
    segment_indexes = np.where(segmentation == lip_type.value)
    segment_pixels = list(zip(segment_indexes[0], segment_indexes[1]))
    new_hsv_color = color_bgr_to_hsv(color)

    for pixel_index in segment_pixels:
        orig_bgr_color = image[pixel_index[0], pixel_index[1]]
        hsv_color = color_bgr_to_hsv(orig_bgr_color)
        hsv_color[0:2] = new_hsv_color[0:2]

        image[pixel_index[0], pixel_index[1]] = color_hsv_to_bgr(hsv_color)

    return image


def change_hair_color(image, segmentation, color):
    segment_indexes = np.where(segmentation == HeadPart.hair.value)
    segment_pixels = list(zip(segment_indexes[0], segment_indexes[1]))
    new_hsv_color = color_bgr_to_hsv(color)

    for pixel_index in segment_pixels:
        orig_bgr_color = image[pixel_index[0], pixel_index[1]]
        hsv_color = color_bgr_to_hsv(orig_bgr_color)
        hsv_color[0:1] = new_hsv_color[0:1]

        image[pixel_index[0], pixel_index[1]] = color_hsv_to_bgr(hsv_color)

    sharpened_image = sharpen(image)
    sharpened_image[segmentation != HeadPart.hair] = image[segmentation != HeadPart.hair]

    return sharpened_image
