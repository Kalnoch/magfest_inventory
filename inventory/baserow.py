import requests
from inventory_system.settings import BASEROW_AUTH_TOKEN


BASE_URL = "https://baserow.magfest.net/api"
HEADERS = {
    "Authorization": BASEROW_AUTH_TOKEN,
    "Accept": "application/json",
    "Content-Type": "application/json",
}
TABLE_IDS = {
    "consoles": 1367,
    "tvs": 1368,
    "games": 1369,
    "peripherals": 1370,
    "avs": 1371,
}


def list_rows(table_id):
    data = []
    results = {
        "next": f"{BASE_URL}/database/rows/table/{table_id}/?user_field_names=true&size=200"
    }
    while results["next"]:
        results = requests.get(results["next"], headers=HEADERS).json()
        data.extend(results["results"])
    return {x['id']: x for x in data}


def get_row(table_id, row_id):
    return requests.get(f"{BASE_URL}/database/rows/table/{table_id}/{row_id}/?user_field_names=true", headers=HEADERS).json()


def list_fields(table_id):
    req = requests.get(f"{BASE_URL}/database/fields/table/{table_id}/", headers=HEADERS)
    return {x['name']: x for x in req.json()}


def update_status(table_id, row_id, status):
    req = requests.patch(f"{BASE_URL}/database/rows/table/{table_id}/{row_id}/?user_field_names=true", headers=HEADERS, json={
        "Status": status
    })
    assert req.status_code == 200


def checkout(table_id, row_id, status):
    req = requests.patch(f"{BASE_URL}/database/rows/table/{table_id}/{row_id}/?user_field_names=true",
                         headers=HEADERS,
                         json={
                             "Checked Out": status
                         })
    assert req.status_code == 200


def checkin(table_id, row_id):
    req = requests.patch(f"{BASE_URL}/database/rows/table/{table_id}/{row_id}/?user_field_names=true",
                         headers=HEADERS,
                         json={
                             "Checked Out": "Checked In"
                         })
    assert req.status_code == 200
