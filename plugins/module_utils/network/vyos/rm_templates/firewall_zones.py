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
    print("inside tmplt_manage_interface ------>", config_data, "dhichik  ????", config_data["interfaces"])
    for interface_name in config_data["interfaces"]:
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
        print("rule set >>>> ", i["rule_set_name"], "from_zone >>>>", i["from_zone"])
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
    for i in config_data["from"]:
        command = ""
        for k, v in i.items():
            if k == "rule_set_name":
                afi_val = _get_parameters(i)
                command = (
                        "zone-policy zone"
                        + " {name} ".format(**config_data)
                        + "from {from_zone} ".format(from_zone=i["from_zone"])
                        + "firewall {firewall_afi} ".format(firewall_afi=afi_val)
                        + "{rule_set_name}".format(rule_set_name=i["rule_set_name"])
                )

            elif k == "from_zone":
                command = (
                        "zone-policy zone"
                        + " {name} ".format(**config_data)
                        + "from {from_zone}".format(from_zone=i["from_zone"])
                )

            elif k == "remove_from" and i["remove_from"]:
                command = (
                        "zone-policy zone"
                        + " {name} ".format(**config_data)
                        + "from"
                )

        if command:
            delete_cmd_list.append(command)
    return delete_cmd_list

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
            #"compval": "interfaces",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "interfaces": [
                        "{{ interfaces }}",
                    ],
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
                \s+(?P<desc>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "zone-policy zone {{ name }} description '{{description}}'",
            #"compval": "description",
            "result": {
                "{{ name }}":{
                    "name": "{{ name }}",
                    "description": "{{ desc }}",
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
            "setval": "zone-policy zone {{ name }} default-action {{default_action}}", #_tmplt_manage_default_action,
            #"compval": "default_action",
            #"remval": "zone-policy zone {{ name }} default-action",
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
            #"compval": "from.rule_set_name",
            "remval": _tmplt_delete_from_configuration,
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "from": {
                        "from zone": "{{ from_zone }}",
                        "firewall": {
                            "afi": '{{ "ipv4" if afi == "ipv4" else "ipv6" }}',
                            "rule_set_name": "{{ rule_set_name }}"
                        }
                    }
                }
            },
        },
        # {
        #     "name": "from_from_zone",
        #     "getval": re.compile(
        #         r"""
        #         ^set
        #         \s+zone-policy
        #         \s+zone
        #         \s+(?P<name>\S+)
        #         \s+from
        #         \s+(?P<from_zone>\S+)from_name
        #         *$""",
        #         re.VERBOSE,
        #     ),
        #     "setval": _tmplt_configure_from,
        #     "result": {
        #         "{{ name }}": {
        #             "name": "{{ name }}",
        #             "from": {
        #                 "from zone": "{{ from_zone }}",
        #             }
        #         }
        #     },
        # },
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
    ]
    # fmt: on
