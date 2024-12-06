"""Repositories are classes where main DB operations are defined, also the predefined operations
can be extended to add more complex operations.
"""

from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Tuple, Type

from tian_drivers import Redis
from tian_repositories.base import AbstractRepository
from tian_core import Entity
from tian_glog import logger
__all__ = ['RedisRepository']


class RedisRepository(AbstractRepository):

    def __init__(
        self,
        driver: Redis,
        log_level: Optional[int] = None,
        debug: Optional[bool] = False,
    ):
        self.driver = driver

    def find_one(self, **kwargs) -> Any:
        logger.info(f"RedisRepository find_one: {kwargs}")

    def find_many(self, **kwargs) -> List[Any]:
        logger.info(f"RedisRepository find_many: {kwargs}")

    def insert_one(self,
                   record: Entity,
                   returning: List[AnyStr] = None) -> Optional[Tuple[Any, ...]]:
        logger.info(f"RedisRepository insert_one: {record}")

    def insert_many(self,
                    records: List[Entity],
                    returning: List[AnyStr] = None) -> Optional[List[Tuple[Any, ...]]]:
        logger.info(f"RedisRepository insert_many: {records}")

    def update(self, data: Dict[AnyStr, Any], **kwargs) -> NoReturn:
        logger.info(f"RedisRepository update: {data}")

    def delete(self, **kwargs) -> NoReturn:
        logger.info(f"RedisRepository delete: {kwargs}")

    def set(self, key, value, ttl) -> Any:
        return self.driver.set_value(key,value, ttl)

    def get(self, key) -> Any:
        return self.driver.get_value(key)
