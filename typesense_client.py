import os
import sys
import typesense
from env import env
# from typesense.exceptions import TypesenseClientError


curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(curr_dir, os.pardir)))


def create_typesense_client():
    client = typesense.Client({
        'api_key': env.TYPESENSE_API_KEY,
        'nodes': [{
            'host': env.TYPESENSE_HOST,
            'port': env.TYPESENSE_PORT,
            'protocol': env.TYPESENSE_PROTOCOL,
        }],
        'connection_timeout_seconds': 2
    })
    return client
