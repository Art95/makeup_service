from makeup_service.face_makeup.image_transformation import *


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


