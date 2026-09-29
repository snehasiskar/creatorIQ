def calculate_engagement(likes: int, comments: int, shares: int, views: int):
    total_engagement = likes + comments + shares

    engagement_rate = (
        (total_engagement / views) * 100
        if views > 0
        else 0
    )

    return {
        "total_engagement": total_engagement,
        "engagement_rate": round(engagement_rate, 2)
    }
