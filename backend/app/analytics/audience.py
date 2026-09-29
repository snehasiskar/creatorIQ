def audience_report(
    followers: int,
    new_followers: int,
    returning_followers: int
):
    growth_rate = (
        (new_followers / followers) * 100
        if followers > 0
        else 0
    )

    return {
        "followers": followers,
        "new_followers": new_followers,
        "returning_followers": returning_followers,
        "growth_rate": round(growth_rate, 2)
    }
