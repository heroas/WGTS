from services import requestor
import Global

ANI_LIST_URL = 'https://graphql.anilist.co'
ANIME_LIST = []

def get_title(obj):
    title_obj = obj["title"]
    english_title = str(title_obj["english"])
    #romaji_title = str(title_obj["romaji"].encode('utf-8'))
    romaji_title = str(title_obj["romaji"])

    if title_obj["english"] is None:
        return romaji_title
    else:
        return english_title
def add_anime_to_list(anime):
    if get_title(anime) not in ANIME_LIST:
        ANIME_LIST.append(get_title(anime))


def filter_anime(obj, page):
    for anime in obj["data"]["Page"]["media"]:
        print(anime["description"])
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
                    description
                }
            }
        }
        '''
    variables = {
        'page': 1,
        'perPage': 50,
    }

    data = requestor.get_json_for_graphql(query,variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)
    page = 1
    lastPage = result["data"]["Page"]["pageInfo"]["lastPage"]
    Global.ANIME_PROCESSING_NUMBER = 0
    filter_anime(result, page)

    while page < lastPage:
        page += 1
        variables = { 'page': page, 'perPage': 50,}

        data = requestor.get_json_for_graphql(query,variables)
        result = requestor.get_json_from_post(ANI_LIST_URL, data)
        filter_anime(result, page);

    return ANIME_LIST

def get_airing_schedule(id):
    query = '''
        query ($id: Int) { # Define which variables will be used in the query (id)
            AiringSchedule (mediaId: $id) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
                id
                mediaId
                episode
                airingAt
            }
        }
    '''

    variables = {
        'id': id
    }

    data = requestor.get_json_for_graphql(query,variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)
    print(result)
