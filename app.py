import os
from dotenv import load_dotenv

from flask import Flask

from api.reviews import reviews_blueprint
from database.db import db
from utils.cache import cache
from utils.parsing import parse_reviews_file, parse_products_file

load_dotenv()
app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cache.init_app(app)
db.init_app(app)
app.register_blueprint(reviews_blueprint)


def setup_database():
    """Create database tables"""
    with app.app_context():
        # db.drop_all()
        db.create_all()


@app.cli.command()
def parse():
    """Custom command to start parsing files, ex. 'flask parse'"""
    parse_products_file()
    parse_reviews_file()
    print("Successfully parsed files!")


if __name__ == '__main__':
    setup_database()
    app.run()
