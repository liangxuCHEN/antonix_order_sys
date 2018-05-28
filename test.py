import requests, json, sys
from requests.auth import HTTPBasicAuth


def fake_data():
    required_field = {
        "FullName": "dasf121",
        "PassWord": "1234",
    }
    # required_field = {
    #     'CustomerID': 2,
    #     'PassWord': '4321',
    #     'new_password': '1234'
    # }

    return required_field


def simple_get_test(username_or_token, passwd):
    #resp = requests.post('http://192.168.3.172:5050/api/v1/afterservice/orders', json=fake_waixie())
    data = {
        'username': username_or_token,
        'password': passwd
    }
    resp = requests.get('http://localhost:5050/api/test', auth=HTTPBasicAuth(data['username'], data['password']))
    print(resp.status_code, resp.content)


def user_test():
    #resp = requests.post('http://192.168.3.172:5050/api/v1/afterservice/orders', json=fake_waixie())

    resp = requests.post('http://localhost:5050/api/v1/open/user', json=fake_data())
    data = resp.json()
    return data


def user_change_password():
    resp = requests.put('http://localhost:5050/api/v1/open/user', json=fake_data())
    print(resp.json())


def get_order_list():
    data = user_test()
    print(data)
    get_data = {
        'CustomerNo': data['data']['CustomerNo']
    }
    resp = requests.get(
        'http://localhost:5050/api/v1/order_list',
        auth=HTTPBasicAuth(data['data']['token'], "111"),
        data=get_data
    )

    print(resp.status_code, resp.json())

if __name__ == '__main__':
    get_order_list()