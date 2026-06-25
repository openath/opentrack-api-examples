"""
Example script which lists events in a competition, modified one, creates
and optionally deletes one.

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



def get_events(comp_id, headers):
    # Get list of EventSpec records in competition.
    resp = requests.get(
        BASE_URL + 'api/events/', 
        params={'competition': comp_id},
        headers=headers
    )
    if resp.status_code == 200:
        return resp.json()["results"]
    else:
        print(f"An error occurred, response status code {resp.status_code}")
        return []


def run():
    comp_id = "58706d25-1289-4032-9277-020575485c39"


    headers = {"Authorization": "Token " + get_token(), "Referer": BASE_URL}
    events = get_events(comp_id, headers)

    print("Listing events in competition:")
    for ev in events:
        print(f"  Event {ev['event_id']} is of type {ev['event_code']} and starts at {ev['r1_time']}")

    # delay start of everything by an hour. Times are always text in format hh:mm
    # this would not work past midnight, but it's just a demo
    for ev in events:
        ev_id = ev["id"]
        start_time = ev["r1_time"]
        if start_time:
            hrs, mins = start_time.split(":")
            new_start_time = str(int(hrs) + 1) + ":" + mins


            event_url = f"{BASE_URL}api/events/{ev_id}/"

            payload = dict(
                competition=comp_id,
                event_id=ev["event_id"],
                event_code=ev["event_code"],
                r1_time=new_start_time
                )
            resp = requests.put(event_url, json=payload, headers=headers)
            print(f" POST to {event_url}")
            if resp.status_code == 200:
                print(f"    Updated start time of {ev['event_id']} to be {new_start_time}")
            else:
                print(resp.status_code)
                pprint(resp.json())
                return

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