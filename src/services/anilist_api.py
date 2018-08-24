from services import requestor

ANI_LIST_URL = 'https://graphql.anilist.co'

def get_title(obj):
    title_obj = obj["data"]["Media"]["title"]
    english_title = str(title_obj["english"])
    romaji_title = str(title_obj["romaji"])

    if title_obj["english"] is None:
        return romaji_title
    else:
        return english_title


def get_anime_from_mal_id(mal_id):
    if mal_id.isdigit():
        query = '''
             query ($malId: Int) {
                    Media (idMal: $malId,type: ANIME) {
                        id
                        idMal
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

        return get_title(result)


def get_anime_from_genre(genre):
    print genre
    query = '''
        query ($genre: String){
            Media (genre: $genre, type: ANIME){
                title {
                    english
                    romaji
                }
            }
        }
        '''
    variables = {
        'genre': genre
    }


    data = requestor.get_json_for_graphql(query,variables)
    result = requestor.get_json_from_post(ANI_LIST_URL, data)
    print result
    return get_title(result)
