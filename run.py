
from instance.config import *
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI


if __name__ == '__main__':
    app.run()