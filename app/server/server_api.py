from fastapi import FastAPI
from app.server.router import router


class CulinaryServer:

    def start_server() -> FastAPI:
        server = FastAPI(title="Culinary Recipes API")
        server.include_router(router)
        return server
