#!/usr/bin/python3
"""Module for HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from os import getenv
from sqlalchemy import Table, ForeignKey


class Place(BaseModel, Base):
    """The Place class that contains information about places"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="all, delete")

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = Table('place_amenity', Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'), nullable=False, primary_key=True),
            Column('amenity_id', String(60), ForeignKey('amenities.id'), nullable=False, primary_key=True)
        )
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    else:
        @property
        def reviews(self):
            """ Getter attribute for reviews (FileStorage) """
            from models import storage
            from models.review import Review
            review_list = []
            all_reviews = storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """ Getter attribute for amenities (FileStorage) """
            from models import storage
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            """ Setter attribute for amenities (FileStorage) """
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
