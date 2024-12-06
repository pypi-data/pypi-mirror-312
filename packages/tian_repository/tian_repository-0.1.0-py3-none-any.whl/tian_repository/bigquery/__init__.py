from tian_core import AbstractRepository
from .models import BaseModel 
from google.cloud import bigquery
from google.oauth2 import service_account

class BigQueryRepository(AbstractRepository):
    def __init__(self, client):
        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
        self.client = client

    def get(self, query):
        results = self.client.query_and_wait(query_string)
        return results

    def insert(self, query):
        return self.client.query(query).result()

    def update(self, query):
        return self.client.query(query).result()

    def delete(self, query):
        return self.client.query(query).result()
    
    # b = BigQuery("credentials.json")
        # # query_string = """SELECT name, SUM(number) as total
        # #     FROM `bigquery-public-data.usa_names.usa_1910_current`
        # #     WHERE name = 'William'
        # #     GROUP BY name;
        # #     """

        # b.query(query_string)