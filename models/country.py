#!/usr/bin/python3
"""Importing BaseModel class"""
from models.base_model import BaseModel

class Country(BaseModel):
    """Country Class"""
    def __init__(self, name):
        super().__init__()
        self.name = name