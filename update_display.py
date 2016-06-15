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
import datetime

verbose = True
actionjsonURL = "https://user.fablab.fau.de/~ew24uped/ib-client/sample_action.json"
# TODO server configurable


def note(text):
    """prints text if verbose is True

    :param text: text to be printed
    :type text: str | unicode
    """
    if verbose:
        print(text)
    return text


def fetch_json(url):
    """fetch the JSON

    :param url: URL where the action-JSON can be found
    :rtype: dict
    """
    note("fetching JSON")
    r = requests.get(url)
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
    nodeID = json.get("showNode")
    nodeURL = json.get("nodeURL")
    note("nodeID: {0}, nodeURL: {1}".format(nodeID, nodeURL))
    note("parsing JSON DONE")
    return nodeID, nodeURL


if __name__ == '__main__':
    note("starting...")
    # TODO http auth

    actionjson = fetch_json(actionjsonURL)

    nodeID, nodeURL = parse_json(actionjson)

    note("updating node")
    nodeURL = nodeURL
    nodeID = nodeID
    doFetch = False
    try:
        # TODO timezones...
        mTime = os.path.getmtime("cache/{0}-timestamp".format(nodeID))
        formTime = note(datetime.datetime.utcfromtimestamp(mTime).strftime("%a, %d %b %Y %H:%M:%S GMT"))
        headers = {'If-Modified-Since': formTime}
    except OSError:
        note("timestamp file for {0} does not exist".format(nodeID))
        formTime = datetime.datetime.fromtimestamp(0).strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {'If-Modified-Since': formTime}

    r = requests.get(nodeURL, headers=headers, stream=True)
    note(r.headers)
    note(r.status_code)
    # TODO update node function
    stat = r.status_code
    if stat == 200:
        """get file and save it to cache"""
        # falls update notwendig
        # cache/id-timestamp touchen
        # node holen und in cache/id entpacken
        pass
    elif stat == 304:
        """file is cached"""
        pass
    else:
        raise Exception("Fetching the node {id} from {url} has failed with HTTP error {error}.".format(
            id=nodeID,
            url=nodeURL,
            error=stat
        ))
    note("updating node DONE")
    # TODO deploy node
    # cache/id nach run verschieben
    # TODO Fehlernode im Fehlerfall deployen (in eine Textdatei die Fehlermeldung schreiben, damit der node was anziegen kann)
    # vielleicht auch mit try catch den fehlerfall deployen
