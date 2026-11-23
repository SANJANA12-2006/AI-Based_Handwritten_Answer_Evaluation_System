from services.ocr_service import extract_handwritten_text


IMAGE_PATH = r"F:\PFS Projects\Handwritten\uploads\answer_sheets\submission_1_3a512f4b90944abf8930b32077801894.jpeg"


try:

    print()
    print("=" * 60)
    print("HANDWRITTEN OCR TEST")
    print("=" * 60)
    print()

    print("Image:")
    print(IMAGE_PATH)

    print()
    print("Sending image to OpenRouter...")
    print()

    text = extract_handwritten_text(
        IMAGE_PATH
    )

    print()
    print("=" * 60)
    print("EXTRACTED TEXT")
    print("=" * 60)
    print()

    print(text)

    print()
    print("=" * 60)
    print("OCR TEST COMPLETED")
    print("=" * 60)

except Exception as error:

    print()
    print("=" * 60)
    print("OCR ERROR")
    print("=" * 60)
    print()

    print(error)