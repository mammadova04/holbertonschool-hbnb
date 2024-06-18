#!/usr/bin/python3
"""Importing BaseModel class"""
from model.base_model import BaseModel
from model.user import User
from model.place import Place

class Review(BaseModel):
    """Creating Review Classs"""
    def __init__(self, rating, comment, user, place):
        super().__init__()
        self.rating = rating
        self.comment = comment
        self.user = user
        self.place = place

