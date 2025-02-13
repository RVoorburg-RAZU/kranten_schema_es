import json
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import ssl

# Load environment variables
load_dotenv()

# Create SSL context that doesn't verify certificate
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Connect to Elasticsearch
es = Elasticsearch(
    f"https://{os.getenv('ES_HOST')}:{os.getenv('ES_PORT')}",
    basic_auth=(os.getenv('ES_USERNAME'), os.getenv('ES_PASSWORD')),
    ssl_context=context
)

# Index name
index_name = "newspapers"

# Load mapping
with open("mapping.json", "r") as f:
    mapping = json.load(f)

# Delete index if it exists
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Create index with mapping
es.indices.create(index=index_name, body=mapping)

# Load bulk data
with open("bulk_import.json", "r", encoding="utf-8") as f:
    bulk_data = f.read()

# Perform bulk import
response = es.bulk(body=bulk_data, index=index_name)

# Check for errors
if response['errors']:
    print("Errors occurred during bulk import:")
    for item in response['items']:
        if 'error' in item['index']:
            print(f"Error: {item['index']['error']}")
else:
    print("Bulk import completed successfully")

# Show index stats
stats = es.indices.stats(index=index_name)
print(f"\nIndex stats:")
print(f"Document count: {stats['_all']['total']['docs']['count']}")
