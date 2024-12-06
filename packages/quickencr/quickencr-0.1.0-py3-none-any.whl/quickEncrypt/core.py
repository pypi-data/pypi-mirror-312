from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """
    Generate a secure encryption key.
    Returns:
        bytes: A newly generated key.
    """
    return Fernet.generate_key()


def encrypt_message(message: str) -> bytes:
    """
    Encrypt a text message.
    Args:
        message (str): The message to encrypt.
        key (bytes): The encryption key.
    Returns:
        bytes: The encrypted message.
    """
    key=generate_key()
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())


def decrypt_message(token: bytes) -> str:
    """
    Decrypt an encrypted message.
    Args:
        token (bytes): The encrypted message.
        key (bytes): The encryption key.
    Returns:
        str: The decrypted message.
    """
    key=generate_key()
    cipher = Fernet(key)
    return cipher.decrypt(token).decode()


def encrypt_file(file_path: str, key: bytes, output_path: str) -> None:
    """
    Encrypt a file and save the result.
    Args:
        file_path (str): Path to the input file.
        key (bytes): The encryption key.
        output_path (str): Path to save the encrypted file.
    """
    cipher = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = cipher.encrypt(file.read())
    with open(output_path, 'wb') as output_file:
        output_file.write(encrypted_data)


def decrypt_file(file_path: str, key: bytes, output_path: str) -> None:
    """
    Decrypt an encrypted file and save the result.
    Args:
        file_path (str): Path to the encrypted file.
        key (bytes): The encryption key.
        output_path (str): Path to save the decrypted file.
    """
    cipher = Fernet(key)
    with open(file_path, 'rb') as file:
        decrypted_data = cipher.decrypt(file.read())
    with open(output_path, 'wb') as output_file:
        output_file.write(decrypted_data)
