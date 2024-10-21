import os
import json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Image(BaseModel):
    id: str
    name: str
    url: str


def load_pic_database(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File not found: {file_path}')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


image_database = load_pic_database('pic_database.json')


@app.get('/images/',
         response_model=List[Image],
         status_code=status.HTTP_200_OK)
async def search_images(name: str):

    matched_images = [img for img in image_database if name in img['name']]

    if not matched_images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No images found matching the query.')

    return matched_images


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
