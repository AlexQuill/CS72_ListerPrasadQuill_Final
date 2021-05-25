import requests
import lyricsgenius
import os
import json
from dotenv import load_dotenv
import pprint
from bs4 import BeautifulSoup


pp = pprint.PrettyPrinter(indent=4)
load_dotenv()


def clean(string):
    string = string.replace(u'\xa0', u' ')
    return string


def get_song_by_id(song_id):
    '''
    -response: {
        -song: {
        annotation_count: 71,
        api_path: "/songs/320",
        apple_music_id: "310908421",
        apple_music_player_url: "https://genius.com/songs/320/apple_music_player",
        +description: {...},
        embed_content: 
        featured_video: true,
        full_title: "Hit 'Em Up by 2Pac (Ft. Outlawz)",
        header_image_thumbnail_url: "https://images.genius.com/a6d7f93a83ec4f3dde28a749c01a6465.300x300x1.jpg",
        header_image_url: "https://images.genius.com/a6d7f93a83ec4f3dde28a749c01a6465.480x480x1.jpg",
        id: 320,
        lyrics_owner_id: 7,
        lyrics_placeholder_reason: null,
        lyrics_state: "complete",
        path: "/2pac-hit-em-up-lyrics",
        pyongs_count: 431,
        recording_location: "Can-Am Studios (Tarzana, CA)",
        release_date: "1996-06-04",
        release_date_for_display: "June 4, 1996",
        song_art_image_thumbnail_url: "https://images.genius.com/a6d7f93a83ec4f3dde28a749c01a6465.300x300x1.jpg",
        song_art_image_url: "https://images.genius.com/a6d7f93a83ec4f3dde28a749c01a6465.480x480x1.jpg",
        +stats: {...},
        title: "Hit ’Em Up",
        title_with_featured: "Hit 'Em Up (Ft. Outlawz)",
        url: "https://genius.com/2pac-hit-em-up-lyrics",
        +current_user_metadata: {...},
        song_art_primary_color: "#c48c24",
        song_art_secondary_color: "#825514",
        song_art_text_color: "#fff",
        +album: {...},
        +custom_performances: [...],
        +description_annotation: {...},
        +featured_artists: [...],
        lyrics_marked_complete_by: null,
        +media: [...],
        +primary_artist: {...},
        +producer_artists: [...],
        +song_relationships: [...],
        +verified_annotations_by: [...],
        +verified_contributors: [...],
        +verified_lyrics_by: [...],
        +writer_artists: [...]
        }
    }
    '''

    request_uri = 'https://api.genius.com/songs/'
    params = {'access_token': os.getenv('CLIENT_ACCESS_TOKEN')}
    r = requests.get(
        request_uri + song_id, headers={}, params=params)
    js_song = json.loads((r.text))

    return (js_song['response']['song'])


def get_artist_hits(artist_name, num=3):

    # search for song
    request_uri = 'https://api.genius.com/search/'

    user_input = artist_name.replace(" ", "-")

    params = {'q': user_input}
    headers = {'Authorization': 'Bearer {}'.format(
        os.getenv('CLIENT_ACCESS_TOKEN'))}

    r = requests.get(request_uri, params=params, headers=headers)
    js = json.loads((r.text))

    top_songs_js = []
    top_songs_lyrics = []
    for i in range(num):
        song_api_path = js['response']['hits'][i]['result']['api_path']
        song_id = song_api_path.split("/")[-1]
        song_js = get_song_by_id(song_id)
        top_songs_js.append(song_js)

        song_lyrics = get_lyrics_by_song_id(song_id)
        top_songs_lyrics.append(song_lyrics)

    return top_songs_js, top_songs_lyrics


def get_lyrics_by_song_id(song_id):
    song_url = "https://api.genius.com/songs/" + str(song_id)
    headers = {'Authorization': 'Bearer {}'.format(
        os.getenv('CLIENT_ACCESS_TOKEN'))}
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]

    # gotta go regular html scraping... come on Genius
    page_url = "https://genius.com" + path

    soup = BeautifulSoup(requests.get(page_url).content, 'lxml')

    for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
        t = tag.get_text(strip=True, separator='\n')
        if t:
            return t
        return None

    return None


song_objects, lyrics = get_artist_hits("2pac", 2)
for words in lyrics:
    for line in words.split('\n')[:10]:
        print(clean(line).replace("\"", ""))
    print('\n')
