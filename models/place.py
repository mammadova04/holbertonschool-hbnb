#!/usr/bin/python3
"""Importing BaseModel class"""
from models.base_model import BaseModel
from models.user import User

class Place(BaseModel):
    """Class named Place"""
    def __init__(self, name, description, host):
        if not isinstance(host, User):
            raise ValueError("Host must be a User")
        super().__init__()
        self.name = name
        self.description = description
        self.host = host
