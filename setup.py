from setuptools import setup, find_packages

setup(
    name="junub-sms",
    version="1.0.0",
    description="Simple Python client for JunubSMS API",
    author="Arok Rokie",
    packages=find_packages(),
    install_requires=["requests>=2.25.0"],
    python_requires=">=3.6",
)