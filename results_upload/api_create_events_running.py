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
    "full_name": "api-test events running",
    "short_name": "api-test",
    "slug": "api-test-slug-2a",
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
                    "event_code": "3k", 
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
                    "event_code": "3k", 
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
                    "event_code": "3k", 
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
            "event_id": "003",
            "event_code": "100",
            "name": "100 metres MEN",
            "genders": "M",
            "category": "M",
            "rounds": "2,1",
            "units": [
                {
                    "status": "finished",
                    "heat": 1,
                    "round": 1,
                    "results_status": "official",
                    "results": [
                        {
                            "place": 1,
                            "points": 0,
                            "bib": "1",
                            "performance": "10.37"
                        },
                        {
                            "place": 2,
                            "points": 0,
                            "bib": "2",
                            "performance": "10.48"
                        }
                    ]
                },
                {
                    "status": "finished",
                    "heat": 2,
                    "round": 1,
                    "results_status": "official",
                    "results": [
                        {
                            "place": 1,
                            "points": 0,
                            "bib": "3",
                            "performance": "10.26"
                        }
                    ]
                },
                {
                    "status": "finished",
                    "heat": 1,
                    "round": 2,
                    "results_status": "official",
                    "results": [
                        {
                            "place": 1,
                            "points": 0,
                            "bib": "1",
                            "performance": "10.07"
                        },
                        {
                            "place": 2,
                            "points": 0,
                            "bib": "3",
                            "performance": "10.37"
                        },
                        {
                            "place": 3,
                            "points": 0,
                            "bib": "2",
                            "performance": "10.47"
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

