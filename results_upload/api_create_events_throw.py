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

#Work in progress: Getting error messages as if this were a height event
comp = {
    "full_name": "api-test events throw",
    "short_name": "api-test",
    "slug": "api-test-slug-2d",
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
            "competitor_id": "1", 
            "date_of_birth": "1966-03-21",
            "events_entered": [
                {
                    "event_code": "JT", 
                    "event_id": "1"
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
            "competitor_id": "2", 
            "date_of_birth": "1967-08-22",
            "events_entered": [
                {
                    "event_code": "JT", 
                    "event_id": "1"
                }
            ], 
            "first_name": "Andy",
            "gender": "M", 
            "last_name": "Weir", 
            "nationality": "GBR",
            "ot_athlete_id": "332b0c3e-da43-4be6-af18-20a70fb23912", 
            "team_id": "THH"
        },
        {
            "age_group": "NA", 
            "category": "NA",
            "competitor_id": "3", 
            "date_of_birth": "1989-04-26",
            "events_entered": [
                {
                    "event_code": "JT", 
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
            "age_groups": [
                "ALL"
            ],
            "category": "MF_ALL",
            "event_code": "JT", 
            "event_id": "F3", 
            "genders": "MF",
            "name": "Javelin",
            "rounds": "1",
            "units": [
                {
                    "day": 1, 
                    "event_id": "F3", 
                    "event_name": "Javelin", 
                    "heat": 1,
                    "results": [
                        {
                            "bib": "1", 
                            "catpos": 1, 
                            "order": 1, 
                            "performance": "47.03", 
                            "place": 2
                        }, 
                        {
                            "bib": "2", 
                            "catpos": 1, 
                            "order": 2, 
                            "performance": "47.04", 
                            "place": 1
                        }, 
                        {
                            "bib": "3", 
                            "catpos": 2, 
                            "order": 3, 
                            "performance": "46.93", 
                            "place": 3
                        }
                    ], 
                    "results_status": "official", 
                    "round": 1, 
                    "rounds": 6,
                    "status": "finished", 
                    "trials": [
                        {
                            "bib": "1", 
                            "result": "47.03", 
                            "round": 1
                        }, 
                        {
                            "bib": "1", 
                            "result": "46.32", 
                            "round": 2
                        }, 
                        {
                            "bib": "1", 
                            "result": "45.13", 
                            "round": 3
                        }, 
                        {
                            "bib": "1", 
                            "result": "43.01", 
                            "round": 4
                        }, 
                        {
                            "bib": "1", 
                            "result": "45.42", 
                            "round": 5
                        }, 
                        {
                            "bib": "1", 
                            "result": "x", 
                            "round": 6
                        }, 
                        {
                            "bib": "2", 
                            "result": "41.61", 
                            "round": 1
                        }, 
                        {
                            "bib": "2", 
                            "result": "47.04", 
                            "round": 2
                        }, 
                        {
                            "bib": "2", 
                            "result": "x", 
                            "round": 3
                        }, 
                        {
                            "bib": "2", 
                            "result": "44.07", 
                            "round": 4
                        }, 
                        {
                            "bib": "2", 
                            "result": "43.08", 
                            "round": 5
                        }, 
                        {
                            "bib": "2", 
                            "result": "45.93", 
                            "round": 6
                        }, 
                        {
                            "bib": "3", 
                            "result": "45.53", 
                            "round": 1
                        }, 
                        {
                            "bib": "3", 
                            "result": "46.08", 
                            "round": 2
                        }, 
                        {
                            "bib": "3", 
                            "result": "45.17", 
                            "round": 3
                        }, 
                        {
                            "bib": "3", 
                            "result": "46.63", 
                            "round": 4
                        }, 
                        {
                            "bib": "3", 
                            "result": "46.93", 
                            "round": 5
                        }, 
                        {
                            "bib": "3", 
                            "result": "41.04", 
                            "round": 6
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

