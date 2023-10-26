from opensearchpy import OpenSearch, helpers
import json

data_path = "path_to_a_json..._lettuce_segmentation_pointclouds_index.json"
with open(data_path, 'r') as file:
    data = json.load(file)

# Convert data for bulk indexing
actions = [
    {
        "_index": "phytooracle-index",
        "_source": entry
    }
    for entry in data
]

with open('actions.json', 'w') as file:
    json.dump(actions, file, indent=4)

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only.

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port, 'scheme': 'https'}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)
response = client.index(index="phytooracle-index", body=data[0])
success, failed = helpers.bulk(client, actions)
print(f"Successfully indexed {success} documents.")
print(f"Failed to index {failed} documents.")

