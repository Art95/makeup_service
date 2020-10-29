import cv2
from PIL import Image
import numpy as np
from skimage.filters import gaussian
from test import evaluate


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


def hair(image, parsing, part, color):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part == 12 or part == 13:
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    else:
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    if part == 17:
        changed = sharpen(changed)

    changed[parsing != part] = image[parsing != part]
    return changed


def main():
    # 1  face
    # 11 teeth
    # 12 upper lip
    # 13 lower lip
    # 17 hair

    video_capture_device_index = 0
    webcam = cv2.VideoCapture(video_capture_device_index)

    table = {
        'hair': 17,
        'upper_lip': 12,
        'lower_lip': 13
    }

    cp = 'cp/79999_iter.pth'

    parts = [table['hair'], table['upper_lip'], table['lower_lip']]

    colors = [[230, 50, 20], [20, 70, 180], [20, 70, 180]]

    while True:
        ret, image = webcam.read()
        image = cv2.flip(image, 1)

        width = image.shape[1]
        height = image.shape[0]
        dim = (width, height)

        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)

        parsing = evaluate(img_pil, cp)
        parsing = cv2.resize(parsing, dim, interpolation=cv2.INTER_NEAREST)

        for part, color in zip(parts, colors):
            image = hair(image, parsing, part, color)

        cv2.imshow('my webcam', image)
        # cv2.imshow('color', cv2.resize(image, (512, 512)))

        if cv2.waitKey(1) == 27:
            break  # esc to quit

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
