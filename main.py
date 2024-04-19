from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import time
from sqlalchemy.exc import OperationalError
from routes import router

app = FastAPI()
app.include_router(router)

def retry_operation(operation, retries=5, delay=10):
    """Retry an operation with a delay between retries."""
    for attempt in range(retries):
        try:
            operation()
            print("Database is ready and tables are created.")
            break
        except OperationalError as e:
            if attempt < retries - 1:
                print(f"Database not ready, retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Database connection failed after several retries.")
                raise




if __name__ == "__main__":
    from database import engine
    from models import Base

    def init_db():
        Base.metadata.create_all(bind=engine)

    retry_operation(init_db)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
