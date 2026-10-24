from dataclasses import dataclass


@dataclass
class Applicant:
    name: str
    aggregate_marks: float       # Percentage or aggregate score
    subject_scores: dict[str, float]
    attendance_percent: float
    annual_income: float


# Example eligibility rules and tie-break order.
# Replace these values with the university's actual policy.
MIN_AGGREGATE = 75
MIN_SUBJECT_SCORE = 60
MIN_ATTENDANCE = 85
MAX_ANNUAL_INCOME = 300_000


def evaluate_applicant(applicant: Applicant) -> tuple[bool, str]:
    if applicant.aggregate_marks < MIN_AGGREGATE:
        return False, "Aggregate marks below minimum"

    if not applicant.subject_scores:
        return False, "No subject scores provided"

    if any(score < MIN_SUBJECT_SCORE for score in applicant.subject_scores.values()):
        return False, "Subject score below minimum"

    if applicant.attendance_percent < MIN_ATTENDANCE:
        return False, "Attendance below minimum"

    if applicant.annual_income > MAX_ANNUAL_INCOME:
        return False, "Income exceeds limit"

    return True, "Eligible"


def allocate_scholarships(applicants: list[Applicant]) -> list[dict]:
    eligible = []
    results = []

    for applicant in applicants:
        is_eligible, reason = evaluate_applicant(applicant)

        if is_eligible:
            eligible.append(applicant)
        else:
            results.append({
                "name": applicant.name,
                "status": "Ineligible",
                "reason": reason,
                "rank": None,
            })

    # Ranking and tie-breakers:
    # 1. Higher aggregate marks
    # 2. Higher attendance
    # 3. Lower annual income
    # 4. Alphabetical name
    eligible.sort(
        key=lambda a: (
            -a.aggregate_marks,
            -a.attendance_percent,
            a.annual_income,
            a.name.casefold(),
        )
    )

    for rank, applicant in enumerate(eligible, start=1):
        results.append({
            "name": applicant.name,
            "status": "Eligible",
            "reason": "Meets all criteria",
            "rank": rank,
            "aggregate_marks": applicant.aggregate_marks,
            "attendance_percent": applicant.attendance_percent,
            "annual_income": applicant.annual_income,
        })

    return results


if __name__ == "__main__":
    applicants = [
        Applicant(
            name="Asha",
            aggregate_marks=91,
            subject_scores={"Math": 88, "Science": 90, "English": 82},
            attendance_percent=95,
            annual_income=240_000,
        ),
        Applicant(
            name="Ravi",
            aggregate_marks=91,
            subject_scores={"Math": 85, "Science": 87, "English": 80},
            attendance_percent=92,
            annual_income=180_000,
        ),
        Applicant(
            name="Mina",
            aggregate_marks=72,
            subject_scores={"Math": 80, "Science": 75, "English": 78},
            attendance_percent=90,
            annual_income=100_000,
        ),
    ]

    for result in allocate_scholarships(applicants):
        if result["status"] == "Eligible":
            print(
                f'Rank {result["rank"]}: {result["name"]} '
                f'(aggregate={result["aggregate_marks"]}, '
                f'attendance={result["attendance_percent"]}%, '
                f'income={result["annual_income"]})'
            )
        else:
            print(f'{result["name"]}: Ineligible — {result["reason"]}')