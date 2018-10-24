from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float
from sqlalchemy.orm import sessionmaker

uri = 'sqlite:///weather_data.db'

Base = declarative_base()
engine = create_engine(uri)


def get_session():
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


def create_db():
    Base.metadata.create_all(engine)


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    city = Column(String(64))
    week = Column(String(16))
    weather = Column(String(16))
    high_temp = Column(Integer)
    low_temp = Column(Integer)


class PM(Base):
    __tablename__ = 'pm'

    id = Column(Integer, primary_key=True)
    city = Column(String(64))
    date = Column(DateTime)
    AQI = Column(String(16))
    PM25 = Column(String(16))
    PM10 = Column(String(16))
    CO = Column(String(16))
    NO2 = Column(String(16))
    SO2 = Column(String(16))
    O3 = Column(String(16))
    humidity = Column(String(16))
    wind = Column(String(16))
    wind_level = Column(String(16))
    ultra_ray = Column(String(16))


if __name__ == '__main__':
    create_db()
