import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("sandwich-orders-firebase-adminsdk-atm32-bee6c475c8.json")
firebase_admin.initialize_app(cred)

ISO_FORMAT = "YYYY-MM-DD"
today = "2020-12-31"  # moment.now().format(ISO_FORMAT)


def get_orders():
    return list(map(
        lambda order: order.to_dict(),
        firestore.client().collection("allOrders").where("date", "==", today).get()
    ))


def get_users():
    users_dict = {}
    raw_data = firestore.client().collection("userData").get()
    for doc in raw_data:
        users_dict[doc.id] = doc.to_dict()
    return users_dict


def get_app_data():
    return firestore.client().document("appData/appConstants").get().to_dict()
