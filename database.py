from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#postgres_url --> 'postgresql://<username>:<password>@localhost:port/Database_name'
URL_DATABASE = 'postgresql://postgres:tiger@localhost:5432/QuizApplication'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()