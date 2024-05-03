import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import string
from faker import Faker

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
fake = Faker()


def generate_random_user():
    full_name = fake.name()
    email = fake.email()
    phone_number = ''.join(random.choices(string.digits, k=10))
    age = random.randint(18, 80)
    state = random.choice([
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
        "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
        "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
        "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Delhi",
        "Lakshadweep", "Puducherry"
    ])

    return {
        "fullName": full_name,
        "emailID": email,
        "phoneNumber": phone_number,
        "age": age,
        "state": state
    }


def populate_firestore():
    users_ref = db.collection("Users")
    for _ in range(80):
        user_data = generate_random_user()
        users_ref.add(user_data)

if __name__ == "__main__":
    populate_firestore()
