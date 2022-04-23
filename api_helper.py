import pprint

import requests
import aiohttp
from objects import Meme, User
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = 'https://api.vk.com/method/'


async def get_photos_from_public(public_id: int, album_id: int) -> list[Meme]:
    if public_id > 0:
        public_id *= -1
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{BASE_URL}/photos.getAll?access_token={TOKEN}&v={5.131}&owner_id={public_id}&count={200}&extended=true') as response:
            data = await response.json()
            items = data['response']['items']
            photos = [item for item in items if item['album_id'] == album_id]
            memes: list[Meme] = list()
            for photo in photos:
                meme = Meme(url=photo['sizes'][-1]['url'], likes=photo['likes']['count'],
                            author=User(user_url=f'vk.com/id{photo["user_id"]}', user_last_name=None,
                                        user_first_name=None))
                memes.append(meme)
            return memes


async def get_all_memes_from_vesdekode() -> list[Meme]:
    data: list[Meme] = await get_photos_from_public(-197700721, 281940823)
    return data


async def get_meme_data_json() -> list[dict]:
    data = await get_all_memes_from_vesdekode()
    meme_json = [
        {'meme_num': index,
         'meme_author': meme.author.user_url,
         'meme_likes': meme.likes,
         'meme_url': meme.url}
        for index, meme in enumerate(data, start=1)
    ]
    return meme_json


async def task_1():
    memes: list[dict] = await get_meme_data_json()
    pprint.pprint(memes)


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(task_1())
    loop.close()


if __name__ == '__main__':
    main()
