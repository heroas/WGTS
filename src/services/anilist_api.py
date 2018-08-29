from services import requestor
import Global

ANI_LIST_URL = 'https://graphql.anilist.co'

def get_title(obj):
    title_obj = obj["title"]
    english_title = str(title_obj["english"])
    romaji_title = title_obj["romaji"].encode('utf-8')

    if title_obj["english"] is None:
        return romaji_title
    else:
        return english_title
def add_anime_to_list(anime):
    if get_title(anime) not in Global.ANIME_LIST:
        Global.ANIME_LIST.append(get_title(anime))


def filter_anime(obj, page):
    for anime in obj["data"]["Page"]["media"]:
        print (get_title(anime))
        Global.ANIME_PROCESSING_NUMBER += 1
        print (Global.ANIME_PROCESSING_NUMBER)
        print(str(anime["averageScore"]))
        if anime["averageScore"] is None:
            rating = 0
        else:
            rating = int(str(anime["averageScore"]))

        genres = anime["genres"]

        print(Global.POPULARITY)
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



def get_anime_from_mal_id(mal_id):
    if mal_id.isdigit():
        query = '''
             query ($malId: Int) {
                    Media (idMal: $malId,type: ANIME, format:TV) {
                        title {
                            english
                            romaji
                        }
                    }
             }
             '''
        variables = {
            'malId':mal_id
        }

        data = requestor.get_json_for_graphql(query,variables)
        result = requestor.get_json_from_post(ANI_LIST_URL, data)

        return get_title(result["data"]["Media"])

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
    page = 1
    lastPage = result["data"]["Page"]["pageInfo"]["lastPage"]
    Global.ANIME_PROCESSING_NUMBER = 0
    filter_anime(result, page)

    while page < lastPage:
        print (page)
        page += 1
        variables = { 'page': page, 'perPage': 50,}

        data = requestor.get_json_for_graphql(query,variables)
        result = requestor.get_json_from_post(ANI_LIST_URL, data)
        filter_anime(result, page);


    print (Global.ANIME_LIST)
    print (len(Global.ANIME_LIST))

    #filter_list(Global.ANIM)

def get_anime_from_genre(genre, rating):
    query = '''
        query ($genre: String, $season: MediaSeason, $seasonYear: Int, $page: Int, $perPage: Int){
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
                media (genre: $genre, type: ANIME, format: TV, status: RELEASING){
                    title {
                        english
                        romaji
                    }
                }
            }
        }
        '''
    variables = {
        'genre': genre,
        'page': 1,
        'perPage': 40,
        'rating': rating
    }


    data = requestor.get_json_for_graphql(query,variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)

    for anime in result["data"]["Page"]["media"]:
        print (get_title(anime))
        if get_title(anime) not in Global.ANIME_LIST:
            Global.ANIME_LIST.append(get_title(anime))
