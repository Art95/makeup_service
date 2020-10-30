import cv2
from PIL import Image
from makeup_service.face_makeup.test import evaluate
from makeup_service.face_makeup.utils import hair
import os


def get_project_root():
    from pathlib import Path
    return Path(__file__).parent.parent


# 1  face
# 11 teeth
# 12 upper lip
# 13 lower lip
# 17 hair

def apply_makeup(video_source, colors, flip=True):
    video_stream = cv2.VideoCapture(video_source)

    table = {
        'hair': 17,
        'upper_lip': 12,
        'lower_lip': 13
    }

    cp = os.path.join(get_project_root(), 'data/bisenet_model.pth')

    parts = [table['hair'], table['upper_lip'], table['lower_lip']]

    while True:
        ret, image = video_stream.read()

        if not ret:
            break

        if flip:
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

        if cv2.waitKey(1) == 27:
            break  # esc to quit

    video_stream.release()
    cv2.destroyAllWindows()
