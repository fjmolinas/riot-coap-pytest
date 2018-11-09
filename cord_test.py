# Copyright (c) 2018 Ken Bannister. All rights reserved.
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

"""
Tests registration to a CORE Resource Directory server.

Requires:
   - RIOTBASE env variable for RIOT root directory

   - AIOCOAP_BASE env variable for aiocoap root directory.

   - Network with ULA fd00:bbbb::1/64
"""

import pytest
import os
import time

from conftest import ExpectHost

#
# fixtures and utility functions
#

@pytest.fixture
def cord_cli():
    """
    Runs the RIOT cord_ep example process as an ExpectHost.
    """
    base_folder = os.environ.get('RIOTBASE', None)

    host = ExpectHost(os.path.join(base_folder, 'examples/cord_ep'), 'make term')
    term = host.connect()
    term.expect('CoRE RD client example!')

    # set ULA
    host.send_recv('ifconfig 7 add unicast fd00:bbbb::2/64',
                   'success:')
    yield host

    # teardown
    host.disconnect()


@pytest.fixture
def aiocoap_server():
    """Runs an aiocoap Resource Directory server as an ExpectHost."""
    folder = os.environ.get('AIOCOAP_BASE', None)
    if folder:
        cmd = os.path.join(folder, 'aiocoap-rd')
    else:
        cmd = 'aiocoap-rd'

    host = ExpectHost(folder, cmd)
    term = host.connect()
    time.sleep(2)
    yield host

    # teardown
    host.disconnect()

#
# tests
#

def test_register(aiocoap_server, cord_cli):
    client = cord_cli

    # expect response like 'Nov 04 11:21:58'
    client.send_recv('cord_ep register [fd00:bbbb::1]',
                     'registration successful')
