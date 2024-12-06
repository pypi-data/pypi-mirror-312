import pytest  


from pypika import Field
from sql_builder import postgres_builder

# Test cases for PostgresSQLQueryBuilder
class TestPostgresSQLQueryBuilder:

    def test_select(self):
        # Test selecting specific fields
        query = postgres_builder().from_table("users").select(['id', 'name']).build()
        expected_query = 'SELECT "id","name" FROM "users"'
        assert query == expected_query

        # Test selecting all fields
        query2 = postgres_builder().from_table('users').select([]).build()
        expected_query = 'SELECT * FROM "users"'
        assert query2 == expected_query

    def test_from_table(self):
        # Test from_table
        query = postgres_builder().from_table("users").select('*').build()
        expected_query = 'SELECT * FROM "users"'
        assert query == expected_query

    def test_where(self):
        # Test where
        query = postgres_builder().from_table("users").select('*').where({'where': [('id', '=', 1)]}).build()
        expected_query = 'SELECT * FROM "users" WHERE "id"=:id'
        assert query == expected_query

    def test_limit(self):
        # Test limit
        query = postgres_builder().from_table("users").select('*').limit(1).build()
        expected_query = 'SELECT * FROM "users" LIMIT 1'
        assert query == expected_query
    
    def test_offset(self):
        # Test offset
        query = postgres_builder().from_table("users").select('*').offset(1).build()
        expected_query = 'SELECT * FROM "users" OFFSET 1'
        assert query == expected_query

    def test_to_table(self):
        # Test to_table
        query = postgres_builder().to_table("users").from_table("users").select('*').build()
        expected_query = 'INSERT INTO "users" SELECT * FROM "users"'
        assert query == expected_query

    def test_insert(self):
        # Test insert
        query = postgres_builder().to_table("users").insert({'id': 1, 'name': 'John'}).build()
        expected_query = 'INSERT INTO "users" ("id","name") VALUES (:id,:name)'
        assert query == expected_query

    def test_update(self):
        # Test update
        query = postgres_builder().update("users",{'name': 'John'}).build()
        expected_query = 'UPDATE "users" SET "name"=:name'
        assert query == expected_query

    # def test_delete(self): //not found delete in pypika
    #     # Test delete
    #     query = postgres_builder().delete("users").build()
    #     expected_query = 'DELETE FROM "users"'
    #     assert query == expected_query

    def test_count(self):
        # Test count
        query = postgres_builder().from_table("users").count().build()
        expected_query = 'SELECT COUNT(*) FROM "users"'
        assert query == expected_query

    def test_sum(self):
        # Test sum
        query = postgres_builder().from_table("users").sum('id').build()
        expected_query = 'SELECT SUM("id") FROM "users"'
        assert query == expected_query

    def test_returning(self):
        # Test returning
        query = postgres_builder().from_table("users").select('*')
        query = query.returning(['id', 'name'])
        expected_query = 'SELECT * FROM "users" RETURNING id, name'
        assert query == expected_query

    def test_ilike(self):
        # Test ilike
        query = postgres_builder().from_table("users").select('*').ilike([{'column': 'name', 'value': 'John'}]).build()
        expected_query = 'SELECT * FROM "users" WHERE "name" ILIKE \'%John%\''
        assert query == expected_query

    def test_multiple_conditions(self):
        # Test multiple conditions
        query = postgres_builder().from_table("users").select('*').where({'where': [('id', '=', 1), ('name', '=', 'John')]}).build()
        expected_query = 'SELECT * FROM "users" WHERE "id"=:id AND "name"=:name'
        assert query == expected_query
    
    def test_order_by(self):
        query = postgres_builder().from_table("users").select('*').order_by({"column_name": 'updated_at', "order_type": 'desc'}).build()
        expected_query = 'SELECT * FROM "users" ORDER BY "updated_at" DESC'
        assert query == expected_query

    def test_group_by(self):
        query = postgres_builder().from_table("users").select(['id', 'name']).group_by({'group_by' :['id', 'name']}).build()
        expected_query = 'SELECT "id","name" FROM "users" GROUP BY "id","name"'
        assert query == expected_query
    
