"""
Example script interacting with team data from outside OpenTrack, using our API

For now the competition and team_id are required fields even if you have the team id

"""

import requests
import os

BASE_URL = 'https://test-data.opentrack.run/'
TEAMS_URL = BASE_URL + 'api/teams/'

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
    competition_id = "58706d25-1289-4032-9277-020575485c39"
    headers = {"Authorization": "Token " + get_token(), "Referer": BASE_URL}
    custom_teams = [
        # Minimum required fields
        {"competition": competition_id, "team_id": "THH19"},
        {"competition": competition_id, "team_id": "HHH19"},
    ]

    # Create - Expect status code 201
    resp = requests.post(
        url=TEAMS_URL,
        json=custom_teams,
        headers=headers,
    )
    if resp.status_code != 201:
        raise ValueError("Status code not 201")
    teams = resp.json()

    # Retrieve - Expect status code 200
    resp = requests.get(
        url=TEAMS_URL + f'{teams[0]["id"]}/',
        headers=headers,
    )
    if resp.status_code != 200:
        raise ValueError("Status code not 200")

    # Update - Expect status code 200
    resp = requests.put(
        url=TEAMS_URL + f'{teams[0]["id"]}/',
        json={**custom_teams[0], "team_name": "TEST8"},
        headers=headers,
    )
    if resp.status_code != 200:
        raise ValueError("Status code not 200")

    # Delete - Expect status code 200
    resp = requests.put(
        url=TEAMS_URL + f'{teams[0]["id"]}/',
        json={**custom_teams[0]},
        headers=headers,
    )
    if resp.status_code != 200:
        raise ValueError("Status code not 200")


if __name__ == '__main__':
    run()
