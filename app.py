from random import random

from flask import Flask, redirect, url_for, request, render_template, abort
import re
from urlToId import murmurhash, transfer

app = Flask(__name__)
root_url = "http://127.0.0.1:5000/"
mapping = []
hash_map = []
original_url = []

# This function checks URL validity with a regex expression


def check_url(url):
    return re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url) is not None

# This function maps the given URL to a unique id


def map_url_id(url):
    # check whether the new url already exists
    if url in original_url:
        return -1

    hash_code = murmurhash(url)
    # avoid generating same hash code
    while hash_code in hash_map:
        hash_code = murmurhash(
            url + random.sample('zyxwvutsrqponmlkjihgfedcba', 3))

    # shorten hash code
    surl = transfer(hash_code)

    # add to mappings
    tup = {surl: url}
    original_url.append(url)
    mapping.append(tup)
    hash_map.append(hash_code)

    return str(mapping.index(tup))

# This function searches for the index of a given value 'v' in the 'mapping' dictionary
def find_value(v):
    for index, item in enumerate(mapping):
        if v in item.values():
            return index
    return -1

# This function searches for the index of a given key 'k' in the 'mapping' dictionary
def find_key(k):
    for index, item in enumerate(mapping):
        if k in item:
            return index
    return -1

# This function gets all the mappings existed
@app.route('/', methods=["GET"])
def get_all():
    return str(200) + " " + str(mapping)

# This function gets the mapping associated with the given id
@app.route('/<identifier>', methods=['GET'])
def get_by_id(identifier):
    index = find_value(identifier)
    if index < 0:
        return str(404)
    return str(301) + " " + str(mapping[index])

# This function deletes all the mappings existed
@app.route('/', methods=['DELETE'])
def delete_all():
    if not mapping:
        return str(404)
    else:
        mapping.clear()
        hash_map.clear()
        original_url.clear()
        return str(204)

# This function deletes the mapping associated with the given id
@app.route('/<identifier>', methods=['DELETE'])
def delete_by_id(identifier):
    index = find_value(identifier)
    if index < 0:
        return str(404)
    d = mapping[index]
    k = list(d.keys())[0]
    if murmurhash(k) in hash_map:
        hash_map.remove(murmurhash(k))
    mapping.remove(d)
    original_url.remove(k)
    return str(204)

# This function creates a new short URL for the given long URL


@app.route('/<new_url>', methods=["POST"])
def post(new_url):
    url = root_url + new_url
    if not check_url(url):
        return str(400) + " " + "Invalid URL"
    index = map_url_id(new_url)
    if index < 0:
        return str(400) + " " + "Failed to generate short URL"
    return str(201) + " " + str(mapping[index])

# This function updates the short URL associated with the given long URL
@app.route('/<url>/<identifier>', methods=["PUT"])
def put(url, identifier):
    # Check if the given long URL exists in the original_url list
    if url not in original_url:
        return str(404)

    index = find_key(url)
    d = mapping[index]
    old_id = d[url]
    if old_id == identifier:
        return str(400) + " New short URL must be different from the old one"
    mapping.remove(d)
    d[url] = identifier
    mapping.append(d)
    return str(200) + " " + str(mapping[index])


if __name__ == '__main__':
    app.run(debug=True)
