#!/usr/bin/python3

import sys
import json
import argparse

debug=False

headers = ["id", "priority", "status", "urgency", "description", "tags", "project"]
ignore_status = ["completed", "deleted"]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--format", action="store", default="markdown",
                        help="The output format to use (markdown|long)")
    args = parser.parse_args()
    return args

def long(jdata):
    for rec in jdata:
        print("Id:", rec["id"])
        print("Pri:", rec["priority"] if "priority" in rec else "")
        print("Stat:", rec["status"][:1])
        print("Urg:", rec["urgency"])
        print("Desc:", rec["description"][:40])
        print("Tags:", ",".join(rec["tags"]) if "tags" in rec else "")
        print("Proj:", rec["project"] if "project" in rec else "")
        if "annotations" in rec:
            for annotation in rec["annotations"]:
                print("  ", annotation["entry"], annotation["description"])
        print("")

def markdown(jdata):
    sformat = "| %5s | %3s | %3s | %40s | %5s | %15s | %15s |\n"
    sys.stdout.write(sformat % ("Id",
                                "Pri",
                                "Sta",
                                "Description",
                                "Urg",
                                "Tags",
                                "Proj"))
    sys.stdout.write(sformat % ("-"*5, "-"*3, "-"*3, "-"*40, "-"*5, "-"*15, "-"*15))
    sformat = "| %5d | %3s | %3s | %40s | %5.2f | %15s | %15s |\n"
    for rec in jdata:
        if debug:
            print(json.dumps(rec, indent=4, sort_keys=True))
        line = {
            "id": rec["id"],
            "priority": rec["priority"] if "priority" in rec else "",
            "status": rec["status"][:1],
            "urgency": rec["urgency"],
            "description": rec["description"][:40],
            "tags": ",".join(rec["tags"]) if "tags" in rec else "",
            "project": rec["project"] if "project" in rec else ""
        }
        if debug:
            print(json.dumps(line, indent=4, sort_keys=True))
        sys.stdout.write(sformat % (line["id"],
                                    line["priority"],
                                    line["status"],
                                    line["description"],
                                    line["urgency"],
                                    line["tags"],
                                    line["project"]))


def main():
    options = parse_args()
    data = sys.stdin.read()
    jdata = json.loads(data)
    jdata = [j for j in jdata if j["status"] not in ignore_status]
    jdata.sort(key=lambda j: j["urgency"], reverse=True)

    if options.format == "markdown":
        markdown(jdata)
    elif options.format == "long":
        long(jdata)

main()
