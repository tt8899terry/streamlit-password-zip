import zipfile
import tarfile
import io
import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# Function to derive a key from the password
def derive_key(password):
    # Retrieve salt from environment or use fallback
    salt = os.getenv('ENCRYPTION_SALT', b'\x00' * 16)  
    if isinstance(salt, str):
        # Ensure salt is in bytes
        salt = salt.encode() 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# Function to encrypt a file with a password and return as a blob
def encrypt_file(file, password, file_type):
    file_buffer = io.BytesIO(file.read())
    encrypted_buffer = io.BytesIO()
    key = derive_key(password)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(file_buffer.getvalue())
    encrypted_buffer.write(encrypted_data)
    encrypted_buffer.seek(0)
    return encrypted_buffer

# Function to decrypt data with a password
def decrypt_data(encrypted_file, password):
    key = derive_key(password)
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_file.read())
    return decrypted_data

# Function to extract files from a zip archive
def extract_zip(decrypted_data):
    extracted_files = {}
    with zipfile.ZipFile(io.BytesIO(decrypted_data)) as zf:
        for member in zf.infolist():
            with zf.open(member) as file_obj:
                extracted_files[member.filename] = file_obj.read()
    return extracted_files

# Function to extract files from a tar archive
def extract_tar(decrypted_data):
    extracted_files = {}
    with tarfile.open(fileobj=io.BytesIO(decrypted_data), mode='r:gz') as tf:
        for member in tf.getmembers():
            file_obj = tf.extractfile(member)
            if file_obj:
                extracted_files[member.name] = file_obj.read()
    return extracted_files

# Function to create a zip file from extracted files
def create_zip(extracted_files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_name, file_content in extracted_files.items():
            zf.writestr(file_name, file_content)
    zip_buffer.seek(0)
    return zip_buffer

# Function to create a tar file from extracted files
def create_tar(extracted_files):
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tf:
        for file_name, file_content in extracted_files.items():
            tarinfo = tarfile.TarInfo(name=file_name)
            tarinfo.size = len(file_content)
            tf.addfile(tarinfo, io.BytesIO(file_content))
    tar_buffer.seek(0)
    return tar_buffer
