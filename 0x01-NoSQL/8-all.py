#!/usr/bin/env python3
"""Lists all documents in a collection using Pymongo"""


def list_all(mongo_collection):
    """Lists all documents in a collection"""
    res = mongo_collection.find()
    return res
