from fastapi import FastAPI
from app.server.router import router


class CulinaryServer:

    def start_server():
        server = FastAPI(title="Culinary Recipes API")
        server.include_router(router)
        return server
