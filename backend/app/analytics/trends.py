def calculate_growth(numbers):
    if not numbers:
        return {
            "data": [],
            "growth": 0,
            "growth_rate": 0
        }

    if len(numbers) < 2:
        return {
            "data": numbers,
            "growth": 0,
            "growth_rate": 0
        }

    growth = numbers[-1] - numbers[0]

    growth_rate = (
        (growth / numbers[0]) * 100
        if numbers[0] != 0
        else 0
    )

    return {
        "data": numbers,
        "growth": growth,
        "growth_rate": round(growth_rate, 2)
    }
