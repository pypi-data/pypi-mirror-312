import requests
from bs4 import BeautifulSoup
from ipm.utils import log

class Resolver:
    def get_latest_version(self, package_name, mirrors):
        """获取指定包的最新版本"""
        log(f"解析 {package_name} 的最新版本...")
        for mirror in mirrors:
            url = f"{mirror}{package_name}/"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all("a")
                files = [link.text.strip() for link in links if link.text.endswith((".whl", ".tar.gz"))]
                if files:
                    latest_file = sorted(files, reverse=True)[0]
                    log(f"最新版本文件为：{latest_file}")
                    return latest_file
        return None
