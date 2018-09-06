def process_detections(detections, data_dir):
    count = 0
    for d in detections:
        count += 1
    print("processed {} detections".format(count))


def process_pings(pings, data_dir):
    count = 0
    for p in pings:
        count += 1
    print("processed {} pings".format(count))
