#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
class Pool(Base):
    """Data model representing lottery pool
    """

    __tablename__ = 'pool'

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(60), nullable = False)
    email = Column(String(120), nullable = False)
    confirmed = Column(Boolean(), nullable = False)
    winner = Column(Boolean(), nullable = False)

# establish database connection to SQLite database
engine = create_engine('sqlite:///lottery.db')

# create an ORM session to talk to the database
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
db_session = DBSession()
