#!/usr/bin/python3
"""This module defines the DBStorage class for database storage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


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
        from models import classes
        result = {}
        if cls is None:
            for cls in classes.values():
                for instance in self.__session.query(cls).all():
                    key = '{}.{}'.format(instance.__class__.__name__, instance.id)
                    result[key] = instance
        else:
            for instance in self.__session.query(cls).all():
                key = '{}.{}'.format(instance.__class__.__name__, instance.id)
                result[key] = instance
        return result

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        from models import classes
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
