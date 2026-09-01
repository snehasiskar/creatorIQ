from fastapi import FastAPI
app=FastAPI(title="Creator Analytics Dashboard API",version="1.0.0")
@app.get("/")
def root():
    return{
        "message": "CreatorIQ API Running"
    }
    @app.get("/health")
    def health():
        return{
            "status":"healthy"
        }            