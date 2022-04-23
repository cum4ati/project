from fastapi import FastAPI
import json
import api_helper

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/task_1')
async def task_1():
    memes = await api_helper.get_meme_data_json()
    print(memes)
    return {
        "data": memes
    }