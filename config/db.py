from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:root@localhost:3306/challengedb?autocommit=true", echo=True)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
