import databases
from app.config import DATABASE_URL


database = databases.Database(DATABASE_URL)

def get_db():
    return database