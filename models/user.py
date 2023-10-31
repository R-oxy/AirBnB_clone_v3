#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if getenv('HBNB_TYPE_STORAGE', 'file') == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if "password" in kwargs:
            kwargs["_password"] = hashlib.md5(kwargs["password"].
                                              encode()).hexdigest()
            del kwargs["password"]
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.__dict__.get('_password', "")

    @password.setter
    def password(self, value):
        """
        hash the password

        Argument:
           value: password new value
        """
        self.__dict__['_password'] = hashlib.md5(
            value.encode()).hexdigest()
