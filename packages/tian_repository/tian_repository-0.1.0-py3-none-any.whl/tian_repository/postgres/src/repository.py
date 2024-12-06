#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Repositories are classes where main DB operations are defined, also the predefined operations
can be extended to add more complex operations.
"""
from tian_core import Entity
from tian_repositories.base import AbstractRepository
from tian_core.error import BuilderError
from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Tuple, Type
from tian_drivers import Postgres
from datetime import datetime
from tian_glog import logger
from tian_repositories.base.src.sql_builder import postgres_builder

from tian_repositories.base.src.common import *

__all__ = ['PostgresRepository']


class PostgresRepository(AbstractRepository):
    """SQL based repository implementation.

    :param driver: Database driver implementation
    :param table: Main table that will handle the repository
    :param entity: Class type that should be handled by the repository
    :param log_level: Logging level
    :param debug: Flag for debug mode
    :param auto_timestamps: Flag to insert timestamps on configured created_at and updated_at fields
    :param created_at: Name for created_at timestamp field
    :param updated_at: Name for updated_at timestamp field
    """

    def __init__(
        self,
        driver: Postgres,
        table: Optional[AnyStr] = None,
        schema: Optional[AnyStr] = 'adtech',
        entity: Optional[Type] = None,
        log_level: Optional[int] = None,
        debug: Optional[bool] = False,
        auto_timestamps: Optional[bool] = False,
        created_at: Optional[AnyStr] = None,
        updated_at: Optional[AnyStr] = None,
    ):
        super().__init__(driver, entity, log_level, debug, auto_timestamps, created_at, updated_at)
        #  self.__schema = Schema(schema)
        self.__table = f'{schema}"."{table}' #TODO: need to check
        self._entity = entity

    def find_one(self, **kwargs) -> Any:
        """Retrieve a single record based on the provided filters.

        :param kwargs: Parameters to filter the query.
            - select: Iterable[AnyStr] | List of fields to be selected by the query.
            - where: Condition for filtering records, e.g., `id = 12` or `name = 'John Doe'`.

        :return: Configured entity instance containing the record information or None if no record found.
        """
        if kwargs is None:
            raise BuilderError("Can't find a record without any filter.")
        
        # Extract fields to select and where conditions from kwargs
        fields = kwargs.get('select', None)
        logger.debug(f"Fields: {fields}", kwargs)

        sql_query = kwargs.get('sql', None)
        params = {}
        where_conditions = kwargs.get('where', None)
        if where_conditions is not None:
            for value in where_conditions:
                params.update({value[0]:value[2]}) #(field, operator, value) 
            # params.extend(where_conditions)
        logger.debug(f"Where conditions: {params}")

        if sql_query is not None:
            logger.debug(f"SQL: {sql_query}")
            record = self.driver.query_one(sql=str(sql_query), args=params)
            
            if not record:
                logger.debug("No record found.")
                return None

            return self.entity().from_record(fields, record)
        
        # Build the SQL query
        sql = (postgres_builder()
            .from_table(self.__table)
            .select(fields)
            .where({"where": where_conditions})
            .build())

        logger.debug(f"SQL: {sql}")

        # Execute the query and fetch the first record
        record = self.driver.query_one(sql=str(sql), args=params)

        # Return None if no record is found
        if not record:
            return None

        logger.debug(f"Record: {record}")
        
        # Create and return an entity instance from the retrieved record
        return self.entity().from_record(fields, record)

    def find_many(self, **kwargs) -> List[Any]:
        if not kwargs:
            raise BuilderError("Can't find a record without any filter.")
        
        fields = kwargs.get('select', None)
        logger.debug(f"Fields: {fields}")

        sql_query = kwargs.get('sql', None)
        params = {}
        where_conditions = kwargs.get('where', None)

        # Handle WHERE conditions
        if where_conditions:
            for condition in where_conditions:
                field, operator, value = condition
                if operator.lower() == 'in' and isinstance(value, list):
                    # Generate parameters for IN clause
                    for i, item in enumerate(value):
                        params[f"{field}_{i}"] = item
                else:
                    params[field] = value
        logger.debug(f"Where conditions: {where_conditions}")
        logger.debug(f"Parameters: {params}")

        # If a raw SQL query is provided, execute it directly
        if sql_query:
            logger.debug(f"SQL Query: {sql_query}")
            records = self.driver.query(sql=str(sql_query), args=params)
            return [self.entity().from_record(fields, record) for record in records] if records else []

        # Build SQL query using the query builder
        sql_builder = (
            postgres_builder()
            .from_table(self.__table)
            .select(fields)
            .where({"where": where_conditions})
        )

        # Apply optional clauses
        if 'limit' in kwargs:
            sql_builder = sql_builder.limit(kwargs['limit'])
        if 'offset' in kwargs:
            sql_builder = sql_builder.offset(kwargs['offset'])
        if 'order_by' in kwargs:
            sql_builder = sql_builder.order_by(kwargs['order_by'])
        if 'group_by' in kwargs:
            sql_builder = sql_builder.group_by(kwargs['group_by'])
        if 'ilike' in kwargs:
            sql_builder = sql_builder.ilike(list(kwargs['ilike']))

        # Finalize the query
        sql_query = sql_builder.build()
        logger.debug(f"Final SQL Query: {sql_query}")

        # Execute the query
        records = self.driver.query(sql=str(sql_query), args=params)
        return [self.entity().from_record(fields, record) for record in records] if records else []

    def insert_one(self, record: Entity, returning: List[AnyStr] = None) -> Optional[Tuple[Any, ...]]:
        try:
            if not record:
                raise BuilderError("Can't insert an empty record.")
            # 
            data = record.to_dict()
            data.setdefault("created_at", datetime.utcnow())
            data.setdefault("updated_at", datetime.utcnow())
            #
            values = {key: handle_extra_types(value) for key, value in data.items()}
            sql_query = postgres_builder().to_table(self.__table).insert(data)
            
            sql_query = sql_query.returning(returning)
            if returning:
                return self.driver.execute(sql=str(sql_query), data=values).fetchone()
            
            return self.driver.execute(sql=str(sql_query), data=values)
        except Exception as e:
            print("errrr", e)


    def insert_many(self, records: List[Entity], returning: List[AnyStr] = None) -> Optional[List[Tuple[Any, ...]]]: #TODO: Minhthu
        if not records or  len(records) == 0:
            raise BuilderError("Can't insert an empty record.")
        # 
        record = records[0]
        data = record.to_dict()
        data.setdefault("created_at", datetime.utcnow())
        data.setdefault("updated_at", datetime.utcnow())
        #
        values = {key: handle_extra_types(value) for key, value in data.items()}

        sql_query = postgres_builder().to_table(self.__table).insert(data)
        
        sql_query= sql_query.returning(returning)
        return self.driver.execute(sql=str(sql_query), data=values)

    def update(self, data: Dict[AnyStr, Any], returning: List[AnyStr] = None, **kwargs) -> NoReturn:
        try:
            if not data:
                raise BuilderError("Can't insert an empty record.")

            data.setdefault("updated_at", datetime.utcnow())
            #
            values = {key: handle_extra_types(value) for key, value in data.items()}
            logger.debug(f"Prepare Update Values: {values} Where: {kwargs}")
            sql_query = postgres_builder().update(self.__table, values).where(kwargs)
            where_conditions = kwargs.get('where', None)
            if where_conditions is not None:  
                for value in where_conditions:
                    values.update({value[0]:value[2]}) #(field, operator, value)          
            logger.debug(f"SQL: {str(sql_query)}", values)
            sql_query= sql_query.returning(returning)
            if returning:
                return self.driver.execute(sql=str(sql_query), data=values).fetchone()
            
            return self.driver.execute(sql=str(sql_query), data=values)
        except Exception as e:
            logger.error(f"Update Error: {e}")
            return None

    def delete(self, **kwargs) -> NoReturn: # TODO: Hard delete
        logger.debug(f">>> Delete: {kwargs}")
        sql_query = postgres_builder().from_table(self.__table).delete().where(kwargs)

        self.driver.execute(sql=str(sql_query))

    def fetch(self, query: AnyStr, **kwargs) -> Any:
        """Fetch records from the database.

        :param query: SQL query
        """

        self.logger.debug(f"SQL: {query}")
        return self.driver.query_one(sql=query, args=kwargs)

    def total(self, **kwargs) -> int:
        """Count the total of records in the table.

        :param kwargs: Filter parameters for the query statement

        :return int: Total of records
        """
        where_conditions = kwargs.get('where', None)

        sql_query = (postgres_builder()
            .from_table(self.__table)
            .count()
            .where(where_conditions)
            .build())
       
        logger.debug(f"SQL: {str(sql_query)}")
        return self.driver.query_one(sql=str(sql_query))[0]
    
    
       