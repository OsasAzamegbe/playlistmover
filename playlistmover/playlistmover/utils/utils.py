import base64


def encode_string_base64(message: str) -> str:
    """
    Encode string in base64
    """
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message
