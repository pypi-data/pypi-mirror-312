import os
import pkg_resources

def log(message):
    """简单的日志打印"""
    print(f"[LOG] {message}")

def list_installed_packages():
    """列出当前环境中已安装的包"""
    installed = {}
    for dist in pkg_resources.working_set:
        installed[dist.project_name] = dist.version
    return installed
