from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

DETECTION_INDEX_NAME = "credo-detections"
DETECTION_INDEX_CONFIG = {
    "settings": {"number_of_shards": 12, "number_of_replicas": 0},
    "mapping": {
        "properties": {
            "accuracy": {"type": "float"},
            "altitude": {"type": "float"},
            "device_id": {"type": "keyword"},
            "frame_content": {"type": "binary"},
            "height": {"type": "long"},
            "id": {"type": "long"},
            "location": {"type": "geo_point"},
            "provider": {"type": "keyword"},
            "source": {"type": "keyword"},
            "team_id": {"type": "keyword"},
            "time_received": {"type": "date"},
            "timestamp": {"type": "date"},
            "user_id": {"type": "keyword"},
            "visible": {"type": "boolean"},
            "width": {"type": "long"},
            "x": {"type": "long"},
            "y": {"type": "long"},
        }
    },
}

PING_INDEX_NAME = "credo-pings"
PING_INDEX_CONFIG = {
    "settings": {"number_of_shards": 12, "number_of_replicas": 0},
    "mapping": {
        "properties": {
            "delta_time": {"type": "long"},
            "device_id": {"type": "keyword"},
            "id": {"type": "long"},
            "on_time": {"type": "long"},
            "time_received": {"type": "date"},
            "timestamp": {"type": "date"},
            "user_id": {"type": "keyword"},
        }
    },
}


ES_HOSTS = ["127.0.0.1"]

es = Elasticsearch(ES_HOSTS, sniff_on_start=False)


def transform_detections(detections):
    for d in detections:
        if d.get("latitude"):
            d["location"] = {"lat": d["latitude"], "lon": d["longitude"]}

        del d["latitude"]
        del d["longitude"]

        yield d


def process_detections(detections, data_dir):
    es.indices.create(DETECTION_INDEX_NAME, body=DETECTION_INDEX_CONFIG, ignore=400)
    bulk(
        es,
        transform_detections(detections),
        index=DETECTION_INDEX_NAME,
        doc_type="detection",
        raise_on_exception=False,
    )


def process_pings(pings, data_dir):
    es.indices.create(PING_INDEX_NAME, body=PING_INDEX_CONFIG, ignore=400)
    bulk(es, pings, index=PING_INDEX_NAME, doc_type="ping", raise_on_exception=False)
