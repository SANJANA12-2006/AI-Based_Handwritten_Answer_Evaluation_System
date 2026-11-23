import os
import base64
import mimetypes

import requests

from dotenv import load_dotenv


load_dotenv()


OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)


def image_to_data_url(image_path):

    mime_type, _ = mimetypes.guess_type(
        image_path
    )

    if not mime_type:
        mime_type = "image/jpeg"

    with open(
        image_path,
        "rb"
    ) as image_file:

        image_data = image_file.read()

    encoded_image = base64.b64encode(
        image_data
    ).decode("utf-8")

    return (
        f"data:{mime_type};base64,"
        f"{encoded_image}"
    )


def extract_handwritten_text(image_path, prompt=None):

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    primary_model = os.getenv(
        "OPENROUTER_MODEL",
        "google/gemma-4-31b-it:free"
    )

    if not api_key:

        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured "
            "in the .env file."
        )


    image_url = image_to_data_url(
        image_path
    )


    default_prompt = """
You are an OCR system for a handwritten examination answer sheet.

Read the handwritten content in this image carefully.

Your task is ONLY to transcribe the student's handwritten answer.

Rules:

1. Preserve the student's wording as closely as possible.
2. Do not correct grammar.
3. Do not improve spelling.
4. Do not summarize.
5. Do not add information that is not visible.
6. Ignore decorative marks and page borders.
7. If a word is unclear, use [unclear].
8. Preserve paragraphs and line breaks where reasonably possible.
9. If question numbers are visible, preserve them.
10. Do not evaluate the answer.
11. Do not assign marks.
12. Return ONLY the extracted handwritten text.

This is an examination answer sheet.
Accuracy of transcription is more important than making
the text look polished.
"""

    prompt = prompt or default_prompt


    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json",

        "HTTP-Referer":
            "http://127.0.0.1:5000",

        "X-Title":
            "Handwritten Notes Evaluation"
    }


    # Primary + fallback models.
    #
    # The primary model is taken from .env.
    # Other models are used if the primary model
    # is temporarily unavailable.

    fallback_models = [

        primary_model,

        "google/gemini-2.5-flash-lite",

        "google/gemini-2.5-flash",

    ]


    # Remove duplicate models while preserving order

    models = []

    for model in fallback_models:

        if model not in models:
            models.append(model)


    payload = {

        "model": models[0],

        "models": models,

        "messages": [

            {
                "role": "user",

                "content": [

                    {
                        "type": "text",
                        "text": prompt
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": image_url
                        }

                    }

                ]

            }

        ],

        "temperature": 0.1,

        "max_tokens": 4000
    }


    response = requests.post(

        OPENROUTER_URL,

        headers=headers,

        json=payload,

        timeout=120

    )


    if response.status_code != 200:

        try:

            error_data = response.json()

        except Exception:

            error_data = response.text


        raise RuntimeError(

            f"OpenRouter OCR request failed "
            f"({response.status_code}): "
            f"{error_data}"

        )


    result = response.json()


    choices = result.get(
        "choices",
        []
    )


    if not choices:

        raise RuntimeError(
            "OpenRouter returned no OCR result."
        )


    message = choices[0].get(
        "message",
        {}
    )


    extracted_text = message.get(
        "content",
        ""
    )


    if not extracted_text:

        raise RuntimeError(
            "OCR model returned empty text."
        )


    return extracted_text.strip()