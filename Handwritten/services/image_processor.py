import os

from PIL import Image, ImageEnhance, ImageOps


def preprocess_image(
    input_path,
    output_path
):
    """
    Prepare a handwritten answer-sheet image
    before sending it to the OCR model.
    """

    image = Image.open(input_path)

    # Convert to RGB
    image = image.convert("RGB")

    # Correct camera orientation if possible
    image = ImageOps.exif_transpose(image)

    # Limit extremely large images
    max_width = 2000
    max_height = 3000

    image.thumbnail(
        (max_width, max_height),
        Image.Resampling.LANCZOS
    )

    # Slight contrast enhancement
    enhancer = ImageEnhance.Contrast(image)

    image = enhancer.enhance(1.15)

    # Slight sharpness enhancement
    sharpness = ImageEnhance.Sharpness(image)

    image = sharpness.enhance(1.2)

    # Ensure output directory exists
    output_directory = os.path.dirname(
        output_path
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    image.save(
        output_path,
        format="JPEG",
        quality=92,
        optimize=True
    )

    return output_path