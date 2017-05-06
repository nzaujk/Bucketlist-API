import os

from app import initialize_app

config_name = os.getenv('APP_SETTINGS')
app = initialize_app(config_name)

if __name__ == '__main__':
    app.run()