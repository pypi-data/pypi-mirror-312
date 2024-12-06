# NyxianXD/client.py

import requests

class NyxianClient:
    def __init__(self, api_key, upload_url="https://nyxiannetwork.web.id/uploader/dorodoto.php"):
        self.api_key = api_key
        self.upload_url = upload_url

    def get_user_info(self):
        """Mengambil informasi pengguna berdasarkan API Key."""
        headers = {"X-API-KEY": self.api_key}
        response = requests.get(self.upload_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.status_code} - {response.text}")

    def upload_file(self, file_path):
        """Mengunggah file ke server."""
        headers = {"X-API-KEY": self.api_key}
        with open(file_path, 'rb') as file:
            files = {"file": file}
            response = requests.post(self.upload_url, headers=headers, files=files)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to upload file: {response.status_code} - {response.text}")
