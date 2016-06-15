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

verbose = True
actionjson = "https://user.fablab.fau.de/~ew24uped/ib-client/sample_action.json"
# TODO server configurable


def note(text):
    """prints text if verbose is True

    :param text: text to be printed
    :type text: str | unicode
    """
    if verbose:
        print(text)


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


if __name__ == '__main__':
    note("starting...")
    # TODO http auth

    json = fetch_json(actionjson)

    note("parsing JSON")
    nodeID = json.get("showNode")
    nodePath = json.get("nodeURL")
    note("nodeID: {0}, nodeURL: {1}".format(nodeID, nodePath))
    note("parsing JSON DONE")

    # TODO update node function
    # TODO deploy node
    # TODO Fehlernode im Fehlerfall deployen (in eine Textdatei die Fehlermeldung schreiben, damit der node was anziegen kann)
    # vielleicht auch mit try catch den fehlerfall deployen
