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

class Firewall_zonesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        prefix = {"set": "set", "remove": "delete"}
        super(Firewall_zonesTemplate, self).__init__(lines=lines, tmplt=self)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                *$""",
                re.VERBOSE
            ),
            "setval": "zone-policy zone {{ name }}",
            "result": {
                "firewall_zones": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                    },
                }
            },
            "shared": True
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
                re.VERBOSE
            ),
            "setval": "zone-policy zone {{ name }} default-action {{ default_action }}",
            "result": {
                "firewall_zones": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                        "default_action": "{{ default_action }}",
                    },
                }
            },
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
                \s+(?P<description>.*\S+)
                *$""",
                re.VERBOSE
            ),
            "compval": "description",
            "setval": "zone-policy zone {{ name }} description '{{ description }}'",
            "result": {
                "firewall_zones": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                        "description": "{{ description }}",
                    },
                }
            },
        },
        {
            "name": "from_name",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+from 
                \s+(?P<from_name>\S+)
                *$""",
                re.VERBOSE
            ),
            "compval": "from_name",
            "setval": "zone-policy zone {{ name }} from {{ from_name }}",
            "result": {
                "firewall_zones": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                        "from": {
                            "{{ from_name }}": {
                                "name": "{{ from_name }}",
                            },
                        },
                    },
                }
            },
        },
        {
            "name": "firewall_name",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+from 
                \s+(?P<from_name>\S+)
                \s+firewall
                \s+name
                \s+(?P<firewall_name>\S+)
                *$""",
                re.VERBOSE
            ),
            "compval": "firewall_name",
            "setval": "zone-policy zone {{ name }} from {{ from_name }} firewall name {{ firewall_name }}",
            "result": {
                "firewall_zones": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                        "from": {
                            "{{ from_name }}": {
                                "name": "{{ from_name }}",
                                "firewall": {
                                    "v4_rule_set": "{{ firewall_name }}",
                                },
                            },
                        },
                    },
                }
            },
        },
        {
            "name": "firewall_v6_name",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+from 
                \s+(?P<from_name>\S+)
                \s+firewall
                \s+ipv6-name
                \s+(?P<firewall_v6_name>\S+)
                *$""",
                re.VERBOSE
            ),
            "compval": "firewall_v6_name",
            "setval": "zone-policy zone {{ name }} from {{ from_name }} firewall ipv6-name {{ firewall_v6_name }}",
            "result": {
                "firewall_zones": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                        "from": {
                            "{{ from_name }}": {
                                "name": "{{ from_name }}",
                                "firewall": {
                                    "v6_rule_set": "{{ firewall_v6_name }}",
                                },
                            },
                        },
                    },
                }
            },
        },
        {
            "name": "interface_name",
            "getval": re.compile(
                r"""
                ^set
                \s+zone-policy
                \s+zone
                \s+(?P<name>\S+)
                \s+interface
                \s+(?P<interface_name>\S+)
                *$""",
                re.VERBOSE,
            ),
            "compval": "interface_name",
            "setval": "zone-policy zone {{ name }} interface {{ interface_name }}",
            "result": {
                "firewall_zones": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                        "interfaces": {
                            "{{ interface_name }}": {
                                "name": "{{ interface_name }}",
                            },
                        },
                    },
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
            "setval": "set zone-policy zone {{ name }} local-zone",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "local_zone": "{{ True if local_zone is defined }}"
                }
            },
        },
    ]
    # fmt: on
