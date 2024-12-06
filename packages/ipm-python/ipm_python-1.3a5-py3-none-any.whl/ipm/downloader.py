import requests
from tqdm import tqdm
from ipm.utils import log

class Downloader:
    def __init__(self, mirrors):
        self.mirrors = mirrors

    def download_package(self, url, destination):
        """下载指定 URL 的包"""
        log(f"开始下载 {url} 到 {destination}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            with open(destination, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                        progress_bar.update(len(chunk))

            log(f"{destination} 下载完成。")
            return destination
        except Exception as e:
            log(f"下载失败：{e}")
            return None
