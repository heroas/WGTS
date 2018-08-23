from services import requestor

ANI_LIST_URL = 'https://graphql.anilist.co'

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

        title_obj = result["data"]["Media"]["title"]
        english_title = str(title_obj["english"])
        romaji_title = str(title_obj["romaji"])

        if title_obj["english"] is None:
            title = romaji_title
        else:
            title = english_title

        return title;
