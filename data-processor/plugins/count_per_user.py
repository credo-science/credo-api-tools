import collections
import json
import os


def process_detections(detections, data_dir):
    # Create a file to store our results
    if not os.path.isfile(data_dir + "/user_detection_count.json"):
        with open(data_dir + "/user_detection_count.json", "w") as f:
            f.write("{}")

    # Load previous results
    with open(data_dir + "/user_detection_count.json", "r") as f:
        c = collections.Counter(json.load(f))

    # Update counter
    for d in detections:
        if d["visible"]:
            c[str(d["user_id"])] += 1

    print("top 10 users after this batch: {}".format(c.most_common(10)))

    # Save results
    with open(data_dir + "/user_detection_count.json", "w") as f:
        json.dump(c, f)


def process_pings(pings, data_dir):
    pass
