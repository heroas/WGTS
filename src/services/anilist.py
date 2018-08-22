import requests

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

        response = requests.post(ANI_LIST_URL, json={'query': query, 'variables': variables})

        data = response.json()
        title_obj = data["data"]["Media"]["title"]
        english_title = str(title_obj["english"])
        romaji_title = str(title_obj["romaji"])

        if title_obj["english"] is None:
            title = romaji_title
        else:
            title = english_title

        return title;
