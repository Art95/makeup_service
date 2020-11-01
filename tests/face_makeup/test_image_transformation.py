import os
from makeup_service.face_makeup.image_transformation import *
from tests.helpers.utils import get_test_files_folder_path


def test_head_part_values():
    expected_hair_value = 17
    expected_upper_lip_value = 12
    expected_lower_lip_value = 13

    assert expected_hair_value == HeadPart.hair.value
    assert expected_upper_lip_value == HeadPart.upper_lip.value
    assert expected_lower_lip_value == HeadPart.lower_lip.value


def test_color_bgr_to_hsv():
    bgr_color = (128, 0, 128)

    expected_hsv_value = (150, 255, 128)
    actual_hsv_value = color_bgr_to_hsv(bgr_color)

    assert np.allclose(expected_hsv_value, actual_hsv_value)


def test_color_hsv_to_bgr():
    hsv_color = (150, 255, 128)

    expected_bgr_value = (128, 0, 128)
    actual_bgr_value = color_hsv_to_bgr(hsv_color)

    assert np.allclose(expected_bgr_value, actual_bgr_value)


def test_change_segment_color():
    image_path = os.path.join(get_test_files_folder_path(), 'test_image.jpg')
    image = cv2.imread(image_path)

    colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    head_parts = [HeadPart.hair, HeadPart.upper_lip, HeadPart.lower_lip]

    segmentation_path = os.path.join(get_test_files_folder_path(), 'segmentation.npy')
    segmentation = np.load(segmentation_path)

    expected_image = cv2.imread(os.path.join(get_test_files_folder_path(), 'expected_image.jpg'))

    actual_image = image.copy()

    for head_part, color in zip(head_parts, colors):
        actual_image = change_segment_color(actual_image, segmentation, head_part, color)

    assert np.allclose(expected_image, actual_image)

