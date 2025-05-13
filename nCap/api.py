from core.imports import FastAPI, CORSMiddleware
from core import tasks

class API:
    def __init__(self):
        self.app = FastAPI()
        self.add_middleware()
        self.include_routers()

    def add_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def include_routers(self):
        self.app.include_router(tasks.router, prefix="/api", tags=["Tasks"])

    def get_app(self):
        return self.app
