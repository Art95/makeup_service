from PIL import Image
from makeup_service.face_makeup.semantic_segmentation import SemanticSegmentation
from makeup_service.face_makeup.image_transformation import *
from makeup_service.server.common import get_data_folder
import os


class FaceMakeupFacade:
    def __init__(self):
        model_path = os.path.join(get_data_folder(), 'bisenet_model.pth')
        self.__segmentation_model = SemanticSegmentation(model_path)

        self.__head_parts = [HeadPart.hair, HeadPart.upper_lip, HeadPart.lower_lip]

    def apply_makeup_on_image(self, image, colors):
        width = image.shape[1]
        height = image.shape[0]
        dim = (width, height)

        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)

        segmentation = self.__segmentation_model.get_segmentation(img_pil)
        segmentation = cv2.resize(segmentation, dim, interpolation=cv2.INTER_NEAREST)

        for head_part, color in zip(self.__head_parts, colors):
            image = change_segment_color(image, segmentation, head_part, color)

        return image

    def apply_makeup_on_video(self, video_source, colors, save_to_file=False, out_file_path='transformed.avi',
                              flip=True):
        video_stream = cv2.VideoCapture(video_source)
        out_stream = None

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

            processed_image = self.apply_makeup_on_image(image, colors)

            if not save_to_file:
                cv2.imshow('Makeup', processed_image)
            else:
                out_stream.write(processed_image)

            if cv2.waitKey(1) == 27:
                break  # esc to quit

        video_stream.release()

        if out_stream:
            out_stream.release()

        cv2.destroyAllWindows()
