import cv2
import os
from makeup_service.server.face_makeup_facade import FaceMakeupFacade
from helpers.utils import get_test_files_folder_path


def test_apply_makeup_on_image():
    image_path = os.path.join(get_test_files_folder_path(), 'test_image.jpg')
    image = cv2.imread(image_path)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    face_makeup = FaceMakeupFacade()
    actual_image = face_makeup.apply_makeup_on_image(image, colors)

    assert actual_image is not None
