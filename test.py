import requests
from requests.auth import HTTPBasicAuth
import json

def fake_data():
    required_field = {
        "FullName": "dasf121",
        "PassWord": "1234",
    }
    # required_field = {
    #     "FullName": "asdf",
    #     "PassWord": "",
    # }
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
        # 'CustomerNo': data['data']['CustomerNo'],
        'begin_date': '2018-05-25',
        'end_date': '2018-05-26',
    }
    # resp = requests.get(
    #     'http://localhost:5050/api/v1/order_list',
    #     auth=HTTPBasicAuth(data['data']['token'], "111"),
    #     data=get_data
    # )
    resp = requests.get(
        'http://localhost:5050/api/v1/order_list',
        # auth=HTTPBasicAuth("123", "111"),
        # data=get_data
    )

    print(resp.content)

    return {'data':resp.json()['data'], 'token':data['data']['token']}


def post_new_order():
    data = user_test()
    print(data)
    post_data = {
        'order_details': [
            {
                "ConsumerNo": data['data']['CustomerNo'],
                "Count": 10,
                "Size": 129,
            },
            {
                "ConsumerNo": data['data']['CustomerNo'],
                "Count": 99,
                "Size": 130,
            },
        ],
    }

    resp = requests.post(
        'http://localhost:5050/api/v1/order_list',
        auth=HTTPBasicAuth(data['data']['token'], "111"),
        json=post_data
    )

    return resp.json()

def get_order_detail_list():
    data = get_order_list()
    print(data)
    get_data = {'OrderID': data['data'][0]['id']}
    resp = requests.get(
        'http://localhost:5050/api/v1/order_detail_list',
        auth=HTTPBasicAuth(data['token'], "111"),
        data=get_data
    )
    print(resp.status_code, resp.json())


def get_archives_list():
    data = user_test()
    print(data)
    # get_data = {
    #     'page': 4,
    #     'per_page': 50
    # }
    resp = requests.get(
        'http://localhost:5050/api/v1/archives_list',
        auth=HTTPBasicAuth(data['data']['token'], "111"),
        # data=get_data
    )

    for d in resp.json()['data']:
        print(d)
    return {'data':resp.json()['data']}


if __name__ == '__main__':
    print(get_order_list())