import base64
import datetime
import os
import random
import re
import json
import string
from typing import Optional
import nacl.encoding
import nacl.hash
from nacl.bindings import crypto_sign_ed25519_sk_to_seed
from nacl.signing import SigningKey, VerifyKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey,X25519PublicKey
from cryptography.hazmat.primitives import serialization
from pydantic import BaseModel
import requests
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad

SUBSCRIBER_ID = "dev-api2.superpe.in"




def hash_message(message):
    if isinstance(message, dict):
        # Convert the dictionary to a JSON string
        message = json.dumps(message, separators=(',', ':'))  # Compact JSON
    elif not isinstance(message, str):
        raise TypeError("Message must be a string or a dictionary")
    
    # Use a secure hashing function, such as BLAKE2b
    digest = nacl.hash.blake2b(bytes(message, 'utf-8'), digest_size=64, encoder=nacl.encoding.Base64Encoder)
    return digest.decode('utf-8')

def create_signing_string(digest_base64, created=None, expires=None):
    if created is None:
        created = int(datetime.datetime.now().timestamp())
    if expires is None:
        expires = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
    signing_string = f"""(created): {created}
(expires): {expires}
digest: BLAKE-512={digest_base64}"""
    return signing_string


def sign_response(signing_key, private_key):
    private_key64 = base64.b64decode(private_key)
    seed = crypto_sign_ed25519_sk_to_seed(private_key64)
    signer = SigningKey(seed)
    signed = signer.sign(bytes(signing_key, encoding='utf8'))
    signature = base64.b64encode(signed.signature).decode()
    return signature

def verify_response(signature, signing_key, public_key):
    try:
        public_key64 = base64.b64decode(public_key)
        VerifyKey(public_key64).verify(bytes(signing_key, 'utf8'), base64.b64decode(signature))
        return True
    except Exception:
        return False


def get_filter_dictionary_or_operation(filter_string):
    filter_string_list = re.split(',', filter_string)
    filter_string_list = [x.strip(' ') for x in filter_string_list]  # to remove white spaces from list
    filter_dictionary_or_operation = dict()
    for fs in filter_string_list:
        splits = fs.split('=', maxsplit=1)
        key = splits[0].strip()
        value = splits[1].strip()
        filter_dictionary_or_operation[key] = value.replace("\"", "")
    return filter_dictionary_or_operation


def create_authorisation_header(request_body, created=None, expires=None):
    print(f"Request body before hashing: {request_body}, type: {type(request_body)}")

    created = int(datetime.datetime.now().timestamp()) if created is None else created
    expires = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()) if expires is None else expires
    hashed_message  =  hash_message(request_body)
    print("\n\n")
    print("Ondc hashed message org",hashed_message)
    print("\n\n")
    signing_key = create_signing_string(hashed_message,
                                        created=created, expires=expires)
    signature = sign_response(signing_key, private_key="AeECv5uo3b6FR6OJDY75ew7v2d6Uhhw/7YqLbZAXYfhmW/1ARRQJU8wmm7e8wSjvncHAJPrc/z2fFL+zKps3DA==")
    print("\n\n")
    print("Ondc signature org",signature)
    print("\n\n")
    subscriber_id = "dev-api2.superpe.in"
    unique_key_id = "super-124-444_unq"
    header = f'"Signature keyId="{subscriber_id}|{unique_key_id}|ed25519",algorithm="ed25519",created=' \
             f'"{created}",expires="{expires}",headers="(created) (expires) digest",signature="{signature}""'
    return header


def verify_authorisation_header(auth_header, request_body_str,
                                public_key):
    # `request_body_str` should request.data i.e. raw data string

    # `public_key` is sender's public key
    # i.e. if Seller is verifying Buyer's request, then seller will first do lookup for buyer-app
    # and will verify the request using buyer-app's public-key
    header_parts = get_filter_dictionary_or_operation(auth_header.replace("Signature ", ""))
    created = int(header_parts['created'])
    expires = int(header_parts['expires'])
    current_timestamp = int(datetime.datetime.now().timestamp())
    if created <= current_timestamp <= expires:
        signing_key = create_signing_string(hash_message(request_body_str), created=created, expires=expires)
        return verify_response(header_parts['signature'], signing_key, public_key=public_key)
    else:
        return False


def generate_key_pairs():
    signing_key = SigningKey.generate()
    private_key = base64.b64encode(signing_key._signing_key).decode()
    #print(private_key)
    public_key = base64.b64encode(bytes(signing_key.verify_key)).decode()
    inst_private_key = X25519PrivateKey.generate()
    #print(base64.b64encode(bytes(tencryption_private_key.).decode()))
    inst_public_key = inst_private_key.public_key()
    bytes_private_key = inst_private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    bytes_public_key = inst_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    encryption_private_key = base64.b64encode(bytes_private_key).decode('utf-8')
    encryption_public_key = base64.b64encode(bytes_public_key).decode('utf-8')
    return {"Signing_private_key": private_key,
            "Signing_public_key": public_key,
            "Encryption_Privatekey": encryption_private_key,
            "Encryption_Publickey": encryption_public_key}


def encrypt(encryption_private_key, encryption_public_key, null):
    private_key = serialization.load_der_private_key(
        base64.b64decode(encryption_private_key),
        password=None
    )
    public_key = serialization.load_der_public_key(
        base64.b64decode(encryption_public_key)
    )
    shared_key = private_key.exchange(public_key)
    cipher = AES.new(shared_key, AES.MODE_ECB)
    text = b'ONDC is a Great Initiative!!'
    return base64.b64encode(cipher.encrypt(pad(text,AES.block_size))).decode('utf-8')


def decrypt(encryption_private_key, encryption_public_key, cipherstring):
    private_key = serialization.load_der_private_key(
        base64.b64decode(encryption_private_key),
        password=None
    )
    public_key = serialization.load_der_public_key(
        base64.b64decode(encryption_public_key)
    )
    shared_key = private_key.exchange(public_key)
    cipher = AES.new(shared_key, AES.MODE_ECB)
    ciphertxt = base64.b64decode(cipherstring)
    # print(AES.block_size, len(ciphertxt))
    return unpad(cipher.decrypt(ciphertxt), AES.block_size).decode('utf-8')

# print(generate_key_pairs())


# print(sign_response("dev-api.superpe.in","0cwAwmLgfDSq9qrahpuUTfnBr2djrAZzABi2uw2K9oEZdGHy9EYKL1z3kIaQMEzvwGna4hjTsLdwd9jSgO9W9Q=="))

raw_text = {
    "context": {
        "domain": "nic2004:52110",
        "action": "search",
        "country": "IND",
        "city": "std:std:080",
        "core_version": "1.1.0",
        "bap_id": "dev-api2.superpe.in",
        "bap_uri": "https://dev-api2.superpe.in/backend/v2/ondc",
        "transaction_id": "supr_4OdrQzQT",
        "message_id": "msg_odputyHn",
        "timestamp": "2024-12-02T12:05:55.140024",
        "ttl": "PT30S"
    },
    "message": {
        "intent": {
            "fulfillment": {"type": "Delivery"},
            "payment": {
                "@ondc/org/buyer_app_finder_fee_type": "percent",
                "@ondc/org/buyer_app_finder_fee_amount": "3"
            }
        }
    }
}

# print(create_authorisation_header(raw_text))

raw_text = {"context":{"domain":"nic2004:52110","action":"search","country":"IND","city":"std:std:080","core_version":"1.1.0","bap_id":"dev-api2.superpe.in","bap_uri":"https://dev-api2.superpe.in/backend/v2/ondc","transaction_id":"supr_4OdrQzQT","message_id":"msg_odputyHn","timestamp":"2024-12-02T12:05:55.140024","ttl":"PT30S"},"message":{"intent":{"fulfillment":{"type":"Delivery"},"payment":{"@ondc/org/buyer_app_finder_fee_type":"percent","@ondc/org/buyer_app_finder_fee_amount":"3"}}}}


# AUTH_header = create_authorisation_header(raw_text)
# print(AUTH_header)



# print(verify_authorisation_header(AUTH_header,raw_text,"Zlv9QEUUCVPMJpu3vMEo753BwCT63P89nxS/syqbNww="))


def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class SearchRequest(BaseModel):
    type: str  # One of 'city', 'item', or 'category'
    city: Optional[str] = None
    item_name: Optional[str] = None
    category_id: Optional[str] = None
    gps: Optional[str] = None
    area_code: Optional[str] = None
    domain: Optional[str] = None
    public_key: Optional[str] = None

def search(request: SearchRequest):
    """
    Dynamically handle different types of search.
    """

    transaction_id = f"supr_{random_string()}"
    message_id = f"msg_{random_string()}"
    timestamp = datetime.datetime.now().isoformat()
    
    context = {
        "domain": request.domain,
        "action": "search",
        "country": "IND",
        "city": request.city,
        "core_version": "1.2.0",
        "bap_id": SUBSCRIBER_ID,
        "bap_uri": "https://dev-api2.superpe.in/backend/v2/ondc/on_search",
        "transaction_id": transaction_id,
        "message_id": message_id,
        "timestamp": timestamp,
        "ttl": "PT30S",
        # "key": ENCRYPTION_PUBLIC_KEY  # Add the public key here
    }

    intent = {
        # "payment": {
        #     "@ondc/org/buyer_app_finder_fee_type": "percent",
        #     "@ondc/org/buyer_app_finder_fee_amount": "3"
        # }
    }

    # Dynamically modify intent based on request type
    if request.type == "item":
        intent["item"] = {"descriptor": {"name": request.item_name}}
        if request.gps or request.area_code:
            intent["fulfillment"]["end"] = {
                "location": {
                    "gps": request.gps,
                    "address": {"area_code": request.area_code} if request.area_code else {}
                }
            }
    elif request.type == "category":
        intent["category"] = {"id": request.category_id}
        if request.gps or request.area_code:
            intent["fulfillment"]["end"] = {
                "location": {
                    "gps": request.gps,
                    "address": {"area_code": request.area_code} if request.area_code else {}
                }
            }
    elif request.type == "city":
        context["city"] = f"{request.city}"
        intent["category"] = {"id": "Foodgrains"}
        intent["fulfillment"] =  {"type": "Delivery"},
        intent["payment"] = {
            "@ondc/org/buyer_app_finder_fee_type": "percent",
            "@ondc/org/buyer_app_finder_fee_amount": "3"
        }
        intent["tags"] = [
            {
                "code": "bap_terms",
                "list": [
                    {"code": "static_terms", "value": ""},
                    {"code": "static_terms_new", "value": "https://github.com/ONDC-Official/NP-Static-Terms/buyerNP_BNP/1.0/tc.pdf"},
                    {"code": "effective_date", "value": "2023-10-01T00:00:00.000Z"}
                ]
            }
        ]



    print("\n\n")
    print("content")
    print(context)
    print("\n\n")


    print("\n\n")
    print("intent")
    print(intent)
    print("\n\n")
    payload = {
        "context": context,
        "message": {"intent": intent},
    }

    # Generate authorization header
    request_body = json.dumps(payload, separators=(',', ':'))

    # print("\n\n")
    # print(request_body)
    # print("\n\n")

    print("\n\n")
    print(json.dumps(payload))
    print("\n\n")

    auth_header = create_authorisation_header(
        request_body=request_body,
        created=None,
        expires=None
    )

    header_check = verify_authorisation_header(auth_header=auth_header,request_body_str=request_body,public_key=request.public_key)
    print(header_check)


    print("\n\n")
    print("Auth header")
    print(auth_header)
    print("\n\n")

    ondc_url = "https://staging.gateway.proteantech.in/search"
    response = requests.post(
        ondc_url,
        json=payload,
        headers={"Authorization": auth_header}
    )

    print("\n\n")
    print("Status from search")
    print(response)
    print("\n\n")
    return response.json()


request = {
  "type": "city",
  "city": "std:080",
"domain": "nic2004:52110"
}

request_body =  SearchRequest(type="city",city="std:080",domain= "ONDC:RET11")


print(search(request_body))