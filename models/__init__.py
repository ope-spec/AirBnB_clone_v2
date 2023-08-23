#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }


if getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
