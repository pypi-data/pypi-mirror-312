import tarfile
import zipfile
from ipm.utils import log

class Installer:
    def install_package(self, package_file):
        """安装指定的包文件"""
        log(f"开始安装包文件 {package_file}...")
        if package_file.endswith(".whl"):
            self._install_wheel(package_file)
        elif package_file.endswith(".tar.gz"):
            self._install_tar(package_file)
        else:
            log("不支持的文件格式")
            return False
        log(f"{package_file} 安装完成。")
        return True

    def _install_wheel(self, wheel_file):
        """安装 .whl 文件"""
        log(f"解压并安装 {wheel_file}...")
        try:
            with zipfile.ZipFile(wheel_file, 'r') as zip_ref:
                zip_ref.extractall()
        except Exception as e:
            log(f"安装 .whl 文件失败：{e}")

    def _install_tar(self, tar_file):
        """安装 .tar.gz 文件"""
        log(f"解压并安装 {tar_file}...")
        try:
            with tarfile.open(tar_file, 'r:gz') as tar_ref:
                tar_ref.extractall()
        except Exception as e:
            log(f"安装 .tar.gz 文件失败：{e}")
