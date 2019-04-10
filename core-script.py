# export GOOGLE_APPLICATION_CREDENTIALS=~/Desktop/firestore/serviceAccountKey.json

# ---------- imports ----------
from math import inf, sin, cos, sqrt, atan2, radians
import requests
import json
import pandas

# ---------- Firebase ----------
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import GeoPoint

cred = credentials.Certificate('serviceAccountKey.json')
def_app = firebase_admin.initialize_app(cred)
db = firestore.Client()


# ----------- Distance Functions --------------
def distance(point1, point2):

    lat1 = radians(point1[0])
    lon1 = radians(point1[1])
    lat2 = radians(point2[0])
    lon2 = radians(point2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # approximate radius of earth in km
    R = 6378.0

    distance = R * c

    return distance


# ------- Decode Polylines --------
def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}
    while index < len(polyline_str):
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates


# ---------- Get PiInfo ---------
def getPiInfo():
    db_piInfo = db.collection('PiInfo')
    for info in db_piInfo.get():
        yield info


# ---------------- Main Function ----------------------
print('Detecting requests ...')


def greencorridor():
    while True:
        doc_GC = db.collection('CreateAdminSideGC')
        for req in doc_GC.where('status', '==', 'unfinished').get():
            req_dict = req.to_dict()
            print(f'request = {req_dict}\n')
            range = float(req_dict['range'])
            req_location = req_dict['source']
            req_location = [req_location.latitude, req_location.longitude]
            dest_location = req_dict['destination']
            dest_location = [dest_location.latitude, dest_location.longitude]

            # req.update({
            #     'status': 'ongoing',
            # })

            db.collection('CreateAdminSideGC').document(req.id).update({
                'status': 'ongoing',
            })

            # ------- Finding Nearest Driver -------
            nearest = inf
            nearest_driver, driverUndict = None, None
            doc_driver = db.collection('Driver')
            for driver in doc_driver.where('d_login_status', '==', 'true').get():
                driverUndict = driver
                driver = driver.to_dict()
                d_location = [float(driver['d_latitude']), float(driver['d_longitude'])]
                dist = distance(d_location, req_location)
                if dist < nearest:
                    nearest = dist
                    nearest_driver = driver
            print(f'nearest driver = {nearest_driver}')

            # ------- Driver to source -------
            G_API2 = 'I won\'t tell you'
            dri2so_link = f'https://maps.googleapis.com/maps/api/directions/json?origin={nearest_driver["d_latitude"]},{nearest_driver["d_longitude"]}&destination={req_location[0]},{req_location[1]}&key={G_API2}'
            print(dri2so_link)
            data = requests.get(dri2so_link).text
            data = json.loads(data)
            path_list1 = []

            for i in data['routes'][0]['legs'][0]['steps']:
                lattitude = i['start_location']['lat']
                longitude = i['start_location']['lng']
                polyline = i['polyline']['points']
                path_list1.append([lattitude, longitude])
                for point in decode_polyline(polyline):
                    path_list1.append(list(point))
            # print(path_list1)
            print()
            # -------- Source to Destination ---------------
            so2dest_link = f'https://maps.googleapis.com/maps/api/directions/json?origin={req_location[0]},{req_location[1]}&destination={dest_location[0]},{dest_location[1]}&key={G_API2}'
            print(so2dest_link)
            data = requests.get(so2dest_link).text
            data = json.loads(data)
            path_list2 = []

            for i in data['routes'][0]['legs'][0]['steps']:
                lattitude = i['start_location']['lat']
                longitude = i['start_location']['lng']
                polyline = i['polyline']['points']
                path_list2.append([lattitude, longitude])
                for point in decode_polyline(polyline):
                    path_list2.append(list(point))
            # print(path_list2)
            print()

            # ------------- Inersection of PiInfo with path_list1 -------------
            pi_activate1 = []
            for point1 in path_list1:
                for pi in pi_info_list:
                    if distance(point1, pi['location']) < 0.07:
                        pi_activate1.append(pi['id'])
            pi_activate1 = pandas.unique(pi_activate1)
            # print(pi_activate1)
            # break

            # ------------- Inersection of PiInfo with path_list2 -------------
            pi_activate2 = []
            for point2 in path_list2:
                for pi in pi_info_list:
                    if distance(point2, pi['location']) < 0.07:
                        pi_activate2.append((pi['id'], pi['location']))
            pi_activate2 = pandas.unique(pi_activate2)
            # print(pi_activate2)

            # ---------- Signalling PIs -----------
            doc_Activate = db.collection('Activate')
            for i, signal in enumerate(pi_activate2):
                if i == len(pi_activate2) - 1:
                    Next = 'Last'
                else:
                    Next = pi_activate2[i + 1][0]

                print('signalling pis', Next)
                # break
                doc_Activate.document(signal[0]).set({
                    'driverID': driverUndict.id,
                    'nextID': Next,
                    'range': range,
                })
        # break


# -------- Executing getPiInfo() ----------
# print('Getting PiInfo ...\n')
pi_info_list = []
for info in getPiInfo():
    info_dict = info.to_dict()
    pi_info_list.append({
        'id': info.id,
        'sides': info_dict['sides'],
        'pi_name': info_dict['pi_name'],
        'location': (info_dict['location'].latitude, info_dict['location'].longitude)
    })


# --------- Calling main function -------------
greencorridor()
