"""
Example script which lists events in a competition, modified one, deletes it, then re-creates it.

This uses a past meeting on our test server
    https://test-data.opentrack.run/en-gb/x/2026/GBR/lac-open-2/
To manipulate any competition, you will need to pick one that you have
meeting director access to.

"""

import requests
import os
from pprint import pprint

BASE_URL = 'https://test-data.opentrack.run/'
EVENTS_URL = BASE_URL + 'api/events/'

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
    comp_id = "58706d25-1289-4032-9277-020575485c39"
    headers = {"Authorization": "Token " + get_token(), "Referer": BASE_URL}

    # Get
    resp = requests.get(EVENTS_URL + f"?competition={comp_id}", headers=headers)
    if resp.status_code != 200:
        raise ValueError("Status code not 200")
    original_event = resp.json()['results'][0]

    # Update
    ev_id = original_event['id']
    event_url = f"{EVENTS_URL}{ev_id}/"
    payload = dict(
        competition=original_event['competition'],
        event_id=original_event['event_id'],
        event_code=original_event['event_code'],
        category="V50", # this is the only actual change, the other fields are just required.
    )
    print(f" PUT to {event_url}")
    resp = requests.put(event_url, json=payload, headers=headers)
    if resp.status_code != 200:
        raise ValueError("Status code not 200")

    # Delete
    print(f" DELETE to {event_url}")
    resp = requests.delete(event_url, headers=headers)
    if resp.status_code != 204:
        raise ValueError("Status code not 204")

    # Create
    print(f" POST to {EVENTS_URL}")
    original_event['parent'] = ''
    resp = requests.post(EVENTS_URL, json=original_event, headers=headers)
    if resp.status_code != 201:
        raise ValueError("Status code not 201")


if __name__ == '__main__':
    run()


""" One event with all its options....
{
            "url": "https://test-data.opentrack.run/api/events/241489/",
            "id": 241489,
            "competition": "ffb87823-e36b-4a8a-aee9-8c50e0958350",
            "event_id": "F01",
            "event_code": "LJ",
            "age_groups": "SEN,U15,U17,U20,U23",
            "genders": "MF",
            "category": "LJ1",
            "limit": 17,
            "name": "Long Jump | U15-SEN",
            "parent": null,
            "question": "",
            "venue": null,
            "venue_r2": null,
            "venue_r3": null,
            "venue_r4": null,
            "name_local": null,
            "primary_colour": null,
            "text_colour": null,
            "rounds": "1",
            "day": 1,
            "r1_time": "18:30",
            "r2_day": 1,
            "r2_time": "",
            "r3_day": 1,
            "r3_time": "",
            "r4_day": 1,
            "r4_time": "",
            "hide_in_timetable": false,
            "heat_time_calculation": "AUTO",
            "heat_time_override": null,
            "record_text": "",
            "record_perf": "",
            "min_perf": "",
            "max_perf": "",
            "max_field_attempts": 3,
            "cut_after_round": 0,
            "cut_survivors": 8,
            "reorder_last_round": false,
            "qual_criteria": "",
            "qual_by_place": 0,
            "qual_fastest_losers": 0,
            "qualifying_performance": "",
            "seeding": "open_meet",
            "seeding_method": "fastest_last",
            "pool_order": "bib",
            "qual_by_place_r3": null,
            "qual_fastest_losers_r3": null,
            "seeding_method_r3": "fastest_last",
            "lanes": 17,
            "lane_prefs": null,
            "lanes_r2": 8,
            "lanes_r3": 8,
            "team_types": "INHERIT",
            "status": "none",
            "r1_status": "none",
            "r2_status": "none",
            "r3_status": "none",
            "r4_status": "none",
            "require_callroom_override": false,
            "callroom_time_override": null,
            "show_form_guide": false,
            "ce_score_formula": "x",
            "combined_event_tables": null,
            "rank_by": "DEFAULT",
            "remote_results_url": null,
            "world_athletics_event_id": null,
            "include_dq_athletes": false,
            "include_dnf_athletes": false,
            "include_dns_athletes": false,
            "exclude_from_scoring_system": false,
            "exclude_from_per_event_checkins": false,
            "entry_limit_per_event": null,
            "entry_limit_per_ns_event": null,
            "non_scorers_per_scoring_event": null,
            "relay_entry_limit_per_event": null
        },
"""