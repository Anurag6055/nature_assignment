from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./url_shortener.db"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class URLMap(Base):
    __tablename__ = "Urls"
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, unique=True, index=True)
    short_code = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, nullabale=True)
    access_count = Column(Integer, default=0)
    last_accessed = Column(Integer, dafault = 0)

Base.metadata.create_all(bind=engine)