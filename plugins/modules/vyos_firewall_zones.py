#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for vyos_firewall_zones
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: vyos_firewall_zones
short_description: Firewall zones resource module
description: This module manages firewall zones on VyOS devices
author:
  - Apoorva Jagtap (@apoorvajagtap)
options:
  config:
    description: A dictionary of Firewall zone options.
    type: list
    elements: dict
    suboptions:
      name: 
        description:
          - Specifies the name of the zone.
        type: str
        required: True
      default_action:
        description:
          - Default-action for traffic coming into this zone.
          - drop (Drop silently (default))
          - reject (Drop and notify source)
        type: str
        choices: ['drop', 'reject']
      description:
        description:
          - Zone description.
        type: str
      from:
        description:
          - Zone from which to filter traffic.
        type: list
        elements: dict
        suboptions:
          from_name:
            description:
              - Zone from which to filter traffic.
            type: str
            required: True
          firewall:
            description:
              - Firewall options.
            type: dict              
            suboptions:
              v4_rule_set: 
                description: 
                  - Specify the ipv4 rule set name.
                type: str
              v6_rule_set: 
                description:
                  - Specify the ipv6 rule set name.
                type: str
      interfaces:
        description:
          - Interface associated with zone.
        type: list
        elements: dict
        suboptions:
          name:
            description:
            - name of the interface
            type: str
      local_zone:
        description:
          - Zone to be local-zone.
        type: bool        
  state:
    description:
    - The state the configuration should be left in
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - rendered
    - parsed  
    default: merged
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.argspec.firewall_zones.firewall_zones import (
    Firewall_zonesArgs,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.config.firewall_zones.firewall_zones import (
    Firewall_zones,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Firewall_zonesArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Firewall_zones(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
