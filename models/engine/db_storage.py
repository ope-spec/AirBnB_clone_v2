#!/usr/bin/python3
"""This module defines the DBStorage class for database storage"""
# Python modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from os import getenv
# console.py modules
from models.base_model import Base, BaseModel
# from models.amenity import Amenity
# from models.city import City
# from models.place import Place
# from models.review import Review
# from models.state import State
from models.user import User



class DBStorage:
    """This class manages database storage using SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self):
        """Create the engine and session"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for cls in BaseModel.__subclasses__():
                query = self.__session.query(cls).all()
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects
 
    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False))()

 
    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
