# 一部引用
# https://github.com/marukun712/YOLOv8-WebUI/blob/master/launch.py
import subprocess
import sys
import importlib.util
import re


def install_pip_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def is_installed(package):
    try:
        spec = importlib.util.find_spec(package)
    except ModuleNotFoundError:
        return False

    return spec is not None


def get_pip_requirements():
    pattern = re.compile(r"^([^=]+)==(.+)$")
    package_names = []
    version_numbers = []

    with open("requirements.txt") as f:
        packages = f.read().splitlines()

    for package in packages:
        match = pattern.match(package)
        if match:
            package_names.append(match.group(1))
            version_numbers.append(match.group(2))
            yield match.group(1), match.group(2)

def pip_install():
    for package, version in get_pip_requirements():
        print(package, str(version))
        if not is_installed(package):
            print(f"{package} is not installed. Installing...")
            install_pip_package(f"{package}=={version}")

def check_other_install():
    try:
        subprocess.check_call(["ffmpeg", "-version"])
    except FileNotFoundError:
        print("FFmpegがインストールされていません。インストールしてください。")
        sys.exit(1)
    print("全てのパッケージがインストールされています。")



if __name__ == "__main__":
    pip_install()
    check_other_install()
