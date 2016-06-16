#!/usr/bin/python
"""Poll the server and update the infobeamer nodes

This script fetches a JSON which describes the node that should be shown.
The node gets then checked and, if necessary, fetched or updated.
As a last step the script swaps the old with the new node and returns with success or failure.

:author: `Patrick Kanzler <patrick.kanzler@fau.fablab.de>`_ and `Michael Zapf <michael.zapf@fau.de>`_
:organization: `FAU FabLab <https://github.com/fau-fablab>`_
:copyright: Copyright (c) 2016 authors
:license: MIT License
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
import os
import shutil
import datetime
import tarfile

########################################################################
# TODO make these values configurable
verbose = True
actionjsonURL = "https://user.fablab.fau.de/~ew24uped/ib-client/sample_action.json"

cachePath = "cache"
stagePath = "stage"
errorNodePath = "samplecontent/errornode"

user = "TODO"
password = "tralala"
auth = (user, password)
#########################################################################

def get_nodepath(cachePath, nid):
    """get the nodepath
    """
    node_path = "{cache}/{id}".format(
        cache=cachePath,
        id=nid
    )
    return node_path


def note(text):
    """prints text if verbose is True

    :param text: text to be printed
    :type text: str | unicode
    """
    if verbose:
        print(text)
    return text


def touch(fname):
    """equivalent to UNIX 'touch'"""
    try:
        os.utime(fname, None)
    except OSError:
        open(fname, 'a').close()


def fetch_json(url):
    """fetch the JSON

    :param url: URL where the action-JSON can be found
    :rtype: dict
    """
    note("fetching JSON")
    r = requests.get(url, auth=auth)
    json = r.json()
    r.raise_for_status()
    note("fetching JSON DONE")
    return json


def parse_json(json):
    """parses the json file containing the current action

    :param json: JSON file from fetch_json
    :type json: dict
    :return: tuple of nodeID and nodeURL
    :rtype: (str|unicode, str|unicode)
    """
    note("parsing JSON")
    nid = json.get("showNode")
    nurl = json.get("nodeURL")
    note("nodeID: {0}, nodeURL: {1}".format(nid, nurl))
    note("parsing JSON DONE")
    return nid, nurl


def unpack_node(r, nid):
    """unpack a node from a requests object

    :param r: request object
    :type r: requests.Response
    :param nid: identifier of the node
    """
    node_path = get_nodepath(cachePath, nid)
    tar = tarfile.open(mode='r|gz', fileobj=r.raw)
    tar.extractall(node_path)
    note("unpacked the node {id} to {path}".format(
        id=nid,
        path=node_path
    ))


def update_node(nid, nurl):
    """update the current node in the cache

    Does nothing if the cache is up to date (uses the HTTP If-Modified-Since-header)
    :param nid: identifier of the node
    :param nurl: url of the node
    """
    note("updating node")
    timestampfile = "{0}-timestamp".format(get_nodepath(cachePath, nid))
    try:
        modified = os.path.getmtime(timestampfile)
    except OSError:
        note("timestamp file for {0} does not exist".format(nid))
        modified = 0

    time = datetime.datetime.utcfromtimestamp(modified).strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers = {'If-Modified-Since': time}
    note("Will send If-Modified-Since: {0}".format(time))

    r = requests.get(nurl, headers=headers, stream=True, auth=auth)
    note("Response headers for {url}:\n{headers}\n".format(
        url=nurl,
        headers=r.headers
    ))

    stat = r.status_code
    if stat == 200:
        # get file and save it to cache
        try:
            os.mkdir(cachePath)
        except OSError:
            note("cache-path already exists")
        unpack_node(r, nid)
        touch(timestampfile)
        note("A new version of the node {0} has been fetched.".format(nid))
    elif stat == 304:
        # file is cached
        note("The node {0} will be used from cache.".format(nid))
    else:
        raise Exception("Fetching the node {id} from {url} has failed with HTTP error {error}.".format(
            id=nid,
            url=nurl,
            error=stat
        ))
    note("updating node DONE")


def deploy_node(nid):
    """deploy a node to the stage directory

    The node ID 'error' is magic! It will deploy an error-node.
    :param nid: id of the node that will be deployed
    """
    try:
        shutil.rmtree(stagePath)
    except OSError:
        note("staging directory ({0}) does not exist".format(stagePath))
    if nid == "error":
        node_path = errorNodePath
    else:
        node_path = get_nodepath(cachePath, nid)
    shutil.copytree(node_path, "{0}".format(stagePath))
    note("deployed node {id} to {stage}".format(
        id=nid,
        stage=stagePath
    ))


if __name__ == '__main__':
    note("starting...")

    try:
        actionjson = fetch_json(actionjsonURL)
        nodeID, nodeURL = parse_json(actionjson)
        update_node(nodeID, nodeURL)
        deploy_node(nodeID)
    except Exception as e:
        message = "An uncatched exception occured:\n{type}:{obj}".format(
            type=type(e),
            obj=e
        )
        note(message)
        deploy_node("error")
        with open("{0}/error.txt".format(stagePath), 'w') as f:
            f.write(message)
