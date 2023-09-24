#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from os import environ
import models


class State(BaseModel, Base):
    """
    State class for representing a state.
    Attributes:
        name (str): The name of the state.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """
            Getter method to return the list of City instances
            with state_id equal to the current State.id.
            """
            all_cities = models.storage.all(City)
            state_cities = []
            for city_ins in all_cities.values():
                if city_ins.state_id == self.id:
                    state_cities.append(city_ins)
            return state_cities
