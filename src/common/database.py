from sqlalchemy import MetaData

def dbconnect():
    from main import db
    return db