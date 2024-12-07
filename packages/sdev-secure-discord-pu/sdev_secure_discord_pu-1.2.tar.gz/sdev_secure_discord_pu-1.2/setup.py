from setuptools import setup

setup(
    name="sdev_secure_discord_pu",
    version="1.2",
    description="Simple Discord userbot library",
    author="SDev Team",
    author_email="admin@anycorp.dev",
    py_modules=["sdev_secure_discord_pu"],
    install_requires=[
        "websocket-client",
        "requests"
    ],
)