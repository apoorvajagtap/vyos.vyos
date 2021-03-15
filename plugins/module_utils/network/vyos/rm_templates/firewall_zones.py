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

def _tmplt_manage_interfaces(config_data):
    cmd_list = []
    print("************config_data******", type(config_data), "?///", type(config_data["interfaces"]))
    for interface_name in config_data["interfaces"]:
        print("##################", interface_name)
        command = (
            "zone-policy zone"
            + " {name} ".format(**config_data)
            + "interface {name}".format(name=interface_name)
        )
        cmd_list.append(command)
    return cmd_list

def _tmplt_configure_from(config_data):
    cmd_list = []
    for i in config_data["from"]:
        afi_val = _get_parameters(i)
        command = (
            "zone-policy zone"
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
        prefix = {"set": "set", "remove": "delete"}
        super(Firewall_zonesTemplate, self).__init__(lines=lines, tmplt=self, prefix=prefix)

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
            "setval": _tmplt_manage_interfaces,
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "interfaces": "{{ interfaces }}",
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
            "setval": "zone-policy zone {{ name }} description '{{description}}'",
            "remval": "zone-policy zone {{ name }} description",
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
            "setval": "zone-policy zone {{ name }} default-action '{{default_action}}'",
            "remval": "zone-policy zone {{ name }} default-action",
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
        },
        {
            "name": "local_zone",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+(?P<local_zone>\'local-zone\')
                *$""",
                re.VERBOSE,
            ),
            "setval": "zone-policy zone {{ name }} local-zone",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "local_zone": "{{ True if local_zone is defined }}"
                }
            },
        },
        {
            "name": "remove_zone",
            "getval": re.compile(
                r"""
                ^delete
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                *$""",
                re.VERBOSE,
            ),
            "remval": "zone-policy zone {{ name }}",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                }
            },
            "shared": True
        },
    ]
    # fmt: on
