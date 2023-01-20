import math

DELTA_INDEX = (
    0, 0.01, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.1, 0.11,
    0.12, 0.14, 0.15, 0.16, 0.17, 0.18, 0.20, 0.21, 0.22, 0.24,
    0.25, 0.27, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42,
    0.44, 0.46, 0.48, 0.5, 0.53, 0.56, 0.59, 0.62, 0.65, 0.68,
    0.71, 0.74, 0.77, 0.80, 0.83, 0.86, 0.89, 0.92, 0.95, 0.98,
    1.0, 1.06, 1.12, 1.18, 1.24, 1.30, 1.36, 1.42, 1.48, 1.54,
    1.60, 1.66, 1.72, 1.78, 1.84, 1.90, 1.96, 2.0, 2.12, 2.25,
    2.37, 2.50, 2.62, 2.75, 2.87, 3.0, 3.2, 3.4, 3.6, 3.8,
    4.0, 4.3, 4.7, 4.9, 5.0, 5.5, 6.0, 6.5, 6.8, 7.0,
    7.3, 7.5, 7.8, 8.0, 8.4, 8.7, 9.0, 9.4, 9.6, 9.8, 10.0)


def create_matrix_identity():
    return \
        (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0)


def adjust_hue(color_matrix, degrees):
    radians = degrees * math.pi / 180

    if radians == 0:
        return

    cos_val = math.cos(radians)
    sin_val = math.sin(radians)
    lum_r, lum_g, lum_b = 0.213, 0.715, 0.072
    matrix = (
        lum_r + cos_val * (1 - lum_r) + sin_val * (-lum_r), lum_g + cos_val * (-lum_g) +
        sin_val * (-lum_g), lum_b + cos_val *
        (-lum_b) + sin_val * (1 - lum_b), 0,
        lum_r + cos_val * (-lum_r) + sin_val * (0.143), lum_g + cos_val * (1 - lum_g) +
        sin_val * (0.140), lum_b + cos_val * (-lum_b) + sin_val * (-0.283), 0,
        lum_r + cos_val * (-lum_r) + sin_val * (-(1 - lum_r)), lum_g + cos_val * (-lum_g) + sin_val * (lum_g), lum_b + cos_val * (1 - lum_b) + sin_val * (lum_b), 0)
    return set_concat(a=color_matrix, b=matrix)


def adjust_contrast(color_matrix, value):
    contrast = int(limit_value(value, 100))
    if contrast == 0:
        return color_matrix

    if contrast < 0:
        x = 127 + contrast / 100 * 127
    else:
        x = DELTA_INDEX[contrast]
        x = x * 127 + 127

    l_matrix = \
        (x / 127, 0, 0, 0,
         0, x / 127, 0, 0,
         0, 0, x / 127, 0,
         0, 0, 0, 1)

    return set_concat(a=color_matrix, b=l_matrix)


def set_concat(a, b):
    idx = 0
    l_matrix = [None] * 12  # 3 x 4 = 12
    for j in range(0, 12, 4):
        for i in range(0, 4, 1):
            l_matrix[idx] = a[j + 0] * b[i + 0] + \
                a[j+1] * b[i+4] + a[j+2] * b[i+8]
            idx += 1

    return l_matrix


def limit_value(value, limit):
    return min(limit, max(-limit, value))
