import requests

def get_json_from_get(url):
    response = requests.get(url)
    return response.json()

def get_json_from_post(url, data):
    result = requests.post(url,json=data);
    return result.json()

def get_json_for_graphql(query, variables):
    return {'query': query, 'variables': variables}
