import hashlib


def int_hash_str(input_string: str) -> int:
    # Convert the string to bytes
    bytes_string = input_string.encode()

    # Create a SHA256 hash object
    hash_object = hashlib.sha256(bytes_string)

    # Hex digest the hash and convert it to an integer
    unique_int = int(hash_object.hexdigest(), 16)

    return unique_int
