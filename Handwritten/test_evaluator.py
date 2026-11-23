from services.ai_evaluator import evaluate_answer


print()
print("=" * 60)
print("HANDWRITTEN NOTES AI EVALUATION TEST")
print("=" * 60)


key_answer = """
Java is a high-level, object-oriented programming language.
It is platform independent and follows the principle
of write once, run anywhere.
"""


student_answer = """
Java is an object oriented programming language.
It is platform independent and can run on different
operating systems using the JVM.
"""


result = evaluate_answer(
    student_answer,
    key_answer,
    5
)


print()
print("KEY ANSWER:")
print(key_answer)

print()
print("STUDENT ANSWER:")
print(student_answer)

print()
print("-" * 60)

print(
    "Semantic Score:",
    result["semantic_score"],
    "%"
)

print(
    "Keyword Score:",
    result["keyword_score"],
    "%"
)

print(
    "Text Match Score:",
    result["text_match_score"],
    "%"
)

print(
    "Final Percentage:",
    result["percentage"],
    "%"
)

print(
    "Marks:",
    result["marks"],
    "/ 5"
)

print(
    "Feedback:",
    result["feedback"]
)

print("=" * 60)