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
  "full_name": "api-test relay teams",
  "short_name": "api-test",
  "slug": "api-test-slug-5",
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
          "event_code": "4x200", 
          "event_id": "27",
        }
      ], 
      "first_name": "Andrew",
      "gender": "M", 
      "last_name": "Robinson", 
      "nationality": "GBR",
      "ot_athlete_id": "44721dcd-3019-44f0-aab0-4b90eb98838d", 
      "team_id": "THH",
    },
    {
      "age_group": "NA", 
      "category": "NA",
      "competitor_id": "2", 
      "date_of_birth": "1967-08-22",
      "events_entered": [
        {
          "event_code": "4x200", 
          "event_id": "27",
        }
      ], 
      "first_name": "Andy",
      "gender": "M", 
      "last_name": "Weir", 
      "nationality": "GBR",
      "ot_athlete_id": "332b0c3e-da43-4be6-af18-20a70fb23912", 
      "team_id": "THH",
    },
    {
      "age_group": "NA", 
      "category": "NA",
      "competitor_id": "3", 
      "date_of_birth": "1989-04-26",
      "events_entered": [
        {
          "event_code": "4x200", 
          "event_id": "27",
        }
      ], 
      "first_name": "Gus",
      "gender": "M", 
      "last_name": "Upton", 
      "nationality": "GBR",
      "ot_athlete_id": "af0a1892-0c9d-4031-a4cf-690c3c37bc49", 
      "team_id": "BEL",
    },
    {
      "age_group": "NA", 
      "category": "NA",
      "competitor_id": "4", 
      "date_of_birth": "1999-02-25",
      "events_entered": [
        {
          "event_code": "4x200", 
          "event_id": "27",
        }
      ], 
      "first_name": "Ben",
      "gender": "M", 
      "last_name": "Hassell", 
      "nationality": "GBR",
      "ot_athlete_id": "6bd44fb9-bc01-487f-bbfb-eaf1df0ed1b4", 
      "team_id": "BEL",
    }
  ], 
  "relay_teams": [
    {
      "event_id": "27",
      "name": "Hare & Hounds",
      "relay_team_id": "THH",
      "runners": [
        "1",
        "2"
      ],
      "team_id": "THH"
    },
    {
      "event_id": "27",
      "name": "Belgrave",
      "relay_team_id": "BEL",
      "runners": [
        "3",
        "4"
      ],
      "team_id": "BEL"
    }
  ],
  "events": [
    {
      "age_groups": ["ALL"], 
      "category": "M", 
      "ce_score_formula": "x", 
      "cut_after_round": 1, 
      "cut_survivors": 1, 
      "day": 1, 
      "event_code": "4x200", 
      "event_id": "27", 
      "genders": "M", 
      "heat_time_calculation": "AUTO", 
      "lanes": 4, 
      "max_field_attempts": 6, 
      "name": "4x200", 
      "r1_time": "15:45", 
      "reorder_last_round": False, 
      "require_callroom_override": False, 
      "rounds": "1", 
      "status": "partial", 
      "team_types": "INHERIT", 
      "units": [
        {
          "day": 1, 
          "distance": 800, 
          "event_id": "27", 
          "event_name": "4x200", 
          "heat": 1, 
          "heat_name": "27 4x200", 
          "precision": 2, 
          "results": [
          {
            "bib": "THH", 
            "lane": 1, 
            "performance": "1:30.59", 
            "place": 1, 
            "points": 0
          }, 
          {
            "bib": "BEL", 
            "lane": 2, 
            "performance": "1:32.60", 
            "place": 2, 
            "points": 0
          }
          ], 
          "results_status": "provisional", 
          "round": 1, 
          "scheduled_start_time": "15:45",
          "status": "finished"
        }
      ]
    }
  ],
  "teams": [
    {
      "flag_url": "https://file.opentrack.run/live/clubflags/GBR/BEL.png", 
      "match_id": "match", 
      "team_id": "BEL", 
      "team_name": "Belgrave Harriers"
    }, 
    {
      "flag_url": "https://file.opentrack.run/live/clubflags/GBR/THH.png", 
      "match_id": "match", 
      "team_id": "THH", 
      "team_name": "Thames Hare & Hounds"
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

