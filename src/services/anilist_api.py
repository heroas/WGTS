from services import requestor
import Global
from models.anime import Anime

ANI_LIST_URL = 'https://graphql.anilist.co'


def get_title(obj):
    title_obj = obj["title"]
    english_title = str(title_obj["english"])
    #romaji_title = str(title_obj["romaji"].encode('utf-8'))
    romaji_title = str(title_obj["romaji"])

    if title_obj["english"] is None:
        return romaji_title
    else:
        return english_title


def add_anime_to_list(full_anime_list, anime_list_obj):
    # for anime in anime_list_obj["data"]["Page"]["media"]:
    #     if anime["nextAiringEpisode"] is not None and anime["averageScore"] is not None and len(anime["genres"]) > 0:
    #         full_anime_list.append(anime)
    for anime in anime_list_obj["data"]["Page"]["media"]:
        full_anime_list.append(anime)

    return full_anime_list


def get_releasing_anime():
    ANIME_LIST = []
    # media (type: ANIME, format: TV, season: WINTER, seasonYear: 2017, sort: POPULARITY_DESC){
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
                media (type: ANIME, format: TV, status:RELEASING, sort: POPULARITY_DESC){
                    id
                    episodes
                    title {
                        english
                        romaji
                    }
                    genres
                    averageScore
                    description(asHtml:false)

                    coverImage {
                        large
                    }
                    nextAiringEpisode {
                        episode
                    }
                    source
                }
            }
        }
        '''
    variables = {
        'page': 1,
        'perPage': 50,
    }

    data = requestor.get_json_for_graphql(query, variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)
    #print(result)
    page = 1
    lastPage = result["data"]["Page"]["pageInfo"]["lastPage"]
    ANIME_LIST = add_anime_to_list(ANIME_LIST, result)

    while page < lastPage:
        page += 1
        variables = {'page': page, 'perPage': 50, }

        data = requestor.get_json_for_graphql(query, variables)
        result = requestor.get_json_from_post(ANI_LIST_URL, data)
        ANIME_LIST = add_anime_to_list(ANIME_LIST, result)

    return ANIME_LIST


def get_next_airing_episode(id):
    query = '''
            query ($id: Int){
                Media (type: ANIME, format: TV, status: RELEASING, sort: POPULARITY_DESC, id: $id){
                    episodes
                    title {
                        english
                        romaji
                    }

                    nextAiringEpisode {
                        episode
                    }

                }

            }
            '''
    variables = {
        'id': id
    }
    data = requestor.get_json_for_graphql(query, variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)
    if result["data"]["Media"]["nextAiringEpisode"] is not None:
        return result["data"]["Media"]["nextAiringEpisode"]["episode"]
    else:
        return result["data"]["Media"]["episodes"]
