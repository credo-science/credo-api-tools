import argparse
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

USER_INDEX_NAME = "credo-users"
USER_INDEX_CONFIG = {
    "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    "mappings": {
        "properties": {
            "id": {"type": "long"},
            "username": {"type": "keyword"},
            "display_name": {"type": "keyword"},
        }
    },
}

DEVICE_INDEX_NAME = "credo-devices"
DEVICE_INDEX_CONFIG = {
    "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    "mappings": {
        "properties": {
            "device_model": {"type": "keyword"},
            "system_version": {"type": "keyword"},
            "device_type": {"type": "keyword"},
            "id": {"type": "long"},
            "user_id": {"type": "keyword"},
        }
    },
}

TEAM_INDEX_NAME = "credo-teams"
TEAM_INDEX_CONFIG = {
    "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    "mappings": {"properties": {"id": {"type": "long"}, "name": {"type": "keyword"}}},
}

parser = argparse.ArgumentParser(
    description="Tool for exporting CREDO mappings to Elasticsearch"
)

parser.add_argument("--host", help="Elasticsearch host", default="127.0.0.1")
parser.add_argument("--clear", help="Clear previously stored data", action="store_true")
parser.add_argument("file", help="File to read data from", default="user_mapping.json")

args = parser.parse_args()

es = Elasticsearch(args.host, sniff_on_start=False)


def export_user_mapping(users):
    es.indices.create(USER_INDEX_NAME, body=USER_INDEX_CONFIG, ignore=400)
    bulk(es, users, index=USER_INDEX_NAME, raise_on_exception=False)


def export_device_mapping(devices):
    es.indices.create(DEVICE_INDEX_NAME, body=DEVICE_INDEX_CONFIG, ignore=400)
    bulk(es, devices, index=DEVICE_INDEX_NAME, raise_on_exception=False)


def export_team_mapping(teams):
    es.indices.create(TEAM_INDEX_NAME, body=TEAM_INDEX_CONFIG, ignore=400)
    bulk(es, teams, index=TEAM_INDEX_NAME, raise_on_exception=False)


def main():
    with open(args.file) as f:
        mapping = json.load(f)

        if "users" in mapping.keys():
            if args.clear:
                es.indices.delete(index=USER_INDEX_NAME, ignore=[400, 404])
            export_user_mapping(mapping["users"])

        if "devices" in mapping.keys():
            if args.clear:
                es.indices.delete(index=DEVICE_INDEX_NAME, ignore=[400, 404])
            export_device_mapping(mapping["devices"])

        if "teams" in mapping.keys():
            if args.clear:
                es.indices.delete(index=TEAM_INDEX_NAME, ignore=[400, 404])
            export_team_mapping(mapping["teams"])


if __name__ == "__main__":
    main()
