import os
from makeup_service.face_makeup.image_transformation import *
from helpers.utils import get_test_files_folder_path


def test_head_part_values():
    expected_hair_value = 17
    expected_upper_lip_value = 12
    expected_lower_lip_value = 13

    assert expected_hair_value == HeadPart.hair.value
    assert expected_upper_lip_value == HeadPart.upper_lip.value
    assert expected_lower_lip_value == HeadPart.lower_lip.value


def test_change_segment_color():
    image_path = os.path.join(get_test_files_folder_path(), 'test_image.jpg')
    image = cv2.imread(image_path)

    segmentation_path = os.path.join(get_test_files_folder_path(), 'segmentation.npy')
    segmentation = np.load(segmentation_path)

    head_part = HeadPart.hair
    color = [255, 0, 0]

    res_image = change_segment_color(image, segmentation, head_part, color)

    assert res_image.shape == image.shape
