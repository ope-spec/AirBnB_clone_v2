#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="all, delete")
    reviews = relationship("Review", backref="user", cascade="all, delete")

    @property
    def places(self):
        """ Getter method for the places linked to the user """
        return self.places

    @places.setter
    def places(self, value):
        """ Setter method for places linked to the user """
        if value and not isinstance(value, list):
            raise ValueError("Places must be a list of Place objects")
        self.places = value

    @property
    def reviews(self):
        """ Getter method for the reviews linked to the user """
        return self.reviews

    @reviews.setter
    def reviews(self, value):
        """ Setter method for reviews linked to the user """
        if value and not isinstance(value, list):
            raise ValueError("Reviews must be a list of Review objects")
        self.reviews = value
