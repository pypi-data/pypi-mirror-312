import requests
from bs4 import BeautifulSoup
import os

API_URL = "https://nyxiannetwork.web.id/uploader/dorodoto.php"

class NyxianXD:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"X-API-KEY": self.api_key}

    def get_user_info(self):
        response = requests.get(API_URL, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data["user_data"]
            else:
                raise Exception(data.get("message", "Unknown error"))
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    def upload_file(self, file_path):
        with open(file_path, "rb") as file:
            response = requests.post(API_URL, headers=self.headers, files={"file": file})
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return data["url"]
                else:
                    raise Exception(data.get("message", "Unknown error"))
            else:
                raise Exception(f"HTTP Error: {response.status_code}")

    def get_pinterest_images(self, keyword, num_images=5):
        """
        Mengambil URL gambar dari Pinterest berdasarkan keyword.

        Args:
            keyword (str): Kata kunci pencarian.
            num_images (int): Jumlah gambar yang diambil (default 5).

        Returns:
            list: Daftar URL gambar.
        """
        search_url = f"https://www.pinterest.com/search/pins/?q={keyword.replace(' ', '%20')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from Pinterest. Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        image_tags = soup.find_all("img", limit=num_images)

        # Filter gambar yang relevan
        image_urls = [img["src"] for img in image_tags if img.get("src")]
        return image_urls[:num_images]

    def download_images(self, image_urls, save_dir="downloads"):
        """
        Mengunduh gambar dari daftar URL.

        Args:
            image_urls (list): Daftar URL gambar.
            save_dir (str): Direktori untuk menyimpan gambar.

        Returns:
            list: Daftar path file gambar yang diunduh.
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        downloaded_files = []
        for idx, url in enumerate(image_urls):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_path = os.path.join(save_dir, f"image_{idx+1}.jpg")
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                downloaded_files.append(file_path)
            else:
                print(f"Failed to download image from {url}")
        return downloaded_files
