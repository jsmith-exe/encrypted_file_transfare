from cryptography.fernet import Fernet
import os
import paramiko
from scp import SCPClient
import glob

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def data_file(file_name):
    with open(file_name, 'rb') as my_data:
        return my_data.read()

def encrypt_data(data):
    return cipher_suite.encrypt(data)

def save_encrypted_file(file_name, encrypted_data):
    base_name, ext = os.path.splitext(file_name)
    with open(f'{base_name}_encrypted{ext}', 'wb') as my_data:
        my_data.write(encrypted_data)
    return f'{base_name}_encrypted{ext}'

def save_key(file_name, key):
    base_name = os.path.splitext(file_name)[0]
    key_file = f'{base_name}.key'
    with open(key_file, 'wb') as my_key:
        my_key.write(key)
    return key_file

def send_to_server(local_file, remote_path, key_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=server_password)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_file, remote_path)
        scp.put(key_file, remote_path)

    ssh.close()

def rm_file(file_name):
    os.remove(file_name)

def process_files():
    for enc_file in glob.glob('*_encrypted.*'):
   	 base_name = enc_file.split('_encrypted')[0]
   	 key_name = f'{base_name}.key'

   	 rm_file(enc_file)
   	 rm_file(key_name)

if __name__ == '__main__':
    file_name = input('Name of file to encrypt: ')
    user = input('Enter the username of the reciever: ')
    host = input('Enter the host address: @')
    remote_path = input('Enter path on server: ')
    server_password = input('Enter the server password: ')
    data = data_file(file_name)
    encrypted_data = encrypt_data(data)
    encrypted_file = save_encrypted_file(file_name, encrypted_data)
    key_file = save_key(file_name, key)

    send_to_server(encrypted_file, remote_path, key_file)
    process_files()
    print(f"Encrypted file and key sent to server: {remote_path}")

