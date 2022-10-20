import hmac
import hashlib
import logging
import os
import io
import sys

try:
    import httplib
except:
    import http.client
import json

from time import time

_api_key = "0b0982ab4e13cc5990f05814a45a4658"

_api_secret = "ACB4EDKG70PVUYQPY631K3QKH8XJD2VRELN2V8J3XW2V676G6Q6L3GUY103ZMT7HB4A3FDWQU1GN42F9"
_endpoint = "www.coinspot.com.au"


# def _request(path, postdata):
#     nonce = int(time() * 10000)
#     postdata["nonce"] = nonce
#     params = json.dumps(postdata, separators=(",", ":"))
#     signed_msg = _get_signed_request(params)
#     headers = {}
#     headers["key"] = _api_key
#     headers["sign"] = signed_msg
#     conn = http.client.HTTPConnection(_endpoint)
#     conn.request("POST", path, params, headers)
#     response = conn.getresponse()
#     response_data = response.read()
#
#     return response_data

def _request(path, postdata):
    nonce = int(time() * 1000000)
    postdata["nonce"] = nonce
    params = json.dumps(postdata, separators=(",", ":"))
    signed_message = _get_signed_request(params)
    headers = {}
    headers["Content-type"] = "application/json"
    headers["Accept"] = "text/plain"
    headers["key"] = _api_key
    headers["sign"] = signed_message


    conn = http.client.HTTPSConnection(_endpoint)

    response_data = '{"status":"invalid","error": "Did not make request"}'
    try:
        conn.request("POST", path, params, headers)
        response = conn.getresponse()

        # print response.status, response.reason
        response_data = response.read()

        conn.close()
    except IOError as error:

            error_text = "Attempting to make request I/O error({0}): {1}".format(
                error.errno, error.strerror
            )

            response_data = '{"status":"invalid","error": "' + error_text + '"}'
    except:
        exit("Unexpected error: {0}".format(sys.exc_info()[0]))

    return response_data


def _get_signed_request(data):
    # print(hmac.new(_api_secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest())
    return hmac.new(
        str(_api_secret).encode("utf-8"),
        data.encode("utf-8"),
        hashlib.sha512,
        ).hexdigest()


def balances():
    """
    List my balances
    :return:
        - **status** - ok, error
        - **balances** - object containing one property for each coin with your balance for that coin.
    """
    return _request("/api/my/balances", {})


def quote_sell(cointype, amount):
    request_data = {"cointype": cointype, "amount": amount}
    return _request("/api/quote/sell", request_data)


def quotebuy(cointype, amount):

    """
    Quick buy quote
    Fetches a quote on rate per coin and estimated timeframe to buy an amount of coins
    :param cointype:
        the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
    :param amount:
        the amount of coins to sell
    :return:
        - **status** - ok, error
        - **quote** - the rate per coin
        - **timeframe** - estimate of hours to wait for trade to complete (0 = immediate trade)
    """
    request_data = {"cointype": cointype, "amount": amount}
    return _request("/api/quote/buy", request_data)


def quotesell(cointype, amount):
    """
    Quick sell quote
    Fetches a quote on rate per coin and estimated timeframe to sell an amount of coins
    :param cointype:
        the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
    :param amount:
        the amount of coins to sell
    :return:
        - **status** - ok, error
        - **quote** - the rate per coin
        - **timeframe** - estimate of hours to wait for trade to complete (0 = immediate trade)
    """
    request_data = {"cointype": cointype, "amount": amount}
    return _request("/api/quote/sell", request_data)

def spot():
    return _request("/api/spot", {})

def my_btc_addr(cointype):
    path = "/my/coin/deposit"
    request_data = {"cointype": cointype}
    return _request(path, request_data)


def history():
    path = "/api/ro/my/sendreceive"
    request_data = {}
    response = _request(path, request_data)

    return response

def bytes_to_json(bytes):
    mybytes = bytes
    fix_bytes_value = mybytes.replace(b"'", b'"')
    my_json = json.load(io.BytesIO(fix_bytes_value))
    return my_json


def print_transations():
    obj = bytes_to_json(history())
    return json.dumps(obj)


print(quotesell("BTC", 10))