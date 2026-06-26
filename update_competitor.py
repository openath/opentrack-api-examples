"""
Example script updating competitors with minimal information

In this example we update the competitors id from 246 to 11111

This uses a past meeting on our test server
    https://test-data.opentrack.run/en-gb/x/2026/GBR/lac-open-2/
To manipulate any competition, you will need to pick one that you have
meeting director access to.
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

    # Only Competition is required, since the competitor's url uses a different id. This one represents a bib number.
    data = {
        "competition": competition_id,
        "competitor_id": "11111", # previously 246
    }
    resp = requests.patch(
        competitors[0]['url'],
        json=data,
        headers=headers,
    )
    print(resp)



if __name__ == '__main__':
    run()
