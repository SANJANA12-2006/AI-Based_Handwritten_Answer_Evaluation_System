import re
from sentence_transformers import SentenceTransformer
from rapidfuzz import fuzz


_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


def clean_text(text):
    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_keywords(answer):
    text = clean_text(answer)

    words = text.split()

    stop_words = {
        "the",
        "is",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "on",
        "for",
        "with",
        "as",
        "by",
        "from",
        "that",
        "this",
        "are",
        "was",
        "were",
        "it",
        "be",
        "has",
        "have",
        "had"
    }

    keywords = [
        word
        for word in words
        if len(word) > 2
        and word not in stop_words
    ]

    return list(dict.fromkeys(keywords))


def calculate_semantic_similarity(
    student_answer,
    key_answer
):
    if not student_answer or not key_answer:
        return 0.0

    model = get_model()

    embeddings = model.encode(
        [
            student_answer,
            key_answer
        ]
    )

    from sklearn.metrics.pairwise import cosine_similarity

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    score = max(
        0.0,
        min(1.0, float(score))
    )

    return score


def calculate_keyword_score(
    student_answer,
    key_answer
):
    student_keywords = set(
        extract_keywords(student_answer)
    )

    key_keywords = set(
        extract_keywords(key_answer)
    )

    if not key_keywords:
        return 0.0

    matched = (
        student_keywords.intersection(
            key_keywords
        )
    )

    return len(matched) / len(key_keywords)


def calculate_text_match(
    student_answer,
    key_answer
):
    if not student_answer or not key_answer:
        return 0.0

    return (
        fuzz.token_set_ratio(
            clean_text(student_answer),
            clean_text(key_answer)
        ) / 100
    )


def evaluate_answer(
    student_answer,
    key_answer,
    max_marks
):
    if not student_answer:
        return {
            "marks": 0,
            "percentage": 0,
            "semantic_score": 0,
            "keyword_score": 0,
            "text_match_score": 0,
            "feedback": "No answer was detected."
        }

    if not key_answer:
        return {
            "marks": 0,
            "percentage": 0,
            "semantic_score": 0,
            "keyword_score": 0,
            "text_match_score": 0,
            "feedback": "Key answer is not available."
        }

    semantic_score = calculate_semantic_similarity(
        student_answer,
        key_answer
    )

    keyword_score = calculate_keyword_score(
        student_answer,
        key_answer
    )

    text_match_score = calculate_text_match(
        student_answer,
        key_answer
    )

    final_score = (
        semantic_score * 0.60
        +
        keyword_score * 0.25
        +
        text_match_score * 0.15
    )

    marks = final_score * max_marks

    marks = round(
        marks,
        2
    )

    percentage = round(
        final_score * 100,
        2
    )

    if percentage >= 85:

        feedback = (
            "Excellent answer. "
            "The response closely matches "
            "the expected answer."
        )

    elif percentage >= 70:

        feedback = (
            "Good answer. "
            "Most important concepts "
            "are covered."
        )

    elif percentage >= 50:

        feedback = (
            "Average answer. "
            "Some important concepts "
            "are missing."
        )

    elif percentage >= 30:

        feedback = (
            "Weak answer. "
            "The response contains limited "
            "relevant information."
        )

    else:

        feedback = (
            "Poor answer. "
            "The response does not sufficiently "
            "match the expected answer."
        )

    return {
        "marks": marks,
        "percentage": percentage,
        "semantic_score": round(
            semantic_score * 100,
            2
        ),
        "keyword_score": round(
            keyword_score * 100,
            2
        ),
        "text_match_score": round(
            text_match_score * 100,
            2
        ),
        "feedback": feedback
    }