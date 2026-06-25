"""
Example script updating PB/SB data from outside OpenTrack, using our API

This is a common requirement in Norway, when competitors are created from a national
entry system without any seeding data; and, sadly, in 2026 in UK, due to temporary 
unavaiability of our national stats system.

The example below was our first test of this, setting seeding data for the Livingston
Open Meeting in Scotland on Friday 19th June.  See...

    https://data.opentrack.run/en-gb/x/2026/GBR/lac-open-2/

thanks to Alistair Dalgleish for providing a great test case and example.

To modify data about a competition, you need a user account with Director rights to
that competition, either via the competition directly, or the organising club/body.
You can check this on "Manage | Officials"

The basic sequence is
1.  Add "json/" to the comptition url, wait for the public 
    json representation, and get the "id" parameter
2.  Authenticate
3.  Fetch a list of all the competitors into a json structure.
    Each json block describes a competitor, and a list of the events they are entering
    with event_id, event_code, sb, pb and qp (qualifying performance)
4.  Loop through this, replacing the "events_entered" attribute, and post back to the server.


The data block with everyone's seeding data is at the bottom of the script. The names are
a nice-to-have and not needed; you could just parse the data a bit differently.

"""

import requests
import os

BASE_URL = 'https://test-data.opentrack.run/'
COMPETITORS_URL = BASE_URL + 'api/competitors/'

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

def parse_data():
    "Create the new events_entered array for each person from the seeding data at bottom of file"
    seed_data = {}
    lines = DATA.splitlines()
    for line in lines:
        if line:
            (bib, first_name, last_name, event_id, event_code, qp, pb, sb) = line.split(",")

            if bib not in seed_data:
                # will be the events_entered array, with 1 of more events.
                seed_data[bib] = []  

            # this block is exactly the structure we store on the server, and which
            # you would retrieve for each competitor, for each of their events.
            ee = dict(
                    event_id=event_id,
                    event_code=event_code,
                    pb=pb,
                    sb=sb,
                    qp=qp
                    )
            seed_data[bib].append(ee)

    return seed_data

def get_competitors(comp_id, headers):
    # Get Competitors.  By default the API returns 50 at a time,
    # but setting a higher limit to return a few hundred in one call 
    # is OK.  This meeting has 360.
    filters = [f"competition={comp_id}", "limit=500"]
    filter_str = f'?{"&".join(filters)}'
    competitors_resp = requests.get(
        COMPETITORS_URL + filter_str,
        headers=headers
    )
    return competitors_resp.json()['results']

def run():
    comp_id = "58706d25-1289-4032-9277-020575485c39"

    UPDATES = parse_data()

    print(f"Seeding data has {len(UPDATES)} rows. Example:\n{UPDATES["50"]}")
    headers = {"Authorization": "Token " + get_token(), "Referer": BASE_URL}
    competitors = get_competitors(comp_id, headers)
    print(f"fetched {len(competitors)} competitors")

    for c in competitors:
        bib = c["competitor_id"]
        if bib in UPDATES:
            new_ee = UPDATES[bib]

            COMPETITOR_URL = COMPETITORS_URL + c["id"] + "/"
            c["events_entered"] = new_ee  # replace

            # send a new json representation back to the endpoint for this
            # particular competitor
            resp = requests.put(
                    COMPETITOR_URL,
                    json=c,
                    headers=headers,
                )
            if resp.status_code == 200:
                print(f"Updated {c['competitor_id']}: {c['first_name']} {c['last_name']}")
        else:
            print(f"NO updates for {c['competitor_id']}: {c['first_name']} {c['last_name']}")


# Bib,First,Last,EventID,EventCode,QP,PB,SB
DATA = """
298,Rory,Millar,T01,150,26.71,26.71,26.71
280,Murray,Macpherson,F02,LJ,3.27,3.27,3.27
280,Murray,Macpherson,T01,150,26.98,26.98,26.98
217,Luke,Crawford,F03,LJ,3.43,3.43,3.43
217,Luke,Crawford,T02,200,27.9,27.9,27.9
29,Lilly,Crawford,F02,LJ,2.67,2.67,2.67
29,Lilly,Crawford,T01,150,27.25,27.25,27.25
334,Aaron,Shaw,F01,LJ,4.59,4.68,4.59
334,Aaron,Shaw,T02,200,26.73,26.73,26.73
135,Airlie,Oakley,T04,800,2:38.92,2:37.31,2:38.92
109,Lucy,Macmillan,T02,200,26.95,26.72,26.95
253,Archie,Hendry,T02,200,23.81,23.81,
154,Holly,Robshaw,T02,200,29.10,29.10,29.10
148,Blythe,Remmo,T04,800,3:10.00,,
149,Orla,Remmo,T04,800,2:44.85,2:44.7,2:44.85
158,Emily,Sharp,T02,200,26.98,26.98,26.98
273,Ruaridh,Laing,F02,LJ,2.52,2.77,2.52
273,Ruaridh,Laing,T01,150,28.35,28.35,
133,Lauren,Nilan,F03,LJ,3.08,3.08,3.08
133,Lauren,Nilan,T02,200,33.32,33.32,
309,Joshua,Neilson,T02,200,26.31,26.31,26.31
164,Lucy,Spinks,F01,LJ,3.94,3.94,3.94
164,Lucy,Spinks,T02,200,29.9,29.9,29.9
236,Jordi,Francisco-Suarez,T02,200,,,
236,Jordi,Francisco-Suarez,T04,800,3:17.93,3:17.93,
87,Rosie,Kirk,T02,200,33.52,33.52,33.52
87,Rosie,Kirk,T04,800,,,
199,Adam,Bayley,T04,800,2:06.85,2:02.87,2:06.85
68,Zoe,Grant,F01,LJ,4.29,4.32,4.29
68,Zoe,Grant,T02,200,30.03,30.03,30.03
126,Lily,Morrison,T01,150,25.0,25.0,25.0
126,Lily,Morrison,T03,600,2:10.3,2:10.3,2:10.3
26,Cayla,Coulter,T02,200,29.31,29.31,
293,Evan,McInnes,F03,LJ,2.37,2.37,
293,Evan,McInnes,T02,200,34.47,34.47,34.47
235,Elliot,Frame,T04,800,1:59.11,1:56.47,1:59.11
310,Emmanuel,Nyamekye,T02,200,22.96,22.96,22.96
228,Oliver,Elliott,T04,800,2:09.07,2:09.07,2:09.07
306,Declan,Murray,T02,200,24.60,23.94,24.60
306,Declan,Murray,T04,800,2:00.52,1:53.74,2:00.52
8,Lucy,Barron,T02,200,27.83,27.25,
71,Breagha,Hastie,T04,800,2:19.07,2:19.07,2:19.07
251,Murdo,Hastie,T04,800,2:00.95,2:00.95,2:00.95
230,Scott,Evans,T02,200,27.42,27.42,
332,Finlay,Sharp,T04,800,2:11.59,2:10.48,2:11.59
333,Lewis,Sharp,F03,LJ,4.41,4.41,4.41
333,Lewis,Sharp,T02,200,31.22,31.22,31.22
141,Arabella,Payne,F03,LJ,2.90,2.90,
141,Arabella,Payne,T02,200,,,
220,Finlay,Cunningham,T02,200,23.50,23.18,23.50
36,Keira,Davidson,T03,600,2:16.6,2:16.6,2:16.6
41,Teria,Desi,F03,LJ,3.15,3.15,3.15
41,Teria,Desi,T02,200,30.3,30.3,30.3
321,Austin,Purdie,F03,LJ,3.86,3.86,3.86
321,Austin,Purdie,T02,200,30.37,30.37,30.37
315,Myles,Oliphant,F02,LJ,,,
315,Myles,Oliphant,T03,600,,,
314,Fletcher,Oliphant,F03,LJ,,,
314,Fletcher,Oliphant,T04,800,,,
206,Nathan,Brown,T04,800,,,
75,Kenzi,Hunter,T02,200,30.32,30.28,30.32
246,Colm,Hackett,T04,800,2:23.59,2:23.59,2:23.59
95,Chloe,Leslie,F02,LJ,2.66,2.78,2.66
95,Chloe,Leslie,T01,150,26.95,26.95,
39,Eilidh,De Klerk,T02,200,25.23,24.83,25.23
156,Noemi,Service,T01,150,23.59,24.54,23.59
156,Noemi,Service,T03,600,2:21.5,2:17.94,2:21.5
96,Eloise,Leslie,F03,LJ,3.86,3.86,3.86
96,Eloise,Leslie,T02,200,31.87,31.87,31.87
52,Joella,Esson,T02,200,34.07,34.07,
52,Joella,Esson,T04,800,2:44.0,2:44.0,2:44.0
51,Darcy,Esson,T02,200,32.97,32.97,
51,Darcy,Esson,T04,800,2:53.4,2:53.4,2:53.4
229,Theodore,Esson,F02,LJ,,,
229,Theodore,Esson,T01,150,27.18,27.18,
254,Alex,Henthorn,T04,800,1:59.96,1:59.96,1:59.96
50,Chloe,Esson,T02,200,33.84,33.84,
50,Chloe,Esson,T04,800,,,
257,Tom,Hilton,T04,800,2:09.98,2:09.98,2:09.98
348,Stan,Walker,T02,200,28.19,23.83,28.19
35,Catherine,Davidson,T02,200,35.51,35.51,
256,Alex,Hilton,T04,800,2:25.34,2:25.34,2:25.34
42,Isla,Dickson,F03,LJ,3.49,3.49,3.49
42,Isla,Dickson,T02,200,36.0,36.0,
350,Christopher,Watt,T02,200,28.89,28.89,
208,Blake,Burchill,T04,800,2:05.24,2:05.24,2:05.24
66,Reeva,Grant,F03,LJ,4.77,4.77,4.77
66,Reeva,Grant,T02,200,27.62,27.62,27.62
224,Pete,Dyer,T04,800,,,
67,Vivienne,Grant,T01,150,,,
67,Vivienne,Grant,T03,600,2:07.52,2:07.01,2:07.52
243,Angus,Gould,T02,200,22.50,21.93,
27,Hannah,Cox,T04,800,2:48.9,2:32.57,
57,Charlie,Frew,T02,200,30.91,29.17,30.91
83,Morven,Kenny,T02,200,27.15,27.66,27.15
82,Annabelle,Kennedy,T04,800,2:56.93,2:56.93,2:56.93
142,Emma,Pedrana,T02,200,25.01,25.01,25.01
78,Clara,Jackson,F02,LJ,3.21,3.21,3.21
78,Clara,Jackson,T01,150,,,
49,Sophie,Edwards,F03,LJ,,,
49,Sophie,Edwards,T02,200,,,
145,Francesca,Queen,F02,LJ,3.52,3.52,
145,Francesca,Queen,T03,600,2:02.16,2:02.16,
215,Richard,Clark,T02,200,30.14,26.61,30.14
150,Josephine,Ripley,T02,200,,,
170,Hannah,Taylor,T04,800,2:08.63,2:08.42,2:08.63
271,Flynn,Kirton,T01,150,,,
271,Flynn,Kirton,T03,600,2:09.91,2:06.10,2:09.91
171,Millie,Taylor,T02,200,33.1,33.1,
171,Millie,Taylor,T04,800,2:28.60,2:28.60,2:28.60
355,Angus,Wilkinson,T04,800,1:55.95,1:55.51,1:55.95
211,Sonny,Campbell,T02,200,22.99,22.81,
94,Eva,Lane,F03,LJ,4.35,4.35,4.35
94,Eva,Lane,T02,200,28.74,28.74,28.74
40,Abigail,Deacon,T02,200,25.95,25.95,25.95
330,Alastair,Scott,T04,800,1:56.69,1:56.69,1:56.69
177,Imogen,Turner,T04,800,2:19.34,2:19.34,2:19.34
266,Murray,Irvine,F02,LJ,3.81,4.07,3.81
266,Murray,Irvine,T01,150,23.21,23.21,
345,Sam,Thomson,T02,200,26.46,26.46,26.46
282,Daniel,Manson,T04,800,2:47.01,2:47.01,2:47.01
54,Amelia,Ferrario,T02,200,,,
54,Amelia,Ferrario,T04,800,3:08.29,3:08.29,3:08.29
186,Cerys,Wright,T04,800,2:15.89,2:13.28,2:15.89
85,Ava,King,T02,200,,,
85,Ava,King,T04,800,,,
113,Flora,Mayer,F02,LJ,2.92,2.92,2.92
113,Flora,Mayer,T01,150,26.20,26.20,
22,Lucy,Chadha,T02,200,26.95,26.80,26.95
299,Innes,Milne,T03,600,,,
93,Anna,Lane,F02,LJ,3.03,3.44,3.03
93,Anna,Lane,T01,150,24.30,24.30,24.30
89,Frances,Kirton,F01,LJ,3.76,3.76,
89,Frances,Kirton,T04,800,2:38.59,2:36.16,2:38.59
222,Charlie,Deacon,T02,200,28.48,28.48,28.48
91,Heidi Alice,Laing,T02,200,29.08,29.08,29.08
172,Sarah,Taylor,T04,800,2:21.23,2:15.43,2:21.23
9,Allyssa,Bennet,F03,LJ,3.93,3.93,3.93
9,Allyssa,Bennet,T02,200,31.33,31.33,
114,Martha,Mayer,F02,LJ,3.22,3.22,
114,Martha,Mayer,T03,600,2:18.4,2:18.4,2:18.4
196,Coinneach,Barnett,F02,LJ,3.68,3.68,3.68
196,Coinneach,Barnett,T01,150,24.04,24.04,
55,Sophia,Ferrario,T02,200,,,
55,Sophia,Ferrario,T04,800,3:22.6,3:22.6,3:22.6
77,Emily,Inglis,T02,200,28.68,28.68,28.68
274,Jack,Laverty,T04,800,2:28.65,2:27.11,2:28.65
308,Riley,Napier,T02,200,,,
182,Isabella,Wilson,T04,800,2:19.13,2:19.13,2:19.13
297,Brodie,Merry,T01,150,,,
297,Brodie,Merry,T03,600,,,
301,Struan,Milne,T04,800,2:17.95,2:17.95,2:17.95
10,Emilia,Bicknell,T03,600,,,
359,Gregor,Wright,T04,800,2:28.41,2:27.40,2:28.41
25,Zoe,Coull,T02,200,30.36,30.15,30.36
25,Zoe,Coull,T04,800,2:32.80,2:32.80,2:32.80
131,Juno,Neal,T04,800,2:42.25,2:40.70,
270,Ross,Kinkade,T02,200,23.70,23.70,23.70
174,Emily,Thomson,T02,200,29.42,28.67,29.42
11,Rachael,Bicknell,T04,800,,,
233,James,Ferrario,T01,150,,,
233,James,Ferrario,T03,600,,,
216,Matthew,Cox,T02,200,23.14,23.14,23.14
279,Harris,Mackie,T02,200,22.08,21.69,22.08
264,Fraser,Inglis,F02,LJ,3.59,3.59,3.59
341,Robin,Snedden,T02,200,23.01,22.36,23.01
7,Rowena,Barnett,F01,LJ,4.02,4.02,4.02
7,Rowena,Barnett,T02,200,28.55,28.55,28.55
169,Emily,Taylor,T04,800,2:17.82,2:17.82,2:17.82
106,Grace,Macdonald,T04,800,2:09.80,2:09.80,2:09.80
197,Lachlan,Barnett,F03,LJ,3.91,3.91,3.91
197,Lachlan,Barnett,T02,200,29.68,29.68,29.68
159,Ella,Shepherd,T04,800,2:44.54,2:42.11,2:44.54
223,Calum,Dick,T04,800,2:00.35,1:58.32,2:00.35
101,Mara,Lowe,T01,150,,,
101,Mara,Lowe,T03,600,1:59.1,1:59.1,1:59.1
198,Ruaraidh,Barnett,T02,200,25.26,25.26,
300,Moray,Milne,T04,800,2:44.42,2:44.42,
23,Louisa,Collum,T04,800,2:33.15,2:33.15,2:33.15
100,Laima,Lowe,T04,800,3:01.5,3:01.5,3:01.5
344,Daniel,Sutherland,T04,800,1:57.69,1:57.69,1:57.69
239,Lewis,Gaffney,F02,LJ,,,
239,Lewis,Gaffney,T03,600,,,
24,Madeleine,Collum,T04,800,3:09.44,3:09.44,
356,Josh,Wood,T04,800,2:03.31,2:03.31,2:03.31
269,Seb,Jellema,T04,800,2:28.71,2:28.71,2:28.71
260,Mateo,Hughes,T02,200,23.06,22.26,23.06
37,Olivia,Davidson,F02,LJ,3.23,3.23,
37,Olivia,Davidson,T01,150,26.48,26.48,
70,Freya,Hamilton,F02,LJ,3.37,3.37,
70,Freya,Hamilton,T01,150,23.02,23.02,
34,Aimee,Davidson,F03,LJ,3.90,3.90,3.90
34,Aimee,Davidson,T02,200,30.88,30.84,30.88
105,Anise,Macaulay Orr,T04,800,2:14.35,2:10.58,2:14.35
248,Connor,Harcus,T02,200,23.18,22.64,23.18
86,Lucy,Kinnear,F02,LJ,3.05,3.05,3.05
86,Lucy,Kinnear,T01,150,,,
285,Michael,Marden,T04,800,3:01.98,3:00.60,
125,Kerry,Morris,F01,LJ,4.67,5.45,4.67
284,Harry,Marden,F02,LJ,2.64,2.64,
284,Harry,Marden,T01,150,27.42,27.42,
16,Iona,Bremner,T04,800,2:31.82,2:31.82,
247,Bobby,Harcus,T02,200,23.09,23.04,23.09
119,Hannah,McMeechan,F01,LJ,4.20,4.20,4.20
119,Hannah,McMeechan,T02,200,30.88,30.69,30.88
102,Rosa,Mabon,T04,800,2:29.3,2:29.3,2:29.3
276,Gavin,Lee,T04,800,2:43.56,2:43.56,2:43.56
189,Aydin,Agh-Atabay,T02,200,26.67,26.67,26.67
205,George,Brown,T02,200,34.3,34.3,
73,Emma,Higgins,T02,200,29.27,29.27,29.27
207,Scott,Brown,T02,200,32.99,32.99,
74,Emma,Horne,T01,150,,,
311,Richard,O Grady,T02,200,,,
240,Blair,Gilchrist,T01,150,,,
240,Blair,Gilchrist,T03,600,1:59.13,1:59.13,
287,Alex,Martin,T04,800,2:58.6,2:58.6,
147,Ella,Reid,F03,LJ,4.16,4.21,4.16
147,Ella,Reid,T02,200,28.91,28.91,28.91
179,Niamh,Watterston,T02,200,28.73,28.72,28.73
283,Gareth,Marchant,T02,200,28.31,27.96,28.31
323,Lewis,Reid,T02,200,27.01,27.01,27.01
187,Margot,Wyrwoll,T04,800,2:20.74,2:19.98,2:20.74
328,Nouh,Saddiq,F02,LJ,,,
328,Nouh,Saddiq,T01,150,,,
163,Aria,Spence,T01,150,23.69,23.69,23.69
79,Phoebe,Jones,T04,800,2:35.78,2:35.78,2:35.78
302,Fraser,Morris,T04,800,2:02.86,1:57.99,2:02.86
65,Isla,Gordon,T01,150,,,
65,Isla,Gordon,T03,600,,,
286,Jacob,Marshall,T04,800,2:13.75,2:13.75,2:13.75
250,Danny,Harris,T04,800,2:23.11,2:23.11,2:23.11
110,Isla,Macrae,T01,150,,,
110,Isla,Macrae,T03,600,2:17.5,2:17.5,2:17.5
143,Elena,Polnay,T04,800,2:31.91,2:31.91,2:31.91
161,Charlotte,Smith,T02,200,27.59,27.59,
2,Victoria,Anestik,T02,200,27.00,27.00,27.00
53,Rebecca,Evans,T04,800,,,
347,Joe,Tunnicliffe,T04,800,,,
181,Esme,Wilson,F02,LJ,2.43,2.43,2.43
181,Esme,Wilson,T03,600,2:25.2,2:25.2,2:25.2
313,Bezalel,Olalekan,F02,LJ,,,
313,Bezalel,Olalekan,T01,150,,,
56,Honor,Ford,T02,200,27.11,27.11,27.11
136,Odunayo (Ayo),Olalekan,F01,LJ,3.64,3.64,
33,Elizabeth Gabriella,David,F02,LJ,2.96,2.96,2.96
33,Elizabeth Gabriella,David,T01,150,,,
202,Jaxon,Boyle,T02,200,29.74,29.23,29.74
202,Jaxon,Boyle,T04,800,2:25.99,2:25.99,2:25.99
17,Leah,Buchan,T04,800,2:20.12,2:20.12,2:20.12
18,Maya,Buchan,T02,200,28.62,28.62,28.62
152,Skye,Robertson,T04,800,2:21.13,2:21.13,2:21.13
227,Jude,Elliott,T04,800,2:21.85,2:21.85,2:21.85
268,Mac,Jamieson,T04,800,2:31.1,2:31.1,2:31.1
188,Costa,Adeyemi,T01,150,21.52,21.52,21.52
72,Sophia,Hawke,T01,150,,,
184,Amanda,Woodrow,T04,800,2:27.19,2:19.6,2:27.19
84,Poppy,Kerr,T04,800,,,
38,Sophia-Belle,Daye,F01,LJ,4.78,4.79,4.78
12,Rebecca,Bowden,T02,200,26.04,25.68,26.04
59,Ava,Gaffney,T02,200,27.47,27.02,27.47
122,Emma,Millar,T02,200,29.92,27.93,
278,Thomas,MacAskill,T04,800,2:01.93,2:01.93,2:01.93
352,Robbie,Welsh,T04,800,1:58.80,1:58.31,1:58.80
351,Irvine,Welsh,T04,800,2:05.18,2:05.18,2:05.18
121,Beth,Mcwilliam,T02,200,26.74,26.74,
44,Emma,Dooey,T02,200,31.45,31.45,
335,Ben,Silver,T02,200,28.07,27.87,28.07
137,Kirsty,Oliver,T02,200,30.54,29.26,30.54
319,Nate,Patterson,T01,150,23.87,23.87,
343,Cooper,Stewart,T02,200,,,
329,Gregor,Samson,T04,800,1:57.09,1:57.09,1:57.09
175,Lucy,Thomson,F01,LJ,3.81,3.81,3.81
175,Lucy,Thomson,T02,200,29.14,29.14,29.14
167,Ava,Starrs,T04,800,2:36.68,2:36.68,2:36.68
21,Katie,Cessford,T04,800,,,
204,Carlo,Brown,T04,800,2:12.52,2:12.52,2:12.52
5,Anna,Balfour-Melville,T02,200,,,
6,Isla,Balfour-Melville,T02,200,27.50,27.50,27.50
277,Sam,Lesley,T04,800,1:58.09,1:56.80,
320,Matthew,Power,T02,200,24.72,22.79,24.72
118,Sophia,McLachlan,T04,800,2:27.39,2:27.39,2:27.39
165,Luciana,Starkey,T04,800,2:36.19,2:36.19,2:36.19
166,Orla,Starkey,T01,150,25.67,25.67,
14,Lexie,Boyd,T04,800,2:34.62,2:34.62,2:34.62
13,Lana,Boyd,T04,800,,,
15,Libby,Boyd,T03,600,2:03.59,2:02.89,2:03.59
185,Emma,Wragg,T02,200,30.96,30.96,30.96
43,Emelia,Don,T03,600,2:06.3,2:06.3,2:06.3
358,Alfie,Wragg,T02,200,,,
48,Rosie,Dyson,T04,800,2:47.4,2:47.4,2:47.4
292,Oliver,McDonald,F01,LJ,4.22,4.22,4.22
292,Oliver,McDonald,T02,200,41.4,41.4,
291,Ian,McDonald,T02,200,24.70,22.66,24.70
203,Thomas,Brennan,T02,200,23.01,22.93,23.01
140,Isobel,Patterson,T04,800,2:30.86,2:30.86,2:30.86
200,Alex,Bellingham,T04,800,2:27.78,2:27.78,2:27.78
64,Yasmin,Giwa,T01,150,23.32,23.32,23.32
195,Grant,Baillie,T04,800,2:11.2,1:57.7,2:11.2
112,Lana,Mapara,T02,200,26.83,26.83,26.83
4,Zoe,Baillie,T04,800,2:18.63,2:18.63,2:18.63
194,Ben,Baillie,T04,800,2:01.91,2:01.91,
115,Kayla,McCrindle,T02,200,30.18,30.18,30.18
318,Tega,Orovwuje,T01,150,22.80,22.80,
138,Karo,Orovwuje,T02,200,29.16,29.16,29.16
272,Pierre-Yves,Koenig,T04,800,1:56.83,1:56.83,1:56.83
130,Akira,Nagda,T03,600,2:17.41,2:15.05,2:17.41
128,Blanka,Murawska,T02,200,,,
157,Blake,Sharp,T01,150,,,
157,Blake,Sharp,T03,600,2:12.3,2:10.95,2:12.3
324,Mason,Riddell,T01,150,,,
324,Mason,Riddell,T03,600,,,
134,Millie,O'Neill,T04,800,2:19.25,2:18.38,2:19.25
294,Sam,Mccarthy,T04,800,2:18.3,2:18.3,
81,Isabella,Kelly,T04,800,2:40.5,2:40.5,
281,Joshua,Manners-Berry,T02,200,,,
176,Natasha,Turnbull,T02,200,27.35,27.35,27.35
1,Katie,Ablett,T02,200,28.48,28.35,28.48
325,Blair,Ritchie,T02,200,27.40,27.40,27.40
238,John,Frood,T04,800,2:03.87,2:02.28,
192,Marcus,Archer,T02,200,23.00,22.48,23.00
237,Jack,Frood,T03,600,1:54.72,1:54.72,
58,Grace,Frood,T04,800,2:53.81,2:42.2,2:53.81
226,Justin,Ekeh,T02,200,23.01,23.01,23.01
190,Euan,Andrews,T04,800,2:16.14,2:16.14,
144,Lily,Pritchard,T04,800,2:38.48,2:38.48,
340,Rory,Smith,T02,200,23.90,23.90,23.90
162,Orla,Smith,T01,150,,,
241,Jack,Gillon,T04,800,2:07.36,2:07.36,2:07.36
88,Amy,Kirkpatrick,T04,800,2:14.21,2:13.53,2:14.21
20,Sophie,Cassie,T04,800,2:33.26,2:33.26,2:33.26
214,Callum,Cassie,T04,800,2:29.60,2:29.60,2:29.60
244,Cole,Gray,T04,800,2:25.56,2:25.56,2:25.56
3,Melissa,Ashelby,T04,800,2:40.00,,
225,David,Edelman,T02,200,30.77,30.40,30.77
209,Callum,Butterworth,T04,800,2:11.59,2:11.59,
219,Dermot,Cummins,T04,800,2:02.83,1:57.19,
258,Matthew,Holden,T04,800,1:57.96,1:56.05,1:57.96
46,Kate,Douglas,T02,200,32.92,32.02,32.92
46,Kate,Douglas,T04,800,2:54.03,2:54.03,2:59.0
76,Sophie,Imlach,T04,800,2:27.01,2:26.91,2:27.01
342,Lochlann,Steele,T02,200,22.97,22.30,22.97
263,Alex,Imlach,T04,800,2:18.76,2:18.76,2:18.76
231,Struan,Fairbairn,T02,200,28.21,28.21,28.21
231,Struan,Fairbairn,T04,800,2:34.67,2:34.67,2:34.67
160,Lena,Skrzydlewska,T04,800,,,
288,Adam,McAllister,T02,200,25.01,25.01,25.01
242,Thomas,Gornall,T04,800,2:22.64,2:22.64,
354,Alfie,Whyte,T04,800,2:18.9,2:18.9,2:18.9
296,Rory,Mcintosh,T03,600,,,
124,Imogen,Montgomery,T04,800,2:52.00,2:52.00,
178,Iona,Watson,T02,200,29.90,29.90,29.90
349,Campbell,Watson,T02,200,26.90,26.90,26.90
312,Simon,Okiti,T02,200,22.02,21.72,22.02
232,Samuel,Fenton,T02,200,24.31,24.31,24.31
265,Corey,Ingram,T04,800,,,
357,Jamie,Work,T04,800,1:58.15,1:58.15,1:58.15
218,Jesse,Cumings,T04,800,2:01.51,2:01.51,
261,Ronald,Hunter,T02,200,26.68,23.91,26.68
322,Ewan,Purves,T02,200,22.47,22.45,22.47
305,Charlie,Murray,T02,200,22.89,22.89,22.89
304,Archie,Murray,T01,150,,,
61,Georgia,Gent,T01,150,23.02,23.02,23.02
346,John,Tindal,T02,200,25.58,24.74,25.58
252,Oliver,Hastie,T04,800,2:05.07,2:05.07,
31,Ava Rose,Curtis,T04,800,2:27.48,2:27.48,2:27.48
151,Zoe,Roberts,T02,200,27.23,27.15,27.23
307,Calum,Murrow,T02,200,22.78,22.78,
249,Zach,Harrington,T04,800,1:59.87,1:59.87,
62,Harriet,Gibb,T02,200,29.73,29.71,29.73
267,Alexander,James,T04,800,2:26.43,2:26.43,2:26.43
63,Zara,Gillespie,T02,200,28.61,28.61,28.61
132,Heidi,Nicholson,T02,200,29.31,29.31,
60,Mairi,Gatherer,T04,800,2:49.03,2:42.38,
108,Skye,Macgregor,T01,150,,,
108,Skye,Macgregor,T03,600,2:18.66,2:16.80,2:18.66
289,Calum,McCormick,T04,800,2:46.86,2:46.86,2:46.86
290,Luke,McCormick,T03,600,2:11.7,2:11.7,2:11.7
104,Karris,MacLennan Green,T03,600,,,
111,Natalia,Mandula,T04,800,2:53.4,2:53.4,
303,Kieran,Murphy,T02,200,24.34,24.34,24.34
336,Brodie,Simon,T02,200,28.20,28.20,
336,Brodie,Simon,T04,800,2:21.09,2:16.96,2:21.09
201,Lewis,Bogle,T01,150,33.54,33.54,
201,Lewis,Bogle,T03,600,,,
90,Cheyenne,Kolegar,T04,800,2:44.50,2:39.42,2:44.50
30,Lily,Crawford,T02,200,29.86,29.48,29.86
30,Lily,Crawford,T04,800,2:44.27,2:44.27,
275,Ethan,Lawn,T03,600,2:02.01,2:02.01,
337,Callum,Sloan,T04,800,,,
191,Alex,Archer,T04,800,3:11.5,3:11.5,
99,Amber,Lloyd-Hirst,T02,200,30.93,30.93,
173,Viktoria,Tennant,T02,200,25.70,25.70,25.70
326,Alan,Robertson,T02,200,24.53,23.09,24.53
183,Niamh,Wilson,T04,800,2:45.68,2:43.07,2:45.68
19,Evanne,Carson,T02,200,28.41,28.41,28.41
97,Imogen,Liddell,T02,200,29.50,29.50,
180,Heidi,Wilmshurst,T02,200,29.05,29.05,29.05
107,Elléra,Macfarlane,T03,600,2:06.8,2:06.8,2:06.8
103,Aria,MacFarlane,T04,800,2:37.9,2:37.9,2:37.9
212,Zak,Carson,T04,800,2:30.58,2:29.57,2:30.58
139,Sandra,Osinska,T01,150,,,
139,Sandra,Osinska,T03,600,2:15.6,2:15.6,2:15.6
123,Kira,Mitchell,T04,800,2:29.22,2:29.22,2:29.22
168,Martha,Steel,T04,800,2:30.19,2:30.19,2:30.19
353,Noah,White,T02,200,25.35,25.23,25.35
262,Struan,Hunter,T01,150,25.67,25.67,25.67
262,Struan,Hunter,T03,600,2:03.8,2:03.8,2:03.8
255,Connor,Higson,T04,800,2:17.61,2:17.61,
339,Joe,Smith,T04,800,1:59.14,1:59.14,1:59.14
338,Jamie,Smith,T04,800,1:54.70,1:54.70,1:54.70
98,Emma,Livingstone,T04,800,2:24.91,2:24.91,2:24.91
153,Molly,Robinson,T02,200,29.39,29.39,
331,Zander,Scott,T02,200,23.14,22.62,23.14
127,Alice,Mourao,T04,800,2:12.15,2:12.15,2:12.15
47,Frida,Duncan,T04,800,2:52.27,2:52.27,2:52.27
120,Bethan,Mcgarey,T02,200,28.50,28.04,28.50
210,Elliot,Cameron,T04,800,2:07.61,2:07.61,2:07.61
316,David,Onatoye,T02,200,27.38,27.38,27.38
317,Joshua,Onatoye,T02,200,27.23,27.23,27.23
45,Carly,Douglas,T04,800,3:01.95,3:01.95,3:01.95
69,Ella,Hackett,T02,200,31.52,31.52,31.52
69,Ella,Hackett,T04,800,2:48.05,2:48.05,2:48.05
80,Ella,Kay,T01,150,,,
80,Ella,Kay,T03,600,2:36.6,2:36.6,2:36.6
259,Robert,Horton,T02,200,23.62,23.62,23.62
28,Grace,Craw,T01,150,,,
28,Grace,Craw,T03,600,,,
92,Sophia,Laing,T02,200,32.70,32.70,32.70
92,Sophia,Laing,T04,800,,,
245,Felix,Gray,T02,200,23.62,24.21,23.62
116,Erin,McGurk,T02,200,25.32,25.32,25.32
155,Catriona,Scott,T04,800,2:37.79,2:32.51,
117,Poppy,McKnight Livingstone,T04,800,,,
221,Fred,Currie,T04,800,2:16.16,2:16.16,2:16.16
213,Charlie,Carstairs,T02,200,23.78,23.12,
327,Samuel,Robertson,T04,800,2:31.13,2:31.13,
295,Scott,Mcclung,T04,800,2:04.18,2:04.18,2:04.18
234,Ewan,Foubister,T04,800,2:01.57,2:01.57,
146,Isla,Reekie,T04,800,2:25.65,2:25.65,2:25.65
129,Isla,Murray,T02,200,30.99,30.99,30.99
193,Richard,Arthurs,T02,200,23.48,23.48,
32,Olivia,Darwin,T04,800,2:31.88,2:31.88,2:31.88
"""

if __name__ == '__main__':
    run()
