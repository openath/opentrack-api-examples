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
    "full_name": "api-test long name events vertical",
    "short_name": "api-test",
    "slug": "api-test-slug-2c",
    "name_local": "api-test in italiano",
    "country_id": "ITA",
    "address": "Via dello Stadio 1, City",
    "latitude": "20.123",
    "longitude": "-15.321",
    "altitude": "1200.14",
    "date": "2020-08-10",
    "finish_date": "2020-08-15",
    "wa_rankings_category_id": "DF",
    "age_groups": ["ALL"],
    "basic_description": "Competition in Italy",
    "contact_details": "example@example.it",
    "organiser_id": "179c0872-f761-4ed1-bb75-3b58a1368bac",
    "website": "https://example.example",
    "entry_link": "https://example.example/entry",
    "results_link": "https://example.example/results",
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