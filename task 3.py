from dataclasses import dataclass


@dataclass
class Patient:
    patient_id: str
    consultation_charge: float
    diagnostic_charge: float
    treatment_charge: float
    concession_rate: float = 0.0
    concession_condition_met: bool = False
    amount_paid: float = 0.0


def process_bill(patient: Patient, payment_policy: dict) -> dict:
    # Validate the charges and payment details.
    if not patient.patient_id.strip():
        raise ValueError("Patient ID is required.")

    charges = [
        patient.consultation_charge,
        patient.diagnostic_charge,
        patient.treatment_charge,
        patient.amount_paid,
    ]
    if any(amount < 0 for amount in charges):
        raise ValueError("Charges and amount paid cannot be negative.")

    if not 0 <= patient.concession_rate <= 100:
        raise ValueError("Concession rate must be between 0 and 100.")

    gross_total = (
        patient.consultation_charge
        + patient.diagnostic_charge
        + patient.treatment_charge
    )

    # Apply the concession only when its condition is satisfied.
    concession = (
        gross_total * patient.concession_rate / 100
        if patient.concession_condition_met
        else 0.0
    )
    net_total = gross_total - concession

    if patient.amount_paid > net_total:
        raise ValueError("Amount paid cannot exceed the final bill.")

    balance = net_total - patient.amount_paid

    # Example policy thresholds; supply values that match your policy.
    full_payment_threshold = payment_policy["full_payment_threshold"]
    partial_payment_threshold = payment_policy["partial_payment_threshold"]

    if not 0 <= partial_payment_threshold <= full_payment_threshold <= 1:
        raise ValueError("Payment thresholds must be between 0 and 1.")

    payment_ratio = patient.amount_paid / net_total if net_total else 1.0

    if payment_ratio >= full_payment_threshold:
        classification = "Paid"
    elif payment_ratio >= partial_payment_threshold:
        classification = "Partially Paid"
    else:
        classification = "Unpaid"

    return {
        "patient_id": patient.patient_id,
        "consultation_charge": patient.consultation_charge,
        "diagnostic_charge": patient.diagnostic_charge,
        "treatment_charge": patient.treatment_charge,
        "gross_total": round(gross_total, 2),
        "concession": round(concession, 2),
        "net_total": round(net_total, 2),
        "amount_paid": round(patient.amount_paid, 2),
        "balance": round(balance, 2),
        "payment_ratio": round(payment_ratio, 4),
        "classification": classification,
    }


if __name__ == "__main__":
    patient = Patient(
        patient_id="P1001",
        consultation_charge=800,
        diagnostic_charge=1200,
        treatment_charge=5000,
        concession_rate=10,
        concession_condition_met=True,  # For example, eligible under hospital policy
        amount_paid=3500,
    )

    policy = {
        "full_payment_threshold": 1.0,     # 100% paid
        "partial_payment_threshold": 0.01, # At least 1% paid
    }

    bill = process_bill(patient, policy)

    for key, value in bill.items():
        print(f"{key.replace('_', ' ').title()}: {value}")