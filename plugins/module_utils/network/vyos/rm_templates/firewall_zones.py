# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Firewall_zones parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)

def _get_parameters(data):
    if data["afi"] == 'ipv6':
        val = 'ipv6-name'
    else:
        val = 'name'
    return val

def _tmplt_set_interfaces(config_data):
    cmd_list = []
    for i in config_data["interfaces"]:
        key, val = list(i.items())[0]
        command = (
            "set zone-policy zone"
            + " {name} ".format(**config_data)
            + "interface {name}".format(name=val)
        )
        cmd_list.append(command)
    return cmd_list

def _tmplt_delete_interfaces(config_data):
    delete_cmd_list = []
    for i in config_data["interfaces"]:
        key, val = list(i.items())[0]
        command = (
            "delete zone-policy zone"
            + " {name} ".format(**config_data)
            + "interface {name}".format(name=val)
        )
        delete_cmd_list.append(command)
    return delete_cmd_list

def _tmplt_configure_from(config_data):
    cmd_list = []
    for i in config_data["from"]:
        afi_val = _get_parameters(i)
        command = (
            "set zone-policy zone"
            + " {name} ".format(**config_data)
            + "from {from_zone} ".format(from_zone=i["from_zone"])
            + "firewall {firewall_afi} ".format(firewall_afi=afi_val)
            + "{rule_set_name}".format(rule_set_name=i["rule_set_name"])
        )
        cmd_list.append(command)
    return cmd_list

def _tmplt_delete_from_configuration(config_data):
    delete_cmd_list = []
    ### Doubts:
    # Multiple delete commands could be used:
    # delete zone-policy zone <zone1-name> from <zone2-name>
    # delete zone-policy zone <zone1-name> from <zone2-name> firewall <ipv6/ipv4>

class Firewall_zonesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Firewall_zonesTemplate, self).__init__(lines=lines, tmplt=self)

    # fmt: off
    PARSERS = [
        {
            "name": "interfaces",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+interface
                \s+(?P<interfaces>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_set_interfaces,
            "remval": _tmplt_delete_interfaces,
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "name": "{{ interfaces }}",
                }
            },
            "shared": True
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+description
                \s+(?P<description>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "set zone-policy zone {{ name }} description '{{description}}'",
            "remval": "delete zone-policy zone {{ name }} description"
            "result": {
                "{{ name }}":{
                    "name": "{{ name }}",
                    "description": "{{ description }}",
                }
            },
        },
        {
            "name": "default_action",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+default-action
                \s+(?P<default_action>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "set zone-policy zone {{ name }} default-action '{{default_action}}'",
            "remval": "delete zone-policy zone {{ name }} default-action"
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "default_action": "{{ default_action }}",
                }
            },
        },
        {
            "name": "from",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+from
                \s+(?P<from_zone>\S+)from_name
                \s+firewall
                \s+(?P<afi>name|ipv6-name)
                \s+(?P<rule_set_name>)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_configure_from,
            "remval": _tmplt_delete_from_configuration,
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "from": {
                        "firewall": {
                            "version": "{{ afi }}",
                            "rule_set_name": "{{ rule_set_name }}"
                        }
                    }
                }
            },
        }
        # {
        #     "name": "local_zone",
        #     "getval": re.compile(
        #         r"""
        #         ^set
        #         \s+zone-policy
        #         \s+zone
        #         \s+(?P<name>\S+)
        #         \s+(?P<local_zone>\'local-zone\')
        #         *$""",
        #         re.VERBOSE,
        #     ),
        #     "setval": "set zone-policy zone {{ name }} local-zone",
        #     "result": {
        #         "{{ name }}": {
        #             "name": "{{ name }}",
        #             "local_zone": "{{ True if local_zone is defined }}"
        #         }
        #     },
        # },
    ]
    # fmt: on
