import requests
import base64
from django.conf import settings

authorization_key = "Basic " + base64.encodestring(''+settings.SG_USER+':'+settings.SG_PWD+'').replace('\n', '')
headers = {'Authorization': authorization_key}


def get_contact_lists():
    CONTACTS_ENDPOINT = "https://api.sendgrid.com/v3/contactdb/lists"
    response = requests.get(CONTACTS_ENDPOINT, headers=headers)
    contact_lists = {}
    if response.status_code == 200:
        contact_list_data = response.json()["lists"]
        for item in contact_list_data:
            contact_lists[item["name"]] = str(item["id"])
        return contact_lists


def create_contact(email_address):
    CONTACTS_ENDPOINT = "https://api.sendgrid.com/v3/contactdb/recipients"
    payload = [{"email": email_address}]
    response = requests.post(CONTACTS_ENDPOINT, headers=headers, json=payload).json()
    return response["persisted_recipients"][0]


def create_contact_list(category_name):
    CONTACTS_ENDPOINT = "https://api.sendgrid.com/v3/contactdb/lists"
    payload = {"name": category_name}
    response = requests.post(CONTACTS_ENDPOINT, headers=headers, json=payload).json()
    return response["id"]
