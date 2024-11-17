import requests
import jsonpath
import json
import uuid
from enum import Enum
class Status(Enum):
    pending = 'pending'
    executed = 'executed'
    canceled = 'canceled'


class Stoks(Enum):
    euro = 'EURO'
    usd = 'USD'
    etg = 'ETH'


fpointer = open('newOrderPOST.json', mode='r')
inputdata = fpointer.read()
inputdatajson = json.loads(inputdata)

def clearDB():
    url = "http://127.0.0.1:8080/orders"
    order = requests.get(url)
    order_json = json.loads(order.text)
    if len(order_json) > 0 and order.status_code == 200:
        for order_idx in range(0, len(order_json)):
            order_id = jsonpath.jsonpath(order_json[order_idx], 'id')
            requests.delete(url + "/" + order_id[0])

def countordersinDB():
    url = "http://127.0.0.1:8080/orders"
    order = requests.get(url)
    order_json = json.loads(order.text)
    if order.status_code == 200:
        return len(order_json)
    else:
        return 0

class TestServer:

    def testserverrunning_TC_001(self):
        # Test: check server is running
        url ="http://127.0.0.1:8080/"
        v_response=requests.get(url)
        assert v_response.status_code == 200
        assert v_response.text=='["Server Running"]'

class TestRetreiveOrders:
    def testgetorders_TC_001(self):
        #Positive scenario
        # Test: check get orders endpoint with orders in DB
        #Test setup:

        clearDB()
        url ="http://127.0.0.1:8080/orders"

        #Test execution
        stok_1 = "ETH"
        quantity_1 = 2
        postresponse_1 = requests.post(url, json={"stoks": stok_1, "quantity": quantity_1}).json()
        v_responseid_1 = jsonpath.jsonpath(postresponse_1, 'id')[0]


        stok_2 = "ETH"
        quantity_2 = 3
        postresponse_2=requests.post(url,json={"stoks": stok_2,"quantity": quantity_2}).json()
        v_responseid_2 = jsonpath.jsonpath(postresponse_2, 'id')[0]

        v_response=requests.get(url)
        v_responsecode=v_response.status_code

        #Expected result
        assert v_responsecode == 200

        assert v_response.json()[0].get('id') == v_responseid_1
        assert v_response.json()[0].get('stoks') == stok_1
        assert v_response.json()[0].get('quantity') == quantity_1
        assert v_response.json()[0].get('status') == 'executed' or v_response.json()[0].get('status') == 'pending'

        assert v_response.json()[1].get('id') == v_responseid_2
        assert v_response.json()[1].get('stoks') == stok_2
        assert v_response.json()[1].get('quantity') == quantity_2
        assert v_response.json()[1].get('status') == 'executed' or v_response.json()[0].get('status') == 'pending'

    def testgetorders_TC_002(self):
        # Negative scenario
        # Test: check get orders endpoint with no orders in DB
        clearDB()
        #delete all existings order in DB
        url = "http://127.0.0.1:8080/orders"


        v_response=requests.get(url)
        v_responsecode=v_response.status_code
        v_responsedetail_json = json.loads(v_response.text)
        v_responsedetail=jsonpath.jsonpath(v_responsedetail_json,'detail')

        assert v_responsecode == 404
        assert v_responsedetail == ['Order not found']

class TestPlaceOrder:

    def testaddorder_TC_001(self):

        orderscountin = countordersinDB()
        url ="http://127.0.0.1:8080/orders"
        v_response=requests.post(url,json=inputdatajson)
        v_responsecode=v_response.status_code
        v_responsebody_json = json.loads(v_response.text)
        v_responseid = jsonpath.jsonpath(v_responsebody_json, 'id')[0]
        v_responsestock = jsonpath.jsonpath(v_responsebody_json, 'stoks')[0]
        v_responsequantity = jsonpath.jsonpath(v_responsebody_json, 'quantity')[0]
        v_responsestatus = jsonpath.jsonpath(v_responsebody_json, 'status')[0]

        orderscount = countordersinDB()
        assert v_responsecode == 201
        assert orderscount == orderscountin+1
        assert uuid.UUID(v_responseid, version=4).version == 4
        assert v_responsestock in Stoks._value2member_map_
        assert v_responsequantity>0
        assert v_responsestatus in Status._value2member_map_

    def testaddorder_TC_002(self):

        orderscountin = countordersinDB()
        url ="http://127.0.0.1:8080/orders"
        v_response=requests.post(url,json={	"stoks": "X","quantity": 1})
        v_responsecode=v_response.status_code
        orderscount = countordersinDB()
        v_responsedetail_json = json.loads(v_response.text)
        v_responsedetail = jsonpath.jsonpath(v_responsedetail_json, 'detail')
       # print(v_response.text)
        assert v_responsecode == 400
        assert orderscount == orderscountin
        assert v_responsedetail == ['Invalid input']

    def testaddorder_TC_003(self):

        orderscountin = countordersinDB()
        url ="http://127.0.0.1:8080/orders"
        v_response=requests.post(url,json={	"stoks": "ETH","quantity": 0})
        v_responsecode=v_response.status_code
        v_responsedetail_json = json.loads(v_response.text)
        v_responsedetail = jsonpath.jsonpath(v_responsedetail_json, 'detail')
        orderscount = countordersinDB()
       # print(v_response.text)
        assert v_responsecode == 400
        assert orderscount == orderscountin
        assert v_responsedetail == ['Invalid input']

    def testaddorder_TC_004(self):

        orderscountin = countordersinDB()
        url ="http://127.0.0.1:8080/orders"
        v_response=requests.post(url,json={	"stoks": "ETH","quantity": 1})
        v_responsecode=v_response.status_code
        orderscount = countordersinDB()
        #print(v_response.text)
        assert v_responsecode == 201
        assert orderscount == orderscountin + 1

def tes1tdeleteorder_TC_001():

    url ="http://127.0.0.1:8080/orders"
    order = requests.get(url)
    order_json = json.loads(order.text)
    order_id = jsonpath.jsonpath(order_json[0],'id')
    #print(order_id[0])
    v_response=requests.delete(url+"/"+order_id[0])
    v_responsecode=v_response.status_code
    assert v_responsecode == 200