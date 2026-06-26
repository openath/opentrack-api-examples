"""
Example script creating competitors with minimal information: competition, competitor_id

This uses a past meeting on our test server
    https://test-data.opentrack.run/en-gb/x/2026/GBR/lac-open-2/
To manipulate any competition, you will need to pick one that you have
meeting director access to.
"""

import json
import os
import requests

BASE_URL = 'https://test-data.opentrack.run/'


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


def run():
    competition_id = '58706d25-1289-4032-9277-020575485c39'

    competitors = [
        {
            # Each competitor at a minimum must be a unique combination of: competition, competitor_id
            "competition": competition_id,
            "competitor_id": "371",
        },
    ]

    headers = {"Authorization": "Token " + get_token(), "Referer": BASE_URL}

    r = requests.post(
        f"{BASE_URL}/api/competitors/?competition={competition_id}/",
        json=competitors,
        headers=headers
    )


    print("Created competitor with status_code %d" %  r.status_code)
    parsed = json.loads(r.text)
    print(json.dumps(parsed, indent=4, sort_keys=False))

if __name__ == '__main__':
    run()

""" One competitor with common options....
competitors = [
    {
        "age_group": "NA",
        "category": "NA",
        "competitor_id": "371",
        "date_of_birth": "1966-03-21",
        "events_entered": [
            {
                "event_code": "PV",
                "event_id": "F2"
            }
        ],
        "first_name": "Andrew",
        "gender": "M",
        "last_name": "Robinson",
        "nationality": "GBR",
        "ot_athlete_id": "44721dcd-3019-44f0-aab0-4b90eb98838d",
        "team_id": "THH"
    },
]
"""