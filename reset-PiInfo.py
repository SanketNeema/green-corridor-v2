# export GOOGLE_APPLICATION_CREDENTIALS=~/Desktop/gitHub/projects/green-corridor-v2/serviceAccountKey.json

import sqlite3

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import GeoPoint

######## Firebase ########
cred = credentials.Certificate('./serviceAccountKey.json')
def_app = firebase_admin.initialize_app(cred)
db = firestore.Client()
doc_ref = db.collection('PiInfo')

######## SQLite3 ########
conn = sqlite3.connect('gc.db')
c = conn.cursor()

####### Drop table #######
c.execute("""drop table pi_info""")

######## Data ########
pi_info_fb = [  # Firebase
    {
        'id': 23152670,
        'name': 'Palasia Square',
        'location': (22.7238405, 75.8867305),
        'sides': {
            '28571426': 1,
            '84453996': 2,
            '68872537': 3,
            '41470006': 4,
        },
    },
    {
        'id': 28571426,
        'name': 'Geeta Bhavan Square',
        'location': (22.718382, 75.884271),
        'sides': {
            '30004812': 1,
            '91661588': 2,
            '23152670': 3,
        },
    },
    {
        'id': 32781349,
        'name': 'GPO Square',
        'location': (22.7074117, 75.8788266),
        'sides': {
            '62973742': 1,
            '30004812': 3,
        }
    },
    {
        'id': 62973742,
        'name': 'Indira Pratima',
        'location': (22.704345, 75.876260),
        'sides': {
            '71884396': 1,
            '32781349': 3,
        }
    },
    {
        'id': 71884396,
        'name': 'Navlakha Square',
        'location': (22.6989073, 75.8779443),
        'sides': {
            '62973742': 3,
        }
    },
    {
        'id': 30004812,
        'name': 'Shivaji Square',
        'location': (22.711393356323242, 75.88285064697266),
        'sides': {
            '32781349': 1,
            '91661588': 2,
            '28571426': 3,
            '53108269': 4,
        },
    },
    {
        'id': 84453996,
        'name': 'Indraprastha Square',
        'location': (22.722846, 75.882380),
        'sides': {
            '28571426': 1,
            '15645842': 2,
            '23152670': 4,
        },
    },
    {
        'id': 63087039,
        'name': 'Industry House Squre',
        'location': (22.727497, 75.888091),
        'sides': {
            '23152670': 1,
            '68872537': 3,
        }
    },
    {
        'id': 61202114,
        'name': 'Lantern Square',
        'location': (22.724677, 75.874212),
        'sides': {
            '15645842': 1,
        }
    },
    {
        'id': 15645842,
        'name': 'High Court Square',
        'location': (22.720626, 75.873911),
        'sides': {
            '89197025': 2,
            '61202114': 3,
            '84453996': 4,
        },
    },
    {
        'id': 89197025,
        'name': 'Regal Square',
        'location': (22.719919, 75.870968),
        'sides': {
            '91661588': 1,
            '15645842': 4,
        },
    },
    {
        'id': 91661588,
        'name': 'Madhumilan Square',
        'location': (22.714157, 75.874363),
        'sides': {
            '30004812': 1,
            '89197025': 3,
            '28571426': 4,
        },
    },
    {
        'id': 53108269,
        'name': 'Agricalture College',
        'location': (22.709623, 75.890748),
        'sides': {
            '30004812': 2,
            '69764261': 4,
        },
    },
    {
        'id': 68872537,
        'name': 'LIG Square',
        'location': (22.733705, 75.890114),
        'sides': {
            '23152670': 1,
            '40502481': 3,
        },
    },
    {
        'id': 40502481,
        'name': 'MR9 Square',
        'location': (22.742567, 75.892867),
        'sides': {
            '68872537': 1,
            '29715322': 3,
        },
    },
    {
        'id': 29715322,
        'name': 'Vijay Nagar Square',
        'location': (22.751030, 75.895422),
        'sides': {
            '40502481': 1,
            '57863362': 4,
        },
    },
    {
        'id': 57863362,
        'name': 'Raddison Square',
        'location': (22.749293, 75.903496),
        'sides': {
            '42552625': 1,
            '29715322': 2,
        },
    },
    {
        'id': 42552625,
        'name': 'Robot Square',
        'location': (22.741220, 75.902471),
        'sides': {
            '78201869': 1,
            '57863362': 3,
        },
    },
    {
        'id': 78201869,
        'name': 'Khajarana Square',
        'location': (22.731709, 75.902254),
        'sides': {
            '30482517': 1,
            '42552625': 3,
        },
    },
    {
        'id': 30482517,
        'name': 'Bangali Square',
        'location': (22.719863, 75.906197),
        'sides': {
            '69764261': 1,
            '78201869': 3,
        },
    },
    {
        'id': 69764261,
        'name': 'Pipliyahana Square',
        'location': (22.705992, 75.905848),
        'sides': {
            '53108269': 2,
            '30482517': 3,
        },
    },
]


pi_info_sqlite3 = []
pi_info_sqlite3.append("""create table pi_info(pi_id int(10) primary key, pi_name varchar(30), pi_lat float(50,20)not null, pi_long float(50, 20)not null)""")
for info in pi_info_fb:
    pi_info_sqlite3.append(f'insert into pi_info values({info["id"]}, \'{info["name"]}\', {", ".join(str(x) for x in info["location"])})')

####### Set-up / Insert########
for info in pi_info_fb:
    doc_ref.document(str(info['id'])).set({
        # 'pi_id': 28571426,
        'location': GeoPoint(*info['location']),
        'pi_name': info['name'],
        'sides': info['sides']
    })

for info in pi_info_sqlite3:
    c.execute(info)
    # print(info)


####### get #######
# c.execute("""select * from pi_info""")
# print(c.fetchall())

for pi in doc_ref.get():
    print(f'{pi.id} = {pi.to_dict()}\n')


####### close connection #######
conn.commit()
conn.close()


####### Schemas #######
'''
Admin(
    username<PK>,
    password,
    name,
    lastname,
)

Requests(
    timestamp<epoch in secs, PK>,
    Users.username,
    status<'accepted', 'rejected', 'tbr'(default), 'completed'>, // tbr = to be respond
    latitude,
    longitude,
)

PiInfo(
    id<PK>,
    name,
    latitude,
    longitude,
    sides<map>,
)

Users(
    username<PK>,
    p_password,
    p_name,
    p_mobile,
    p_latitude,
    p_longitude,
    d_email<Driver.username, None(default)>,
)

Driver(
    username<PK>,
    d_mobile,
    d_name,
    d_password,
    d_latitude,
    d_longitude,
    p_email<User.username, ""(default)>,
)

Signal(
    id<PK>,
    Driver.username,
    nextID<'None'(if last)>,
)
'''
