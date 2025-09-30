from typing import Union
from fastapi import FastAPI
from config.database import init_db, session
import uvicorn

app = FastAPI()

init_db()

@app.get("/")
def read_root():
    return {"Hello": "test"}


if __name__ == "__main__":
    uvicorn.run(app="main:app",port=8000, reload=True)