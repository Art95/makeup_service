import cv2
import os
import numpy as np
from PIL import Image
from makeup_service.face_makeup.semantic_segmentation import SemanticSegmentation
from makeup_service.server.common import get_data_folder
from helpers.utils import get_test_files_folder_path


def test_get_segmentation():
    image_path = os.path.join(get_test_files_folder_path(), 'test_image.jpg')
    model_path = os.path.join(get_data_folder(), 'bisenet_model.pth')
    expected_segmentation_path = os.path.join(get_test_files_folder_path(), 'segmentation.npy')

    image = cv2.imread(image_path)
    width = image.shape[1]
    height = image.shape[0]
    dim = (width, height)

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    segmentation_model = SemanticSegmentation(model_path)
    actual_segmentation = segmentation_model.get_segmentation(img_pil)
    actual_segmentation = cv2.resize(actual_segmentation, dim, interpolation=cv2.INTER_NEAREST)

    expected_segmentation = np.load(expected_segmentation_path)

    assert np.allclose(expected_segmentation, actual_segmentation)



