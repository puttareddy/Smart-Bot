import os

class DefaultConfig:

    PORT = 3978
    APP_ID = os.getenv('APP_ID')
    APP_PASSWORD = os.getenv('APP_PASSWORD')