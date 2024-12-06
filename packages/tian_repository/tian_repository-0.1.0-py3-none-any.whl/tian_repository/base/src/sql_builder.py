
from pypika.queries import QueryBuilder
from pypika import Field, Order, Parameter, Table, JoinType, functions as fn, Parameter

from typing import Any, AnyStr, Iterable, List, Mapping, Dict
from uuid import UUID
from datetime import datetime

def handle_extra_types(value: Any) -> Any:
    """Convert unhandled types to a default value.
    :param value: Value to be converted
    :return Any: converted value
    """

    if isinstance(value, UUID):
        return str(value)

    return value

class PostgresSQLQueryBuilder():
    def __init__(self):
        super().__init__()
        self.sql = QueryBuilder()
         

    def select(self, fields: Iterable[AnyStr]= None) -> 'PostgresSQLQueryBuilder':
        fields = list(fields)
        if fields is None or len(fields) == 0:
            self.sql = self.sql.select('*')
        else:
            self.sql = self.sql.select(*fields)
            print(self.sql.get_sql())
        return self
    
    def from_table(self, table: AnyStr) -> 'PostgresSQLQueryBuilder':
        self.sql = self.sql.from_(table)
        return self
    
    def where(self, params: Mapping = None, **kwargs) -> 'PostgresSQLQueryBuilder':
        # Initialize params to an empty dictionary if none are provided
        if params is None:
            params = {}

        # Merge params with kwargs to handle both ways of passing conditions
        if kwargs:
            if 'where' not in params:
                params['where'] = []
            for key, value in kwargs.items():
                # For keyword arguments, assume equality if the value is not a list
                if isinstance(value, list):
                    params['where'].append((key, 'in', value))
                else:
                    params['where'].append((key, '=', value))

        # Extract 'where' conditions from params
        conditions = params.get('where', [])

        # Apply conditions to the query
        if conditions:
            for condition in conditions:
                if len(condition) != 3:
                    continue  # Skip invalid conditions
                
                column_name, operator, value = condition
                field = Field(column_name)  # Assuming Field is a way to refer to table columns

                # Apply the operator to the SQL query
                if operator == '=':
                    self.sql = self.sql.where(field == Parameter(f":{column_name}"))
                elif operator == '>':
                    self.sql = self.sql.where(field > Parameter(f":{column_name}"))
                elif operator == '<':
                    self.sql = self.sql.where(field < Parameter(f":{column_name}"))
                elif operator == '!=':
                    self.sql = self.sql.where(field != Parameter(f":{column_name}"))
                elif operator == '>=':
                    self.sql = self.sql.where(field >= Parameter(f":{column_name}"))
                elif operator == '<=':
                    self.sql = self.sql.where(field <= Parameter(f":{column_name}"))
                elif operator.lower() == 'like':
                    self.sql = self.sql.where(field.like(Parameter(f":{column_name}")))
                elif operator.lower() == 'in' and isinstance(value, list):
                    # Handle IN clause
                    field, operator, value = condition
                    field_obj = Field(field)
                    self.sql = self.sql.where(field_obj.isin(value))
                    # Bind parameters for each value in the array
                    if operator.lower() == 'in' and isinstance(value, list):
                        # Use PyPika's 'isin' method for 'IN' clauses
                        self.sql = self.sql.where(field_obj.isin(value))
                    else:
                        # Handle other operators
                        self.sql = self.sql.where(self._apply_operator(field_obj, operator, value))
                else:
                    raise ValueError(f"Unsupported operator: {operator}")

        return self
    
    def to_table(self, table: AnyStr) -> 'PostgresSQLQueryBuilder':
        self.sql = self.sql.into(table)
        return self
    
    def insert(self, values: Dict[AnyStr, Any]) -> 'PostgresSQLQueryBuilder':
        columns = []
        for key, values in values.items():
            if (key == 'id' or key == 'uuid') and ((isinstance(values, int) and values == 0) or (isinstance(values, str) and len(values) == 0)):
                continue
            columns.append(key)
                
        values = [Parameter(f":{col}") for col in columns]
        
        self.sql = self.sql.insert(values).columns(*columns)
        return self
    
    def update(self, table: AnyStr, data: Mapping) -> 'PostgresSQLQueryBuilder':
        # Initialize the update query on the specified table
        self.sql = self.sql.update(table)
        
        # Iterate over the data dictionary and set values for each field
        for key, value in data.items():
            # Handle custom types if necessary
            value = handle_extra_types(value)
            
            # Set each field with the appropriate parameter
            self.sql = self.sql.set(Field(key), Parameter(f":{key}"))
            
        return self
    
    def delete(self, table: AnyStr) -> 'PostgresSQLQueryBuilder':
        self.sql = self.sql.delete().from_(self.__table)
        return self
    
    def count(self) -> 'PostgresSQLQueryBuilder':
        self.sql = self.sql.select(fn.Count("*"))
        return self
    
    def sum(self, column) -> 'PostgresSQLQueryBuilder':
        self.sql = self.sql.select(fn.Sum(Field(column)))
        return self
    
    def returning(self, columns: List[str]) -> str: #TODO: Not good
        # Get the existing SQL statement
        sql_query = self.sql.get_sql()
        if columns is not None:
            # Manually append the RETURNING clause
            returning_clause = f" RETURNING {', '.join(columns)}"
            # Rebuild the SQL statement with the returning clause
            return f"{sql_query}{returning_clause}"
        return sql_query
    
        
    def limit(self, limit: int = 1) -> 'PostgresSQLQueryBuilder':
        if limit:
            self.sql = self.sql.limit(limit)
        return self
    
    def offset(self, offset: int =1) -> 'PostgresSQLQueryBuilder':
        if offset:
            self.sql = self.sql.offset(offset)
        return self
    
    def ilike(self, ilike_filters: list) -> 'PostgresSQLQueryBuilder':
        if ilike_filters:
            conditions = []
            for column_filters in ilike_filters:
                column_name = column_filters.get('column')
                value = column_filters.get('value')
                
                if column_name and value:
                    value = f"%{value}%"
                    # if column_filters.get('schema') and column_filters.get('table'):
                    #     schema = column_filters.get('schema')
                    #     table = column_filters.get('table')
                    #     column_name = f'{schema}"."{table}"."{column_name}'
                    condition = Field(column_name).ilike(value)
                    conditions.append(condition)
           
            if conditions:
                combined_condition = conditions[0]
                for condition in conditions[1:]:
                    combined_condition |= condition      
                self.sql = self.sql.where(combined_condition)
        return self
    
    def order_by(self, params: Mapping) -> 'PostgresSQLQueryBuilder':
        if params is not None and params.get('column_name', None):
            column_name, order_type = params.get('column_name', None), params.get('order_type', None)
            if column_name and order_type:
              self.sql = self.sql.orderby(Field(column_name), order=Order.asc if order_type == 'asc' else Order.desc)
        return self

    def group_by(self, params: Mapping) -> 'PostgresSQLQueryBuilder':
        group_by = params.get('group_by', [])
        if group_by:
            self.sql = self.sql.groupby(*[Field(column) for column in group_by])
        return self
    
    def join(self, params: Mapping) -> 'PostgresSQLQueryBuilder':
        """Implement join logic."""
        join_data = params.get('join', [])
        for join in join_data:
            table, on_condition, join_type = join['table'], join['on'], join['type']
            join_type = JoinType.left if join_type == 'left' else JoinType.inner
            self.sql = self.sql.join(Table(table), how=join_type).on(on_condition)
        return self

    def set_statement(self, params: Mapping) -> 'PostgresSQLQueryBuilder':
        """Handle SET clauses in updates."""
        set_data = params.get('set', {})
        for field, value in set_data.items():
            self.sql = self.sql.set(Field(field), value)
        return self

    def build(self) -> AnyStr:
        return self.sql.get_sql()
    

def postgres_builder():
    return PostgresSQLQueryBuilder()