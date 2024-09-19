from cryptography.fernet import Fernet
import os
import glob

def data_file(file_name):
    with open(file_name, 'rb') as my_data:
        return my_data.read()

def key_file(key_name):
    with open(key_name, 'rb') as my_key:
        return my_key.read()

def decrypt_data(enc_data, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(enc_data)

def save_file(file_name, data):
    n, ext = os.path.splitext(file_name)
    base_name = file_name.split('_encrypted')[0]
    with open(f'{base_name}{ext}', 'wb') as my_data:
        my_data.write(data)
    return f'{base_name}{ext}'

def rm_file(file_name):
    os.remove(file_name)

def process_files(directory):
    os.chdir(directory)
    for enc_file in glob.glob('*_encrypted*'):
        base_name = enc_file.split('_encrypted')[0]
        key_name = f'{base_name}.key'

        if os.path.exists(key_name):
            enc_data = data_file(enc_file)
            key = key_file(key_name)
            data = decrypt_data(enc_data, key)
            decrypted_file = save_file(enc_file, data)

            print(f"Decrypted {enc_file} to {decrypted_file}")

            rm_file(enc_file)
            rm_file(key_name)
            print(f"Removed {enc_file} and {key_name}")
        else:
            print(f"Key file not found for {enc_file}")

if __name__ == '__main__':
    directory = input('Enter path to files: ')
    process_files(directory)

