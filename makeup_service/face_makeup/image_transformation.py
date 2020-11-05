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
    r = color[2]
    g = color[1]
    b = color[0]

    r_t = r / 255.0
    g_t = g / 255.0
    b_t = b / 255.0

    c_max = max(r_t, g_t, b_t)
    c_min = min(r_t, g_t, b_t)

    delta = c_max - c_min

    h = calc_hue(r_t, g_t, b_t, delta, c_max)
    s = calc_saturation(delta, c_max)
    v = c_max

    return [h, s, v]


def calc_hue(r_t, g_t, b_t, delta, c_max):
    hue = None

    if delta == 0:
        hue = 0
    elif c_max == r_t:
        hue = 60 * (((g_t - b_t) / delta) % 6)
    elif c_max == g_t:
        hue = 60 * (((b_t - r_t) / delta) + 2)
    elif c_max == b_t:
        hue = 60 * (((r_t - g_t) / delta) + 4)

    return hue


def calc_saturation(delta, c_max):
    st = delta / c_max if c_max != 0 else 0.0
    return st


def color_hsv_to_bgr(color):
    h = color[0]
    s = color[1]
    v = color[2]

    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    r_t, g_t, b_t = None, None, None

    if 0 <= h < 60:
        r_t, g_t, b_t = c, x, 0
    elif 60 <= h < 120:
        r_t, g_t, b_t = x, c, 0
    elif 120 <= h < 180:
        r_t, g_t, b_t = 0, c, x
    elif 180 <= h < 240:
        r_t, g_t, b_t = 0, x, c
    elif 240 <= h < 300:
        r_t, g_t, b_t = x, 0, c
    elif 300 <= h < 360:
        r_t, g_t, b_t = c, 0, x

    r = round((r_t + m) * 255)
    g = round((g_t + m) * 255)
    b = round((b_t + m) * 255)

    return [int(b), int(g), int(r)]


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
