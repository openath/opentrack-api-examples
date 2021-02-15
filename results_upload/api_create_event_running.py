import requests
import json

EMAIL = '<put your email here>'
PASSWORD = '<put your password here>'

r = requests.post(
    "https://test-api.opentrack.run/api/v1/auth/token", 
    data={"username": EMAIL, "password": PASSWORD})

resp = r.json()
token = resp["access_token"]

headers = {'Authorization': 'Bearer %s' % token}

comp = {
    "full_name": "api-test long name events",
    "short_name": "api-test",
    "slug": "api-test-slug-2",
    "name_local": "api-test in italiano",
    "country_id": "ITA",
    "address": "Via dello Stadio 1, City",
    "venue_id": "051e8072-f667-4f10-aa82-b16a9317588e",
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
                            "bib": "ZZ000002",
                            "performance": "10.37"
                        },
                        {
                            "place": 2,
                            "points": 0,
                            "bib": "ZZ000011",
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
                            "bib": "ZZ000003",
                            "performance": "10.26"
                        },
                        {
                            "place": 2,
                            "points": 0,
                            "bib": "ZZ000004",
                            "performance": "10.47"
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
                            "bib": "ZZ000002",
                            "performance": "10.07"
                        },
                        {
                            "place": 2,
                            "points": 0,
                            "bib": "ZZ000003",
                            "performance": "10.37"
                        },
                        {
                            "place": 3,
                            "points": 0,
                            "bib": "ZZ000011",
                            "performance": "10.47"
                        },
                        {
                            "place": 4,
                            "points": 0,
                            "bib": "ZZ000004",
                            "performance": "10.48"
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