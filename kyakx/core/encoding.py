import base64
import urllib.parse

def encode_payload(payload, encoding_type):
    if encoding_type == "base64":
        return base64.b64encode(payload.encode()).decode()
    elif encoding_type == "url":
        return urllib.parse.quote(payload)
    elif encoding_type == "double_url":
        return urllib.parse.quote(urllib.parse.quote(payload))
    return payload
