import cv2
import numpy as np


def apply_style(image_path, profile):
    """
    Apply a Style Mirror editing profile to an image.

    The profile values are expected to be approximately in the
    range -100 to +100.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not load image.")

    # Convert to float for safe processing
    image = image.astype(np.float32)

    # =========================================================
    # 1. LIGHTNESS
    # =========================================================

    lightness = float(profile.get("lightness", 0))

    # Keep the effect controlled
    lightness = np.clip(lightness, -100, 100)

    # Reduce the raw effect so large AI values don't destroy
    # the image.
    image += lightness * 0.45

    # =========================================================
    # 2. CONTRAST
    # =========================================================

    contrast = float(profile.get("contrast", 0))
    contrast = np.clip(contrast, -100, 100)

    # Convert -100..100 to a controlled contrast factor
    contrast_factor = 1.0 + (contrast / 100.0) * 0.65

    image = 128.0 + (image - 128.0) * contrast_factor

    # =========================================================
    # 3. WARMTH
    # =========================================================

    warmth = float(profile.get("warmth", 0))
    warmth = np.clip(warmth, -100, 100)

    # OpenCV uses BGR
    # Positive warmth = warmer image
    warmth_effect = warmth * 0.35

    image[:, :, 2] += warmth_effect
    image[:, :, 0] -= warmth_effect

    # =========================================================
    # 4. TINT
    # =========================================================

    tint = float(profile.get("tint", 0))
    tint = np.clip(tint, -100, 100)

    tint_effect = tint * 0.30

    # Positive tint adds green
    image[:, :, 1] += tint_effect

    # Slight magenta correction for negative tint
    if tint < 0:
        image[:, :, 2] += abs(tint_effect) * 0.35
        image[:, :, 0] += abs(tint_effect) * 0.35

    # =========================================================
    # 5. SATURATION
    # =========================================================

    saturation = float(profile.get("saturation", 0))
    saturation = np.clip(saturation, -100, 100)

    # First keep values in a valid image range
    image = np.clip(image, 0, 255).astype(np.uint8)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)

    saturation_factor = 1.0 + (saturation / 100.0) * 0.65

    hsv[:, :, 1] *= saturation_factor

    hsv[:, :, 1] = np.clip(
        hsv[:, :, 1],
        0,
        255
    )

    image = cv2.cvtColor(
        hsv.astype(np.uint8),
        cv2.COLOR_HSV2BGR
    ).astype(np.float32)

    # =========================================================
    # 6. HIGHLIGHTS
    # =========================================================

    highlight = float(profile.get("highlight", 0))
    highlight = np.clip(highlight, -100, 100)

    gray = cv2.cvtColor(
        np.clip(image, 0, 255).astype(np.uint8),
        cv2.COLOR_BGR2GRAY
    ).astype(np.float32)

    # Create a smooth highlight mask instead of a hard
    # "all pixels above 180" mask.
    highlight_mask = np.clip(
        (gray - 150.0) / 105.0,
        0.0,
        1.0
    )

    # Make the effect much safer than directly adding
    # the entire profile value.
    highlight_effect = highlight * 0.30

    image += (
        highlight_mask[:, :, np.newaxis]
        * highlight_effect
    )

    # =========================================================
    # 7. SHADOWS
    # =========================================================

    shadow = float(profile.get("shadow", 0))
    shadow = np.clip(shadow, -100, 100)

    # Smooth shadow mask
    shadow_mask = np.clip(
        (100.0 - gray) / 100.0,
        0.0,
        1.0
    )

    shadow_effect = shadow * 0.30

    image += (
        shadow_mask[:, :, np.newaxis]
        * shadow_effect
    )

    # =========================================================
    # 8. FINAL PROTECTION
    # =========================================================

    # Prevent pixels from becoming pure white or pure black
    # unnecessarily.
    image = np.clip(
        image,
        0,
        255
    )

    # Convert to uint8 for saving/displaying
    image = image.astype(np.uint8)

    return image


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    test_profile = {
        "lightness": 20,
        "contrast": 15,
        "warmth": 10,
        "tint": 0,
        "saturation": 10,
        "highlight": -10,
        "shadow": 10
    }

    input_image = (
        r"C:\Users\DELL\Downloads"
        r"\Butterfly Wallpaper Laptop Aesthetic.jpg"
    )

    output_image = apply_style(
        input_image,
        test_profile
    )

    output_path = "media/edited_butterfly.jpg"

    success = cv2.imwrite(
        output_path,
        output_image
    )

    if success:
        print("Style applied successfully!")
        print("Saved to:", output_path)
    else:
        print("Could not save the output image.")