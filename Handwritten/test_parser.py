from services.answer_parser import parse_answers


def test_numbered_handwritten_ocr():
    ocr_text = """
    1 what in Java?
    → Java is a interpreted programming Language.

    24 Expand oop?
    → Object Oriented programming

    34 what is Inheritance?
    → Inheritance is a process of accessing elements
    of one class to another class.
    """

    expected_numbers = [1, 2, 3]
    answers = parse_answers(ocr_text, expected_numbers=expected_numbers)

    assert answers[1].startswith("Java")
    assert answers[2].startswith("Object")
    assert answers[3].startswith("Inheritance")


def test_single_question_without_numbering():
    ocr_text = "Computer Networks"
    answers = parse_answers(ocr_text, expected_numbers=[1])

    assert answers == {1: "Computer Networks"}


if __name__ == "__main__":
    test_numbered_handwritten_ocr()
    test_single_question_without_numbering()
    print("parser regression tests passed")