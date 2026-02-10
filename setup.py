from setuptools import setup, find_packages
setup(name="badusb", version="2.0.0", author="bad-antics", description="BadUSB/HID attack payload development toolkit", packages=find_packages(where="src"), package_dir={"": "src"}, python_requires=">=3.8")
