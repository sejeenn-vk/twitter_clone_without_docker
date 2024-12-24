from fastapi import FastAPI
import uvicorn


main_app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:main_app")