from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP, create_engine, BOOLEAN
from sqlalchemy.sql import func

import uuid

Base = declarative_base()

engine = create_engine("postgresql+psycopg2://smartest:sdfghjklwqazx@103.88.241.137:5432/zametki")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True)
    password = Column(String, unique=True)
    email = Column(String)

    name = Column(String)

    notes_id = Column(JSONB)

    reg_time = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)

    uuid = Column(String)

    creator_id = Column(Integer)

    name = Column(String)
    text = Column(String)

    delete = Column(BOOLEAN, server_default="False")
    edit = Column(BOOLEAN, server_default="False")

    delete_time = Column(TIMESTAMP)
    edited_time = Column(TIMESTAMP)
    created_time = Column(TIMESTAMP, server_default=func.now())

Base.metadata.create_all(engine)