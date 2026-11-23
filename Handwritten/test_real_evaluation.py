from app import create_app

from services.evaluation_engine import evaluate_submission


app = create_app()


with app.app_context():

    submission_id = 2

    print()
    print("=" * 70)
    print("REAL SUBMISSION AI EVALUATION")
    print("=" * 70)

    try:

        result = evaluate_submission(
            submission_id
        )

        print()
        print(
            "Submission ID:",
            result["submission_id"]
        )

        print(
            "Total Marks:",
            result["total_marks"],
            "/",
            result["max_marks"]
        )

        print(
            "Percentage:",
            result["percentage"],
            "%"
        )

        print()
        print("-" * 70)

        for evaluation in result["evaluations"]:

            print()

            print(
                "Question:",
                evaluation["question_number"]
            )

            print(
                "Marks:",
                evaluation["marks"],
                "/",
                evaluation["max_marks"]
            )

            print(
                "Semantic:",
                evaluation["semantic_score"],
                "%"
            )

            print(
                "Keywords:",
                evaluation["keyword_score"],
                "%"
            )

            print(
                "Text Match:",
                evaluation["text_match_score"],
                "%"
            )

            print(
                "Feedback:",
                evaluation["feedback"]
            )

            print("-" * 70)

        print()
        print(
            "EVALUATION COMPLETED SUCCESSFULLY!"
        )

    except Exception as error:

        print()
        print(
            "EVALUATION FAILED!"
        )

        print()
        print(
            type(error).__name__,
            ":",
            error
        )

    print()
    print("=" * 70)