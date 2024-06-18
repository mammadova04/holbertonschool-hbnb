#!/usr/bin/python3

"""Importing libs for configure datetime"""
import uuid
from datetime import datetime

class BaseModel:
    """BaseModel class"""
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
