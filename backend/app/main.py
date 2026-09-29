from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.analytics import router as analytics_router
from app.routers.revenue import router as revenue_router

# Authentication router
from app.routers.auth import router as auth_router


app = FastAPI(
    title="CreatorIQ API",
    description="Creator Analytics and Revenue Analytics API",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(analytics_router)
app.include_router(revenue_router)
app.include_router(auth_router)


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "CreatorIQ API is running"
    }
