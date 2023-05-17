import csv
import json
from os import listdir
import uuid
from opensearchpy import OpenSearch
import click
from pathlib import Path
import datetime


host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True,
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ca_certs = None,
    
    ssl_assert_hostname = False,
    ssl_show_warn = False,
)


@click.group("cli")
def cli():
   """An example CLI for interfacing with a document"""
   pass


def log_elastic_response(response):
    print(json.dumps(response, indent=4))

    
    
PathToResourses : Path = Path('./demo/resourses')
PathToIndexData : Path = PathToResourses / 'index_data'
PathToSettings : Path = PathToResourses / 'settings'

@cli.command('load_data')
def load_data():
    with open(PathToIndexData / 'airport-codes.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)
            response = client.create('airport', id=uuid.uuid4(), body=row)
            # log_elastic_response(response)
            
@cli.command('create_index')
def create_index():
    index_name = f'airport-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
    response = client.indices.create(index_name)
    log_elastic_response(response)


@cli.command('create_templates')
def create_templates():
    with open(PathToSettings / 'airports_template.json') as file:
        response = client.indices.put_template('airports_template', body=file.read())
        log_elastic_response(response)


@cli.command('list_indexes')
def list_indexes():
    print(client.cat.indices())

@click.argument('index', nargs=1, type=click.STRING)
@cli.command('delete_index')
def delete_index(index):
    response = client.indices.delete(index = index)
    log_elastic_response(response)

@click.argument('airport_name', nargs=1, type=click.STRING)
@cli.command('search_airport')
def search_airport(airport_name):
    body_query = {
  "query": {
    "match": {
      "name": {
        "query": airport_name
      }
    }
  }
}
    response = client.search(index = 'airport', body=body_query)
    log_elastic_response(response)
 

def main():
   cli(prog_name="cli")
 
if __name__ == '__main__':
   main()
    


