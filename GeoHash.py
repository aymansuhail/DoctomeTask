import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import geohash2
from datetime import datetime, timedelta


cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def generate_geohashes_within_radius(center_geohash, radius):
    geohashes = set()
    for dx in range(-radius, radius+1):
        for dy in range(-radius, radius+1):
            lat, lon = geohash2.decode(center_geohash)
            lat, lon = float(lat), float(lon)
            new_geohash = geohash2.encode(lat + dx*0.002, lon + dy*0.002, precision=6)
            if new_geohash[:3] == center_geohash[:3]:
                geohashes.add(new_geohash)
    return geohashes


def generate_structure_for_date_and_geohash(date, geohash):
    doc_ref = db.collection("geoHashStates").document(geohash)
    doc_ref.set({"geoHash": geohash, "isActive": True})


    general_slots_ref = doc_ref.collection("availableGeneralSlots").document(date.strftime("%Y%m%d"))


    time_slots = []
    current_time = 900
    while current_time <= 1800:
        time_slots.append({"available": 15, "timeSlot": current_time})
        current_time += 100

    general_slots_ref.set({"date": int(date.strftime("%Y%m%d")), "timeSlots": time_slots})


def generate_structure_for_month():
    start_date = datetime(2024, 5, 1)
    end_date = datetime(2024, 5, 31)
    central_geohash = "tepepn"

    for date in daterange(start_date, end_date):
        neighboring_geohashes = generate_geohashes_within_radius(central_geohash, 1)
        for geohash in neighboring_geohashes:
            generate_structure_for_date_and_geohash(date, geohash)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

if __name__ == "__main__":
    generate_structure_for_month()
