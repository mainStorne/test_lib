import uvicorn
from web.app.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", log_level="info")
