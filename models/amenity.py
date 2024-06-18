#!/usr/bin/python3
"""Importing BaseModel Class"""
from models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity Class"""
    def __init__(self, name):
        super().__init__()
        self.name = name
