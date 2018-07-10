#This creates the user database

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    emailaddress = Column(String)
    bio = Column(String)
    dob = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, username, password, emailaddress, bio, dob):
        """"""
        self.username = username
        self.password = password
        self.emailaddress = emailaddress
        self.bio = bio
        self.dob = dob
        
# create tables
Base.metadata.create_all(engine)
