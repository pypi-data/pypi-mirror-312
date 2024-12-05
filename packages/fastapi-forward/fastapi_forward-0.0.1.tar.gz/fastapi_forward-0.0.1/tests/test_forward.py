from fastapi import FastAPI
from fastapi_forward import forward, init_app
import uvicorn
from threading import Thread
import httpx
import time


def setup_app():
    """Create a fresh FastAPI app for testing."""

    def t():
        app = FastAPI()
        init_app(app)

        @app.get("/")
        @forward("http://127.0.0.1:10001")
        async def root():
            return {"message": "Hello World"}
        
        uvicorn.run(app, host="0.0.0.0", port=9999)

    def t2():
        app = FastAPI()

        @app.get("/")
        async def root():
            return {"message": "Hello FastAPI"}
        
        uvicorn.run(app, host="0.0.0.0", port=10001)

    thread = Thread(target=t)
    thread.daemon = True
    thread.start()

    thread2 = Thread(target=t2)
    thread2.daemon = True
    thread2.start()


def test_forward():
    """Test that the forward middleware correctly forwards requests."""
    setup_app()
    time.sleep(1)
    response = httpx.get("http://127.0.0.1:9999/")
    assert response.status_code == 200
    # The response should be from example.com, not our local endpoint
    assert response.json() == {"message": "Hello FastAPI"}
