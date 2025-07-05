# bmcpmlib.py
# Copyright (C) Yin Yang / TikTok: Yin Yang - All Rights Reserved

import requests

__ENDPOINT_URL__ = "https://cpmnuker.anasov.ly/api"

class CPMNuker:
    def __init__(self, access_key) -> None:
        self.auth_token = None
        self.access_key = access_key

    def login(self, email, password):
        payload = { "account_email": email, "account_password": password }
        params = { "key": self.access_key }
        r = requests.post(f"{__ENDPOINT_URL__}/account_login", params=params, data=payload)
        rj = r.json()
        if rj.get("ok"):
            self.auth_token = rj.get("auth")
        return rj

    def register(self, email, password):
        payload = { "account_email": email, "account_password": password }
        params = { "key": self.access_key }
        r = requests.post(f"{__ENDPOINT_URL__}/account_register", params=params, data=payload)
        return r.json()

    def set_money(self, amount):
        payload = { "account_auth": self.auth_token, "amount": amount }
        params = { "key": self.access_key }
        r = requests.post(f"{__ENDPOINT_URL__}/set_money", params=params, data=payload)
        return r.json()

    def set_coins(self, amount):
        payload = { "account_auth": self.auth_token, "amount": amount }
        params = { "key": self.access_key }
        r = requests.post(f"{__ENDPOINT_URL__}/set_coins", params=params, data=payload)
        return r.json()

    def set_name(self, name):
        payload = { "account_auth": self.auth_token, "name": name }
        params = { "key": self.access_key }
        r = requests.post(f"{__ENDPOINT_URL__}/set_name", params=params, data=payload)
        return r.json()

    def unlock_all_cars(self):
        payload = { "account_auth": self.auth_token }
        params = { "key": self.access_key }
        r = requests.post(f"{__ENDPOINT_URL__}/unlock_all_cars", params=params, data=payload)
        return r.json()

    def clone_account(self, email, password):
        payload = {
            "account_auth": self.auth_token,
            "account_email": email,
            "account_password": password
        }
        params = { "key": self.access_key }
        r = requests.post(f"{__ENDPOINT_URL__}/clone", params=params, data=payload)
        return r.json()
