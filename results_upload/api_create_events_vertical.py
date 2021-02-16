import requests
import json

EMAIL = '<Your authorised Email>'
PASSWORD = '<Your authorised password>'

r = requests.post(
    "https://test-api.opentrack.run/api/v1/auth/token", 
    data={"username": EMAIL, "password": PASSWORD})

resp = r.json()
token = resp["access_token"]

headers = {'Authorization': 'Bearer %s' % token}

comp = {
    "full_name": "api-test events vertical",
    "short_name": "api-test",
    "slug": "api-test-slug-2c",
    "name_local": "api-test",
    "country_id": "GBR",
    "address": "Kingsmeadow, Jack Goodchild Way, Kingston Road, Kingston upon Thames, UK",
    "date": "2020-08-10",
    "finish_date": "2020-08-15",
    "wa_rankings_category_id": "DF",
    "age_groups": ["ALL"],
    "basic_description": "This is an opentrack api test",
    "contact_details": "example@example.com",
    "organiser_id": "6b2af700-0481-4f73-b9ae-8221ae619b55",
    "website": "https://example.example",
    "entry_link": "https://example.example/entry",
    "results_link": "https://example.example/results",
    "competitors": [
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
        {
            "age_group": "NA", 
            "category": "NA",
            "competitor_id": "302", 
            "date_of_birth": "1989-04-26",
            "events_entered": [
                {
                    "event_code": "PV", 
                    "event_id": "1"
                }
            ], 
            "first_name": "Gus",
            "gender": "M", 
            "last_name": "Upton", 
            "nationality": "GBR",
            "ot_athlete_id": "af0a1892-0c9d-4031-a4cf-690c3c37bc49", 
            "team_id": "BEL"
        }
    ],
    "events": [
        {
            "age_groups": ["SEN"],
            "category": "SEN",
            "event_code": "PV", 
            "event_id": "F2", 
            "genders": "MF",
            "name": "Pole Vault",
            "rounds": "1", 
            "status": "complete",
            "units": [
                {
                    "event_id": "F2", 
                    "event_name": "Pole Vault", 
                    "heat": 1,
                    "heights": [
                        "3.10", 
                        "3.25", 
                        "3.40", 
                        "3.55", 
                        "3.70"
                    ],
                    "results": [
                        {
                            "bib": "371",
                            "performance": "3.40", 
                            "place": 2
                        }, 
                        {
                            "bib": "302",
                            "performance": "3.55", 
                            "place": 1
                        }
                    ], 
                    "results_status": "official", 
                    "round": 1, 
                    "status": "finished", 
                    "trials": [
                        {
                            "bib": "371", 
                            "height": "3.10", 
                            "result": "o"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.10", 
                            "result": "o"
                        }, 
                        {
                            "bib": "371", 
                            "height": "3.25", 
                            "result": "o"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.25", 
                            "result": "o"
                        }, 
                        {
                            "bib": "371", 
                            "height": "3.40", 
                            "result": "o"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.40", 
                            "result": "o"
                        }, 
                        {
                            "bib": "371", 
                            "height": "3.55", 
                            "result": "x"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.55", 
                            "result": "x"
                        }, 
                        {
                            "bib": "371", 
                            "height": "3.55", 
                            "result": "x"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.55", 
                            "result": "x"
                        }, 
                        {
                            "bib": "371", 
                            "height": "3.55", 
                            "result": "x"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.55", 
                            "result": "o"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.70", 
                            "result": "x"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.70", 
                            "result": "x"
                        }, 
                        {
                            "bib": "302", 
                            "height": "3.70", 
                            "result": "x"
                        }
                    ]
                }
            ]
        }
    ]
}


r = requests.post(
    "https://test-api.opentrack.run/api/v1/competitions/", 
    data=json.dumps(comp),
    headers=headers
    )

print("Created competiton with status_code %d" %  r.status_code)
parsed = json.loads(r.text)
print(json.dumps(parsed, indent=4, sort_keys=False))
