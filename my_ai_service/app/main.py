from fastapi import FastAPI
from core.config import settings
from core.database import engine
from api.endpoints import authentication, job, credit  # Adjusted import path

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Include your routers here
app.include_router(authentication.router, prefix="/auth", tags=["authentication"])
app.include_router(job.router, prefix="/job", tags=["job"])
app.include_router(credit.router, prefix="/credit", tags=["credit"])

@app.get("/")
def read_root():
    return {"message": "Welcome to MyAIApp!"}

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
