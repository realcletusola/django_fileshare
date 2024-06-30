import os 
from databases import Database  
from dotenv import load_dotenv

# load env variables
load_dotenv()

# define and connect async database
DATABASE_URL = os.getenv('DATABASE_URL')
database = Database(DATABASE_URL)