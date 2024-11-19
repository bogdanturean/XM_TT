import time
import requests
import jsonpath
def testserverrunning_responsetime_TC_001():

    start_time = time.time()
    url = "http://127.0.0.1:8080/"
    v_response = requests.get(url)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"API response time: {execution_time} seconds")

    assert v_response.status_code == 200
    assert execution_time < 1, f"API response time exceeded threshold: {execution_time} seconds"


def testgetorders_responsetime_TC_001():
    url = "http://127.0.0.1:8080/orders"
    stok_1 = "ETH"
    quantity_1 = 2
    postresponse_1 = requests.post(url, json={"stoks": stok_1, "quantity": quantity_1}).json()
    v_responseid_1 = jsonpath.jsonpath(postresponse_1, 'id')[0]

    start_time = time.time()

    v_response = requests.get(url)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"API response time: {execution_time} seconds")

    assert v_response.status_code == 200
    assert execution_time < 1, f"API response time exceeded threshold: {execution_time} seconds"

def testaddorder_responsetime_TC_001():
    url = "http://127.0.0.1:8080/orders"

    start_time = time.time()
    v_response = requests.post(url, json={"stoks": "USD", "quantity": 3.2})
    end_time = time.time()
    execution_time = end_time - start_time

    assert v_response.status_code == 201
    assert execution_time < 1, f"API response time exceeded threshold: {execution_time} seconds"