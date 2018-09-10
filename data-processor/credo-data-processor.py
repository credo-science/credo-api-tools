#!/usr/bin/env python3
import argparse
import errno
import importlib.util
import json
import os

parser = argparse.ArgumentParser(description="Tool for incremental processing of CREDO data")

parser.add_argument("--dir", "-d", help="Path to data directory", default="credo-data-export")
parser.add_argument("--plugin-dir", help="Path to directory containing processing plugins", default="plugins")
parser.add_argument("--data-type", "-k", help="Type of event to process (ping/detection/all)", default="all")
parser.add_argument("--delete", action="store_true", help="Delete processed files")

args = parser.parse_args()

args.dir = args.dir.rstrip("/")
args.plugin_dir = args.plugin_dir.rstrip("/")


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

    if not os.path.exists(args.dir + "/processed_detections"):
        with open(args.dir + "/processed_detections", "w+") as _:
            pass

    if not os.path.exists(args.dir + "/processed_pings"):
        with open(args.dir + "/processed_pings", "w+") as _:
            pass


def get_new_files(data_type):
    with open("{}/processed_{}s".format(args.dir, data_type)) as f:
        files_old = set(f.read().splitlines(False))
    files_current = set(os.listdir("{}/{}s".format(args.dir, data_type)))
    return files_current - files_old


def process_detections(detections, plugins):
    for p in plugins:
        p.process_detections(detections, args.dir)


def process_pings(pings, plugins):
    for p in plugins:
        p.process_pings(pings, args.dir)


def process(events, plugins):
    if events.get("detections"):
        process_detections(events["detections"], plugins)
    elif events.get("pings"):
        process_pings(events["pings"], plugins)


def process_new(data_type):
    specs = [
        importlib.util.spec_from_file_location(file, "{}/{}".format(args.plugin_dir, file))
        for file in os.listdir(args.plugin_dir)
        if file.endswith(".py")
    ]

    plugins = [importlib.util.module_from_spec(spec) for spec in specs]

    for spec, plugin in zip(specs, plugins):
        spec.loader.exec_module(plugin)
        print("Loaded plugin: {}".format(plugin))

    for file in get_new_files(data_type):
        with open("{}/{}s/{}".format(args.dir, data_type, file)) as f:
            events = json.load(f)

        process(events, plugins)
        del events

        with open("{}/processed_{}s".format(args.dir, data_type), "a") as f:
            f.write("{}\n".format(file))

        if args.delete:
            os.remove("{}/{}s/{}".format(args.dir, data_type, file))


def main():
    if args.data_type in ["detection", "all"]:
        print("Processing new detections")
        process_new("detection")

    if args.data_type in ["ping", "all"]:
        print("Processing new pings")
        process_new("ping")


if __name__ == "__main__":
    prepare_workspace()
    main()
