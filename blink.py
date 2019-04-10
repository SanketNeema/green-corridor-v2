# export GOOGLE_APPLICATION_CREDENTIALS=~/Desktop/green-corridor-v2/serviceAccountKey.json
# cd Desktop/green-corridor-v2/
# ------- RPi ---------
import RPi.GPIO as GPIO
import time

pi_info = [23152670, 'Palasia Square', 22.7238405, 75.8867305]
# pi_info = [28571426, 'Geeta Bhavan Square', 22.718382, 75.884271]
# pi_info = [30004812, 'Shivaji Square', 22.711393356323242, 75.88285064697266]

# -------- imports ---------
from math import inf, sin, cos, sqrt, atan2, radians

# ---------- Firebase ----------
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import GeoPoint

cred = credentials.Certificate('serviceAccountKey.json')
def_app = firebase_admin.initialize_app(cred)
db = firestore.Client()


# ---------- Get PiInfo ---------
def getPiInfo():
    db_piInfo = db.collection('PiInfo')
    for info in db_piInfo.get():
        yield info


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


# ------- get driver location --------
def getDriverLocation(driverID):
    driver_location = db.collection('Driver')
    d_locatoin = driver_location.document(driverID).get().to_dict()
    d_lat = float(d_locatoin['d_latitude'])
    d_lon = float(d_locatoin['d_longitude'])
    return [d_lat, d_lon]


# -------- Pin Setup ---------
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)


# --------- 4 side functions ------------
def side1():
    GPIO.output(16, False)
    GPIO.output(18, True)
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(29, True)
    GPIO.output(31, False)
    GPIO.output(38, True)
    GPIO.output(40, False)
    time.sleep(5)


def side2():
    GPIO.output(16, True)
    GPIO.output(18, False)
    GPIO.output(11, False)
    GPIO.output(13, True)
    GPIO.output(29, True)
    GPIO.output(31, False)
    GPIO.output(38, True)
    GPIO.output(40, False)
    time.sleep(5)


def side3():
    GPIO.output(16, True)
    GPIO.output(18, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(29, False)
    GPIO.output(31, True)
    GPIO.output(38, True)
    GPIO.output(40, False)
    time.sleep(5)


def side4():
    GPIO.output(16, True)
    GPIO.output(18, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(29, True)
    GPIO.output(31, False)
    GPIO.output(38, False)
    GPIO.output(40, True)
    time.sleep(5)
# ----------- End side functions -------------


# -------- increment turn ---------
turn = 0


def incTurn():
    global turn
    turn = (turn + 1) % 4


# ------ Blink -----
def blink(side):
    # control = [side1, side2, side3, side4]
    # if side is not None:
    #     control(side)()
    # else:
    #     control(turn)
    # incTurn()

    if side == 1:
        print('side1')
        side1()
    elif side == 2:
        print('side2')
        side2()
    elif side == 3:
        print('side3')
        side3()
    elif side == 4:
        print('side4')
        side4()
    else:
        if turn == 0:
            print('else 0')
            side1()
        elif turn == 1:
            print('else 1')
            side2()
        elif turn == 2:
            print('else 2')
            side3()
        elif turn == 3:
            print('else 3')
            side4()
    incTurn()
    print(turn, side)


# ------------ Main Function ------------
while True:
    print('Loop started')
    doc_GC = db.collection('Activate')
    checkSignal = doc_GC.document(str(pi_info[0])).get()
    checkSignalDict = checkSignal.to_dict()
    if checkSignalDict is not None:
        # print(checkSignalDict)    # {'driverID': 'raghav@gmail.com', 'nextID': '28571426'}
        if checkSignalDict['nextID'] != 'Last':
            whichSide = db.collection('PiInfo').document(str(pi_info[0])).get().to_dict()['sides'][checkSignalDict['nextID']]
        else:
            # db.collection('CreateAdminSideGC').document(checkSignal.id).update({
            #     'status': 'finished',
            # })
            whichSide = None
        print(whichSide)
        print(checkSignalDict['driverID'])
        while distance(getDriverLocation(checkSignalDict['driverID']), pi_info[2:]) > checkSignalDict['range']:
            print('blink normal', getDriverLocation(checkSignalDict['driverID']), pi_info[2:])
            blink(None)
            # break
        while distance(getDriverLocation(checkSignalDict['driverID']), pi_info[2:]) < checkSignalDict['range']:
            print('blink red', distance(getDriverLocation(checkSignalDict['driverID']), pi_info[2:]))
            blink(whichSide)
    else:
        blink(None)


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
