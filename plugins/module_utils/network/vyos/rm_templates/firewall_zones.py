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


def _tmplt_set_interfaces(config_data):

    command = (
        "set zone-policy zone"
        + " {name} ".format(**config_data)
        + "interface {name}".format(**config_data["interfaces"][-1])
    )
    return command

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
            "setval": _tmplt_set_interfaces, #"set zone-policy zone {{ name }} interface {{ name }}",
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
            "setval": "set zone-policy zone {{ name }} description '{{description}}'",
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
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "default_action": "{{ default_action }}",
                }
            },
        },
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
        # {
        #     "name": "from",
        #     "getval": re.compile(
        #         r"""
        #         ^set
        #         \s+zone-policy
        #         \s+zone
        #         \s+(?P<name>\S+)
        #         \s+from
        #         \s+(?P<from_name>\S+)
        #         \s+firewall
        #         \s+(?P<afi>name|ipv6-name)
        #         \s+(?P<v4_rule_set>)
        #         \s+(?P<v6_rule_set>)
        #         *$""",
        #         re.VERBOSE,
        #     ),
        #     "setval": _tmplt_configure_trafic_from,
        # }
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
