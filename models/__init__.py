# coding:utf-8

# MongoDB
from app import mdb


# SQL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import *
SQL_Engine = create_engine(SQLALCHEMY_DATABASE_URI)
SQLBase = declarative_base()

SessionClass = sessionmaker(bind=SQL_Engine)
sql_session = SessionClass()






