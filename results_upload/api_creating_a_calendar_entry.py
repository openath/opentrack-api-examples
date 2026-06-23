"""
Example script creating a competition. Please note if it's not managed by OpenTrack, it may not appear in the listing.

To create a competition, you need a user account with federation access.

The basic sequence is
1.  Authenticate
2.  Create a minimal competition dictionary
3.  Send a POST request to the server to create a competition
"""

import json
import os
import requests

# recommend to keep your real passwords in memory
username = os.environ.get("username")
password = os.environ.get("password")

BASE_URL = 'https://test-data.opentrack.run/'
TOKEN_URL = BASE_URL + 'api/get-auth-token/'
COMPETITION_URL = BASE_URL + 'api/competitions/'

r = requests.post(
    TOKEN_URL,
    data={'username': username, 'password': password}
)

resp = r.json()
try:
    token = resp["token"]
    print("Got a token: %s..." % token[0:30])
except KeyError:
    raise KeyError("Unable to authenticate, check credentials")


headers = {'Authorization': 'Token %s' % token}

comp = {
  "full_name": "api-test open meeting 2026",
  "short_name": "api-test",
  "slug": "api-test-slug",
  "name_local": "api-test",
  "country_id": "GBR",
  "address": "Kingsmeadow, Jack Goodchild Way, Kingston Road, Kingston upon Thames, UK",
  "year": "2026",
  "country": "GBR",
  "date": "2026-06-10",
  "finish_date": "2026-06-25",
  "wa_rankings_category_id": "DF",
  "age_groups": ["ALL"],
  "basic_description": "This is an opentrack api test",
  "contact_details": "example@example.com",
  "organiser": "6b2af700-0481-4f73-b9ae-8221ae619b55",
  "website": "https://example.example",
  "entry_link": "https://example.example/entry",
  "results_link": "https://example.example/results"
}


r = requests.post(
    COMPETITION_URL,
    json=comp,
    headers=headers
)

print("Created competiton with status_code %d" %  r.status_code)
parsed = json.loads(r.text)
print(json.dumps(parsed, indent=4, sort_keys=False))
