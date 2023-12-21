# import Part
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, File, Depends, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.param_functions import File, Form
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import DateTime, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from datetime import datetime

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

status = {'led': 0, 'auto': 0}

# BackEnd Part
app = FastAPI()

## CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 오리진 목록
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 헤더 목록
)

@app.get("/")
def root():
    return "ourfarm-back"


@app.get("/image")
async def get_image():
    image_path = "./current.jpeg"
    return FileResponse(image_path)

@app.get("/score")
async def get_score():
    return sum(get_temperature_score+get_humidity_score+get_lightness_score)//3

@app.get("/temperature")
async def get_temperature():
    db_session = SessionLocal()
    items = db_session.query(FarmData).order_by(FarmData.create_date.desc()).limit(20).all()
    db_session.close()
    temperatures = [item.temperature for item in items]
    return temperatures

@app.get("/tscore")
async def get_temperature_score():
    return 100

@app.get("/humidity")
async def get_humidity():
    db_session = SessionLocal()
    items = db_session.query(FarmData).order_by(FarmData.create_date.desc()).limit(20).all()
    db_session.close()
    humidities = [item.humidity for item in items]
    return humidities

@app.get("/hscore")
async def get_humidity_score():
    return 100

@app.get("/lightness")
async def get_lightness():
    db_session = SessionLocal()
    items = db_session.query(FarmData).order_by(FarmData.create_date.desc()).limit(20).all()
    db_session.close()
    lightnesses = [item.lightness for item in items]
    return lightnesses

@app.get("/lscore")
async def get_lightness_score():
    return 100

@app.get("/autostatus")
async def get_auto_status():
    return status["auto"]

@app.get("/ledstatus")
async def get_led_status():
    return status["led"]

@app.get("/auto/{control}")
async def auto_off(control: str):
    if control=="on":
        status["auto"]=1
    else:
        status["auto"]=0
    return control

@app.get("/led/{control}")
async def led_off(control: str):
    if control=="on":
        status["led"]=1
    else:
        status["led"]=0
    return control

@app.post("/uploadimage")
async def save_image(request: Request):
    contents = await request.body()
    with open("current.jpeg", "wb") as fp:
        fp.write(contents)

    return "image send finished"


@app.post("/upload")
async def save_sensor(request: Request):
    data = await request.json()
    ligthness = data.get('photo')
    humidity = data.get('humidity')
    temperature = data.get('temp')

    db_session = SessionLocal()
    new_text = FarmData(uid="ourfarm", create_date = datetime.now(), temperature=temperature, humidity=humidity, lightness=ligthness)
    db_session.add(new_text)
    db_session.commit()
    db_session.refresh(new_text)
    db_session.close()
    return
