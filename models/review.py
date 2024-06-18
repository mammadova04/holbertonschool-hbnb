#!/usr/bin/python3
"""Importing BaseModel class"""
from models.base_model import BaseModel
from models.user import User
from models.place import Place

class Review(BaseModel):
    """Creating Review Classs"""
    def __init__(self, rating, comment, user, place):
        super().__init__()
        self.rating = rating
        self.comment = comment
        self.user = user
        self.place = place
    
    def __str__(self):
        return f"Review(rating={self.rating}, comment='{self.comment}', user='{self.user}', place='{self.place}')"
