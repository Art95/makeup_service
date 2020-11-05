from makeup_service.face_makeup.image_transformation import *


def test_head_part_values():
    expected_hair_value = 17
    expected_upper_lip_value = 12
    expected_lower_lip_value = 13

    assert expected_hair_value == HeadPart.hair.value
    assert expected_upper_lip_value == HeadPart.upper_lip.value
    assert expected_lower_lip_value == HeadPart.lower_lip.value


def test_color_bgr_to_hsv():
    bgr_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0), (255, 255, 255), (128, 128, 128), (35, 110, 95)]

    expected_hsv_values = [(0, 1.0, 1.0), (120, 1.0, 1.0), (240, 1.0, 1.0), (0, 0.0, 0.0), (0, 0.0, 1.0),
                           (0, 0.0, 0.502), (72, 0.682, 0.431)]

    for i, bgr in enumerate(bgr_colors):
        actual_hsv_value = color_bgr_to_hsv(bgr)
        assert np.allclose(expected_hsv_values[i], actual_hsv_value, atol=0.001)


def test_color_hsv_to_bgr():
    hsv_values = [(0, 1.0, 1.0), (120, 1.0, 1.0), (240, 1.0, 1.0), (0, 0.0, 0.0), (0, 0.0, 1.0),
                  (0, 0.0, 0.502), (72, 0.682, 0.431)]

    expected_bgr_values = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0), (255, 255, 255), (128, 128, 128),
                           (35, 110, 95)]

    for i, hsv in enumerate(hsv_values):
        actual_bgr_value = color_hsv_to_bgr(hsv)
        assert np.allclose(expected_bgr_values[i], actual_bgr_value)
