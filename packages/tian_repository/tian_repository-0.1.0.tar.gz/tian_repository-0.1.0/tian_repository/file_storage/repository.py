from tian_core import Entity
from tian_repositories.base import AbstractRepository
import os
from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Type
import pickle
from .examples import *

class FileStorageRepository(AbstractRepository):
    def __init__(self):
        file_path: str = "uploads"
        self.file_path = file_path
        self.data: List = []

    # def open(self):
    #     if os.path.exists(self.file_path):
    #         try:
    #             with open(self.file_path, 'rb') as f:
    #                 f.seek(0)
    #                 self.data = pickle.load(f)
    #                 f.close()
    #         except EOFError as e:
    #             print(e)

    def close(self):
        pass  # Closing file not necessary for read-only operations

    def add(self, item):
        self.data.append(item)
        for item in self.data:
            print(item)

    def get(self, id):
        for item in self.data:
            if item.id == id:
                return item
        return None

    def get_all(self):
        for item in self.data:
            print(item)
        return [product.to_json() for product in self.data]

    def save(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.data, f)

    def find_one(self, **kwargs) -> Any:
        """Find one record from passed filters."""
        raise NotImplementedError('find_one method is not implemented.')

    def find_many(self, **kwargs) -> List[Any]:
        """Find many records from passed filters."""
        raise NotImplementedError('find_many method is not implemented.')

    def insert_one(self, record: Entity) -> Any:
        """Insert one record to the DB and return the assigned ID"""
        raise NotImplementedError('insert_one method is not implemented.')

    def insert_many(self, records: List[Entity]) -> Any:
        """Insert many records at once to the DB."""
        raise NotImplementedError('insert_many method is not implemented.')

    def update(self, **kwargs) -> NoReturn:
        """Update records according parameters."""
        raise NotImplementedError('update method is not implemented.')

    def delete(self, **kwargs) -> NoReturn:
        """Delete records according parameters."""
        raise NotImplementedError('delete method is not implemented.')
