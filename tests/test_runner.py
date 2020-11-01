import os
import cv2
import numpy as np
from makeup_service.runner import apply_makeup_on_image, get_data_folder
from makeup_service.face_makeup.semantic_segmentation import SemanticSegmentation
from makeup_service.face_makeup.image_transformation import HeadPart
from tests.helpers.utils import get_test_files_folder_path


def test_apply_makeup_on_image():
    image_path = os.path.join(get_test_files_folder_path(), 'test_image.jpg')
    model_path = os.path.join(get_data_folder(), 'bisenet_model.pth')
    expected_image_path = os.path.join(get_test_files_folder_path(), 'expected_image.jpg')

    image = cv2.imread(image_path)
    head_parts = [HeadPart.hair, HeadPart.upper_lip, HeadPart.lower_lip]
    colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

    segmentation_model = SemanticSegmentation(model_path)

    expected_image = cv2.imread(expected_image_path)
    actual_image = apply_makeup_on_image(image, segmentation_model, head_parts, colors)

    assert np.allclose(expected_image, actual_image)
