from persistence.persistence import IPersistenceManager
from models.country import Country
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DataManager(IPersistenceManager):
    def __init__(self):
        # Store Entities
        self.dataStore = {
            "Amenity": {},
            "City": {},
            "Country": {},
            "Place": {},
            "Review": {},
            "User": {}
        }
    
    # Save Entity entity can be City, Country ...
    def save(self, entity):
        # Define type of entity
        entityType = type(entity).__name__
        # Get ID
        entityID = entity.id
        # Save entity
        self.dataStore[entityType][entityID] = entity
    
    # Get Entities
    def get(self, entityID, entityType):
        # if there is no entityType return {}. If there is no entityID return None 
        return self.dataStore.get(entityType, {}).get(entityID, None)
    
    # Upadte Entities
    def update(self, entity):
        # Define Type
        entityType = type(entity).__name__
        # Get ID
        entityID = entity.id

        # Update entity for entityType and entityID
        if entityType in self.dataStore and entityID in self.dataStore[entityType]:
            self.dataStore[entityType][entityID] = entity
        else:
            raise ValueError(f"{entityType} doesn't exist.")
    
    # Delete Entities
    def delete(self, entityID, entityType):
        if entityType in self.dataStore and entityID in self.dataStore[entityType]:
            del self.dataStore[entityType][entityID]
        else:
            raise ValueError(f"{entityID} nad {entityType} doesn't exists")