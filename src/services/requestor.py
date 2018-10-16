import requests
from requests_futures.sessions import FuturesSession

session = FuturesSession()

def get_json_from_get(url):
    response = requests.get(url)
    return response.json()

def bg_cb(sess, resp):
    # parse the json storing the result on the response object
    resp.data = resp.json()

def get_json_from_post(url, data):
    #future = session.post(url, json = data)
    #response = requests.post(url, json = data)

    future = session.post(url,json=data, background_callback=bg_cb)
    # do some other stuff, send some more requests while this one works
    response = future.result()
    print(response.data)
    # data will have been attached to the response object in the background
    return response.data

def get_json_for_graphql(query, variables):
    return {'query': query, 'variables': variables}
