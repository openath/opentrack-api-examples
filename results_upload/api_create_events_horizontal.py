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
    "full_name": "api-test events horizontal",
    "short_name": "api-test",
    "slug": "api-test-slug-2b",
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
                    "event_code": "LJ", 
                    "event_id": "H3"
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
            "date_of_birth": "1989-04-26",
            "events_entered": [
                {
                    "event_code": "JT", 
                    "event_id": "H3"
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
            "category": "M_ALL",
            "event_code": "LJ", 
            "event_id": "H3", 
            "genders": "M",
            "name": "LJ M",
            "rounds": "3",
            "units": [
                {
                    "day": 1, 
                    "event_id": "H3", 
                    "event_name": "LJ M", 
                    "heat": 1,
                    "results": [
                        {
                            "bib": "1", 
                            "catpos": 1,
                            "order": 1, 
                            "performance": "5.74", 
                            "place": 1
                        }, 
                        {
                            "bib": "2", 
                            "catpos": 2,
                            "order": 2, 
                            "performance": "5.72", 
                            "place": 2
                        }
                    ], 
                    "results_status": "official", 
                    "round": 1,
                    "rounds": 3,
                    "status": "finished", 
                    "trials": [
                        {
                            "bib": "1", 
                            "result": "5.74", 
                            "round": 1
                        }, 
                        {
                            "bib": "1", 
                            "result": "x", 
                            "round": 2
                        }, 
                        {
                            "bib": "1", 
                            "result": "5.60", 
                            "round": 3
                        }, 
                        {
                            "bib": "2", 
                            "result": "5.72", 
                            "round": 1
                        }, 
                        {
                            "bib": "2", 
                            "result": "5.51", 
                            "round": 2
                        }, 
                        {
                            "bib": "2", 
                            "result": "x", 
                            "round": 3
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
