import requests
import aiohttp
from objects import Meme, User
from dotenv import load_dotenv
import os

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


async def get_all_memes_from_vesdekode() -> list[str]:
    data: list[Meme] = await get_photos_from_public(-197700721, 281940823)
    memes_str_data_list = [f'Автор - {meme.author.user_url}, Лайков - {meme.likes}, Ссылка на мем - {meme.url}' for meme in data]
    return memes_str_data_list


def task_1():
    memes: list[Meme] = get_all_memes_from_vesdekode()
    for meme in memes:
        print(f'Author link - {meme.author.user_url}, Likes: {meme.likes}, meme link: {meme.url}')


def main():
    task_1()


if __name__ == '__main__':
    main()
