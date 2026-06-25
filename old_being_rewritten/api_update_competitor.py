"""
Example script updating competitors with minimal information
"""

import requests
import os

BASE_URL = 'https://test-data.opentrack.run/'
COMPETITORS_URL = BASE_URL + 'api/competitors/'

def get_token():
    # recommend to keep your real passwords in memory
    username = os.environ.get("username")
    password = os.environ.get("password")

    r1 = requests.post(
        BASE_URL + 'api/get-auth-token/',
        data=dict(username=username, password=password)
    )
    try:
        token = r1.json()["token"]
        print("Got a token: %s..." % token[0:30])
    except KeyError:
        raise KeyError("Unable to authenticate, check credentials")
    else:
        return token

def get_competitors(comp_id, headers):
    # Get Competitors.  By default the API returns 50 at a time,
    # but setting a higher limit to return a few hundred in one call
    # is OK.  This meeting has 360.
    filters = [f"competition={comp_id}", "limit=500"]
    filter_str = f'?{"&".join(filters)}'
    competitors_resp = requests.get(
        COMPETITORS_URL + filter_str,
        headers=headers
    )
    return competitors_resp.json()['results']

def run():
    competition_id = "58706d25-1289-4032-9277-020575485c39"
    headers = {"Authorization": "Token " + get_token(), "Referer": BASE_URL}
    competitors = get_competitors(competition_id, headers)
    data = {
        "competition": competition_id,
        "competitor_id": "11111",
    }
    resp = requests.patch(
        competitors[0]['url'],
        json=data,
        headers=headers,
    )
    print(resp)



if __name__ == '__main__':
    run()
