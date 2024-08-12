#!/usr/bin/env python3
"""Adding the top 10 of the most present IPs in the collection nginx of the database logs"""

from pymongo import MongoClient


def log_stats():
    """Log stats"""
    client = MongoClient()
    logs = client.logs.nginx
    print(f"{logs.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    print(f"{logs.count_documents({'path': '/status'})} status check")

    print("IPs:")
    ips = logs.aggregate(
        [
            {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10},
            {"$project": {"_id": False, "ip": True, "count": True}},
        ]
    )
    for ip in ips:
        print(f"\t{ip.get('ip')}: {ip.get('count')}")


if __name__ == "__main__":
    log_stats()
