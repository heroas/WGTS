from services import requestor
import Global
from async_gui.toolkits.kivy import KivyEngine

engine = KivyEngine()
ANI_LIST_URL = 'https://graphql.anilist.co'
ANIME_LIST = []
engine = KivyEngine()

def get_title(obj):
    title_obj = obj["title"]
    english_title = str(title_obj["english"])
    romaji_title = title_obj["romaji"].encode('utf-8')

    if title_obj["english"] is None:
        return romaji_title
    else:
        return english_title
def add_anime_to_list(anime):
    if get_title(anime) not in ANIME_LIST:
        ANIME_LIST.append(get_title(anime))


def filter_anime(obj, page):
    for anime in obj["data"]["Page"]["media"]:
        Global.ANIME_PROCESSING_NUMBER += 1
        if anime["averageScore"] is None:
            rating = 0
        else:
            rating = int(str(anime["averageScore"]))

        genres = anime["genres"]

        if Global.POPULARITY is not None:
            if Global.POPULARITY >= Global.ANIME_PROCESSING_NUMBER:
                add_anime_to_list(anime)
                continue

        if len(Global.GENRES) > 0:
            for genre in Global.GENRES:
                if genre in genres:
                    if Global.RATING_IN_GENRE == 0:
                        add_anime_to_list(anime)
                        continue
                    else:
                        if rating >= Global.RATING:
                            add_anime_to_list(anime)
                            continue

        if Global.RATING_IN_GENRE == 0 and rating >= Global.RATING:
            add_anime_to_list(anime)
            continue

@engine.async
def get_releasing_anime():
    query = '''
        query ($page: Int, $perPage: Int){
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media (type: ANIME, format: TV, status: RELEASING, sort: POPULARITY_DESC){
                    title {
                        english
                        romaji
                    }
                    genres
                    averageScore
                }
            }
        }
        '''
    variables = {
        'page': 1,
        'perPage': 50,
    }
    Global.ANIME_LIST = []

    data = requestor.get_json_for_graphql(query,variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)
