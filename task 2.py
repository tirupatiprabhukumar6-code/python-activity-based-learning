from dataclasses import dataclass


@dataclass
class MonthUsage:
    month: str
    units: float


# Example tariff settings; replace them with your provider's rates.
SLABS = [
    (100, 0.10),   # First 100 units at 0.10 per unit
    (200, 0.15),   # Next 200 units at 0.15 per unit
    (float("inf"), 0.25),  # Remaining units at 0.25 per unit
]
FIXED_CHARGE = 20.00
SURCHARGE_RATE = 5.0  # Percent
REBATE_RATE = 2.0     # Percent
UNUSUAL_INCREASE_RATE = 25.0  # Percent compared with previous month


def calculate_slab_charge(units: float) -> float:
    if units < 0:
        raise ValueError("Units consumed cannot be negative.")

    charge = 0.0
    previous_limit = 0.0
    remaining_units = units

    for limit, rate in SLABS:
        slab_units = min(remaining_units, limit - previous_limit)
        charge += slab_units * rate
        remaining_units -= slab_units
        previous_limit = limit

        if remaining_units <= 0:
            break

    return charge


def calculate_bill(units: float) -> dict:
    energy_charge = calculate_slab_charge(units)
    subtotal = energy_charge + FIXED_CHARGE
    surcharge = subtotal * SURCHARGE_RATE / 100
    rebate = subtotal * REBATE_RATE / 100
    total = subtotal + surcharge - rebate

    return {
        "units": units,
        "energy_charge": round(energy_charge, 2),
        "fixed_charge": round(FIXED_CHARGE, 2),
        "surcharge": round(surcharge, 2),
        "rebate": round(rebate, 2),
        "total": round(total, 2),
    }


def compare_months(months: list[MonthUsage]) -> list[dict]:
    results = []
    previous_bill = None

    for usage in months:
        bill = calculate_bill(usage.units)
        increase_percent = None
        unusual_increase = False

        if previous_bill is not None:
            increase = bill["total"] - previous_bill
            increase_percent = (
                (increase / previous_bill) * 100 if previous_bill else None
            )
            unusual_increase = (
                increase_percent is not None
                and increase_percent >= UNUSUAL_INCREASE_RATE
            )

        results.append({
            "month": usage.month,
            **bill,
            "increase_percent": (
                round(increase_percent, 2)
                if increase_percent is not None else None
            ),
            "unusual_increase": unusual_increase,
        })
        previous_bill = bill["total"]

    return results


if __name__ == "__main__":
    monthly_usage = [
        MonthUsage("January", 120),
        MonthUsage("February", 145),
        MonthUsage("March", 220),
        MonthUsage("April", 400),
    ]

    for result in compare_months(monthly_usage):
        increase = result["increase_percent"]
        increase_text = (
            f'{increase:.2f}%' if increase is not None else "N/A"
        )
        alert = " — UNUSUAL INCREASE" if result["unusual_increase"] else ""

        print(
            f'{result["month"]}: {result["units"]} units, '
            f'bill={result["total"]:.2f}, '
            f'monthly increase={increase_text}{alert}'
        )