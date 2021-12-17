import requests
import json

api_key = '929f80543269e894e3a190fa4a615a8e'
request_token = '536239f01927014e1c3a42c48cdecfbbf25f1b4a'
guest_session_id = '1f2732cd17e643bcbea3213078392cd5'


def get_genre_list():
    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}'
    response = requests.get(url).text
    json_data = json.loads(response)['genres']

    genres = []
    for line in json_data:
        genres.append(line)

    return genres


def get_movies_by_genre(genre: str):
    genres = get_genre_list()
    genre_id = -1
    for line in genres:
        if line['name'].lower() == genre:
            genre_id = line['id']
            break
    if genre_id == -1:
        return json.dumps({'error': 'invalid genre'})

    url = f'https://api.themoviedb.org/3/discover/movie?' \
          f'api_key={api_key}&' \
          f'with_genres={genre_id}&sort_by=popularity.desc'
    response = requests.get(url).text
    json_data = json.loads(response)['results']

    data = {'movies': []}
    movie = {}
    for line in json_data:
        try:
            movie['title'] = line['title']
        except:
            movie['title'] = 'Invalid title'
        try:
            movie['popularity'] = line['popularity']
        except:
            movie['popularity'] = 'Invalid popularity value'
        try:
            movie['release_date'] = line['release_date']
        except:
            movie['release_date'] = 'Invalid release date'
        data['movies'].append(movie.copy())
        movie.clear()

    json_dump = json.dumps(data)
    return json_dump
