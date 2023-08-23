#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", backref="cities", cascade="all, delete")

    @property
    def places(self):
        """ Getter method for the places linked to the city """
        return self.places

    @places.setter
    def places(self, value):
        """ Setter method for places linked to the city """
        if value and not isinstance(value, list):
            raise ValueError("Places must be a list of Place objects")
        self.places = value
