from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://dbadmin:D:m/=P\$6X+0x~,C@35.221.223.117:5432/chat-db"
SQLALCHEMY_DATABASE_URL2 = "postgresql://dbadmin:D:m/=P\$6X+0x~,C@35.221.223.117:5432/emotion-db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

engine2 = create_engine(
    SQLALCHEMY_DATABASE_URL2
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)


Base = declarative_base()
Base2 = declarative_base() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_db2():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()