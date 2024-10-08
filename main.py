import streamlit as st
from PIL import Image
import os
from lib.encryption_utils import (
    encrypt_file, decrypt_data, extract_zip, extract_tar, create_zip, create_tar
)
from cryptography.fernet import InvalidToken
from mainComponent.readMarkdown import ShowStMarkDown


icon = Image.open("asset/favicon.ico")

st.set_page_config(
    page_title="Zip Lock",
    page_icon=icon,
)


# user h1 cause markdown will have anchor
st.html(
'''
<h1>
Secure Zip File Encryption and Decryption
</h1>
'''
)

if 'ENCRYPTION_SALT' not in os.environ:
    st.write( 'secret is not set not set')

tabEncrypt, tabDecrypt,tabReadMe = st.tabs(["Encrypt", "Decrypt","Read Me"])

with tabEncrypt:
    # Upload file to encrypt
    uploaded_file = st.file_uploader("Upload a file to encrypt", type=["zip", "tar", "tar.gz"])
   # clear password 
    if 'encrypt_password' not in st.session_state:
        st.session_state.encrypt_password = None
    def submit_password():
        st.session_state.encrypt_password = st.session_state.encrypt_password_input
        st.session_state.encrypt_password_input = ''

    st.text_input("Enter a password to encrypt the file",key="encrypt_password_input", type="password",on_change=submit_password)
    encrypt_password = st.session_state.encrypt_password
    if uploaded_file and encrypt_password:
        file_type = uploaded_file.name.split('.')[-1]
        encrypted_blob = encrypt_file(uploaded_file, encrypt_password, file_type)
        st.success("File encrypted successfully!")
        st.download_button("Download encrypted file", data=encrypted_blob, file_name=f'encrypted.{file_type}')

with tabDecrypt:
# Upload encrypted file to decrypt
    uploaded_encrypted_file = st.file_uploader("Upload an encrypted file to decrypt", type=["zip", "tar.gz"], key="decrypt")
     # clear password 
    if 'decrypt_password' not in st.session_state:
        st.session_state.decrypt_password = None
    def submit_password():
        st.session_state.decrypt_password = st.session_state.decrypt_password_input
        st.session_state.decrypt_password_input = ''

    st.text_input("Enter the password to decrypt the file",key='decrypt_password_input', type="password",on_change=submit_password )
    decrypt_password = st.session_state.decrypt_password

    if uploaded_encrypted_file and decrypt_password:
        try:
            file_type = uploaded_encrypted_file.name.split('.')[-1]
            decrypted_data = decrypt_data(uploaded_encrypted_file, decrypt_password)
            if decrypted_data:
                if file_type == 'zip':
                    decrypted_files = extract_zip(decrypted_data)
                elif file_type in ['tar', 'gz']:
                    decrypted_files = extract_tar(decrypted_data)
                st.success(f"File decrypted successfully! Files: {', '.join(decrypted_files.keys())}")
                
                # Select format for the decrypted files
                format_option = st.selectbox("Select format for the decrypted files", ["zip", "tar"])
                
                if format_option == "zip":
                    zip_buffer = create_zip(decrypted_files)
                    st.download_button("Download zip file", data=zip_buffer, file_name="decrypted_files.zip")
                elif format_option == "tar":
                    tar_buffer = create_tar(decrypted_files)
                    st.download_button("Download tar file", data=tar_buffer, file_name="decrypted_files.tar.gz")
        except RuntimeError as e:
            st.error(f"An error occurred: {e}")
        except InvalidToken :
            st.error("Invalid password or corrupted file.")

with tabReadMe:
    ShowStMarkDown('markdown/readme.md')