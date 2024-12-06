# pybase64_reddy/__init__.py

import base64

def b64encode(data: bytes) -> bytes:
    """
    Encode bytes to base64.

    Args:
        data (bytes): The bytes to encode.

    Returns:
        bytes: The base64 encoded bytes.
    """
    return base64.b64encode(data)

def b64decode(data: bytes) -> bytes:
    """
    Decode base64 bytes.

    Args:
        data (bytes): The base64 encoded bytes to decode.

    Returns:
        bytes: The decoded bytes.

    Raises:
        ValueError: If the input is not valid base64.
    """
    try:
        return base64.b64decode(data)
    except Exception as e:
        raise ValueError("Invalid base64 input") from e
