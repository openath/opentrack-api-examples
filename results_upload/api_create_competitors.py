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
    'full_name': 'api-test long name competitors',
    'short_name': 'api-test',
    'slug': 'api-test-slug-3',
    'name_local': 'api-test in italiano',
    'country_id': 'ITA',
    'address': 'Via dello Stadio 1, City',
    'latitude': '20.123',
    'longitude': '-15.321',
    'altitude': '1200.14',
    'date': '2020-08-10',
    'finish_date': '2020-08-15',
    'wa_rankings_category_id': 'DF',
    'age_groups': ['ALL'],
    'basic_description': 'Competition in Italy',
    'contact_details': 'example@example.it',
    'organiser_id': '179c0872-f761-4ed1-bb75-3b58a1368bac',
    'website': 'https://example.example',
    'entry_link': 'https://example.example/entry',
    'results_link': 'https://example.example/results',
    'competitors': [
        {
            'age_group': 'SEN',
            'category': 'SW',
            'competitor_id': 'ZZ000002',
            'date_of_birth': '1998-08-19',
            'events_entered': [
                {
                    'event_code': '200',
                    'event_id': '004'
                },
                {
                    'event_code': '400',
                    'event_id': '006'
                }
            ],
            'first_name': 'name',
            'gender': 'F',
            'last_name': 'surname',
            'team_id': 'ITA'
        },
        {
            'age_group': 'U20',
            'category': 'U20W',
            'competitor_id': 'ZZ000011',
            'date_of_birth': '1999-10-08',
            'events_entered': [
                {
                    'event_code': '10KW',
                    'event_id': '043'
                },
                {
                    'event_code': '10KW',
                    'event_id': '243'
                }
            ],
            'first_name': 'name2',
            'gender': 'M',
            'last_name': 'surname2',
            'team_id': 'ALG'
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