# export GOOGLE_APPLICATION_CREDENTIALS=~/Desktop/gitHub/projects/green-corridor-v2/serviceAccountKey.json

# THIS SCRIPT RESETS FIREBASE COLLECTIONS TO DEFAULT VALUES FOR SOME DOCUMENTS WHICH MATTERS

import sqlite3

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import GeoPoint

######## Firebase ########
cred = credentials.Certificate('./serviceAccountKey.json')
def_app = firebase_admin.initialize_app(cred)
db = firestore.Client()

######## SQLite3 ########
conn = sqlite3.connect('gc.db')
c = conn.cursor()


# ---------------Driver---------------
Drivers = [
    {
        'id': 'chunnudriver@gmail.com',     # Robot Square
        'd_latitude': '22.741220',
        'd_longitude': '75.902471',
        'd_mobile': '7987330291',
        'd_name': 'Chunnu Bakliwal',
        'd_password': 'shinchan',
        'p_email': 'neerajkumar@gmail.com',
    },
    {
        'id': 'raghav@gmail.com',   # Before Palasia Square
        'd_latitude': '22.7238405',
        'd_longitude': '75.8867305',
        'd_mobile': '7000907835',
        'd_name': 'Raghav Gupta',
        'd_password': '1231',
        'p_email': '',
    },
    {
        'id': 'sachinpatidar@gmail.com',    # Vijay Nagar
        'd_latitude': '22.751030',
        'd_longitude': '75.895422',
        'd_mobile': '9183658291',
        'd_name': 'Sachin Patidar',
        'd_password': '1234',
        'p_email': 'neerajkumar@gmail.com',
    },
]


def DriverReset():
    doc_ref = db.collection('Driver')

    for driver in Drivers:
        doc_ref.document(driver['id']).set({
            'd_latitude': driver['d_latitude'],
            'd_longitude': driver['d_longitude'],
            'd_mobile': driver['d_mobile'],
            'd_name': driver['d_name'],
            'd_password': driver['d_password'],
            'p_email': driver['p_email'],
        })
    ###### print all #######
    # for doc in doc_ref.get():
        # print(f'{doc.id} - {doc.to_dict()}')
        # print()


# ---------------Users---------------
Users = [
    {
        'id': 'makhanlal@gmail.com',    # Shivaji Square
        'p_mobile': '9103820103',
        'p_name': 'Makhanlal Chaturvedi',
        'p_password': '1234',
        'p_latitude': '22.711393356323242',
        'p_longitude': '75.88285064697266',
        'd_email': 'None',
    },
    {
        'id': 'mangilal@gmail.com',     # Indira Pratima
        'p_mobile': '8978675434',
        'p_name': 'Mangilal Halwaiwala',
        'p_password': 'mangi123',
        'p_latitude': '22.704345',
        'p_longitude': '75.874212',
        'd_email': 'None',

    },
    {
        'id': 'neerajkumar@gmail.com',  # Navlakha Square
        'p_mobile': '987654578',
        'p_name': 'Neeraj Kumar Jetha',
        'p_password': '1234',
        'p_latitude': '22.6989073',
        'p_longitude': '75.8779443',
        'd_email': 'None',
    },
]


def UsersReset():
    doc_ref = db.collection('Users')

    for user in Users:
        doc_ref.document(user['id']).set({
            'p_mobile': user['p_mobile'],
            'p_name': user['p_name'],
            'p_password': user['p_password'],
            'p_latitude': user['p_latitude'],
            'p_longitude': user['p_longitude'],
            'd_email': user['d_email'],
        })
    ###### print all #######
    # for doc in doc_ref.get():
    #     print(f'{doc.id} - {doc.to_dict()}')
    #     print()


# ---------------Requests---------------
Requests = [
    {
        'id': '1550768983',
        'username': 'mangilal@gmail.com',   # Indira pratima
        'latitude': '22.7043036',
        'longitude': '75.87648879999999',
        'status': 'completed',
    },
    {
        'id': '1550770067',
        'username': 'mangilal@gmail.com',   # GPO
        'latitude': '22.7074117',
        'longitude': '75.8788266',
        'status': 'completed',
    },
    {
        'id': '1550770631',
        'username': 'makhanlal@gmail.com',  # Shivaji Square
        'latitude': '22.711393356323242',
        'longitude': '75.88285064697266',
        'status': 'tbr',
    }
]


def RequestsReset():
    doc_ref = db.collection('Requests')

    for reqs in Requests:
        doc_ref.document(reqs['id']).set({
            'username': reqs['username'],
            'latitude': reqs['latitude'],
            'longitude': reqs['longitude'],
            'status': reqs['status'],
        })
    ##### print all #######
    # for doc in doc_ref.get():
    #     print(f'{doc.id} - {doc.to_dict()}')
    #     print()


# ---------------Call Reset functions---------------
UsersReset()
DriverReset()
RequestsReset()
