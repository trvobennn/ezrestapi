"""
Simple REST API for handling IOUs

Includes unit test
"""

import json


class RestAPI:
    def __init__(self, database=None):
        if database is not None:
            self.database = database

    def get(self, url, payload=None):
        # 'get' method using url = '/users' and json payload
        copy_set = {"users": []}
        use_url = url[1:]

        if url == "/users":
            if payload is None:
                # if no payload, return whole list
                if "users" in self.database:
                    copy_set["users"] = self.database[use_url]
                    return json.dumps(copy_set)
                if "users" not in self.database:
                    return json.dumps(self.database)
            elif payload is not None:
                # if payload, return specified user(s)
                payload = json.loads(payload)
                if "user" in payload.keys():
                    raise ValueError("For get method, you must enter 'users'")
                if "users" in self.database:
                    for u_set in self.database[use_url]:
                        for indx, user in enumerate(payload["users"]):
                            ind_1 = 0
                            if user in u_set.values():
                                ind_1 += self.database[use_url].index(u_set)
                                copy_set["users"].append(self.database[use_url][ind_1])
                    return json.dumps(copy_set)

    def post(self, url, payload=None):
        use_ = "users"
        copy_set = {"users": []}

        # '/add' branch of post method
        if url == "/add":
            # need json payload
            if payload is None:
                return 'N/A'
            elif payload is not None:
                payload = json.loads(payload)
                if "users" in self.database:
                    for u_set in self.database[use_]:
                        if payload["user"] in u_set.values():
                            raise ValueError("User found. Enter unique user")
                        if payload["user"] not in u_set.values():
                            user_info = {'name': payload["user"], 'owes': {}, 'owed_by': {}, 'balance': 0.0}
                            self.database["users"].append(user_info)
                            return json.dumps(user_info)
                    if len(self.database[use_]) == 0:
                        user_info = {'name': payload["user"], 'owes': {}, 'owed_by': {}, 'balance': 0.0}
                        self.database["users"].append(user_info)
                        return json.dumps(user_info)

        if url == "/iou":
            if payload is None:
                return 'N/A'
            elif payload is not None:
                payload = json.loads(payload)
                if "users" in self.database:
                    for u_set in self.database[use_]:
                        # u_set is the dictionary containing user info
                        # first deal with 'lender'
                        if payload["lender"] in u_set.values():
                            # establishing whether lender name is in list of values for given dictionary
                            # abbreviate the indexing function which will be used often in this branch
                            # credits_ and debits_ keep track of total amounts in 'owes' and 'owed_by'
                            # make dict item in lender user with borrower name and amount, or update it if it exists
                            ind_1 = self.database[use_].index(u_set)
                            credits_ = 0
                            debits_ = 0
                            self.database[use_][ind_1]['owed_by'][payload['borrower']] = payload['amount']
                            for name in self.database[use_][ind_1]['owes']:
                                # iterate through list of names in 'owes' to see if borrower appears in both
                                # if borrower appears in both and is less in the 'owed_by' set, pop it
                                # add to total debits_ with the int/float value paired with key/name
                                if name == payload['borrower'] and name in self.database[use_][ind_1]['owes'].keys():
                                    if self.database[use_][ind_1]['owed_by'][name] < \
                                         self.database[use_][ind_1]['owes'][name]:
                                        self.database[use_][ind_1]['owes'][name] -= \
                                            self.database[use_][ind_1]['owed_by'][name]
                                        self.database[use_][ind_1]['owed_by'].pop(name)

                                debits_ += self.database[use_][ind_1]['owes'][name]
                            for name in self.database[use_][ind_1]['owed_by']:
                                credits_ += self.database[use_][ind_1]['owed_by'][name]
                                if name == payload['borrower'] and name in self.database[use_][ind_1]['owes'].keys():
                                    if self.database[use_][ind_1]['owed_by'][name] > \
                                            self.database[use_][ind_1]['owes'][name]:
                                        self.database[use_][ind_1]['owed_by'][name] -= \
                                            self.database[use_][ind_1]['owes'][name]
                                        self.database[use_][ind_1]['owes'].pop(name)


                            self.database[use_][ind_1]['balance'] = round(credits_ - debits_,3)
                            # check if balance is null and whether same name appears in both owed_by and owes sections
                            if self.database[use_][ind_1]['balance'] == 0 and payload['borrower'] in self.database[use_][ind_1]['owed_by']:
                                if payload['borrower'] in self.database[use_][ind_1]['owes']:
                                    self.database[use_][ind_1]['owed_by'].pop(payload['borrower'])
                                    self.database[use_][ind_1]['owes'].pop(payload['borrower'])
                            copy_set['users'].append(u_set)

                        # next deal with 'borrower' in mirror fashion
                        if payload["borrower"] in u_set.values():
                            ind_2 = self.database[use_].index(u_set)

                            credits_ = 0
                            debits_ = 0
                            self.database[use_][ind_2]['owes'][payload['lender']] = payload['amount']
                            for name in self.database[use_][ind_2]['owes']:
                                if name == payload['lender'] and name in self.database[use_][ind_2]['owed_by'].keys():
                                    if self.database[use_][ind_2]['owes'][name] > \
                                            self.database[use_][ind_2]['owed_by'][name]:
                                        self.database[use_][ind_2]['owes'][name] -= self.database[use_][ind_2]['owed_by'][name]
                                        self.database[use_][ind_2]['owed_by'].pop(name)

                                debits_ += self.database[use_][ind_2]['owes'][name]
                            for name in self.database[use_][ind_2]['owed_by']:
                                credits_ += self.database[use_][ind_2]['owed_by'][name]
                                if name == payload['lender'] and name in self.database[use_][ind_2]['owes'].keys():
                                    if self.database[use_][ind_2]['owes'][name] < \
                                            self.database[use_][ind_2]['owed_by'][name]:
                                        self.database[use_][ind_2]['owed_by'][name] -= self.database[use_][ind_2]['owes'][name]
                                        self.database[use_][ind_2]['owes'].pop(name)

                            self.database[use_][ind_2]['balance'] = round(credits_ - debits_,3)
                            if self.database[use_][ind_2]['balance'] == 0 and payload['lender'] in self.database[use_][ind_2]['owed_by']:
                                if payload['lender'] in self.database[use_][ind_2]['owes']:
                                    self.database[use_][ind_2]['owed_by'].pop(payload['lender'])
                                    self.database[use_][ind_2]['owes'].pop(payload['lender'])
                            copy_set['users'].append(u_set)

                    return json.dumps(copy_set)





import unittest

""" Inputs must be in following format:
get, 'get' - url='users', (optional) payload={'users':[names_in_db]}
post, 'add' - url='/add', payload={'user':name_not_in_db}
post, 'iou' - url='/iou', payload={'lender': name1_in_db, 'borrower': name2_in_db, 'amount': 0.00}
Database must preserve the nested structure below for this app 
"""

class Rest_test(unittest.TestCase):
    db1 = {
        "users": [
            {"name": "Adam", "owes": {}, "owed_by": {"Diane": 12.50}, "balance": 12.50},
            {"name": "Bob", "owes": {"Carol": 8.87}, "owed_by": {}, "balance": -8.87},
            {"name": "Carol", "owes": {}, "owed_by": {"Bob": 8.87}, "balance": 8.87},
            {"name": "Diane", "owes": {"Adam": 12.50}, "owed_by": {}, "balance": -12.50}
        ]
    }



    def test_no_users(self):
        db = {'users': []}
        api = RestAPI(db)
        api_response = api.get('/users')
        self.assertEqual(json.loads(api_response), db)

    def test_add_user(self):
        db = {'users': []}
        api = RestAPI(db)
        api_payload = json.dumps({'user': 'Adam'})
        api_response = api.post('/add', api_payload)
        expected_resp = {'name': 'Adam', "owes": {}, "owed_by": {}, "balance": 0.0}
        self.assertDictEqual(json.loads(api_response), expected_resp)

    def test_get_user(self):
        db = {
        "users": [
            {"name": "Jim", "owes": {}, "owed_by": {}, "balance": 0.0},
            {"name": "Steve", "owes": {}, "owed_by": {}, "balance": 0.0}
        ]
    }
        api = RestAPI(db)
        api_response = api.get('/users', json.dumps({'users': ['Steve']}))
        expected_resp = {'users': [{"name": "Steve", "owes": {}, "owed_by": {}, "balance": 0.0}]}
        self.assertDictEqual(json.loads(api_response), expected_resp)

    def test_get_both_users(self):
        db = {
        "users": [
            {"name": "Jim", "owes": {}, "owed_by": {}, "balance": 0.0},
            {"name": "Steve", "owes": {}, "owed_by": {}, "balance": 0.0}
        ]
    }
        api = RestAPI(db)
        api_response = api.get('/users', json.dumps({'users': ['Jim','Steve']}))
        expected_resp = {'users': [{"name": "Jim", "owes": {}, "owed_by": {}, "balance": 0.0},
            {"name": "Steve", "owes": {}, "owed_by": {}, "balance": 0.0}]}
        self.assertDictEqual(json.loads(api_response), expected_resp)

    def test_no_balance(self):
        db = {
        "users": [
            {"name": "Adam", "owes": {}, "owed_by": {}, "balance": 0.0},
            {"name": "Bob", "owes": {"Chuck": 3.0}, "owed_by": {}, "balance": -3.0},
            {"name": "Chuck", "owes": {}, "owed_by": {"Bob": 3.0}, "balance": 3.0}
        ]
    }
        api = RestAPI(db)
        payload = json.dumps({'lender': 'Bob', 'borrower': 'Chuck', 'amount': 3.00})
        api_response = api.post('/iou', payload)
        expected_resp = {
        "users": [
            {"name": "Bob", "owes": {}, "owed_by": {}, "balance": 0.0},
            {"name": "Chuck", "owes": {}, "owed_by": {}, "balance": 0.0}
        ]
    }
        self.assertDictEqual(json.loads(api_response), expected_resp)

    def test_lender_negative(self):
        db = {
        "users": [
            {"name": "Adam", "owes": {}, "owed_by": {}, "balance": 0.0},
            {"name": "Bob", "owes": {"Chuck": 3.0}, "owed_by": {}, "balance": -3.0},
            {"name": "Chuck", "owes": {}, "owed_by": {"Bob": 3.0}, "balance": 3.0}
        ]
    }
        api = RestAPI(db)
        payload = json.dumps({'lender': 'Bob', 'borrower': 'Chuck', 'amount': 1.00})
        api_response = api.post('/iou', payload)
        expected_resp = {
            "users": [
                {"name": "Bob", "owes": {'Chuck': 2.00}, "owed_by": {}, "balance": -2.00},
                {"name": "Chuck", "owes": {}, "owed_by": {'Bob': 2.00}, "balance": 2.00}
            ]
        }
        self.assertDictEqual(json.loads(api_response), expected_resp)

    def test_borrower_negative(self):
        db = {
        "users": [
            {"name": "Adam", "owes": {}, "owed_by": {}, "balance": 0.0},
            {"name": "Bob", "owes": {"Chuck": 3.0}, "owed_by": {}, "balance": -3.0},
            {"name": "Chuck", "owes": {}, "owed_by": {"Bob": 3.0}, "balance": 3.0}
        ]
    }
        api = RestAPI(db)
        payload = json.dumps({'lender': 'Bob', 'borrower': 'Chuck', 'amount': 6.00})
        api_response = api.post('/iou', payload)
        expected_resp = {
            "users": [
                {"name": "Bob", "owes": {}, "owed_by": {'Chuck': 3.00}, "balance": 3.00},
                {"name": "Chuck", "owes": {'Bob': 3.00}, "owed_by": {}, "balance": -3.00}
            ]
        }
        self.assertDictEqual(json.loads(api_response), expected_resp)

    def test_new_balance(self):
        db = Rest_test.db1
        api = RestAPI(db)
        payload = json.dumps({'lender': 'Adam', 'borrower': 'Diane', 'amount': 4.50})
        api_response = api.post('/iou', payload)
        expected_resp = {
            "users": [
                {"name": "Adam", "owes": {}, "owed_by": {'Diane': 4.50}, "balance": 4.50},
                {"name": "Diane", "owes": {'Adam': 4.50}, "owed_by": {}, "balance": -4.50}
            ]
        }
        self.assertDictEqual(json.loads(api_response), expected_resp)

    def test_iou_2(self):
        db = {
        "users": [
            {"name": "Adam", "owes": {}, "owed_by": {"Diane": 4.50}, "balance": 4.50},
            {"name": "Bob", "owes": {"Carol": 8.87}, "owed_by": {}, "balance": -8.87},
            {"name": "Carol", "owes": {}, "owed_by": {"Bob": 8.87}, "balance": 8.87},
            {"name": "Diane", "owes": {"Adam": 4.50}, "owed_by": {}, "balance": -4.50}
        ]
    }
        api = RestAPI(db)
        payload = json.dumps({'lender': 'Bob', 'borrower': 'Adam', 'amount': 2.50})
        api_response = api.post('/iou', payload)
        expected_resp = {
            "users": [
                {"name": "Adam", "owes": {'Bob': 2.50}, "owed_by": {'Diane': 4.50}, "balance": 2.00},
                {"name": "Bob", "owes": {"Carol": 8.87}, "owed_by": {'Adam': 2.50}, "balance": -6.37}
            ]
        }
        self.assertDictEqual(json.loads(api_response), expected_resp)

if True:
    unittest.main()
