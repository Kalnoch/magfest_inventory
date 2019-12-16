#~1xxJnQ is OKAYDUDE, badge 25, and ~ixKa5g is COOLDUDE, badge 26

import json
import requests
from inventory_system.settings import UBER_AUTH_TOKEN


class ReggieInterface:
    """
    Interface code to interact with reggie
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'X-Auth-Token': UBER_AUTH_TOKEN})
        # Test URL
        # self.BASE_URL = 'https://staging-reggie.magfest.org/jsonrpc/'
        self.BASE_URL = 'https://staging-super.reggie.magfest.org/jsonrpc/'
        # Prod URL
        # self.BASE_URL = 'https://onsite.uber.magfest.org/jsonrpc/'

    def lookup_attendee_from_barcode(self, barcode):
        payload = json.dumps({"method": "barcode.lookup_attendee_from_barcode", "params": [barcode]})
        r = self.session.post(self.BASE_URL, payload)
        print(r.status_code)
        print(r.text)
        if r.status_code == 200:
            j = r.json()
            return j
        return None

    def lookup_attendee_from_badge_num(self, badge_num):
        payload = json.dumps({"method": "attendee.lookup", "params": [badge_num]})
        r = self.session.post(self.BASE_URL, payload).json()
        if r.status_code == 200:
            j = r.json()
            return j
        return None
