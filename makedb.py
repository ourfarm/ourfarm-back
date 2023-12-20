from sqlalchemy import DateTime, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import random
from datetime import datetime
import time

# Database Part
DATABASE_URL = "sqlite:///./farmdatas.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class FarmData(Base):
    __tablename__ = "farmdatas"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String)
    create_date = Column(DateTime, nullable=False)
    temperature = Column(Integer)
    humidity = Column(Integer)
    lightness = Column(Integer)

Base.metadata.create_all(bind=engine)

def generate_random_data():
    # 임의의 온도, 습도, 밝기 값을 생성하는 함수
    temperature = random.uniform(15.0, 35.0)  # 예를 들어 15.0도에서 35.0도 사이
    humidity = random.uniform(30.0, 90.0)     # 예를 들어 30.0%에서 90.0% 사이
    lightness = random.uniform(100, 1000)     # 예를 들어 100에서 1000 사이의 값
    return temperature, humidity, lightness

db_session = SessionLocal()

for i in range(40):
    temperature, humidity, lightness = generate_random_data()
    new_data = FarmData(
        uid="ourfarm",
        create_date=datetime.now(),
        temperature=temperature,
        humidity=humidity,
        lightness=lightness
    )
    db_session.add(new_data)
    time.sleep(10)

db_session.commit()
db_session.close()
