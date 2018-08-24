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


def get_anime_from_genre(genre):
    print genre
    print Global.SEASON
    print Global.SEASON_YEAR

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
                media (genre: $genre, season: $season, seasonYear: $seasonYear, type: ANIME, format: TV){
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
        'season': Global.SEASON,
        'seasonYear': Global.SEASON_YEAR,
        'page': 1,
        'perPage': 30
    }


    data = requestor.get_json_for_graphql(query,variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)

    for anime in result["data"]["Page"]["media"]:
        print get_title(anime)
        Global.ANIME_LIST.append(get_title(anime))
