from core.imports import uvicorn
from config       import Config
from api          import API

config = Config()
api    = API()

if __name__ == "__main__":
    uvicorn.run("main:api.app", host=config.ip, port=config.port, reload=True)