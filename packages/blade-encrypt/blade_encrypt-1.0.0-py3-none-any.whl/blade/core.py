import os
import zipfile
from cryptography.fernet import Fernet

class Blade:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = self.cipher.encrypt(data)
        new_file = file_path + ".BLADE-777"
        with open(new_file, 'wb') as file:
            file.write(encrypted_data)
        os.remove(file_path)
        return new_file

    def decrypt_file(self, file_path):
        if not file_path.endswith(".BLADE-777"):
            raise ValueError("Invalid encrypted file extension.")
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        data = self.cipher.decrypt(encrypted_data)
        original_file = file_path.replace(".BLADE-777", "")
        with open(original_file, 'wb') as file:
            file.write(data)
        os.remove(file_path)
        return original_file

    def compress_folder(self, folder_path, output_zip):
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        return output_zip

    def decompress_folder(self, zip_path, extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_to)
        return extract_to

    def encrypt_folder(self, folder_path):
        zip_path = self.compress_folder(folder_path, folder_path + ".zip")
        encrypted_zip = self.encrypt_file(zip_path)
        return encrypted_zip

    def decrypt_folder(self, encrypted_zip, output_folder):
        decrypted_zip = self.decrypt_file(encrypted_zip)
        self.decompress_folder(decrypted_zip, output_folder)
        os.remove(decrypted_zip)
        return output_folder
