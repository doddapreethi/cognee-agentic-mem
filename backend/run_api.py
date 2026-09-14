import uvicorn

from app import config


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.BACKEND_PORT,
        reload=False,
        access_log=False,
    )
