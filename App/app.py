from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')

app = Flask(__name__)

client = MongoClient(mongo_uri)
db = client.get_default_database()




if __name__ == '__main__':
    app.run(debug=True)