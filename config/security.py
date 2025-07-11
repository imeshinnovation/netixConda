import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = os.getenv("ACCESS_TOKEN_EXPIRE")
MONGO_URI = os.getenv("MONGO_URI")
PORT = os.getenv("PORT")