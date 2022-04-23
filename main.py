import requests
from pprint import pprint
from objects import Meme, User

TOKEN = '34b6b66ed69aa8cd8e145f825b8a3269d870d5118d5a1140d1da390ca86c63c633cedfac465d9c535c2c1'
BASE_URL = 'https://api.vk.com/method/'


def get_photos_from_public(public_id: int, album_id: int) -> list[Meme]:
    if public_id > 0:
        public_id *= -1

    r = requests.get(
        f'{BASE_URL}/photos.getAll?access_token={TOKEN}&v={5.131}&owner_id={public_id}&count={200}&extended=true')
    data = r.json()
    items = data['response']['items']
    photos = [item for item in items if item['album_id'] == album_id]
    memes: list[Meme] = list()
    for photo in photos:
        meme = Meme(url=photo['sizes'][-1]['url'], likes=photo['likes']['count'],
                    author=User(user_url=f'vk.com/id{photo["user_id"]}', user_last_name=None, user_first_name=None))
        memes.append(meme)
    return memes


def get_all_memes_from_vesdekode():
    return get_photos_from_public(-197700721, 281940823)


def task_1():
    memes: list[Meme] = get_all_memes_from_vesdekode()
    for meme in memes:
        print(f'Author link - {meme.author.user_url}, Likes: {meme.likes}, meme link: {meme.url}')


def main():
    task_1()

if __name__ == '__main__':
    main()