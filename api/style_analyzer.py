import cv2
import numpy as np


def analyze_image(image_path):
    """
    Analyze a reference image and extract
    useful aesthetic editing parameters.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read the image.")

    # Convert BGR to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Convert to LAB
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # --------------------------------------------------
    # 1. LIGHTNESS
    # --------------------------------------------------

    brightness = np.mean(lab[:, :, 0])

    lightness = round(float((brightness - 128) * 0.8), 2)

    # --------------------------------------------------
    # 2. CONTRAST
    # --------------------------------------------------

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    contrast_std = np.std(gray)

    contrast = round(float(contrast_std), 2)

    # --------------------------------------------------
    # 3. SATURATION
    # --------------------------------------------------

    saturation_mean = np.mean(hsv[:, :, 1])

    saturation = round(
        float((saturation_mean - 127) * 0.8),
        2
    )

    # --------------------------------------------------
    # 4. WARMTH
    # --------------------------------------------------

    red_mean = np.mean(rgb[:, :, 0])
    blue_mean = np.mean(rgb[:, :, 2])

    warmth = round(
        float((red_mean - blue_mean) * 0.5),
        2
    )

    # --------------------------------------------------
    # 5. HIGHLIGHTS
    # --------------------------------------------------

    bright_pixels = gray > 200

    if np.any(bright_pixels):
        highlight_value = np.mean(gray[bright_pixels])
    else:
        highlight_value = 0

    highlight = round(
        float((highlight_value - 128) * 0.8),
        2
    )

    # --------------------------------------------------
    # 6. SHADOWS
    # --------------------------------------------------

    dark_pixels = gray < 80

    if np.any(dark_pixels):
        shadow_value = np.mean(gray[dark_pixels])
    else:
        shadow_value = 0

    shadow = round(
        float((128 - shadow_value) * 0.8),
        2
    )

    # --------------------------------------------------
    # 7. HUE
    # --------------------------------------------------

    hue_mean = np.mean(hsv[:, :, 0])

    hue = round(
        float((hue_mean - 90) * 0.5),
        2
    )

    # --------------------------------------------------
    # 8. SHARPNESS
    # --------------------------------------------------

    sharpness_value = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    # Convert to a simple 0-100 style value
    sharpen = min(
        round(float(sharpness_value / 100), 2),
        100
    )

    # --------------------------------------------------
    # 9. COLOR PALETTE
    # --------------------------------------------------

    small_image = cv2.resize(
        rgb,
        (100, 100)
    )

    pixels = small_image.reshape(-1, 3).astype(
        np.float32
    )

    criteria = (
        cv2.TERM_CRITERIA_EPS
        + cv2.TERM_CRITERIA_MAX_ITER,
        20,
        1.0
    )

    number_of_colors = 5

    _, labels, centers = cv2.kmeans(
        pixels,
        number_of_colors,
        None,
        criteria,
        10,
        cv2.KMEANS_PP_CENTERS
    )

    centers = np.uint8(centers)

    color_palette = []

    for color in centers:
        color_palette.append({
            "r": int(color[0]),
            "g": int(color[1]),
            "b": int(color[2])
        })

    # --------------------------------------------------
    # 10. HSL-LIKE INFORMATION
    # --------------------------------------------------

    hsl = {
        "dominant_hue": round(float(hue_mean), 2),
        "average_saturation": round(
            float(saturation_mean),
            2
        ),
        "average_brightness": round(
            float(brightness),
            2
        ),
        "palette": color_palette
    }

    # --------------------------------------------------
    # 11. CURVE
    # --------------------------------------------------

    curve = {
        "points": [
            [0, 0],
            [64, 64],
            [128, 128],
            [192, 192],
            [255, 255]
        ]
    }

    # --------------------------------------------------
    # 12. OTHER EFFECTS
    # --------------------------------------------------

    fade = 0
    tint = 0
    color = 0
    vignette = 0
    grain = 0

    # --------------------------------------------------
    # FINAL STYLE PROFILE
    # --------------------------------------------------

    style = {
        "lightness": lightness,
        "contrast": contrast,
        "warmth": warmth,
        "tint": tint,
        "saturation": saturation,
        "curve": curve,
        "hsl": hsl,
        "fade": fade,
        "highlight": highlight,
        "shadow": shadow,
        "color": color,
        "hue": hue,
        "vignette": vignette,
        "sharpen": sharpen,
        "grain": grain
    }

    return style