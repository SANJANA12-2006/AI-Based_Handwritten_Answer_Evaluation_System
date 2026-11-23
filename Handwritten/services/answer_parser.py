import re


def normalize_text(text):
    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text.strip()


def detect_question_number(raw_number, expected_numbers=None):
    """
    OCR sometimes merges question numbers with text.

    Example:
        24 Expand oop?
        34 what is inheritance?

    If expected question numbers are:
        [1, 2, 3]

    then:
        24 -> 2
        34 -> 3
    """

    try:
        number = int(raw_number)
    except (ValueError, TypeError):
        return None

    if expected_numbers:

        if number in expected_numbers:
            return number

        number_text = str(number)

        for digit in number_text:

            digit_number = int(digit)

            if digit_number in expected_numbers:
                return digit_number

    return number


def extract_arrow_answer(block):
    """
    Extract the actual answer when OCR contains:

    Question text
    → Answer text
    """

    if not block:
        return ""

    arrow_patterns = [
        "→",
        "->",
        "=>",
        "➜",
        "➔",
        "➤"
    ]

    positions = []

    for arrow in arrow_patterns:

        position = block.find(arrow)

        if position != -1:
            positions.append(position)

    if positions:

        position = min(positions)

        answer = block[
            position + 1:
        ]

        # Handle multi-character arrows
        answer = re.sub(
            r"^[>\-=\s]+",
            "",
            answer
        )

        return answer.strip()

    return block.strip()


def parse_numbered_blocks(
    text,
    expected_numbers=None
):
    """
    Handles handwritten OCR formats such as:

    1 what is Java?
    → Java is an object oriented language.

    24 Expand oop?
    → Object oriented programming.

    34 what is inheritance?
    → Inheritance is a process...
    """

    text = normalize_text(text)

    if not text:
        return {}

    lines = text.split("\n")

    blocks = []

    current_number = None
    current_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        match = re.match(
            r"^(\d+)\s*(?:[\.\):\-]\s*)?(.*)$",
            line
        )

        if match:

            raw_number = match.group(1)

            remainder = match.group(2).strip()

            question_number = detect_question_number(
                raw_number,
                expected_numbers
            )

            if (
                expected_numbers
                and question_number not in expected_numbers
            ):
                continue

            if current_number is not None:

                blocks.append(
                    (
                        current_number,
                        current_lines
                    )
                )

            current_number = question_number

            current_lines = []

            if remainder:
                current_lines.append(
                    remainder
                )

        else:

            if current_number is not None:
                current_lines.append(line)

    if current_number is not None:

        blocks.append(
            (
                current_number,
                current_lines
            )
        )

    answers = {}

    for question_number, lines in blocks:

        block_text = "\n".join(lines).strip()

        if not block_text:
            continue

        answer = extract_arrow_answer(
            block_text
        )

        if answer:

            answers[question_number] = answer

    return answers


def parse_clean_numbered_answers(
    text,
    expected_numbers=None
):
    """
    Handles clean formats such as:

    1. Java is...
    2. Inheritance is...
    3. Polymorphism is...
    """

    text = normalize_text(text)

    if not text:
        return {}

    pattern = re.compile(
        r"(?:^|\n)\s*"
        r"(\d+)"
        r"\s*[\.\):\-]\s*"
        r"(.*?)(?="
        r"\n\s*\d+\s*[\.\):\-]"
        r"|\Z)",
        re.DOTALL
    )

    matches = pattern.findall(text)

    answers = {}

    for raw_number, answer in matches:

        question_number = detect_question_number(
            raw_number,
            expected_numbers
        )

        if (
            expected_numbers
            and question_number not in expected_numbers
        ):
            continue

        answer = answer.strip()

        if answer:

            answers[question_number] = (
                extract_arrow_answer(answer)
            )

    return answers


def parse_single_question_answer(
    text,
    expected_numbers=None
):
    """
    Fallback for tests where the answer sheet contains only
    one question and the OCR text has no visible numbering.

    Example:
        "Computer Networks"
        expected_numbers=[1]

    should resolve to:
        {1: "Computer Networks"}
    """

    text = normalize_text(text)

    if not text or not expected_numbers:
        return {}

    if len(expected_numbers) != 1:
        return {}

    answer = extract_arrow_answer(text)

    if not answer:
        return {}

    return {
        expected_numbers[0]: answer
    }


def parse_answers(
    text,
    expected_numbers=None
):
    """
    Main OCR answer parser.

    Supports:

    1. Clean numbered answers
    2. Handwritten OCR question + arrow answer
    3. OCR merged question numbers
    4. Single-question unnumbered answer sheets
    """

    answers = parse_numbered_blocks(
        text,
        expected_numbers
    )

    if answers:
        return answers

    answers = parse_clean_numbered_answers(
        text,
        expected_numbers
    )

    if answers:
        return answers

    answers = parse_single_question_answer(
        text,
        expected_numbers
    )

    if answers:
        return answers

    return {}