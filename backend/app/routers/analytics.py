from fastapi import APIRouter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/overview")
def analytics_overview():

    return {
        "views": 12500,
        "likes": 3200,
        "comments": 450,
        "shares": 280,
        "saves": 620,
        "watch_time": 5400,
        "reach": 9800,
        "engagement_rate": 46.43
    }