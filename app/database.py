from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The SQLALCHEMY_DATABASE_URL have been hidden for security reasons
SQLALCHEMY_DATABASE_URL = r"postgresql://dbadmin..."
SQLALCHEMY_DATABASE_URL2 = r"postgresql://dbadmin..."  

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