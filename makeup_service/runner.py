from pathlib import Path
from PIL import Image
from makeup_service.face_makeup.semantic_segmentation import SemanticSegmentation
from makeup_service.face_makeup.image_transformation import *
import os


def get_data_folder():
    root_folder = Path(__file__).parent.parent
    data_folder = os.path.join(root_folder, 'data')

    return data_folder


def apply_makeup_on_image(image, segmentation_model, head_parts, colors):
    width = image.shape[1]
    height = image.shape[0]
    dim = (width, height)

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    segmentation = segmentation_model.get_segmentation(img_pil)
    segmentation = cv2.resize(segmentation, dim, interpolation=cv2.INTER_NEAREST)

    for head_part, color in zip(head_parts, colors):
        image = change_segment_color(image, segmentation, head_part, color)

    return image


def apply_makeup_on_video(video_stream, colors, save_to_file=False, out_file_path='transformed.avi', flip=True):
    out_stream = None

    model_path = os.path.join(get_data_folder(), 'bisenet_model.pth')
    segmentation_model = SemanticSegmentation(model_path)

    head_parts = [HeadPart.hair, HeadPart.upper_lip, HeadPart.lower_lip]

    if save_to_file:
        frame_width = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video_stream.get(cv2.CAP_PROP_FPS))

        out_stream = cv2.VideoWriter(out_file_path, cv2.VideoWriter_fourcc('M','J','P','G'), fps,
                                     (frame_width, frame_height))

    while True:
        ret, image = video_stream.read()

        if not ret:
            break

        if flip:
            image = cv2.flip(image, 1)

        processed_image = apply_makeup_on_image(image, segmentation_model, head_parts, colors)

        if not save_to_file:
            cv2.imshow('my webcam', processed_image)
        else:
            out_stream.write(processed_image)

        if cv2.waitKey(1) == 27:
            break  # esc to quit

    video_stream.release()

    if out_stream:
        out_stream.release()

    cv2.destroyAllWindows()


def run_on_video(video_source, colors, save_to_file=False, out_file_path='transformed.avi', flip=True):
    video_stream = cv2.VideoCapture(video_source)
    apply_makeup_on_video(video_stream, colors, save_to_file, out_file_path, flip)
