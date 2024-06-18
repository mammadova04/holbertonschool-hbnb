#!/usr/bin/python3
"""Importing BaseModel class"""
from model.base_model import BaseModel
from model.country import Country

class City(BaseModel):
    """City class"""
    def __init__(self, name, country):
        super().__init__()
        self.name = name
        self.country = country
