def calculate_engagement_rate(
    likes,
    comments,
    shares,
    saves,
    reach
):
    if reach == 0:
        return 0

    total_engagement = (
        likes +
        comments +
        shares +
        saves
    )

    return round(
        (total_engagement / reach) * 100,
        2
    )