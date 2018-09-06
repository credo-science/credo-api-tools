#!/usr/bin/env python3
import argparse
import errno
import os
import platform
import time

import requests

parser = argparse.ArgumentParser(description="Tool for incremental data export from CREDO")

parser.add_argument("--username", "-u", help="Username")
parser.add_argument("--password", "-p", help="Password")
parser.add_argument("--endpoint", help="API endpoint", default="https://api.credo.science/api/v2")
parser.add_argument("--dir", "-d", help="Path to data directory", default="credo-data-export")
parser.add_argument("--token", "-t", help="Access token, used instead of username and password to authenticate")
parser.add_argument("--data-type", "-k", help="Type of event to update (ping/detection/all)", default="all")

args = parser.parse_args()

args.endpoint = args.endpoint.rstrip("/")
args.dir = args.dir.rstrip("/")


def prepare_workspace():
    if not os.path.exists(args.dir):
        try:
            os.makedirs(args.dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    if not os.path.exists(args.dir + "/detections"):
        os.makedirs(args.dir + "/detections")

    if not os.path.exists(args.dir + "/pings"):
        os.makedirs(args.dir + "/pings")

    if not os.path.exists(args.dir + "/device_id"):
        with open(args.dir + "/device_id", "w+") as f:
            f.write(os.urandom(16).hex())


def get_base_request():
    with open(args.dir + "/device_id") as f:
        device_id = f.readline()

    return {
        "device_id": device_id,
        "device_type": "credo-data-exporter",
        "device_model": platform.system(),
        "system_version": platform.release(),
        "app_version": 1,
    }


def get_token():
    if args.token:
        print("Using token provided by user")
        return args.token

    j = get_base_request()
    j["username"] = args.username
    j["password"] = args.password

    r = requests.post(args.endpoint + "/user/login", json=j)

    if not r.ok:
        print(r.json())
        r.raise_for_status()

    return r.json()["token"]


def update_data(data_type):
    repeat = False
    time_since = 0

    if os.path.exists(args.dir + "/last_exported_" + data_type):
        with open(args.dir + "/last_exported_" + data_type) as f:
            time_since = int(f.readline())

    j = get_base_request()

    j["since"] = time_since
    j["until"] = int((time.time() + 3600 * 24) * 1000)
    j["limit"] = 250000
    j["data_type"] = data_type

    r = requests.post(args.endpoint + "/data_export", json=j, headers={"authorization": "Token " + get_token()})

    if not r.ok:
        print(r.json())
        r.raise_for_status()

    export_url = r.json()["url"]

    print("Exported data will appear at {}".format(export_url))

    time.sleep(30)

    while True:
        r = requests.get(export_url)

        if r.status_code == 404:
            print("Waiting for data export to finish")
            time.sleep(10)

        else:
            if not r.ok:
                print(r)
                r.raise_for_status()

            events = r.json()[data_type + "s"]
            if len(events) == 250000:
                repeat = True

            if events:
                last_timestamp = events[-1]["time_received"]
                del events

                with open(
                    "{}/{}s/export_{}_{}.json".format(args.dir, data_type, time_since, last_timestamp), "wb"
                ) as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

                with open(args.dir + "/last_exported_" + data_type, "w+") as f:
                    f.write(str(last_timestamp))
            else:
                print("No new events")

            break

    if repeat:
        del r

        print("There is more data to download, updating again.")
        update_data(data_type)


def main():
    if args.data_type in ["detection", "all"]:
        print("Updating detections")
        update_data("detection")

    if args.data_type in ["ping", "all"]:
        print("Updating pings")
        update_data("ping")


if __name__ == "__main__":
    prepare_workspace()
    main()
